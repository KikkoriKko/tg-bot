class KhufuCore:
    def __init__(self, key=None):
        if not key:
            raise ValueError("Ключ не задан!")
        if isinstance(key, str):
            self.key = sum(ord(c) for c in key) % 256  # Преобразуем строку в числовое значение (сумма ASCII кодов)
        else:
            self.key = key

    def text_to_blocks(self, text, block_size=16):
        byte_text = text.encode('utf-8')
        while len(byte_text) % block_size != 0:
            byte_text += b'\0'
        return [byte_text[i:i + block_size] for i in range(0, len(byte_text), block_size)]

    def blocks_to_text(self, blocks):
        byte_text = b''.join(blocks)
        return byte_text.rstrip(b'\0').decode('utf-8')

    def encrypt_block(self, block):
        return bytes([(b + self.key) % 256 for b in block])

    def decrypt_block(self, block):
        return bytes([(b - self.key) % 256 for b in block])

    def encrypt(self, text):
        blocks = self.text_to_blocks(text)
        ciphertext = [self.encrypt_block(block) for block in blocks]
        return ''.join(f'{int.from_bytes(c, "big"):032x}' for c in ciphertext)

    def decrypt(self, encrypted_text):
        blocks = [bytes.fromhex(encrypted_text[i:i + 32]) for i in range(0, len(encrypted_text), 32)]
        decrypted_blocks = [self.decrypt_block(block) for block in blocks]
        return self.blocks_to_text(decrypted_blocks)
