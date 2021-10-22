from Crypto.Cipher import AES
key_for_enc = bytes.fromhex('8ac0f91054c003924d595a7996a99f5a')
iv = bytes.fromhex('576D5A7134743677397A24432646294A')
empty_byte = 0b00000000


def aes_encryption(plain):
    cipher = AES.new(key_for_enc, AES.MODE_ECB)
    return cipher.encrypt(plain)


def aes_decryption(ciphertext):
    cipher = AES.new(key_for_enc, AES.MODE_ECB)
    return cipher.decrypt(ciphertext)


def ecb_encryption(plaintext, key):
    ciphertext = bytearray()
    text_bytes = bytearray(plaintext, 'utf-8')
    cipher_enc = AES.new(key, AES.MODE_ECB)
    pad(text_bytes)  # add missing bytes
    for i in range(0, len(text_bytes), 16):
        block = bytes(text_bytes[i: i + 16])
        enc_block = cipher_enc.encrypt(block)
        ciphertext += enc_block
    return ciphertext


def ecb_decryption(ciphertext, key):
    initial_text = bytearray()
    cipher_dec = AES.new(key, AES.MODE_ECB)
    for i in range(0, len(ciphertext), 16):
        block = bytes(ciphertext[i: i + 16])
        dec_block = cipher_dec.decrypt(block)
        initial_text += dec_block
    unpad(initial_text)  # removes initial padding
    return initial_text.decode('utf-8')


def ofb_encryption(plaintext, key):
    ciphertext = bytearray()
    text_bytes = bytearray(plaintext, 'utf-8')
    cipher = AES.new(key, AES.MODE_ECB)
    prev_block = cipher.encrypt(iv)
    for i in range(0, len(text_bytes), 16):
        block = bytes(text_bytes[i: i + 16])
        enc_block = xor(prev_block, block)
        ciphertext += enc_block
        prev_block = cipher.encrypt(enc_block)
    return ciphertext


def ofb_decryption(ciphertext, key):
    initial_text = bytearray()
    cipher = AES.new(key, AES.MODE_ECB)
    prev_block = cipher.encrypt(iv)
    for i in range(0, len(ciphertext), 16):
        block = bytes(ciphertext[i: i + 16])
        dec_block = xor(prev_block, block)
        initial_text += dec_block
        prev_block = cipher.encrypt(block)
    unpad(initial_text) # removes initial padding
    return initial_text.decode('utf-8')


def unpad(text):
    for byte in reversed(text):
        if byte == empty_byte:
            text.remove(byte)
        else:
            return


def pad(text):
    # adauga 0-uri la capatul variabilei text,
    # pentru ca ultimul sau block sa fie de 16 bytes
    pad_length = 16 - (len(text) % 16)
    for i in range(pad_length):
        text.append(empty_byte)


def xor(block1, block2):
    result = bytearray()
    min_size = min(len(block1), len(block2))
    for i in range(min_size):
        result.append(block1[i] ^ block2[i])
    if len(block1) > min_size:
        for i in range(min_size,len(block1)):
            result.append(block1[i])
    elif len(block2) > min_size:
        for i in range(min_size, len(block2)):
            result.append(block2[i])
    return bytes(result)
