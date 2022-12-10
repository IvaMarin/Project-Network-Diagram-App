import os 
import zipfile
import pyzipper

class encrypt_decrypt():
    def __init__(self):

        pass

    def encrypt():
        # files = ["words1.txt", "words2.txt", "words3.txt", "words4.txt", "words5.txt"]
        pathToEncry = os.path.abspath(os.curdir) + '\\test_encry'
        print("\n")
        print(pathToEncry)
        print("\n")
        files = os.listdir(pathToEncry)

        print(files)

        ###################################################################
    secret_password = b'pirat_encrypt123'

    with pyzipper.AESZipFile('encry_data.zip',
                            'w',
                            compression=pyzipper.ZIP_LZMA,
                            encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(secret_password)
        # zf.write('test.txt')

        for file in files:
            zf.write('test_encry' + '\\' + file)

    # with pyzipper.AESZipFile(pathToEncry + '\\encry_data.zip') as zf:
    #     zf.setpassword(secret_password)
        # my_secrets = zf.read(pathToEncry + '\\test.txt')
        # print(my_secrets)

    input()

    with pyzipper.AESZipFile('encry_data.zip', 'r', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) \
            as extracted_zip:
        try:
            extracted_zip.extractall(pwd=secret_password)
        except RuntimeError as ex:
            print(ex)
###################################################################



# def encrypt(path):
#     filename = 'test_encry\\test_tnp.txt'
#     if os.path.exists(filename):
#         os.chmod(filename, )

# def encrypt111():
#     path = "D:\\projectMil\\myProj\\Military-Project\\test_encry"
#     file_dir = os.listdir(path)

#     with zipfile.ZipFile('test.zip', mode='w', \
#                          compression=zipfile.ZIP_DEFLATED) as zf:
#         for file in file_dir:
#             add_file = os.path.join(path, file)
#             zf.write(add_file)

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
# def encrypt():
#     # files = ["words1.txt", "words2.txt", "words3.txt", "words4.txt", "words5.txt"]
#     pathToEncry = os.path.abspath(os.curdir) + '\\test_encry'
#     print("\n")
#     print(pathToEncry)
#     print("\n")
#     files = os.listdir(pathToEncry)

#     print(files)

    

# ###################################################################
#     secret_password = b'pirat_encrypt123'

#     with pyzipper.AESZipFile('encry_data.zip',
#                             'w',
#                             compression=pyzipper.ZIP_LZMA,
#                             encryption=pyzipper.WZ_AES) as zf:
#         zf.setpassword(secret_password)
#         # zf.write('test.txt')

#         for file in files:
#             zf.write('test_encry' + '\\' + file)

    # with pyzipper.AESZipFile(pathToEncry + '\\encry_data.zip') as zf:
    #     zf.setpassword(secret_password)
        # my_secrets = zf.read(pathToEncry + '\\test.txt')
        # print(my_secrets)

#     input()

#     with pyzipper.AESZipFile('encry_data.zip', 'r', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) \
#             as extracted_zip:
#         try:
#             extracted_zip.extractall(pwd=secret_password)
#         except RuntimeError as ex:
#             print(ex)
# ###################################################################


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
    
    encry_decry = encrypt_decrypt()
    # encrypt()