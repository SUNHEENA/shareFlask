from cryptography.fernet import Fernet # symmetric encryption
import os

class FernetEnDecrypt:
    def __init__(self, key=None):
        if key is None:  # 키가 없다면
            key = Fernet.generate_key()  # 키를 생성한다
        self.key = key
        self.f = Fernet(self.key)

    def encrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.f.encrypt(data)  # 바이트형태이면 바로 암호화
        else:
            ou = self.f.encrypt(data.encode('utf-8'))  # 인코딩 후 암호화
        if is_out_string is True:
            return ou.decode('utf-8')  # 출력이 문자열이면 디코딩 후 반환
        else:
            return ou

    def decrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.f.decrypt(data)  # 바이트형태이면 바로 복호화
        else:
            ou = self.f.decrypt(data.encode('utf-8'))  # 인코딩 후 복호화
        if is_out_string is True:
            return ou.decode('utf-8')  # 출력이 문자열이면 디코딩 후 반환
        else:
            return ou


def encrypt_account(system_name : str, id : str, pwd : str, badge_no=None):
    key = Fernet.generate_key()
    endecrypt = FernetEnDecrypt(key=key)
    encrypted_id = endecrypt.encrypt(id)
    # print(type(encrypted_id))
    encrypted_pwd = endecrypt.encrypt(pwd)

    f = open(os.getcwd() + "/" + system_name + "_account_" + id, 'w')
    f.writelines(key.decode('utf-8') + '\n')
    f.writelines(encrypted_id + '\n')
    f.writelines(encrypted_pwd)
    if badge_no is not None and badge_no != "":
        encrypted_badge_no = endecrypt.encrypt(badge_no)
        f.writelines(encrypted_badge_no)
    f.close()


def decrypt_account(system_name : str, id : str):
    f = open(os.getcwd() + "/" + system_name + "_account_" + id, 'rb')
    key = f.readline()
    id = f.readline()
    pwd = f.readline()
    badge_no = f.readline()
    f.close()
    endecrypt = FernetEnDecrypt(key=key)
    id =  endecrypt.decrypt(id)
    pwd = endecrypt.decrypt(pwd)
    decrypted_badge_no = ""
    if badge_no != b'':
        decrypted_badge_no = endecrypt.decrypt(badge_no)
    # print(id, pwd, decrypted_badge_no)
    return id, pwd, decrypted_badge_no


if __name__ == '__main__':
    encrypt_account("mysqlAdmin", "root", "Amkor123!")
    accountUser = decrypt_account('mysqlAdmin','root')
    print(accountUser)
    



# key = Fernet.generate_key()
# print("key : ", key)
# simpleEnDecrypt = FernetEnDecrypt(key=key)
# plain_text = 'hello crypto world'
# print(plain_text)
# encrypt_text = simpleEnDecrypt.encrypt(plain_text)
# print(encrypt_text)
# decrypt_text = simpleEnDecrypt.decrypt(encrypt_text)
# print(decrypt_text)