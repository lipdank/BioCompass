def calculate_user_profile(questions, answers):

    profile = {}
    weights_sum = {}

    for question, answer in zip(questions, answers):

        # 1 -> 0%, 5 -> 100%
        answer_percent = (answer - 1) / 4 * 100

        for characteristic, weight in question["weights"].items():

            if characteristic not in profile:
                profile[characteristic] = 0
                weights_sum[characteristic] = 0

            # Учитываем силу влияния вопроса
            profile[characteristic] += answer_percent * weight
            weights_sum[characteristic] += abs(weight)

    # Нормализуем каждую характеристику отдельно
    for characteristic in profile:

        if weights_sum[characteristic] != 0:
            profile[characteristic] /= weights_sum[characteristic]

        # Ограничиваем диапазон 0–100
        profile[characteristic] = max(
            0,
            min(100, profile[characteristic])
        )

    return profile


def normalize_profile(profile, questions):

    # Профиль уже находится в диапазоне 0–100,
    # поэтому дополнительная нормализация не нужна.
    return profile


def calculate_match(user_profile, specialization_profile):

    total_score = 0
    total_weight = 0

    for characteristic, target_value in specialization_profile.items():

        user_value = user_profile.get(characteristic, 0)

        # Чем важнее характеристика для направления,
        # тем сильнее она влияет на результат.
        weight = target_value

        # Считаем не просто наличие характеристики,
        # а насколько пользователь ей соответствует.
        score = user_value * weight

        total_score += score
        total_weight += weight

    if total_weight == 0:
        return 0

    return total_score / total_weight
