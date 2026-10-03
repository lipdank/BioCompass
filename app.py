import streamlit as st

from questions import questions
from profiles import profiles
from scoring import (
    calculate_user_profile,
    normalize_profile,
    calculate_match
)


# ============================================================
# НАЛАШТУВАННЯ СТОРІНКИ
# ============================================================

st.set_page_config(
    page_title="BioCompass",
    page_icon="🧬",
    layout="centered"
)


# ============================================================
# CSS — ДИЗАЙН
# ============================================================

st.markdown("""
<style>

    /* Загальний фон */
    .stApp {
        background-color: #f5f8f6;
    }

    /* Основний контейнер */
    .block-container {
        max-width: 850px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    /* Заголовок */
    .main-title {
        font-size: 3.2rem;
        font-weight: 800;
        color: #173b2c;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.15rem;
        color: #64756d;
        margin-bottom: 2.5rem;
    }

    /* Заголовки секцій */
    h2 {
        color: #173b2c !important;
        margin-top: 2rem;
    }

    h3 {
        color: #244f3c !important;
    }

    /* Текст питань */
    .question-text {
        font-size: 1.05rem;
        font-weight: 600;
        color: #26352e;
        margin-bottom: 0.5rem;
    }

    /* Картка результату */
    .result-card {
        background: white;
        border-radius: 18px;
        padding: 1.4rem 1.5rem;
        margin: 1rem 0;
        border: 1px solid #dfe8e2;
        box-shadow: 0 3px 12px rgba(30, 60, 45, 0.06);
    }

    /* Перше місце */
    .top-result {
        border: 2px solid #4f9d73;
        background: linear-gradient(
            135deg,
            #ffffff 0%,
            #f0f8f3 100%
        );
    }

    .result-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #173b2c;
    }

    .result-score {
        font-size: 1.1rem;
        font-weight: 600;
        color: #3f8b64;
        margin-top: 0.3rem;
    }

    .explanation {
        color: #5c6c64;
        margin-top: 0.8rem;
        line-height: 1.7;
    }

    /* Кнопка */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        background-color: #3f8b64;
        color: white;
        font-size: 1.05rem;
        font-weight: 700;
        padding: 0.75rem;
        transition: 0.2s;
    }

    .stButton > button:hover {
        background-color: #327451;
        color: white;
    }

    /* Radio */
    div[role="radiogroup"] {
        gap: 0.3rem;
    }

    /* Роздільник */
    hr {
        border: none;
        border-top: 1px solid #dce5df;
        margin: 2.5rem 0;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# НАЗВИ ХАРАКТЕРИСТИК
# ============================================================

characteristic_names = {

    "molecules": "інтерес до молекул і білків",
    "cells": "інтерес до клітинних процесів",
    "genetics": "інтерес до генетики",
    "microorganisms": "інтерес до мікроорганізмів",
    "viruses": "інтерес до вірусів",
    "plants": "інтерес до рослин",
    "animals": "інтерес до тварин",
    "human": "інтерес до людини та фізіології",
    "laboratory": "схильність до лабораторної роботи",
    "microscopy": "інтерес до мікроскопії",
    "computer": "схильність до роботи з комп'ютером",
    "mathematics": "інтерес до математики та кількісного аналізу",
    "field": "схильність до польової роботи",
    "ecology": "інтерес до екології",
    "reproduction": "інтерес до репродукції",
    "immunity": "інтерес до імунної системи",
    "development": "інтерес до розвитку організмів і тканин"
}


# ============================================================
# ПОЯСНЕННЯ РЕЗУЛЬТАТІВ
# ============================================================

def get_explanation(user_profile, specialization_profile):

    strengths = []
    weaknesses = []

    for characteristic, target_value in specialization_profile.items():

        user_value = user_profile.get(characteristic, 0)
        target_percent = target_value * 100

        difference = user_value - target_percent

        if difference >= 15:
            strengths.append({
                "characteristic": characteristic,
                "user_value": user_value
            })

        elif difference <= -25:
            weaknesses.append({
                "characteristic": characteristic,
                "user_value": user_value,
                "target_value": target_percent
            })

    strengths.sort(
        key=lambda x: x["user_value"],
        reverse=True
    )

    weaknesses.sort(
        key=lambda x: x["user_value"]
    )

    return strengths[:3], weaknesses[:3]

# ============================================================
# ЗАГОЛОВОК
# ============================================================

st.markdown(
    '<div class="main-title">🧬 BioCompass</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Знайди біологічний напрям, який найбільше відповідає твоїм інтересам.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# ШКАЛА ВІДПОВІДЕЙ
# ============================================================

scale = {
    "1 — зовсім не цікаво": 1,
    "2 — скоріше не цікаво": 2,
    "3 — нейтрально": 3,
    "4 — скоріше цікаво": 4,
    "5 — дуже цікаво": 5
}


# ============================================================
# ПИТАННЯ
# ============================================================

answers = []

for number, question in enumerate(questions, start=1):

    st.markdown(
        f'<div class="question-text">'
        f'{number}. {question["text"]}'
        f'</div>',
        unsafe_allow_html=True
    )

    answer_text = st.radio(
        "Оберіть відповідь:",
        list(scale.keys()),
        key=f"question_{number}",
        label_visibility="collapsed"
    )

    answer = scale[answer_text]

    answers.append(answer)

    if number != len(questions):
        st.markdown("<hr>", unsafe_allow_html=True)


# ============================================================
# КНОПКА ЗАВЕРШЕННЯ
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🧬 Завершити тест"):

    # --------------------------------------------------------
    # Розрахунок профілю
    # --------------------------------------------------------

    user_profile = calculate_user_profile(
        questions,
        answers
    )

    normalized_profile = normalize_profile(
        user_profile,
        questions
    )


    # --------------------------------------------------------
    # Результати
    # --------------------------------------------------------

    results = []

    for specialization, specialization_profile in profiles.items():

        match = calculate_match(
            normalized_profile,
            specialization_profile
        )

        results.append({
            "specialization": specialization,
            "score": match
        })


    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    # --------------------------------------------------------
    # Заголовок результатів
    # --------------------------------------------------------

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown(
        "## 🔬 Результати",
    )

    st.write(
        "Ось біологічні напрями, профілі яких найбільше "
        "відповідають твоїм відповідям."
    )

    # ============================================================
    # КАРТКИ РЕЗУЛЬТАТІВ
    # ============================================================

    medals = ["🥇", "🥈", "🥉"]

    for index, result in enumerate(results):

        specialization = result["specialization"]
        score = result["score"]

        if index < 3:
            medal = medals[index]
        else:
            medal = "🧬"

        # Перше місце виділяємо окремим заголовком
        if index == 0:
            st.success(
                f"### {medal} {specialization}\n\n"
                f"**Відповідність: {score:.1f}%**"
            )
        else:
            st.subheader(
                f"{medal} {specialization}"
            )

            st.write(
                f"Відповідність: **{score:.1f}%**"
            )

        # Показуємо рівень відповідності
        st.progress(
            min(score / 100, 1.0)
        )

        # Пояснення
        strengths, weaknesses = get_explanation(
            normalized_profile,
            profiles[specialization]
        )

        if strengths:

            st.write(
                "**🟢 Чому цей напрям тобі підходить:**"
            )

            for item in strengths:
                reason = characteristic_names.get(
                    item["characteristic"],
                    item["characteristic"]
                )

                st.write(
                    f"• {reason}"
                )

        if weaknesses:

            st.write(
                "**🔴 Менш виражені інтереси:**"
            )

            for item in weaknesses:
                reason = characteristic_names.get(
                    item["characteristic"],
                    item["characteristic"]
                )

                st.write(
                    f"• {reason}"
                )