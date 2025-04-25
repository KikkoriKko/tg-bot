from struct import pack, unpack

# Определение констант для ключа
K0 = 0x9e3779b97f4a7c15
K1 = 0x3c6ef372fe94f82b

def key_schedule(key):
    if len(key) < 32:
        key = key.ljust(32, b'\x00')  # Дополнение ключа до 256 бит
    key_int = int.from_bytes(key, 'big')
    k0 = (key_int >> 128) & 0xFFFFFFFFFFFFFFFF
    k1 = key_int & 0xFFFFFFFFFFFFFFFF

    round_keys = [k0, k1]
    for i in range(30):
        k0 = ((k0 << 8) | (k0 >> (128 - 8))) ^ (round_keys[-2] + K0 + i)
        k1 = ((k1 << 8) | (k1 >> (128 - 8))) ^ (round_keys[-1] + K1 + i)
        round_keys.append(k0 & 0xFFFFFFFFFFFFFFFF)
        round_keys.append(k1 & 0xFFFFFFFFFFFFFFFF)

    return round_keys

# Упрощенная версия шифрования и дешифрования
def encrypt_block(block, round_keys):
    for i in range(32):
        block ^= round_keys[i]
    return block

def decrypt_block(block, round_keys):
    for i in range(31, -1, -1):
        block ^= round_keys[i]
    return block

def serpent_encrypt(message, key):
    round_keys = key_schedule(key)
    # Добавление паддинга
    padding_length = 16 - (len(message) % 16)
    message = message + b'\x00' * padding_length  # Паддинг с нулевыми байтами
    ciphertext = []
    for i in range(0, len(message), 16):
        block = int.from_bytes(message[i:i + 16], 'big')
        encrypted_block = encrypt_block(block, round_keys)
        ciphertext.append(encrypted_block)
    return b''.join(block.to_bytes(16, 'big') for block in ciphertext)

def serpent_decrypt(encrypted_message, key):
    round_keys = key_schedule(key)
    decrypted_text = []
    for i in range(0, len(encrypted_message), 16):
        block = int.from_bytes(encrypted_message[i:i + 16], 'big')
        decrypted_block = decrypt_block(block, round_keys)
        decrypted_text.append(decrypted_block.to_bytes(16, 'big'))
    
    decrypted_data = b''.join(decrypted_text).rstrip(b'\x00')  # Удаление паддинга
    return decrypted_data.decode('utf-8', errors='replace')  # Возвращаем строку без паддинга
