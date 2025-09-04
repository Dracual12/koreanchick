import re
from config import dp, bot, db
import difflib
import json
import random
import pandas as pd
from files.icons import icons


def read_table(user, category: str, mood: str, style: str, rec: str,
               blacklist: list, whitelist: list, numb: int, price: int, g: int, first_dish_name: str or None):
    # Загружаем таблицу с меню
    df = pd.DataFrame(db.menu_get(), columns=[
        'id',
        'Категория',
        'Название блюда',
        'Комментарий нейросети',
        'Ингредиенты',
        'Простые ингредиенты',
        'КБЖУ',
        'Граммы',
        'Цена',
        'Размер',
        'iiko_id',
        'Стиль питания',
        'Настроение',
        'Рекомендации нутрициолога',
        'Ссылка',
        'Дополнительные продажи',
        'Рейтинг',
        'Отзывы',
        'Коины'
    ])
    # Получаем рейтинги пользователя
    user_ratings = {}
    try:
        result = db.cursor.execute("SELECT users_dish_coefficients FROM correlation_coefficient WHERE user_id = ?",
                                   (user,)).fetchone()
        if result and result[0]:
            user_ratings = eval(result[0])
    except Exception as e:
        print(f"Error getting user ratings: {e}")
    df = df[df['Настроение'].str.contains(mood)]
    df = df.loc[df['Категория'] == category]
    df = df.values.tolist()

    if not len(df):
        return None, None, None

    rec_mood = {
        'Радость': 0,
        'Печаль': 1,
        'Гнев': 2,
        'Спокойствие': 3,
        'Волнение': 4,
    }

    rec_item = 0
    if rec == 'Нутрициолог' and (df[0][9] != 'None' or df[0][9] != '' or df[0][9] is not None):
        rec_item = 13
    if rec == 'Пользователи' and (df[0][10] != 'None' or df[0][10] != '' or df[0][10] is not None):
        rec_item = 10
    if rec == 'Обломов' and (df[0][11] != 'None' or df[0][11] != '' or df[0][11] is not None):
        rec_item = 11
    if rec == 'Ивлев' and (df[0][12] != 'None' or df[0][12] != '' or df[0][12] is not None):
        rec_item = 12

    if rec_item == 0:
        return None, None, None

    def sort_by(item):
        # Получаем базовый порядок из рекомендаций
        mood_info = item[rec_item].split(', ')

        min_order = float('inf')
        for info in mood_info:
            match = re.match(r'(\w+)\s*=\s*(\d+)', info)
            if match:
                mood_name, mood_order = match.groups()
                if mood_name.strip() == mood:
                    min_order = min(min_order, int(mood_order))

        # Учитываем рейтинг пользователя
        dish_id = str(item[0])
        if dish_id in user_ratings:
            # Если у блюда есть рейтинг пользователя, корректируем порядок
            # Чем выше рейтинг, тем ниже порядок (ближе к началу списка)
            rating_data = user_ratings[dish_id]
            if isinstance(rating_data, dict):
                user_rating = rating_data['rating']
                rating_count = rating_data['count']
                # Учитываем как рейтинг, так и количество оценок
                # Чем больше оценок, тем сильнее влияние рейтинга
                min_order = min_order - (user_rating * 10 * (1 + rating_count / 10))
            else:
                # Для обратной совместимости со старым форматом
                user_rating = float(rating_data)
                min_order = min_order - (user_rating * 10)

        return min_order

    # Изменение в сортировке, передача rec_item в sort_by функцию
    ccal_user = db.get_temp_users_ccal(user)
    df2 = []
    if ccal_user is not None and ccal_user != 'пусто':
        for e in df:
            dish_ccal = float(e[6].split('Кк')[1]) * (float(e[7]) / 100)
            if e[6] is not None:
                if float(db.get_temp_users_ccal(user)) > float(dish_ccal) != 0:
                    df2.append(e)
    else:
        df2 = df
    # Добавляем вторичный ключ сортировки для стабильного порядка
    # Используем название блюда как третий ключ для гарантии стабильного порядка
    df_new = sorted(df2, key=lambda x: (sort_by(x), x[0], x[2]))  # x[2] - название блюда
    dishes = []
    dishes_white = []
    try:
        stop_list = list(eval(db.get_stop_list(db.get_client_temp_rest(user))).keys())
    except Exception as e:
        stop_list = []
    if first_dish_name:
        first_dish = db.restaurants_get_by_name(first_dish_name)
        dish_ingredients_unformatted = str(first_dish[5]).strip().lower()
        dish_ingredients = dish_ingredients_unformatted.split(',')
        dishes_white.append({
            "Категория": first_dish[1],
            "Название": first_dish[2],
            "Описание": first_dish[3],
            "Ингредиенты": dish_ingredients,
            "Стиль питания": first_dish[11],
            "Настроение": mood,
            "Ссылка": first_dish[13],
            "Рейтинг": first_dish[16],
            "Цена": first_dish[8],
            "Грамм": first_dish[7],
            "Размер": first_dish[9],
            "КБЖУ": first_dish[6]
        })
    for dish in df_new:
        dish_ingredients = [ingredient.strip() for ingredient in str(dish[5]).lower().split(',')]
        if set(blacklist) & set(dish_ingredients):
            continue

        if dish[2] == first_dish_name or dish[2] in stop_list:
            continue

        dish_data = {
            "Категория": dish[1],
            "Название": dish[2],
            "Описание": dish[3],
            "Ингредиенты": dish_ingredients,
            "Стиль питания": dish[11],
            "Настроение": mood,
            "Ссылка": dish[13],
            "Рейтинг": dish[16],
            "Цена": dish[8],
            "Грамм": dish[7],
            "Размер": dish[9],
            "КБЖУ": dish[6]
        }

        # Добавляем информацию о рейтинге пользователя
        dish_id = str(dish[0])
        if dish_id in user_ratings:
            rating_data = user_ratings[dish_id]
            if isinstance(rating_data, dict):
                dish_data["user_rating"] = rating_data['rating']
                dish_data["rating_count"] = rating_data['count']
            else:
                dish_data["user_rating"] = float(rating_data)
                dish_data["rating_count"] = 1

        if set(whitelist) & set(dish_ingredients):
            dishes_white.append(dish_data)
        else:
            dishes.append(dish_data)

    # Формируем итоговый список: сначала dishes_white, потом dishes без дублей
    all_dishes = dishes_white + [d for d in dishes if d["Название"] not in [w["Название"] for w in dishes_white]]

    # Возвращаем результат
    if len(all_dishes) > 0:
        if len(all_dishes) > numb:
            return all_dishes[numb], len(all_dishes), len(all_dishes) - numb - 1
        else:
            return all_dishes[-1], len(all_dishes), 0
    else:
        return None, None, None


