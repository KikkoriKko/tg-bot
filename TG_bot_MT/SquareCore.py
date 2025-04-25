########################################################################################
#           Программный модуль блочного шифрования и дешифрования                      #
#                                                                                      #
# Название: Square                                                                     #
# Назначение: Реализация алгоритма блочного шифрования с использованием таблиц         #
# подстановок, операций поля Галуа и матриц линейных преобразований.                   #
########################################################################################
class Square:
    def __init__(self):
        self.ListInText = []  # Текст, разбитый на блоки по 16 байт
        self.ListKeysRounds = []  # Ключи для каждого раунда
        self.table = [ # Инициализация таблицы S-box
            0xB1, 0xCE, 0xC3, 0x95, 0x5A, 0xAD, 0xE7, 0x02, 0x4D, 0x44, 0xFB, 0x91, 0x0C, 0x87, 0xA1, 0x50,
            0xCB, 0x67, 0x54, 0xDD, 0x46, 0x8F, 0xE1, 0x4E, 0xF0, 0xFD, 0xFC, 0xEB, 0xF9, 0xC4, 0x1A, 0x6E,
            0x5E, 0xF5, 0xCC, 0x8D, 0x1C, 0x56, 0x43, 0xFE, 0x07, 0x61, 0xF8, 0x75, 0x59, 0xFF, 0x03, 0x22,
            0x8A, 0xD1, 0x13, 0xEE, 0x88, 0x00, 0x0E, 0x34, 0x15, 0x80, 0x94, 0xE3, 0xED, 0xB5, 0x53, 0x23,
            0x4B, 0x47, 0x17, 0xA7, 0x90, 0x35, 0xAB, 0xD8, 0xB8, 0xDF, 0x4F, 0x57, 0x9A, 0x92, 0xDB, 0x1B,
            0x3C, 0xC8, 0x99, 0x04, 0x8E, 0xE0, 0xD7, 0x7D, 0x85, 0xBB, 0x40, 0x2C, 0x3A, 0x45, 0xF1, 0x42,
            0x65, 0x20, 0x41, 0x18, 0x72, 0x25, 0x93, 0x70, 0x36, 0x05, 0xF2, 0x0B, 0xA3, 0x79, 0xEC, 0x08,
            0x27, 0x31, 0x32, 0xB6, 0x7C, 0xB0, 0x0A, 0x73, 0x5B, 0x7B, 0xB7, 0x81, 0xD2, 0x0D, 0x6A, 0x26,
            0x9E, 0x58, 0x9C, 0x83, 0x74, 0xB3, 0xAC, 0x30, 0x7A, 0x69, 0x77, 0x0F, 0xAE, 0x21, 0xDE, 0xD0,
            0x2E, 0x97, 0x10, 0xA4, 0x98, 0xA8, 0xD4, 0x68, 0x2D, 0x62, 0x29, 0x6D, 0x16, 0x49, 0x76, 0xC7,
            0xE8, 0xC1, 0x96, 0x37, 0xE5, 0xCA, 0xF4, 0xE9, 0x63, 0x12, 0xC2, 0xA6, 0x14, 0xBC, 0xD3, 0x28,
            0xAF, 0x2F, 0xE6, 0x24, 0x52, 0xC6, 0xA0, 0x09, 0xBD, 0x8C, 0xCF, 0x5D, 0x11, 0x5F, 0x01, 0xC5,
            0x9F, 0x3D, 0xA2, 0x9B, 0xC9, 0x3B, 0xBE, 0x51, 0x19, 0x1F, 0x3F, 0x5C, 0xB2, 0xEF, 0x4A, 0xCD,
            0xBF, 0xBA, 0x6F, 0x64, 0xD9, 0xF3, 0x3E, 0xB4, 0xAA, 0xDC, 0xD5, 0x06, 0xC0, 0x7E, 0xF6, 0x66,
            0x6C, 0x84, 0x71, 0x38, 0xB9, 0x1D, 0x7F, 0x9D, 0x48, 0x8B, 0x2A, 0xDA, 0xA5, 0x33, 0x82, 0x39,
            0xD6, 0x78, 0x86, 0xFA, 0xE4, 0x2B, 0xA9, 0x1E, 0x89, 0x60, 0x6B, 0xEA, 0x55, 0x4C, 0xF7, 0xE2
        ]
        self.MakePowTable(285, 2)

