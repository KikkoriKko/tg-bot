from dicrionary import all_symbols

class TuringMachineVignerEncoder:
    def __init__(self, tape, key, initial_state, final_state):
        self.tape = list(tape)  # Лента с текстом
        self.key = key  # Ключ для шифрования
        self.head = 0  # Позиция головки
        self.state = initial_state  # Начальное состояние
        self.final_state = final_state  # Конечное состояние
        self.encoded_text = ""  # Защифрованный текст

    def step(self, is_encrypt=True):
        # Шаг Тьюринга
        symbol = self.tape[self.head] if self.head < len(self.tape) else '_'
        key_symbol = self.key[self.head % len(self.key)]  # Символ ключа
        shift = all_symbols.index(key_symbol)  # Определяем сдвиг на основе ключа

        if symbol == '_':
            return False  # Остановка, если дошли до конца ленты

        if is_encrypt:
            # Шифрование
            new_symbol = all_symbols[(all_symbols.index(symbol) + shift) % len(all_symbols)]
        else:
            # Дешифрование (сдвиг в обратную сторону)
            new_symbol = all_symbols[(all_symbols.index(symbol) - shift) % len(all_symbols)]

        self.tape[self.head] = new_symbol  # Записываем зашифрованный/расшифрованный символ
        self.head += 1  # Перемещаем головку

        return True

    def run(self, is_encrypt=True):
        # Запуск машины Тьюринга до конца ленты
        while self.head < len(self.tape):
            if not self.step(is_encrypt):
                break

        # Возвращаем результат в зависимости от типа операции
        if is_encrypt:
            self.encoded_text = ''.join(self.tape)
            return self.encoded_text
        else:
            return ''.join(self.tape)

class TuringMachineVignerDecoder:
    def __init__(self, tape, key, initial_state, final_state):
        self.tape = list(tape)  # Лента с текстом
        self.key = key  # Ключ для дешифрования
        self.head = 0  # Позиция головки
        self.state = initial_state  # Начальное состояние
        self.final_state = final_state  # Конечное состояние
        self.decoded_text = ""  # Расшифрованный текст

    def step(self, is_encrypt=False):
        # Шаг Тьюринга
        symbol = self.tape[self.head] if self.head < len(self.tape) else '_'
        key_symbol = self.key[self.head % len(self.key)]  # Символ ключа
        shift = all_symbols.index(key_symbol)  # Определяем сдвиг на основе ключа

        if symbol == '_':
            return False  # Остановка, если дошли до конца ленты

        if is_encrypt:
            # Шифрование
            new_symbol = all_symbols[(all_symbols.index(symbol) + shift) % len(all_symbols)]
        else:
            # Дешифрование (сдвиг в обратную сторону)
            new_symbol = all_symbols[(all_symbols.index(symbol) - shift) % len(all_symbols)]

        self.tape[self.head] = new_symbol  # Записываем зашифрованный/расшифрованный символ
        self.head += 1  # Перемещаем головку

        return True

    def run(self, is_encrypt=False):
        # Запуск машины Тьюринга до конца ленты
        while self.head < len(self.tape):
            if not self.step(is_encrypt):
                break

        # Возвращаем результат
        return ''.join(self.tape)
