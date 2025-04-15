import streamlit as st
from lib.utility_functions import encrypt_data, hash_passkey
import psycopg2


# create

def main():
    if not st.experimental_user.is_logged_in:
        st.title("Please login to access the Store Data page.")

    if st.experimental_user.is_logged_in:
        st.title("STORE DATA")
        
        user_data = st.text_area("Enter your data")
        
        secret_passkey = st.text_input("Enter your passkey")
        
        if st.button("Encrypt and Save"):
            hashed_passkey = hash_passkey(secret_passkey)
            encrypted_data = encrypt_data(user_data)
            
            conn = psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password="fucku@stupid@idiot",
            port=5432)
            
            cur = conn.cursor()
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS encrypted_data (
                    id SERIAL PRIMARY KEY,
                    encrypted_text TEXT NOT NULL,
                    passkey TEXT NOT NULL
                )
            """)
            
            cur.execute("INSERT INTO encrypted_data (encrypted_text, passkey) VALUES (%s, %s)", (encrypted_data, hashed_passkey))
            
            conn.commit()
            
            cur.close()
            conn.close()
            
            st.success("Data encrypted and saved successfully.")
            
            
            
        
    

   
if __name__ == "__main__":
    main()            