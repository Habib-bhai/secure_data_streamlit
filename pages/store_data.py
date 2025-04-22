import streamlit as st
from lib.utility_functions import encrypt_data, hash_passkey
from lib.utility_functions import generate_salt
import psycopg2

def main():
    if not st.experimental_user.is_logged_in:
        st.title("Please login to access the Store Data page.")
        return

    st.title("STORE DATA")
    
    user_data = st.text_area("Enter your data")
    secret_passkey = st.text_input("Enter your passkey", type="password")
    
    if st.button("Encrypt and Save") and user_data and secret_passkey:
        try:
            # Generate new salt for this encryption
            salt = generate_salt()
            hashed_passkey = hash_passkey(secret_passkey)
            encrypted_data = encrypt_data(user_data, secret_passkey, salt)
            
            # Store all three components in database
            conn = psycopg2.connect(
                host="ep-dark-morning-a4yy58re-pooler.us-east-1.aws.neon.tech",
                dbname="secureNeonDB",
                user="secureNeonDB_owner",
                password="npg_erjOGhI5T9QX",
                port=5432
            )
            
            with conn.cursor() as cur:
                cur.execute("""
                     CREATE TABLE IF NOT EXISTS encrypted_data (
                    id SERIAL PRIMARY KEY,
                    encrypted_text TEXT NOT NULL,
                    passkey TEXT NOT NULL,
                    salt BYTEA NOT NULL  # Changed to BYTEA for binary storage
                        )
                    """)
                
                cur.execute(
                    "INSERT INTO encrypted_data (encrypted_text, passkey, salt) VALUES (%s, %s, %s)",
                    (encrypted_data, hashed_passkey, salt)
                )
                
                conn.commit()
            
            st.success("Data encrypted and saved successfully.")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

if __name__ == "__main__":
    main()