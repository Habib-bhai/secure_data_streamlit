import streamlit as st
import psycopg2
from lib.utility_functions import hash_passkey, decrypt_data

if not st.experimental_user.is_logged_in:
    st.title("Please login to access the Retrieve Data page.")
else:
    st.title("Retrieve Data")

    # Initialize session state
    if "encrypted_records" not in st.session_state:
        st.session_state.encrypted_records = []
    if "failed_attempts" not in st.session_state:
        st.session_state.failed_attempts = 0
        
    # Retrieve data button
    if st.button("Retrieve Data"):
        try:
            with psycopg2.connect(
                host="ep-dark-morning-a4yy58re-pooler.us-east-1.aws.neon.tech",
                dbname="secureNeonDB",
                user="secureNeonDB_owner",
                password="npg_erjOGhI5T9QX",
                port=5432
            ) as conn:
                with conn.cursor() as cur:
                    cur.execute('''SELECT encrypted_text, passkey, salt FROM encrypted_data''')
                    st.session_state.encrypted_records = cur.fetchall()
            
            st.success(f"Retrieved {len(st.session_state.encrypted_records)} records!")
            
        except Exception as e:
            st.error(f"Database error: {str(e)}")

    # Display decryption interface if data exists
    if st.session_state.encrypted_records:
        # Create mapping of display text to full record
        options = {f"Encrypted Data {i+1}": record for i, record in enumerate(st.session_state.encrypted_records)}
        selected = st.selectbox("Select encrypted data", options.keys())
        
        user_passkey = st.text_input("Enter your passkey", type="password")
        
        if st.button("Decrypt Data"):
            encrypted_text, stored_hash, salt = options[selected]
    
    # Ensure salt is bytes (Postgres returns memoryview for BYTEA)
            if isinstance(salt, memoryview):
                salt = bytes(salt)
            elif isinstance(salt, str):
                salt = salt.encode()  # Fallback for text representation
            
            # Verify passkey first
            if hash_passkey(user_passkey) != stored_hash:
                st.session_state.failed_attempts += 1
                st.warning(f"Invalid passkey! Attempts: {st.session_state.failed_attempts}/3")
                if st.session_state.failed_attempts >= 3:
                    st.error("Too many failed attempts. Logging out...")
                    st.logout()
                st.stop()
    
            try:
                # Reset attempts on successful verification
                st.session_state.failed_attempts = 0
                
                # Decrypt with proper salt handling
                decrypted = decrypt_data(encrypted_text, user_passkey, salt)
                st.success("Decrypted successfully!")
                st.subheader("Decrypted Data:")
                st.text_area("", value=decrypted, height=200)
                
            except Exception as e:
                st.error(f"Decryption failed: {str(e)}")
    else:
        st.write("No encrypted data available. Retrieve data first.")