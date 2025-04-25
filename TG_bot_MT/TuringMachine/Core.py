from TuringMachine.MGSSnakeEater.SnakeCoder import encode_snake, decode_snake
from TuringMachine.Vigner.VignerCoder import encode_vigner, decode_vigner
from dicrionary import text, method, variant_shifra

# Функция для кодирования
def encode(text, method):
    if method == '1':  # Змейка (RailFence)
        encrypted_text, rail_lengths = encode_snake(text)
        print("Зашифрованный текст:", encrypted_text)  # Выводим зашифрованный текст
        print("Длины рельс:", rail_lengths)  # Выводим длины рельс
        return encrypted_text, rail_lengths

    elif method == '2':  # Виженер
        encrypted_text, key = encode_vigner(text)
        print("Зашифрованный текст:", encrypted_text)  # Выводим зашифрованный текст
        print("Сгенерированный ключ:", key)  # Выводим ключ
        return encrypted_text, key

    else:
        print("Некорректный выбор метода шифрования.")
        return None, None

# Функция для декодирования
def decode(text, method):
    if method == '1':  # Змейка (RailFence)
        rail_lengths_input = input("Введите длину первого и второго рельса через пробел: ")

        # Разделяем строку на два числа
        rail_lengths = list(map(int, rail_lengths_input.split()))

        # Проверяем, что введено два числа
        if len(rail_lengths) != 2:
            print("Ошибка: нужно ввести две длины рельсов.")
            return None

        rail1_length, rail2_length = rail_lengths

        if rail1_length + rail2_length != len(text):  # Сумма длин рельсов должна быть равна длине зашифрованного текста
            print("Ошибка: сумма длин рельсов не совпадает с длиной зашифрованного текста.")
            return None
        decrypted_text = decode_snake(text, rail_lengths)
        print("Расшифрованный текст:", decrypted_text)  # Выводим расшифрованный текст
        return decrypted_text

    elif method == '2':  # Виженер
        key = input("Введите ключ для декодирования: ")  # Ввод ключа
        decrypted_text = decode_vigner(text, key)
        print("Расшифрованный текст:", decrypted_text)  # Выводим расшифрованный текст
        return decrypted_text

    else:
        print("Некорректный выбор метода дешифрования.")
        return None

# Выбор варианта: кодировать или декодировать
variant_shifra = variant_shifra()  # Метод кодировки или декодировки
text_input = text()  # Запрос текста из dicrionary.py

# Кодирование или декодирование в зависимости от варианта
if variant_shifra == 1:  # Универсальная функция кодирования
    method_choice = method()  # Метод кодировки (например, '1' для змейки или '2' для Виженера)
    encode(text_input, method_choice)

elif variant_shifra == 2:  # Универсальная функция декодирования
    method_choice = method()  # Метод декодировки (например, '1' для змейки или '2' для Виженера)
    decode(text_input, method_choice)

else:
    print("Некорректный выбор варианта шифрования.")
