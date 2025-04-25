import telebot
import codecs
import os
import string
import random
from dicrionary import random_char_replacement
from TuringMachine.MGSSnakeEater.SnakeCoder import encode_snake, decode_snake
from TuringMachine.Vigner.VignerCoder import encode_vigner, decode_vigner
from dicrionary import text
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from SquareCore import Square  # Импортируем класс Square для шифрования
from SerpentCore import serpent_encrypt, serpent_decrypt  # Импортируем функции шифрования и дешифрования Serpent
from KhufuCore import KhufuCore
from KhafreCore import KhafreCore

API_TOKEN = 'нету токена...'
bot = telebot.TeleBot(API_TOKEN)
user_data = {}  # Хранилище данных пользователя
active_cipher = None  # Активный алгоритм шифрования

# Универсальная функция для генерации случайного ключа
def generate_random_key(length):
    chars = string.ascii_letters + string.digits  # Буквы (верхний и нижний регистр) и цифры
    return ''.join(random.choice(chars) for _ in range(length))

# Генерация случайного ключа для Serpent и Khufu/Khafre (32 символа)
def generate_random_key_for_serpent():
    return generate_random_key(32)

# Генерация случайного ключа для Khufu и Khafre (32 символа)
def generate_random_key_for_khufu_khafre():
    return generate_random_key(32)

# Генерация случайного ключа для Square (16 символов)
def generate_random_key_for_square():
    return generate_random_key(16)

# Функция для обработки ввода ключа
def process_key_input(message, key_length, generate_random_key_func):
    # Проверяем, не ввел ли пользователь 'rand'
    key = message.text.strip()
    if key.lower() == "rand":
        key = generate_random_key_func()
        bot.send_message(message.chat.id, f"Сгенерирован случайный ключ: {key}")
    elif len(key) != key_length:
        bot.send_message(message.chat.id, f"Ключ должен быть ровно {key_length} символов!")
        return None
    return key
# Переменная для хранения состояния выбранного шифра
active_cipher = None

# Путь к папке с руководствами
guides_folder = r"C:\Users\Пользователь\source\repos\TG_bot_MT\TG_bot_MT\guides"

# Хранение временных данных о сессии пользователя
user_data = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Используйте панель ниже для управления.")
    show_main_menu(message.chat.id)

# Главное меню
def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("🔩 Python", callback_data="switch_python"),
        InlineKeyboardButton("🔩 C++", callback_data="switch_cpp"),
        InlineKeyboardButton("🔃 Khufu", callback_data="cipher_khufu"),
        InlineKeyboardButton("🔃 Khafre", callback_data="cipher_khafre"),
        InlineKeyboardButton("🔃 Square", callback_data="cipher_square"),
        InlineKeyboardButton("🔃 Serpent", callback_data="cipher_serpent"),
        InlineKeyboardButton("🧮 Машина Тьюринга", callback_data="turing_machine"),
    )
    bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)

# Обработка кнопок переключения языка
@bot.callback_query_handler(func=lambda call: call.data in ["switch_python", "switch_cpp"])
def switch_language(call):
    if call.data == "switch_python":
        bot.answer_callback_query(call.id, "⚙️ Язык переключен на Python!", show_alert=True)
    elif call.data == "switch_cpp":
        bot.answer_callback_query(call.id, "⚙️ Язык переключен на C++!", show_alert=True)

# Общая функция для обработки кнопки "Назад"
@bot.callback_query_handler(func=lambda call: call.data.startswith("back_to_"))
def handle_back_buttons(call):
    if call.data == "back_to_main":
        show_main_menu(call.message.chat.id)
    elif call.data == "back_to_turing":
        turing_menu(call)

# Обработка выбора машины Тьюринга
@bot.callback_query_handler(func=lambda call: call.data == "turing_machine")
def turing_menu(call):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🔀 Змейка (RailFence)", callback_data="turing_snake"),
        InlineKeyboardButton("🔁 Виженер", callback_data="turing_vigner"),
        InlineKeyboardButton("📄 Документация", callback_data="cipher_infoT"),
        InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")
    )
    bot.edit_message_text("Выберите метод шифрования для машины Тьюринга:", call.message.chat.id, call.message.message_id, reply_markup=markup)

