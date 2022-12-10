import os 
import zipfile
import pyzipper

# class encrypt_decrypt():
#     def __init__(self):

#         pass

# def encrypt(path):
#     filename = 'test_encry\\test_tnp.txt'
#     if os.path.exists(filename):
#         os.chmod(filename, )

def encrypt111():
    path = "D:\\projectMil\\myProj\\Military-Project\\test_encry"
    file_dir = os.listdir(path)

    with zipfile.ZipFile('test.zip', mode='w', \
                         compression=zipfile.ZIP_DEFLATED) as zf:
        for file in file_dir:
            add_file = os.path.join(path, file)
            zf.write(add_file)

    # filename = 'test_encry\\test_tnp.txt'
    # if os.path.exists(filename):
    #     jungle_zip = zipfile.ZipFile(os.path(filename), 'w')
    #     jungle_zip.write(os.path(filename), compress_type=zipfile.ZIP_DEFLATED)
        
    #     jungle_zip.close()


# path = '/home/docs-python/script/sql-script/'
# file_dir = os.listdir(path)

# with zipfile.ZipFile('test.zip', mode='w', \
#                      compression=zipfile.ZIP_DEFLATED) as zf:
#     for file in file_dir:
#         add_file = os.path.join(path, file)
#         zf.write(add_file)

# >>> os.system('file test.zip')
# # test.zip: Zip archive data, at least v2.0 to extract


# shuf -n5 /usr/share/dict/words > words.txt
def encrypt():
    # files = ["words1.txt", "words2.txt", "words3.txt", "words4.txt", "words5.txt"]
    pathToEncry = os.path.abspath(os.curdir) + '\\test_encry'
    print("\n")
    print(pathToEncry)
    print("\n")
    files = os.listdir(pathToEncry)

    print(files)

    # archive = "test_encry\\archive.zip"
    # password = b"1234"

    # with zipfile.ZipFile(archive, "w") as zf:
    #     for file in files:
    #         zf.write(file)

    #     zf.setpassword(password)

    # with zipfile.ZipFile(archive, "r") as zf:
    #     crc_test = zf.testzip()
    #     if crc_test is not None:
    #         print(f"Неверный CRC или заголовки файлов: {crc_test}")

###################################################################
    secret_password = b'pirat_encrypt123'

    with pyzipper.AESZipFile('encry_data.zip',
                            'w',
                            compression=pyzipper.ZIP_LZMA,
                            encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(secret_password)
        # zf.write('test.txt')

        for file in files:
            zf.write(file)

    with pyzipper.AESZipFile('new_test.zip') as zf:
        zf.setpassword(secret_password)
        my_secrets = zf.read('test.txt')
        print(my_secrets)
###################################################################


        # info = zf.infolist()  # also zf.namelist()
        # print(info)
        # [ <ZipInfo filename='words1.txt' filemode='-rw-r--r--' file_size=37>,
        #   <ZipInfo filename='words2.txt' filemode='-rw-r--r--' file_size=47>,
        #   ... ]

        # file = info[0]
        # with zf.open(file) as f:
        #     print(f.read().decode())
        #     # Olav
        #     # teakettles
        #     # ...

        # так же, попробуйте zf.extractall()
        # zf.extract(file, "/tmp", pwd=password)

if __name__ == "__main__":
    encrypt()