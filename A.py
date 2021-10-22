import socket
import codecs
from ENCRYPTION import*


def main():
    while 1:
        operation_mode = input("Mode(ECB/OFB): ")
        if operation_mode.lower() == "ecb" or operation_mode.lower() == "ofb":
            break
        else:
            print(f"Mode {operation_mode.upper()} not valid\n")
    key_enc = get_key_from_km(operation_mode)
    print("Received encrypted key from Key Manager:", key_enc.hex())
    connexion_with_b(operation_mode, key_enc)


def get_key_from_km(operation_mode):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 8889))
        s.sendall(bytes(operation_mode, 'utf-8'))
        return s.recv(1024)


def connexion_with_b(operation_mode, key_enc):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 8890))
        s.sendall(bytes(operation_mode, 'utf-8'))
        s.recv(1024)   # receive confirmation message
        s.sendall(key_enc)
        print("Encrypted key sent to Node B")
        key = aes_decryption(key_enc)
        print("Decrypted key:", key.hex())
        print(f"Received response from Node B: \"{codecs.decode(s.recv(1024))}\"")
        f = open('input.txt', "r")
        text = f.read()

        if operation_mode == "ECB":
            enc_text = ecb_encryption(text, key)
        else:
            enc_text = ofb_encryption(text, key)

        s.sendall(bytes(enc_text))
        print("Sent file encrypted to Node B.")


if __name__ == '__main__':
    main()