# Обработчик кнопки "Документация"
@bot.callback_query_handler(func=lambda call: call.data == "cipher_infoT")
def send_documentation(call):
    try:
        # Путь к файлу документации
        doc_path = "guides\Руководство к машине Тьюринга.docx"  # Укажите полный или относительный путь к файлу
        with open(doc_path, "rb") as doc:
            bot.send_document(call.message.chat.id, doc)
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "Файл документации не найден. Пожалуйста, проверьте путь.")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Произошла ошибка: {str(e)}")
        
# Обработка выбора метода для змейки или виженера
@bot.callback_query_handler(func=lambda call: call.data in ["turing_snake", "turing_vigner"])
def turing_method_selection(call):
    global active_cipher
    active_cipher = call.data

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🔒 Кодировать", callback_data="turing_encode"),
        InlineKeyboardButton("🔓 Декодировать", callback_data="turing_decode"),
        InlineKeyboardButton("🔙 Назад", callback_data="back_to_turing")
    )
    bot.edit_message_text("Выберите действие:", call.message.chat.id, call.message.message_id, reply_markup=markup)

# Обработка кодирования и декодирования
@bot.callback_query_handler(func=lambda call: call.data in ["turing_encode", "turing_decode"])
def turing_action_selection(call):
    action = call.data
    if action == "turing_encode":
        msg = bot.send_message(call.message.chat.id, "Введите текст для кодирования:")
        bot.register_next_step_handler(msg, process_turing_text, action="encode")
    elif action == "turing_decode":
        msg = bot.send_message(call.message.chat.id, "Введите текст для декодирования:")
        bot.register_next_step_handler(msg, process_turing_text, action="decode")


# Обработка введенного текста для кодирования или декодирования
def process_turing_text(message, action):
    user_data[message.chat.id] = {'text': message.text}
    
    if active_cipher == "turing_snake":
        if action == "encode":
            encrypted_text, rail_lengths = encode_snake(message.text)
            bot.send_message(message.chat.id, f"Зашифрованный текст (Змейка): {encrypted_text}\nДлины рельс: {rail_lengths}")
        elif action == "decode":
            msg = bot.send_message(message.chat.id, "Введите длины рельс через пробел:")
            bot.register_next_step_handler(msg, process_snake_decryption, text=message.text)
    
    elif active_cipher == "turing_vigner":
        if action == "encode":
            encrypted_text, key = encode_vigner(message.text)
            bot.send_message(message.chat.id, f"Зашифрованный текст (Виженер): {encrypted_text}\nКлюч: {key}")
        elif action == "decode":
            msg = bot.send_message(message.chat.id, "Введите ключ для декодирования:")
            bot.register_next_step_handler(msg, process_vigner_decryption, text=message.text)

# Декодирование текста для метода Змейка
def process_snake_decryption(message, text):
    try:
        rail_lengths = list(map(int, message.text.split()))
        if len(rail_lengths) != 2:
            raise ValueError("Ошибка: нужно ввести две длины рельсов.")
        decrypted_text = decode_snake(text, rail_lengths)
        bot.send_message(message.chat.id, f"Расшифрованный текст (Змейка): {decrypted_text}")
    except ValueError as e:
        bot.send_message(message.chat.id, str(e))

# Декодирование текста для метода Виженер
def process_vigner_decryption(message, text):
    try:
        key = message.text
        decrypted_text = decode_vigner(text, key)
        bot.send_message(message.chat.id, f"Расшифрованный текст (Виженер): {decrypted_text}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка декодирования: {str(e)}")

# Обновление панели с кнопками для шифрования/дешифрования
def show_cipher_menu(chat_id, message_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🔒 Шифровать", callback_data="encrypt"),
        InlineKeyboardButton("🔓 Дешифровать", callback_data="decrypt"),
        InlineKeyboardButton("📄 Документация", callback_data="cipher_info"),
        InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")
    )
    bot.edit_message_reply_markup(chat_id, message_id, reply_markup=markup)

