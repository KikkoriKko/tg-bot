from dicrionary import all_symbols


class TuringMachineSnailEncoder:
    def __init__(self, tape_encoder, transitions_encoder, initial_state_encoder, final_state_encoder):
        self.tape_encoder = list(tape_encoder)  # Лента с текстом
        self.head_encoder = 0  # Позиция головки
        self.state_encoder = initial_state_encoder  # Начальное состояние
        self.transitions_encoder = transitions_encoder  # Правила переходов
        self.final_state_encoder = final_state_encoder  # Конечное состояние
        self.rail1 = []  # Первый рельс
        self.rail2 = []  # Второй рельс

    def step(self):
        symbol_encoder = self.tape_encoder[self.head_encoder] if self.head_encoder < len(self.tape_encoder) else '_'
        action_encoder = self.transitions_encoder.get((self.state_encoder, symbol_encoder))

        if action_encoder is None:
            return False  # Остановка, если нет правила

        new_symbol, direction, new_state_encoder, write_to_rail = action_encoder

        # Записываем символ в указанный рельс
        if write_to_rail == 'rail1':
            self.rail1.append(symbol_encoder)
        elif write_to_rail == 'rail2':
            self.rail2.append(symbol_encoder)

        if direction == 'R':
            self.head_encoder += 1
        elif direction == 'L':
            self.head_encoder -= 1

        self.state_encoder = new_state_encoder
        return True

    def run(self):
        while self.state_encoder != self.final_state_encoder:
            if not self.step():
                break

        # Соединяем рельсы для создания зашифрованного текста
        return ''.join(self.rail1) + ''.join(self.rail2)


# Правила переходов для кодирования
def generate_transitions_snail_encoder():
    transitions = {}
    states = ['q0', 'q1']
    for i, state in enumerate(states):
        write_to_rail = 'rail1' if state == 'q0' else 'rail2'
        transitions[(state, '_')] = ('_', 'R', 'qf', None)
        for symbol in all_symbols:
            next_state = 'q1' if state == 'q0' else 'q0'
            transitions[(state, symbol)] = (symbol, 'R', next_state, write_to_rail)
    return transitions


class TuringMachineSnailDecoder:
    def __init__(self, text, transitions, initial_state, final_state, rail_lengths):
        self.tape = list(text)  # Лента с зашифрованным текстом
        self.head = 0  # Позиция головки
        self.state = initial_state  # Начальное состояние
        self.transitions = transitions  # Правила переходов
        self.final_state = final_state  # Конечное состояние
        # Разделяем текст обратно на рельсы
        self.rails = [
            list(text[:rail_lengths[0]]),
            list(text[rail_lengths[0]:rail_lengths[0] + rail_lengths[1]])
        ]

    def decode_from_rails(self):
        decoded_text = []
        # Чередуем символы с рельсов
        rail1, rail2 = self.rails
        while rail1 or rail2:
            if rail1:
                decoded_text.append(rail1.pop(0))
            if rail2:
                decoded_text.append(rail2.pop(0))
        return ''.join(decoded_text)



# Генерация правил для декодирования
def generate_transitions_snail_decoder():
    transitions = {}
    states = ['q0']
    for rail in range(2):
        for symbol in all_symbols:
            transitions[(states[0], symbol)] = (symbol, 'R', states[0], rail)
    transitions[(states[0], '_')] = ('_', 'R', 'qf', None)
    return transitions