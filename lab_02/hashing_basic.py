import hashlib, os


def hash_string(data):
    return hashlib.sha256(data.encode()).hexdigest()
input_data = "secure_password"
hashed_data = hash_string(input_data)
print(f"Original Data: {input_data}")
print(f"Hashed Data: {hashed_data}")

def verify_hash(data,hashed):
    return hash_string(data) == hashed
correct_data = "secure_password"
incorrect_data = "wrong_password"
print("Verification (correct): ", verify_hash(correct_data,hashed_data))
print("Verification (incorrect): ", verify_hash(incorrect_data,hashed_data))

def hash_file(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()
file_hash = hash_file("sample.txt")
print(f"File Hash: {file_hash}")

def hash_string_md5(data):
    return hashlib.md5(data.encode()).hexdigest()

def hash_string_sha1(data):
    return hashlib.sha1(data.encode()).hexdigest()

print("MD5 Hash: ",hash_string_md5("secure_password"))
print("SHA-1 Hash: ",hash_string_sha1("secure_password"))

def hash_with_salt(data):
    salt = os.urandom(16)
    hasher = hashlib.pbkdf2_hmac('sha256',data.encode(),salt,100000)
    return salt + hasher
print("Salted Hash: ",hash_with_salt("secure_password"))