# Обработка выбора шифра
@bot.callback_query_handler(func=lambda call: call.data.startswith("cipher_") and call.data != "cipher_info")
def cipher_selection(call):
    global active_cipher
    cipher_map = {
        "cipher_khufu": "Khufu",
        "cipher_khafre": "Khafre",
        "cipher_square": "Square",
        "cipher_serpent": "Serpent"
    }
    active_cipher = cipher_map[call.data]
    bot.answer_callback_query(call.id, f"Выбран режим {active_cipher}!")
    
    # Обновляем меню с кнопкой "Информация"
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🔒 Шифровать", callback_data="encrypt"),
        InlineKeyboardButton("🔓 Дешифровать", callback_data="decrypt"),
        InlineKeyboardButton("📄 Документация", callback_data="cipher_info"),
        InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")
    )
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)

# Обработка кнопки "Информация"
@bot.callback_query_handler(func=lambda call: call.data == "cipher_info")
def cipher_info(call):
    send_guide_file(call.message.chat.id, active_cipher)
    
# Обработка шифрования
@bot.callback_query_handler(func=lambda call: call.data == "encrypt")
def encrypt_message(call):
    if active_cipher == "Khufu":
        msg = bot.send_message(call.message.chat.id, "Введите текст для шифрования:")
        bot.register_next_step_handler(msg, process_khufu_encryption_text)
    if active_cipher == "Square":
        msg = bot.send_message(call.message.chat.id, "Введите текст для шифрования:")
        bot.register_next_step_handler(msg, process_encryption_text)
    elif active_cipher == "Serpent":
        msg = bot.send_message(call.message.chat.id, "Введите текст для шифрования:")
        bot.register_next_step_handler(msg, process_serpent_encryption_text)
    elif active_cipher == "Khafre":
        msg = bot.send_message(call.message.chat.id, "Введите текст для шифрования:")
        bot.register_next_step_handler(msg, process_khafre_encryption_text)
    else:
        bot.answer_callback_query(call.id, "Шифрование доступно только для Khufu, Khafre, Serpent и Square!", show_alert=False)

def process_khufu_encryption_text(message):
    user_data[message.chat.id] = {'text': message.text}
    msg = bot.send_message(message.chat.id, "Введите ключ (32 символа) или 'rand' для случайного ключа:")
    bot.register_next_step_handler(msg, process_khufu_encryption_key)

def process_khufu_encryption_key(message):
    try:
        key = process_key_input(message, 32, generate_random_key_for_khufu_khafre)
        if not key:
            return
        
        khufu = KhufuCore(key)
        encrypted_text = khufu.encrypt(user_data[message.chat.id]['text'])
        bot.send_message(message.chat.id, f"Зашифрованный текст (Khufu): {encrypted_text}")
    except ValueError as e:
        bot.send_message(message.chat.id, str(e))

def process_khafre_encryption_text(message):
    user_data[message.chat.id] = {'text': message.text}
    msg = bot.send_message(message.chat.id, "Введите ключ (32 символа) или 'rand' для случайного ключа:")
    bot.register_next_step_handler(msg, process_khafre_encryption_key)

def process_khafre_encryption_key(message):
    try:
        key = process_key_input(message, 32, generate_random_key_for_khufu_khafre)
        if not key:
            return
        
        khafre = KhafreCore(key)
        encrypted_text = khafre.encrypt(user_data[message.chat.id]['text'])
        bot.send_message(message.chat.id, f"Зашифрованный текст (Khafre): {encrypted_text}")
    except ValueError as e:
        bot.send_message(message.chat.id, str(e))

# Обработка дешифрования для Khufu
@bot.callback_query_handler(func=lambda call: call.data == "decrypt" and active_cipher == "Khufu")
def decrypt_khufu_message(call):
    msg = bot.send_message(call.message.chat.id, "Введите текст для дешифрования:")
    bot.register_next_step_handler(msg, process_khufu_decryption_text)

def process_khufu_decryption_text(message):
    user_data[message.chat.id] = {'text': message.text}
    msg = bot.send_message(message.chat.id, "Введите ключ (32 символа):")
    bot.register_next_step_handler(msg, process_khufu_decryption_key)

