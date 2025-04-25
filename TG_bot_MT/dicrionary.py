import random
import string

# Создаем строку всех символов, включая английские и русские буквы, знаки препинания и пробел
all_symbols = """1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя=.,+?!:;«»()—-"'"\ """

def text():
    user_input = input("Введите текст:")  # Получаем текст от пользователя
    return user_input  # Возвращаем введенный текст
def method():
    user_method = input("Выберите метод:")  # Получаем номер метода от пользователя
    return user_method  # Возвращаем введенный текст
def variant_shifra():
    variant_shifra = int(input("выберите метод шиифрования"))  # Получаем номер варианта 1 - кодирование 2 - декодирование
    return variant_shifra  # Возвращаем номер варианта
def hex_text():
    hex_text = input("введите текст в формате hex")
    return hex_text
def key_square():
    while True:
        key = input("Введите ключ (16 символов): ")
        if len(key) == 16 and key.isascii():
            return key
        else:
            print("Ключ должен быть ровно 16 символов и содержать только ASCII-символы.")
# Функция рандомной замены символов в случае невозможности их расшифровки при помощи UTF-8
def random_char_replacement(error):
    # Возвращаем случайный символ
    random_char = random.choice(string.ascii_letters + string.digits + string.punctuation + ' ')
    # Возвращаем новый символ
    return random_char, error.start + 1