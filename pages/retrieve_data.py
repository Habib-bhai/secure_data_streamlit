import streamlit as st
import psycopg2
from lib.utility_functions import hash_passkey, decrypt_data

# Check if user is logged in
if not st.experimental_user.is_logged_in:
    st.title("Please login to access the Retrieve Data page.")
else:
    st.title("Retrieve Data")

    # Initialize session state for encrypted data and passkeys
    if "encrypted_data" not in st.session_state:
        st.session_state.encrypted_data = []

    if "failed_attempts" not in st.session_state:
        st.session_state.failed_attempts = 0
        
    # Retrieve data button
    if st.button("Retrieve Data"):
        try:
            # Database connection
            conn = psycopg2.connect(
                host="localhost",
                dbname="postgres",
                user="postgres",
                password="fucku@stupid@idiot",
                port=5432
            )
            cur = conn.cursor()
            
            # Fetch all encrypted data with passkeys
            cur.execute('''SELECT encrypted_text, passkey FROM encrypted_data;''')
            records = cur.fetchall()
            
            # Store results in session state (encrypted_text, hashed_passkey)
            st.session_state.encrypted_data = records
            
            st.success(f"Retrieved {len(records)} encrypted records!")
            
        except Exception as e:
            st.error(f"Database error: {str(e)}")
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()

    # Only show selection if data exists
    if st.session_state.encrypted_data:
        # Get list of encrypted texts for display
        encrypted_texts = [record[0] for record in st.session_state.encrypted_data]
        
        # User selection
        selected_encrypted = st.selectbox(
            "Select encrypted data",
            encrypted_texts,
            key="encrypted_select"
        )
        
        # Passkey input
        user_passkey = st.text_input(
            "Enter your passkey",
            type="password",
            key="passkey_input"
        )
        
        # Decryption button
        if st.button("Decrypt Data"):
            try:
                # Find corresponding hashed passkey
                stored_passkey = None
                for record in st.session_state.encrypted_data:
                    if record[0] == selected_encrypted:
                        stored_passkey = record[1]
                        break
                
                if stored_passkey:
                    # Hash user input
                    hashed_input = hash_passkey(user_passkey)
                    
                    if hashed_input != stored_passkey:
                        st.session_state.failed_attempts +=1
                        st.warning(st.session_state.failed_attempts)
                        if st.session_state.failed_attempts > 3:
                            st.logout()
                    
                    # Verify passkey
                    if hashed_input == stored_passkey:
                        # Decrypt data
                        decrypted = decrypt_data(selected_encrypted, stored_passkey)
                        st.success("Decrypted successfully!")
                        st.subheader("Decrypted Data:")
                        st.write(decrypted)
                    else:
                        st.error("Invalid passkey - decryption failed")
                else:
                    st.error("No passkey found for selected data")
                    
            except Exception as e:
                st.error(f"Decryption error: {str(e)}")
    else:
        st.write("No encrypted data available. Retrieve data first.")