def process_khufu_decryption_key(message):
    try:
        key = message.text.strip()
        if len(key) != 32:
            raise ValueError("Ключ должен быть ровно 32 символа!")
        
        # Передаем строковый ключ в конструктор KhufuCore
        khufu = KhufuCore(key)
        decrypted_text = khufu.decrypt(user_data[message.chat.id]['text'])
        bot.send_message(message.chat.id, f"Расшифрованный текст (Khufu): {decrypted_text}")
    except ValueError as e:
        bot.send_message(message.chat.id, str(e))

# Обработка дешифрования для Khafre
@bot.callback_query_handler(func=lambda call: call.data == "decrypt" and active_cipher == "Khafre")
def decrypt_khafre_message(call):
    msg = bot.send_message(call.message.chat.id, "Введите текст для дешифрования:")
    bot.register_next_step_handler(msg, process_khafre_decryption_text)

def process_khafre_decryption_text(message):
    user_data[message.chat.id] = {'text': message.text}
    msg = bot.send_message(message.chat.id, "Введите ключ (32 символа):")
    bot.register_next_step_handler(msg, process_khafre_decryption_key)

def process_khafre_decryption_key(message):
    try:
        key = message.text.strip()
        if len(key) != 32:
            raise ValueError("Ключ должен быть ровно 32 символа!")
        
        # Передаем строковый ключ в конструктор KhafreCore
        khafre = KhafreCore(key)
        decrypted_text = khafre.decrypt(user_data[message.chat.id]['text'])
        bot.send_message(message.chat.id, f"Расшифрованный текст (Khafre): {decrypted_text}")
    except ValueError as e:
        bot.send_message(message.chat.id, str(e))

def process_encryption_text(message):
    user_data[message.chat.id] = {'text': message.text}
    msg = bot.send_message(message.chat.id, "Введите ключ (16 символов) или 'rand' для случайного ключа:")
    bot.register_next_step_handler(msg, process_encryption_key)

def process_encryption_key(message):
    try:
        key = process_key_input(message, 16, generate_random_key_for_square)
        if not key:
            return
        
        text = user_data[message.chat.id]['text']
        
        if active_cipher == "Square":
            cipher = Square()
            encrypted_text = cipher.Encryption(text, key)
        
        bot.send_message(message.chat.id, f"Зашифрованный текст (в hex): {encrypted_text.hex()}")
    except ValueError as e:
        bot.send_message(message.chat.id, str(e))
        

# Обработка дешифрования для Square
def process_square_decryption_text(message):
    try:
        # Зашифрованный текст в hex
        encrypted_text_hex = message.text.strip()
        encrypted_text_bytes = bytes.fromhex(encrypted_text_hex)  # Преобразуем hex в байты
        
        # Сохраняем данные для текущего пользователя
        user_data[message.chat.id] = {'encrypted_text_bytes': encrypted_text_bytes}
        
        # Запрашиваем ключ
        msg = bot.send_message(message.chat.id, "Введите ключ (16 символов):")
        bot.register_next_step_handler(msg, process_square_decryption_key)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка: введите корректный зашифрованный текст в hex формате.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка обработки: {str(e)}")

def process_square_decryption_key(message):
    try:
        # Получаем ключ
        key = message.text.strip()
        if len(key) != 16:
            raise ValueError("Ключ должен быть ровно 16 символов!")
        
        # Проверяем, есть ли данные в user_data
        if message.chat.id not in user_data or 'encrypted_text_bytes' not in user_data[message.chat.id]:
            raise ValueError("Ошибка: отсутствуют данные для дешифрования. Попробуйте снова.")

        # Получаем зашифрованные байты
        encrypted_text_bytes = user_data[message.chat.id]['encrypted_text_bytes']
        
        # Расшифровка с использованием Square
        cipher = Square()
        decrypted_bytes = cipher.Decryption(encrypted_text_bytes, key)

        # Преобразование символов на рандомные при неправильном ключе
        codecs.register_error("random_replace", random_char_replacement)

        # Преобразуем байты в строку, удаляя нулевые байты
        decrypted_text = decrypted_bytes.rstrip(b'\x00').decode('utf-8', errors='random_replace')
        
        # Отправляем результат пользователю
        bot.send_message(message.chat.id, f"Расшифрованный текст: {decrypted_text}")
    except ValueError as e:
        bot.send_message(message.chat.id, f"Ошибка: {str(e)}")
    except UnicodeDecodeError:
        bot.send_message(message.chat.id, "Ошибка: невозможно декодировать расшифрованный текст. Проверьте ключ.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка дешифрования: {str(e)}")
