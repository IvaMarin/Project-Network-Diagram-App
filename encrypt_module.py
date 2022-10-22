from Crypto.Cipher import AES
from secrets import token_bytes
from pathlib import Path
import subprocess
import hashlib
import os


def generate_teacher_token(cnt_bytes):
    return token_bytes(cnt_bytes)


def aes_generate_key():
    machine_id_str = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
    return hashlib.md5(machine_id_str.encode()).hexdigest().encode()


def aes_encrypt(content, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    cipher_content, tag = cipher.encrypt_and_digest(content)
    return nonce, cipher_content, tag


def aes_decrypt(nonce, cipher_content, tag, key):
    try:
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(cipher_content)
        cipher.verify(tag)
        return plaintext
    except ValueError:
        return b"ERROR_DECRYPT"


def encrypt_files_in_dir(directory):
    names = os.listdir(directory)
    for name in names:
        name = os.path.join(directory, name)
        with open(name, "rb") as input_file:
            content = input_file.read()
        with open(name, "wb") as output_file:
            nonce, cipher_content, tag = aes_encrypt(content, aes_generate_key())
            output_file.write(nonce)
            output_file.write(tag)
            output_file.write(cipher_content)


def encrypt_files(directory: Path, key: str):
    for root, dirs, files in os.walk(directory.resolve()):
        for file in files:
                path_file = os.path.join(root, file)
                with open(path_file, "rb") as input_file:
                    content = input_file.read()
                with open(path_file, "wb") as output_file:
                    nonce, cipher_content, tag = aes_encrypt(content, key.encode())
                    output_file.write(nonce)
                    output_file.write(tag)
                    output_file.write(cipher_content)


def decrypt_file(directory, filename, key: str = None):
    try:
        with open(os.path.join(directory, filename), "rb") as input_file:
            print("MISS IN ENCRYPT try 1")
            nonce = input_file.read(16)
            tag = input_file.read(16)
            cipher_content = input_file.read()
            print("MISS IN ENCRYPT try 5")
            if key is None:
                print("MISS IN ENCRYPT try 6")
                return aes_decrypt(nonce, cipher_content, tag, aes_generate_key())
            else:
                print("MISS IN ENCRYPT try 7")
                return aes_decrypt(nonce, cipher_content, tag, key.encode())
    except Exception:
        print("MISS IN ENCRYPT")
        return b"ERROR_DECRYPT"


def initial_decrypt_file(file: Path, key: str) -> bytes:
    try:
        with open(file.resolve(), "rb") as input_file:
            nonce = input_file.read(16)
            tag = input_file.read(16)
            cipher_content = input_file.read()
            return aes_decrypt(nonce, cipher_content, tag, key.encode())
    except Exception:
        return b"ERROR_DECRYPT"
