from pathlib import Path
<<<<<<< Updated upstream
import encrypt_module

encrypt_module.encrypt_files(Path("encrypted_data"), "pirat_encrypt123")
=======
from utils.encrypt import encrypt_module

encrypt_module.encrypt_files(Path("../../encrypted_data"), "pirat_encrypt123")
>>>>>>> Stashed changes

# with open("res1.docx", "wb") as f:
#     f.write(encrypt_module.decrypt_file("../../reports", "f_f.docx", "pirat_encrypt123"))