# Обработчик для дешифрования Serpent
# Дешифровка текста для метода Serpent
@bot.callback_query_handler(func=lambda call: call.data == "decrypt")
def decrypt_message(call):
    if active_cipher == "Serpent":
        msg = bot.send_message(call.message.chat.id, "Введите зашифрованный текст (в hex формате):")
        bot.register_next_step_handler(msg, process_serpent_decryption_text)
    elif active_cipher == "Square":
        msg = bot.send_message(call.message.chat.id, "Введите зашифрованный текст (в hex формате):")
        bot.register_next_step_handler(msg, process_square_decryption_text)
    else:
        bot.answer_callback_query(call.id, f"Дешифрование недоступно для {active_cipher}!", show_alert=True)

def process_serpent_encryption_text(message):
    user_data[message.chat.id] = {'text': message.text}
    msg = bot.send_message(message.chat.id, "Введите ключ (32 символа) или 'rand' для случайного ключа:")
    bot.register_next_step_handler(msg, process_serpent_encryption_key)

def process_serpent_encryption_key(message):
    try:
        key = process_key_input(message, 32, generate_random_key_for_serpent)
        if not key:
            return
        
        key = key.encode()  # Преобразуем ключ в байты
        text = user_data[message.chat.id]['text'].encode('utf-8')
        
        encrypted_text = serpent_encrypt(text, key)
        bot.send_message(message.chat.id, f"Зашифрованный текст (в hex): {encrypted_text.hex()}")
    except ValueError as e:
        bot.send_message(message.chat.id, str(e))
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка шифрования: {str(e)}")
# Обработка зашифрованного текста для дешифрования Serpent
def process_serpent_decryption_text(message):
    try:
        # Получаем зашифрованный текст в hex формате
        encrypted_text_hex = message.text.strip()
        encrypted_text_bytes = bytes.fromhex(encrypted_text_hex)  # Преобразуем hex в байты

        # Сохраняем данные для текущего пользователя
        user_data[message.chat.id] = {'encrypted_text_bytes':encrypted_text_bytes}

        # Запрашиваем ключ у пользователя
        msg = bot.send_message(message.chat.id, "Введите ключ (32 символа):")
        bot.register_next_step_handler(msg, process_serpent_decryption_key)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка: введите корректный зашифрованный текст в hex формате.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка обработки: {str(e)}")

# Обработка ключа для дешифрования Serpent
def process_serpent_decryption_key(message):
    try:
        # Преобразуем ключ в байты
        key = message.text.encode()  
        if len(key) != 32:  # Ключ должен быть 32 байта (256 бит)
            raise ValueError("Ключ должен быть ровно 32 символа!")

        # Получаем зашифрованный текст из данных
        encrypted_text_bytes = user_data[message.chat.id]['encrypted_text_bytes']

        # Дешифровка с использованием Serpent
        decrypted_text = serpent_decrypt(encrypted_text_bytes, key)

        # Проверяем, что результат дешифровки — это байты
        if isinstance(decrypted_text, bytes):
            try:
                # Пытаемся декодировать в строку UTF-8
                decrypted_text_str = decrypted_text.decode('utf-8', errors='ignore')  
                if not decrypted_text_str:
                    decrypted_text_str = f"Дешифрованные данные не содержат текст. Вот байты: {decrypted_text.hex()}"
            except UnicodeDecodeError:
                decrypted_text_str = f"Ошибка декодирования. Вот необработанные байты: {decrypted_text.hex()}"
        else:
            decrypted_text_str = decrypted_text  # Если это уже строка, просто выводим её

        bot.send_message(message.chat.id, f"Расшифрованный текст: {decrypted_text_str}")

    except ValueError as e:
        bot.send_message(message.chat.id, str(e))
    except UnicodeDecodeError:
        bot.send_message(message.chat.id, "Ошибка декодирования UTF-8. Проверьте корректность введенных данных.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка дешифрования: {str(e)}")


