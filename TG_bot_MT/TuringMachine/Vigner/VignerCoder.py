import random
from TuringMachine.Vigner.VignerCore import TuringMachineVignerDecoder, TuringMachineVignerEncoder
from dicrionary import all_symbols

def generate_random_key(text_length, min_key_length=5, max_key_length=None): # Генерируем случайную длину ключа в пределах от min_key_length до max_key_length (или текста)
    key_length = random.randint(min_key_length, min(max_key_length or text_length, text_length))
    return ''.join(random.choice(all_symbols) for _ in range(key_length))

# Функция кодирования Виженера
def encode_vigner(text):
    key = generate_random_key(len(text))  # Генерация случайного ключа
    machine = TuringMachineVignerEncoder(text, key, 'q0', 'qf')
    encoded_text = machine.run(is_encrypt=True)
    return encoded_text, key

# Функция декодирования Виженера
def decode_vigner(encoded_text, key):
    machine = TuringMachineVignerDecoder(encoded_text, key, 'q0', 'qf')
    decoded_text = machine.run(is_encrypt=False)
    return decoded_text


