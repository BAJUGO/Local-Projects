from passlib.context import CryptContext



my_hasher = CryptContext(["sha256_crypt"])



passwords_hashed = []

def add_password():
    password = input()
    passwords_hashed.append(my_hasher.hash(password))

add_password()


print(passwords_hashed)


print(my_hasher.verify("kiril12AZ", "$5$rounds=535000$xKyaWLYLwHUDYu7c$y9Ei/JB.Mv2yDS999EvPF22.YOEUOPw7Du8EzybNocB"))