def send_guide_file(chat_id, cipher):
    # Составляем название файла на основе выбранного шифра
    file_name_user = f"{cipher}_пользователю.docx"
    file_name_dev = f"{cipher}_разработчику.docx"
    
    # Полные пути к файлам
    file_path_user = os.path.join(guides_folder, file_name_user)
    file_path_dev = os.path.join(guides_folder, file_name_dev)

    # Проверяем существование файлов
    if os.path.exists(file_path_user) and os.path.exists(file_path_dev):
        # Отправляем сначала файл для пользователя
        with open(file_path_user, 'rb') as file:
            bot.send_document(chat_id, file, caption=f"Руководство для пользователя по {cipher}")
        
        # Отправляем файл для разработчика
        with open(file_path_dev, 'rb') as file:
            bot.send_document(chat_id, file, caption=f"Руководство для разработчика по {cipher}")
    else:
        bot.send_message(chat_id, "Ошибка: не найдено нужных файлов для выбранного шифра.")

# Обработчик текстовых файлов
@bot.message_handler(content_types=['document'])
def handle_document(message):
    if active_cipher is None:
        bot.send_message(message.chat.id, "Пожалуйста, выберите алгоритм шифрования перед загрузкой файла.")
        return

    # Сохраняем файл
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Сохраняем текст из файла
    file_path = os.path.join("temp", message.document.file_name)
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Извлечение текста из файла
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Сохраняем текст для дальнейшей обработки
    user_data[message.chat.id] = {'text': text, 'file_path': file_path}

    # Отправляем кнопки шифрования/дешифрования
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🔒 Шифровать", callback_data="encrypt_file"),
        InlineKeyboardButton("🔓 Дешифровать", callback_data="decrypt_file")
    )
    bot.send_message(message.chat.id, "Файл получен. Выберите действие:", reply_markup=markup)

# Обработка шифрования файла
@bot.callback_query_handler(func=lambda call: call.data == "encrypt_file")
def encrypt_file(call):
    chat_id = call.message.chat.id
    text = user_data[chat_id]['text']
    file_path = user_data[chat_id]['file_path']

    try:
        # Запрос ключа для шифрования
        msg = bot.send_message(chat_id, "Введите ключ для шифрования (или напишите 'rand' для генерации случайного ключа):")
        bot.register_next_step_handler(msg, process_file_encryption, text=text, file_path=file_path)
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка шифрования: {str(e)}")

# Обработка шифрования с ключом
def process_file_encryption(message, text, file_path):
    chat_id = message.chat.id
    user_key = message.text.strip()

    try:
        # Если ключ "rand" - генерируем случайный ключ
        if user_key.lower() == "rand":
            if active_cipher == "Serpent":
                key = generate_random_key_for_serpent()
            elif active_cipher in ["Khufu", "Khafre"]:
                key = generate_random_key_for_serpent()  # Для Khufu и Khafre используем 32 символа
            elif active_cipher == "Square":
                key = generate_random_key_for_square()
        else:
            # Преобразуем введенный ключ
            if active_cipher in ["Khufu", "Khafre"]:
                key = user_key  # Строка из 32 символов
            elif active_cipher == "Serpent":
                key = user_key  # Строка из 32 символов
            elif active_cipher == "Square":
                key = user_key  # Строка из 16 символов

        print(f"Используемый ключ: {key}")  # Для отладки
        print(f"Длина ключа: {len(key)}")  # Для отладки

        # Шифрование текста
        if active_cipher == "Khufu":
            cipher = KhufuCore(key)
            encrypted_text = cipher.encrypt(text)
        elif active_cipher == "Khafre":
            cipher = KhafreCore(key)
            encrypted_text = cipher.encrypt(text)
        elif active_cipher == "Serpent":
            encrypted_text = serpent_encrypt(text.encode('utf-8'), key.encode('utf-8'))
        elif active_cipher == "Square":
            cipher = Square()
            encrypted_text = cipher.Encryption(text, key)

        # Сохранение результата в файл
        result_file = file_path.replace('.txt', f'_{active_cipher}_шифрованный.txt')
        with open(result_file, 'w', encoding='utf-8') as file:
            file.write(encrypted_text.hex() if isinstance(encrypted_text, bytes) else encrypted_text)

        # Отправка результата
        with open(result_file, 'rb') as file:
            bot.send_document(chat_id, file, caption=f"Зашифрованный файл. Метод: {active_cipher}\nКлюч: {key}")

    except Exception as e:
        bot.send_message(chat_id, f"Ошибка шифрования: {str(e)}")

