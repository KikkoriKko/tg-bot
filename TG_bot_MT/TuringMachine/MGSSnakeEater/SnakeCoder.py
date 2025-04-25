from TuringMachine.MGSSnakeEater.SnakeEater import generate_transitions_snail_decoder, generate_transitions_snail_encoder, \
    TuringMachineSnailDecoder, TuringMachineSnailEncoder
# Функция кодирования змейки
def encode_snake(text):
    transitions = generate_transitions_snail_encoder()
    machine = TuringMachineSnailEncoder(text, transitions, 'q0', 'qf')
    encrypted_text = machine.run()
    rail_lengths = [len(machine.rail1), len(machine.rail2)]
    return encrypted_text, rail_lengths


# Функция декодирования змейки
def decode_snake(text, rail_lengths):
    transitions = generate_transitions_snail_decoder()
    machine = TuringMachineSnailDecoder(text, transitions, 'q0', 'qf', rail_lengths)
    return machine.decode_from_rails()