#  Создание степенной и логарифмической таблиц GF(256)
    def MakePowTable(self, poly, prim_member):
        self.GF_256_power_a = [0] * 256
        self.GF_256_log_a = [0] * 256
        self.GF_256_power_a[0] = 1
        self.GF_256_log_a[1] = 0
        self.GF_256_power_a[1] = prim_member
        self.GF_256_log_a[prim_member] = 1

        for i in range(2, 256):
            self.GF_256_power_a[i] = (self.GF_256_power_a[i - 1] * prim_member) % 256
            self.GF_256_log_a[self.GF_256_power_a[i]] = i

# Побитовая операция XOR над двумя массивами байт
    def AddGaul(self, mas1, mas2):
        return [x ^ y for x, y in zip(mas1, mas2)]

# Подготовка ключей раундов, разбивает текст на блоки и запускает процесс шифрования. Возвращает зашифрованный текст в виде байт
    def Encryption(self, text, key):
        self.SetKeysRounds(key)
        self.CreateListBlocksBytes(text)
        return self.EncryptionProcess()

# Подготовка ключей раундов, разбивает текст на блоки и запускает процесс шифрования. Возвращает зашифрованный текст в виде байт
    def Decryption(self, encrypted_text, key):
        self.SetKeysRounds(key)
        self.CreateListBlocksBytes(encrypted_text)
        return self.DecryptionProcess()

# Генерирует раундовые ключи на основе первоначального ключа
    def SetKeysRounds(self, key0):
        mas_bytes = list(map(ord, key0))
        self.ListKeysRounds.append(self.GetInputBlock(mas_bytes)) # Генерация первых 4x4 блоков ключа
        constant = 1
        for _ in range(8): # Генерация раундовых ключей
            mas_result = [0] * 4
            key = [[0] * 4 for _ in range(4)]
            pred_key = self.ListKeysRounds[-1]
            mas1, mas2 = pred_key[0], pred_key[3][:]
            mas2 = mas2[1:] + mas2[:1]
            mas_result = self.AddGaul(self.AddGaul(mas1, mas2), [0, 0, 0, constant])
            key[0] = mas_result
            for j in range(1, 4):
                mas1, mas2 = pred_key[j], key[j - 1]
                key[j] = self.AddGaul(mas1, mas2)
            self.ListKeysRounds.append(key)
            constant *= 2

# Преобразует массив байтов в матрицу размером 4x4 (основной формат данных для алгоритма).
    def GetInputBlock(self, masb):
        result = [[0] * 4 for _ in range(4)]
        k = 0
        for i in range(4):
            for j in range(4):
                if k < len(masb):
                    result[i][j] = masb[k]
                    k += 1
        return result

# Разбивает входной текст на блоки по 16 байт. Если текст короче, дополняет его нулями.
    def CreateListBlocksBytes(self, text):
        self.ListInText = []
        # Если входной текст - строка, то перекодируем его в байты, иначе оставляем как есть
        if isinstance(text, str):
            mas_bytes = list(text.encode('utf-8'))
        else:
            mas_bytes = list(text)

        # Разбиваем на блоки по 16 байт
        for i in range(0, len(mas_bytes), 16):
            block = mas_bytes[i:i + 16]
            block += [0] * (16 - len(block))  # Дополняем до 16 байт
            self.ListInText.append(block)

# Реализует процесс шифрования для каждого блока текста. Применяет последовательность раундов
    def EncryptionProcess(self):
        ListResultBytes = []
        for block in self.ListInText:
            input_state = self.GetInputBlock(block) # Преобразование в 4x4 блок
            input_state = self.AddRoundKey(input_state, self.ListKeysRounds[0]) # Побитовая операция XOR между блоком и стартовым ключом
            for j in range(1, 9):
                input_state = self.LinerPreob(input_state) # Применение полиномиальной функции над каждым байтом
                input_state = self.NotLinerPreob(input_state) # Замена каждого байта с использованием таблицы S-box
                input_state = self.TransMatrix(input_state) # Перемещение байтов по определенному шаблону
                input_state = self.AddRoundKey(input_state, self.ListKeysRounds[j]) # Побитовая операция XOR с текущим раундовым ключом.
            ListResultBytes.append(input_state) # Финальный блок добавляется в результирующий массив
        return self.GetResultBytes(ListResultBytes)