@bot.callback_query_handler(func=lambda call: call.data == "decrypt_file")
def decrypt_file(call):
    chat_id = call.message.chat.id
    text = user_data[chat_id]['text']
    file_path = user_data[chat_id]['file_path']

    try:
        # Запрос ключа для дешифрования
        msg = bot.send_message(chat_id, "Введите ключ для дешифрования:")
        bot.register_next_step_handler(msg, process_file_decryption, text=text, file_path=file_path)
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка при запросе ключа для дешифрования: {str(e)}")

def process_file_decryption(message, text, file_path):
    try:
        key = message.text.strip()

        # Логирование ключа и данных
        print(f"Получен ключ для дешифрования: {key}")
        print(f"Текст для дешифрования: {text[:50]}...")  # Только первые 50 символов для логирования

        if active_cipher == "Khufu":
            # Дешифрование с использованием алгоритма Khufu
            try:
                cipher = KhufuCore(key)  # Передаем строковый ключ
                decrypted_text = cipher.decrypt(text)
            except ValueError as e:
                bot.send_message(message.chat.id, f"Ошибка: Невалидный ключ для дешифрования. {str(e)}")
                return
        elif active_cipher == "Khafre":
            # Дешифрование с использованием алгоритма Khafre
            try:
                cipher = KhafreCore(key)  # Передаем строковый ключ
                decrypted_text = cipher.decrypt(text)
            except ValueError as e:
                bot.send_message(message.chat.id, f"Ошибка: Невалидный ключ для дешифрования. {str(e)}")
                return
        elif active_cipher == "Serpent":
            # Дешифрование с использованием алгоритма Serpent
            try:
                # Преобразуем ключ в байты (передается как строка)
                key_bytes = message.text.encode('utf-8')  # Преобразуем строку в байты UTF-8

                decrypted_bytes = bytes.fromhex(text)  # Преобразуем текст в байты
                decrypted_data = serpent_decrypt(decrypted_bytes, key_bytes)

                if isinstance(decrypted_data, bytes):
                    try:
                        decrypted_text = decrypted_data.decode('utf-8')  # Пытаемся декодировать как строку
                    except UnicodeDecodeError:
                        decrypted_text = decrypted_data.hex()  # Если не получилось, выводим как HEX
                else:
                    decrypted_text = decrypted_data
            except ValueError:
                bot.send_message(message.chat.id, "Ошибка: Некорректный формат данных для дешифрования.")
                return
        elif active_cipher == "Square":
            # Дешифрование с использованием алгоритма Square
            try:
                cipher = Square()
                codecs.register_error("random_replace", random_char_replacement)
                decrypted_text = cipher.Decryption(bytes.fromhex(text), key).decode('utf-8', errors = 'random_replace')
            except Exception as e:
                bot.send_message(message.chat.id, f"Ошибка при дешифровании методом Square: {str(e)}")
                return

        # Логирование результата дешифрования
        print(f"Дешифрованный текст: {decrypted_text[:50]}...")  # Логируем первые 50 символов

        # Сохранение результата в файл
        result_file = file_path.replace('.txt', f'_{active_cipher}_дешифрованный.txt')
        with open(result_file, 'w', encoding='utf-8') as file:
            file.write(decrypted_text)

        # Отправка результата
        with open(result_file, 'rb') as file:
            bot.send_document(message.chat.id, file, caption=f"Дешифрованный файл. Метод: {active_cipher}")

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при дешифровании: {str(e)}")

        
# Запуск бота
bot.polling(none_stop=True)