def get_dish(user: int):
    ank1 = db.get_users_first_q(user)
    ank2 = db.get_users_second_q(user)
    category = db.get_temp_users_category(user)
    mood = ank1[1]
    style = ank2[3]
    rec = 'Нутрициолог'
    blacklist = [ingredient.strip() for ingredient in db.get_temp_users_dont_like_to_eat(user).split(",")]
    whitelist = [ingredient.strip() for ingredient in db.get_temp_users_like_to_eat(user).split(",")]
    numb = db.get_client_temp_dish(user)
    price = db.get_dish_price(user)
    g = db.get_g(user)
    first_dish = None
    recommendation = generate_recommendation(user)
    db.set_temp_rec(user, f"{recommendation}")
    if recommendation:
        for item in recommendation:
            if item[0] == icons[category]:
                first_dish = item[1]
    return read_table(user, category, mood, style, rec, blacklist, whitelist, numb, price, g, first_dish)


def generate_recommendation(user):
    mood = db.get_temp_users_mood(user)
    style = db.get_temp_users_style(user)
    blacklist = [ingredient.strip() for ingredient in db.get_temp_users_dont_like_to_eat(user).split(",")]
    whitelist = [ingredient.strip() for ingredient in db.get_temp_users_like_to_eat(user).split(",")]

    # Получаем оценки пользователя
    user_ratings = {}
    try:
        result = db.cursor.execute("SELECT users_dish_coefficients FROM correlation_coefficient WHERE user_id = ?",
                                   (user,)).fetchone()
        if result and result[0]:
            user_ratings = eval(result[0])
    except Exception as e:
        print(f"Error getting user ratings: {e}")

    # Загружаем таблицу с меню
    df = pd.DataFrame(db.menu_get(), columns=[
        'id',
        'Категория',
        'Название блюда',
        'Комментарий нейросети',
        'Ингредиенты',
        'Простые ингредиенты',
        'КБЖУ',
        'Граммы',
        'Цена',
        'Размер',
        'iiko_id',
        'Стиль питания',
        'Настроение',
        'Рекомендации нутрициолога',
        'Ссылка',
        'Дополнительные продажи',
        'Рейтинг',
        'Отзывы',
        'Коины'
    ])
    df = df[df['Настроение'].str.contains(mood)]
    df = df[df['Стиль питания'].str.contains(style)]
    if df.empty:
        return None

    # Получаем стоп-лист
    try:
        stop_list = list(eval(db.get_stop_list(db.get_client_temp_rest(user))).keys())
    except Exception as e:
        stop_list = []

    # Функция для сортировки блюд по рейтингу (как в read_table)
    def sort_by_rating(dish_data):
        # Находим оригинальные данные блюда из DataFrame
        original_dish = None
        for dish in df.values.tolist():
            if str(dish[0]) == str(dish_data['id']):
                original_dish = dish
                break

        if not original_dish:
            return 0

        # Получаем базовый порядок из рекомендаций нутрициолога
        mood_info = original_dish[13].split(', ')  # Рекомендации нутрициолога

        min_order = float('inf')
        for info in mood_info:
            match = re.match(r'(\w+)\s*=\s*(\d+)', info)
            if match:
                mood_name, mood_order = match.groups()
                if mood_name.strip() == mood:
                    min_order = min(min_order, int(mood_order))

        # Учитываем рейтинг пользователя
        dish_id = str(dish_data['id'])
        if dish_id in user_ratings:
            rating_data = user_ratings[dish_id]
            if isinstance(rating_data, dict):
                user_rating = rating_data['rating']
                rating_count = rating_data['count']
                min_order = min_order - (user_rating * 10 * (1 + rating_count / 10))
            else:
                user_rating = float(rating_data)
                min_order = min_order - (user_rating * 10)

        return min_order

    # Группируем блюда по категориям и фильтруем
    category_dishes = {}
    banned_categories = ["Хлеб", "Соус"]

    for dish in df.values.tolist():
        category = dish[1]

        # Пропускаем запрещённые категории
        if category in banned_categories:
            continue

        # Проверяем ингредиенты
        dish_ingredients = [ingredient.strip() for ingredient in str(dish[5]).lower().split(',')]
        if set(blacklist) & set(dish_ingredients):
            continue

        # Проверяем стоп-лист
        if dish[2] in stop_list:
            continue

        # Проверяем, что категория есть в иконках
        if category not in icons:
            continue

        dish_data = {
            "Категория": category,
            "Название": dish[2],
            "Цена": dish[8],
            "Размер": dish[9],
            "id": dish[0],
            "Ингредиенты": dish_ingredients
        }

        # Добавляем информацию о рейтинге пользователя
        dish_id = str(dish[0])
        if dish_id in user_ratings:
            dish_data["user_rating"] = user_ratings[dish_id]

        # Разделяем на whitelist и обычные блюда
        if set(whitelist) & set(dish_ingredients):
            if category not in category_dishes:
                category_dishes[category] = {"white": [], "regular": []}
            category_dishes[category]["white"].append(dish_data)
        else:
            if category not in category_dishes:
                category_dishes[category] = {"white": [], "regular": []}
            category_dishes[category]["regular"].append(dish_data)

    # Выбираем предпочтительные категории или случайные, если предпочтительных нет
    available_categories = list(category_dishes.keys())
    if len(available_categories) == 0:
        return None

    # Получаем предпочтительные категории
    prefer_categories = db.get_prefer_categories()

    # Фильтруем только те предпочтительные категории, которые доступны
    available_prefer_categories = [cat for cat in prefer_categories if cat in available_categories]

    if len(available_prefer_categories) >= 5:
        # Если предпочтительных категорий достаточно, берём первые 5
        selected_categories = available_prefer_categories[:5]
    elif len(available_prefer_categories) > 0:
        # Если предпочтительных категорий меньше 5, дополняем случайными
        remaining_categories = [cat for cat in available_categories if cat not in available_prefer_categories]
        needed_random = 5 - len(available_prefer_categories)
        random_categories = random.sample(remaining_categories, min(needed_random, len(remaining_categories)))
        selected_categories = available_prefer_categories + random_categories
    else:
        # Если предпочтительных категорий нет, выбираем случайные
        selected_categories = random.sample(available_categories, min(5, len(available_categories)))

    recommendation = []

    for category in selected_categories:
        # Сначала берём из whitelist, потом из обычных
        dishes_to_choose = category_dishes[category]["white"] + category_dishes[category]["regular"]

        if dishes_to_choose:
            # Сортируем по рейтингу и берём лучшее блюдо
            dishes_to_choose.sort(key=sort_by_rating)
            best_dish = dishes_to_choose[0]

            recommendation.append((
                f"{icons[category]}",
                best_dish["Название"],
                best_dish["Цена"],
                best_dish.get("user_rating", 0)
            ))

    # Сортируем по цене (как было раньше)
    recommendation = sorted(recommendation, key=lambda x: int(x[2]), reverse=True)

    # Применяем корректировки на основе оценок пользователя
    for i in range(len(recommendation)):
        rating = recommendation[i][3]
        if rating == 5:  # Поднимаем на 2 позиции вверх
            if i > 1:
                recommendation[i], recommendation[i - 2] = recommendation[i - 2], recommendation[i]
        elif rating == 4:  # Поднимаем на 1 позицию вверх
            if i > 0:
                recommendation[i], recommendation[i - 1] = recommendation[i - 1], recommendation[i]
        elif rating == 2:  # Опускаем на 1 позицию вниз
            if i < len(recommendation) - 1:
                recommendation[i], recommendation[i + 1] = recommendation[i + 1], recommendation[i]
        elif rating == 1:  # Опускаем на 2 позиции вниз
            if i < len(recommendation) - 2:
                recommendation[i], recommendation[i + 2] = recommendation[i + 2], recommendation[i]

    # Убираем рейтинг из кортежа перед возвратом
    recommendation = [(icon, name, price) for icon, name, price, _ in recommendation]
    return recommendation
