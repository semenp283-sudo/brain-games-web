
import math
import random

import streamlit as st


# -------------------------
# Настройки сайта
# -------------------------

st.set_page_config(
    page_title="Brain Games",
    page_icon="🧠",
    layout="centered",
)


# -------------------------
# Генерация игровых заданий
# -------------------------

def is_prime(number):
    if number < 2:
        return False

    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            return False

    return True


def generate_question(game):
    if game == "Проверка на чётность":
        number = random.randint(1, 100)
        answer = "yes" if number % 2 == 0 else "no"
        question = str(number)

    elif game == "Калькулятор":
        number1 = random.randint(1, 30)
        number2 = random.randint(1, 30)
        operator = random.choice(["+", "-", "*"])

        if operator == "+":
            answer = number1 + number2
        elif operator == "-":
            answer = number1 - number2
        else:
            answer = number1 * number2

        question = f"{number1} {operator} {number2}"

    elif game == "НОД":
        number1 = random.randint(1, 100)
        number2 = random.randint(1, 100)

        answer = math.gcd(number1, number2)
        question = f"{number1} и {number2}"

    elif game == "Арифметическая прогрессия":
        first_number = random.randint(1, 20)
        difference = random.randint(1, 10)
        hidden_index = random.randint(0, 9)

        progression = [
            first_number + difference * index
            for index in range(10)
        ]

        answer = progression[hidden_index]

        progression[hidden_index] = ".."
        question = " ".join(map(str, progression))

    elif game == "Простое число":
        number = random.randint(1, 100)

        answer = "yes" if is_prime(number) else "no"
        question = str(number)

    return question, str(answer)


# -------------------------
# Состояние игры
# -------------------------

def reset_game(game):
    st.session_state.selected_game = game
    st.session_state.round_number = 1
    st.session_state.game_finished = False
    st.session_state.game_won = False
    st.session_state.message = ""
    st.session_state.message_type = ""

    question, answer = generate_question(game)

    st.session_state.question = question
    st.session_state.correct_answer = answer


def check_answer(user_answer, correct_answer):
    user_answer = user_answer.strip().lower()

    if correct_answer in ("yes", "no"):
        return user_answer == correct_answer

    try:
        return int(user_answer) == int(correct_answer)
    except ValueError:
        return False


# -------------------------
# Интерфейс
# -------------------------

st.title("🧠 Brain Games")
st.subheader("Тренируй свой мозг!")

st.write(
    "Пять игр для тренировки логики, "
    "математики и сообразительности."
)

games = [
    "Проверка на чётность",
    "Калькулятор",
    "НОД",
    "Арифметическая прогрессия",
    "Простое число",
]

game = st.selectbox(
    "Выбери игру:",
    games,
)

# Первый запуск или переключение игры
if (
    "selected_game" not in st.session_state
    or st.session_state.selected_game != game
):
    reset_game(game)


st.divider()

st.subheader(game)

st.write(f"Раунд: {st.session_state.round_number} из 3")

# Описание задания
if game == "Проверка на чётность":
    st.write("Ответь yes, если число чётное, или no, если нечётное.")

elif game == "Калькулятор":
    st.write("Вычисли результат выражения.")

elif game == "НОД":
    st.write("Найди наибольший общий делитель двух чисел.")

elif game == "Арифметическая прогрессия":
    st.write("Найди пропущенное число в последовательности.")

elif game == "Простое число":
    st.write("Ответь yes, если число простое, или no, если составное.")


# Показываем задание
st.title(st.session_state.question)


# -------------------------
# Ответ игрока
# -------------------------

if not st.session_state.game_finished:

    if game in ("Проверка на чётность", "Простое число"):
        answer = st.radio(
            "Твой ответ:",
            ["yes", "no"],
            horizontal=True,
            key=f"answer_{st.session_state.round_number}",
        )
    else:
        answer = st.text_input(
            "Введи свой ответ:",
            key=f"answer_{st.session_state.round_number}",
        )

    if st.button("Ответить", key="submit_answer"):

        if not answer.strip():
            st.warning("Сначала введи ответ!")
        elif check_answer(
            answer,
            st.session_state.correct_answer,
        ):
            if st.session_state.round_number < 3:
                st.session_state.message = "Правильно! Отличная работа!"
                st.session_state.message_type = "success"

                st.session_state.round_number += 1

                question, correct_answer = generate_question(game)

                st.session_state.question = question
                st.session_state.correct_answer = correct_answer

            else:
                st.session_state.game_finished = True
                st.session_state.game_won = True
                st.session_state.message = (
                    "Поздравляем! Ты прошёл все три раунда!"
                )
                st.session_state.message_type = "success"

            st.rerun()

        else:
            st.session_state.game_finished = True
            st.session_state.game_won = False
            st.session_state.message = (
                f"Неправильно! Правильный ответ: "
                f"{st.session_state.correct_answer}"
            )
            st.session_state.message_type = "error"

            st.rerun()


# -------------------------
# Результат
# -------------------------

if st.session_state.message:

    if st.session_state.message_type == "success":
        st.success(st.session_state.message)
    else:
        st.error(st.session_state.message)


# -------------------------
# Завершение игры
# -------------------------

if st.session_state.game_finished:

    if st.session_state.game_won:
        st.balloons()
        st.success("Ты настоящий гений! 🧠")
    else:
        st.info("Не сдавайся! Попробуй ещё раз.")

    if st.button("Играть заново"):
        reset_game(game)
        st.rerun()
