import streamlit as st
# import hashlib
# from cryptography.fernet import Fernet





# defining pages
home_page = st.Page(
    page="pages/home.py",
    title="home page",
    default=True
    )
store_data = st.Page(
    page="pages/store_data.py",
    title="Store data"
    )

retrieve_data = st.Page(
    page="pages/retrieve_data.py",
    title="retrieve data"
    )


# setting up navigation
pg = st.navigation([home_page, store_data, retrieve_data])

if st.sidebar.button("🔒 LogOut"):
    st.logout()
    
if st.sidebar.button("🔓 LogIn"):
    st.login("auth0")


pg.run()







# # Initialize session state for key, stored_data, and failed_attempts
# if "KEY" not in st.session_state:
#     st.session_state.KEY = Fernet.generate_key()

# cipher = Fernet(st.session_state.KEY)

# if "stored_data" not in st.session_state:
#     st.session_state.stored_data = {}

# if "failed_attempts" not in st.session_state:
#     st.session_state.failed_attempts = 0

# # Function to hash passkey
# def hash_passkey(passkey):
#     return hashlib.sha256(passkey.encode()).hexdigest()

# # Function to encrypt data
# def encrypt_data(text):
#     return cipher.encrypt(text.encode()).decode()

# # Function to decrypt data
# def decrypt_data(encrypted_text, passkey):
#     hashed_passkey = hash_passkey(passkey)
    
#     # Check if encrypted_text exists in stored_data
#     if encrypted_text in st.session_state.stored_data:
#         entry = st.session_state.stored_data[encrypted_text]
#         if entry["passkey"] == hashed_passkey:
#             st.session_state.failed_attempts = 0  # Reset attempts on success
#             return cipher.decrypt(encrypted_text.encode()).decode()
    
#     # Increment failed attempts if not found or passkey wrong
#     st.session_state.failed_attempts += 1
#     return None

# st.title("🔒 Secure Data Encryption System")

# # Navigation
# menu = ["Home", "Store Data", "Retrieve Data", "Login"]
# choice = st.sidebar.selectbox("Navigation", menu)

# if choice == "Store Data":
#     st.subheader("📂 Store Data Securely")
#     user_data = st.text_area("Enter Data:")
#     passkey = st.text_input("Enter Passkey:", type="password")

#     if st.button("Encrypt & Save"):
#         if user_data and passkey:
#             hashed_passkey = hash_passkey(passkey)
#             encrypted_text = encrypt_data(user_data)
            
#             # Store in session state
#             st.session_state.stored_data[encrypted_text] = {
#                 "encrypted_text": encrypted_text,
#                 "passkey": hashed_passkey
#             }
#             st.success("✅ Data stored securely!")
#         else:
#             st.error("⚠️ Both fields are required!")

# elif choice == "Retrieve Data":
#     st.subheader("🔍 Retrieve Your Data")
    
#     # Check if there's any data stored
#     if not st.session_state.stored_data:
#         st.warning("No data stored yet!")
#     else:
#         options = list(st.session_state.stored_data.keys())
#         select_encrypted_text = st.selectbox("Select your data", options)
#         passkey = st.text_input("Enter Passkey:", type="password")

#         if st.button("Decrypt"):
#             if select_encrypted_text and passkey:
#                 decrypted_text = decrypt_data(select_encrypted_text, passkey)

#                 if decrypted_text:
#                     st.success(f"✅ Decrypted Data: {decrypted_text}")
#                 else:
#                     remaining_attempts = 3 - st.session_state.failed_attempts
#                     st.error(f"❌ Incorrect passkey! Attempts remaining: {remaining_attempts}")
                    
#                     if st.session_state.failed_attempts >= 3:
#                         st.warning("🔒 Too many failed attempts! Redirecting to Login Page.")
#                         st.experimental_rerun()
#             else:
#                 st.error("⚠️ Both fields are required!")

# elif choice == "Login":
#     st.subheader("🔑 Reauthorization Required")
#     login_pass = st.text_input("Enter Master Password:", type="password")

#     if st.button("Login"):
#         if login_pass == "admin123":  # Hardcoded for demo, replace with proper auth
#             st.session_state.failed_attempts = 0  # Reset attempts
#             st.success("✅ Reauthorized successfully! Redirecting to Retrieve Data...")
#             st.experimental_rerun()
#         else:
#             st.error("❌ Incorrect password!")