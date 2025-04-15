import hashlib
from cryptography.fernet import Fernet
import psycopg2

KEY = Fernet.generate_key()
cipher = Fernet(KEY)


# Function to hash passkey
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Function to encrypt data
def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

# Function to decrypt data
# def decrypt_data(encrypted_text, passkey):
#     global failed_attempts
#     hashed_passkey = hash_passkey(passkey)

#     for key, value in stored_data.items():
#         if value["encrypted_text"] == encrypted_text and value["passkey"] == hashed_passkey:
#             failed_attempts = 0
#             return cipher.decrypt(encrypted_text.encode()).decode()
    
#     failed_attempts += 1
#     return None



# def db_connection_and_queries(query: str):
#     try:
        
#         import psycopg2
#         conn = psycopg2.connect(
#             host="localhost",
#             dbname="postgres",
#             user="postgres",
#             password="fucku@stupid@idiot",
#             port=5432
            
#         )
#         cur = conn.cursor()
        
#         cur.execute(query)
        
#         conn.commit()
        
#         cur.close()
#         conn.close()
#     except Exception as e:
#         print(f"Error: {e}")
#         return None    
    
  
  
  
  
def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

# Function to decrypt data
def decrypt_data(encrypted_text, passkey):
    return cipher.decrypt(encrypted_text.encode()).decode()
   

            