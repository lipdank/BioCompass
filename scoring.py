def calculate_user_profile(questions, answers):
    profile = {}

    for question, answer in zip(questions, answers):

        weights = question["weights"]

        for characteristic, weight in weights.items():

            score = answer * weight

            if characteristic not in profile:
                profile[characteristic] = 0

            profile[characteristic] += score

    return profile


def normalize_profile(profile, questions):
    min_profile = {}
    max_profile = {}

    for question in questions:

        for characteristic, weight in question["weights"].items():

            if characteristic not in min_profile:
                min_profile[characteristic] = 0
                max_profile[characteristic] = 0

            possible_min = min(1 * weight, 5 * weight)
            possible_max = max(1 * weight, 5 * weight)

            min_profile[characteristic] += possible_min
            max_profile[characteristic] += possible_max

    normalized = {}

    for characteristic, score in profile.items():

        minimum = min_profile[characteristic]
        maximum = max_profile[characteristic]

        if maximum == minimum:
            normalized[characteristic] = 50
        else:
            normalized[characteristic] = (
                (score - minimum) /
                (maximum - minimum)
            ) * 100

    return normalized


def calculate_match(user_profile, specialization_profile):

    total_score = 0
    total_weight = 0

    for characteristic, target_value in specialization_profile.items():

        user_value = user_profile.get(characteristic, 0)

        # Переводим профиль специальности из 0–1 в 0–100
        target_percent = target_value * 100

        # Насколько выражена нужная характеристика у пользователя
        score = min(user_value, target_percent)

        total_score += score * target_value
        total_weight += target_value

    if total_weight == 0:
        return 0

    match = total_score / total_weight

    return match