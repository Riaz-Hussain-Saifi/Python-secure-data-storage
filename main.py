import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import base64

# Initialize session state variables if they don't exist
if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}  # {"user1_data": {"encrypted_text": "xyz", "passkey": "hashed"}}

if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0

if 'authorized' not in st.session_state:
    st.session_state.authorized = True

if 'key' not in st.session_state:
    # Generate a key (this should be stored securely in production)
    st.session_state.key = Fernet.generate_key()
    st.session_state.cipher = Fernet(st.session_state.key)

# Function to hash passkey
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Function to encrypt data
def encrypt_data(text, passkey):
    # We use the passkey as additional identifier but encrypt with our Fernet key
    return st.session_state.cipher.encrypt(text.encode()).decode()

# Function to decrypt data
def decrypt_data(encrypted_text, passkey):
    hashed_passkey = hash_passkey(passkey)

    # Look for this data in our storage
    for data_id, data_info in st.session_state.stored_data.items():
        if data_info["encrypted_text"] == encrypted_text and data_info["passkey"] == hashed_passkey:
            st.session_state.failed_attempts = 0
            try:
                return st.session_state.cipher.decrypt(encrypted_text.encode()).decode()
            except Exception:
                st.error("Error decrypting data. The encrypted text may be corrupted.")
                return None

    # If we get here, either the encrypted_text wasn't found or the passkey was wrong
    st.session_state.failed_attempts += 1
    return None

# Streamlit UI
st.title("🔒 Secure Data Encryption System")

# Check if user is authorized after too many failed attempts
if not st.session_state.authorized:
    st.subheader("🔑 Reauthorization Required")
    st.warning("Too many failed attempts. Please reauthorize to continue.")
    login_pass = st.text_input("Enter Master Password:", type="password")

    if st.button("Login"):
        if login_pass == "admin123":  # Hardcoded for demo, replace with proper auth
            st.session_state.failed_attempts = 0
            st.session_state.authorized = True
            st.success("✅ Reauthorized successfully!")
            st.rerun() # <--- CHANGE HERE
        else:
            st.error("❌ Incorrect password!")
else:
    # Navigation
    menu = ["Home", "Store Data", "Retrieve Data"]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "Home":
        st.subheader("🏠 Welcome to the Secure Data System")
        st.write("Use this app to **securely store and retrieve data** using unique passkeys.")
        st.info("Your data is encrypted and can only be accessed with the correct passkey.")

        # Display stored data IDs (without showing the actual data)
        if st.session_state.stored_data:
            st.subheader("Currently Stored Data IDs:")
            for i, data_id in enumerate(st.session_state.stored_data.keys()):
                st.write(f"{i+1}. {data_id}")
        else:
            st.write("No data stored yet. Go to 'Store Data' to add your first encrypted entry.")

    elif choice == "Store Data":
        st.subheader("📂 Store Data Securely")

        # Generate a unique ID for this data entry
        data_id = st.text_input("Enter a unique ID for this data:",
                               help="This ID helps you identify your data later")

        user_data = st.text_area("Enter Data to Encrypt:")
        passkey = st.text_input("Enter Passkey:", type="password",
                               help="This passkey will be required to decrypt your data")

        if st.button("Encrypt & Save"):
            if user_data and passkey and data_id:
                if data_id in st.session_state.stored_data:
                    st.error("⚠️ This ID already exists! Please choose a different ID.")
                else:
                    hashed_passkey = hash_passkey(passkey)
                    encrypted_text = encrypt_data(user_data, passkey)

                    # Store in the correct format
                    st.session_state.stored_data[data_id] = {
                        "encrypted_text": encrypted_text,
                        "passkey": hashed_passkey
                    }

                    st.success("✅ Data stored securely!")

                    # Display the encrypted text
                    st.info("Your encrypted data:")
                    st.code(encrypted_text)
            else:
                st.error("⚠️ All fields are required!")

    elif choice == "Retrieve Data":
        st.subheader("🔍 Retrieve Your Data")

        # Show available data IDs
        if not st.session_state.stored_data:
            st.warning("No data stored yet! Go to 'Store Data' to add encrypted data first.")
        else:
            st.info(f"You have {len(st.session_state.stored_data)} stored data entries.")

            data_id = st.selectbox("Select Data ID:",
                                 options=list(st.session_state.stored_data.keys()))

            if data_id:
                encrypted_text = st.session_state.stored_data[data_id]["encrypted_text"]
                st.text_area("Encrypted Data:", value=encrypted_text, height=100, disabled=True)

                passkey = st.text_input("Enter Passkey to Decrypt:", type="password")

                if st.button("Decrypt"):
                    if passkey:
                        decrypted_text = decrypt_data(encrypted_text, passkey)

                        if decrypted_text:
                            st.success("✅ Data decrypted successfully!")
                            st.subheader("Decrypted Data:")
                            st.text_area("", value=decrypted_text, height=200)
                        else:
                            remaining_attempts = 3 - st.session_state.failed_attempts
                            st.error(f"❌ Incorrect passkey! Attempts remaining: {remaining_attempts}")

                            if st.session_state.failed_attempts >= 3:
                                st.session_state.authorized = False
                                st.warning("🔒 Too many failed attempts! Redirecting to Login Page.")
                                st.rerun() # <--- CHANGE HERE
                    else:
                        st.error("⚠️ Passkey is required!")

# Display the current status in the sidebar
st.sidebar.subheader("System Status")
st.sidebar.info(f"Failed Attempts: {st.session_state.failed_attempts}/3")
st.sidebar.info(f"Stored Data Entries: {len(st.session_state.stored_data)}")

# Reset attempts button (for testing)
if st.sidebar.button("Reset Failed Attempts"):
    st.session_state.failed_attempts = 0
    st.session_state.authorized = True
    st.sidebar.success("Attempts reset!")
    st.rerun() # <--- CHANGE HERE
