import socket

from Crypto.Cipher import AES


def encrypt_string(value: str):
    aes = AES.new("zAG5bUGU5rHQh5zP", AES.MODE_CFB, "KDfpDKv7AYHtYnew")
    return aes.encrypt(value)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

target: str = "192.168.1.21"
port: int = 4444

sock.connect(
    (
        target, port
    )
)

message = str(input("Message: "))
sock.send(encrypt_string(message))
