import socket
import codecs
from ENCRYPTION import *


def main():
    port = 8890
    print(f"Listening on port {port}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('localhost', port))
        s.listen()
        conn, address_info = s.accept()
        with conn:
            print("Connexion established with node A")
            operation_mode = codecs.decode(conn.recv(1024))
            print("The operation mode received from Node A is ", operation_mode)
            conn.sendall(b'ok')
            key_enc = conn.recv(1024)
            print("Encrypted key received is ", key_enc.hex())
            key = aes_decryption(key_enc)
            print("Decrypted key:", key.hex())
            conn.sendall(b'Send file')
            print("Awaiting file from Node A...")
            file_enc = conn.recv(10240)
            print("Encrypted file received from Node A:\n", file_enc.hex(), "\n")
            if operation_mode == "ECB":
                file = ecb_decryption(file_enc, key)
            else:
                file = ofb_decryption(file_enc, key)
            print("Decrypted file:\n", file)



if __name__ == '__main__':
    main()