# Реализует процесс дешифрования для каждого блока текста. Применяет последовательность обратных раундов
    def DecryptionProcess(self):
        ListResultBytes = []
        for block in self.ListInText:
            input_state = self.GetInputBlock(block) # Преобразование в 4x4 блок (аналогично шифрованию)
            for j in range(8, 0, -1):
                input_state = self.AddRoundKey(input_state, self.ListKeysRounds[j]) # Побитовая операция XOR между текущим блоком и ключом для данного раунда
                input_state = self.ReverseTransMatrix(input_state) # Перемещение байтов по обратному шаблону, восстановление исходного порядка
                input_state = self.ReverseNotLinerPreob(input_state) # Замена каждого байта с использованием обратной таблицы S-box
                input_state = self.ReverseLinerPreob(input_state) # Применение обратной полиномиальной функции для каждого байта
            input_state = self.AddRoundKey(input_state, self.ListKeysRounds[0]) #
            ListResultBytes.append(input_state) # Добавление начального ключа (первый раунд)
        return self.GetResultBytes(ListResultBytes) # Преобразование блока обратно в массив байт.

# Преобразует список матриц 4x4 в одномерный массив байтов.
    def GetResultBytes(self, ListResultBytes):
        mas_result = []
        for matrix in ListResultBytes:
            for i in range(4):
                for j in range(4):
                    mas_result.append(matrix[i][j])
        return bytes(mas_result)

# Выполняет операцию XOR между текущим состоянием блока (матрица 4x4) и ключом раунда.
    def AddRoundKey(self, input_state, input_key):
        return [[input_state[i][j] ^ input_key[i][j] for j in range(4)] for i in range(4)]

# Реализует линейное преобразование матрицы 4x4, используя фиксированные коэффициенты поля Галуа
    def LinerPreob(self, input_state):
        coef = [
            [2, 3, 1, 1],
            [1, 2, 3, 1],
            [1, 1, 2, 3],
            [3, 1, 1, 2]
        ]
        return self.apply_coef(input_state, coef)

# Реализует обратное линейное преобразование матрицы 4x4.
    def ReverseLinerPreob(self, input_state):
        coef = [
            [14, 11, 13, 9],
            [9, 14, 11, 13],
            [13, 9, 14, 11],
            [11, 13, 9, 14]
        ]
        return self.apply_coef(input_state, coef)

# Выполняет нелинейное преобразование (SubBytes) с использованием S-box таблицы.
    def NotLinerPreob(self, input_state):
        for i in range(4):
            for j in range(4):
                input_state[i][j] = self.table[input_state[i][j]]
        return input_state

# Выполняет обратное нелинейное преобразование (Reverse SubBytes).
    def ReverseNotLinerPreob(self, input_state):
        reverse_table = [self.table.index(i) for i in range(256)]
        for i in range(4):
            for j in range(4):
                input_state[i][j] = reverse_table[input_state[i][j]]
        return input_state

# Реализует перестановку столбцов и строк (ShiftRows).
    def TransMatrix(self, input_state):
        return [[input_state[j][i] for j in range(4)] for i in range(4)]

# Реализует обратную перестановку столбцов и строк (Reverse ShiftRows).
    def ReverseTransMatrix(self, input_state):
        return self.TransMatrix(input_state)  #  Перестановка такая же для обратной операции

# Применяет коэффициенты преобразования к матрице 4x4, реализуя умножение в поле Галуа.
    def apply_coef(self, input_state, coef):
        result = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                result[i][j] = (
                        self.galois_mult(input_state[i][0], coef[j][0]) ^
                        self.galois_mult(input_state[i][1], coef[j][1]) ^
                        self.galois_mult(input_state[i][2], coef[j][2]) ^
                        self.galois_mult(input_state[i][3], coef[j][3])
                )
        return result

# Выполняет умножение двух чисел в поле Галуа GF(256).
    def galois_mult(self, a, b):
        p = 0
        for i in range(8):
            if b & 1:
                p ^= a
            hi_bit_set = a & 0x80
            a = (a << 1) & 0xFF
            if hi_bit_set:
                a ^= 0x1B  # Полином для поля Галуа
            b >>= 1
        return p
