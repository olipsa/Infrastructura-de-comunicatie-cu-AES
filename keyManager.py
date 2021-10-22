from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import socket
from ENCRYPTION import*


def main():
    port = 8889
    print(f"Listening on port {port}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', port))
        s.listen()
        conn, address_info = s.accept()
        with conn:
            print("Node A connected")
            conn.recv(1024)
            key = get_random_bytes(16)
            print(f"Node A requested the generated key ( '{key.hex()}' )")
            key_enc = aes_encryption(key)
            conn.sendall(key_enc)
            print(f"Sent to node A the key encrypted with AES mode OFB ( '{key_enc.hex()}' ) ")


if __name__ == '__main__':
    main()
