# Secure Data Encryption System (Streamlit Demo)

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-brightgreen)](https://streamlit.io)
[![Cryptography](https://img.shields.io/badge/cryptography-Fernet-yellow)](https://cryptography.io/en/latest/fernet/)

A simple web application built with Streamlit to demonstrate secure encryption and decryption of text data using user-defined passkeys. Data is encrypted using the Fernet symmetric encryption scheme from the `cryptography` library.

**Note:** This application uses Streamlit's session state for storage. This means **all stored data is temporary and will be lost** when the Streamlit server stops or restarts, or the user session ends. It serves as a demonstration of encryption principles within a web app context, not as a persistent secure storage solution.

## Features

*   **Encrypt Data:** Enter text data and a passkey to encrypt it.
*   **Store Data:** Assign a unique ID to the encrypted data for later retrieval.
*   **Retrieve Data:** Select a stored data ID and enter the correct passkey to decrypt and view the original text.
*   **Passkey Hashing:** User passkeys are hashed (SHA256) before being associated with the encrypted data for verification during decryption.
*   **Attempt Limiting:** Basic protection against brute-force decryption attempts (locks after 3 incorrect passkey entries).
*   **Simple UI:** Easy-to-use interface powered by Streamlit.

## How it Works

1.  **Encryption Key:** A unique Fernet encryption key is generated when the application session starts and stored in the session state.
2.  **Storing Data:**
    *   User provides a unique ID, plaintext data, and a passkey.
    *   The passkey is hashed using SHA256.
    *   The plaintext data is encrypted using the session's Fernet key.
    *   The unique ID, the encrypted data, and the *hashed* passkey are stored together in the Streamlit session state dictionary.
3.  **Retrieving Data:**
    *   User selects a data ID and provides a passkey.
    *   The provided passkey is hashed.
    *   The application checks if the hashed passkey matches the stored hash associated with the selected data ID.
    *   If the hashes match, the application attempts to decrypt the stored encrypted text using the session's Fernet key.
    *   If decryption is successful, the original plaintext is displayed.
    *   Incorrect passkeys increment a failure counter. After 3 failures, the user is temporarily locked out and needs to re-authenticate (using a hardcoded demo password).

## Technologies Used

*   **Python:** Core programming language.
*   **Streamlit:** Web application framework for the UI.
*   **Cryptography:** Python library providing cryptographic recipes (specifically Fernet for symmetric encryption).
*   **Hashlib:** Standard Python library for hashing (used for passkeys).

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd secure-data-storage
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    *   Make sure you have a `requirements.txt` file with the following content:
        ```txt
        streamlit
        cryptography
        ```
    *   Then run:
        ```bash
        pip install -r requirements.txt
        ```
4.  **Run the Streamlit application:**
    ```bash
    streamlit run main.py
    ```
    The application should open in your default web browser.

## Usage

1.  Navigate using the sidebar: "Home", "Store Data", "Retrieve Data".
2.  **Store Data:**
    *   Go to the "Store Data" page.
    *   Enter a unique identifier (e.g., `my_secret_notes`).
    *   Enter the text you want to encrypt in the text area.
    *   Enter a secure passkey (you'll need this later).
    *   Click "Encrypt & Save". The encrypted text will be shown.
3.  **Retrieve Data:**
    *   Go to the "Retrieve Data" page.
    *   Select the ID of the data you want to retrieve from the dropdown.
    *   Enter the correct passkey you used when storing the data.
    *   Click "Decrypt". If the passkey is correct, the original data will be displayed.

## Important Limitations & Security Notes

*   🚨 **Ephemeral Storage:** Data is NOT saved permanently. It only exists within the current Streamlit session. Closing the browser tab or stopping the server will erase all stored data.
*   🚨 **Session-Specific Key:** The encryption key is generated *per session*. Data encrypted in one session cannot be decrypted in a different session (e.g., after restarting the app).
*   🚨 **Hardcoded Master Password:** The re-authorization password (`admin123`) is hardcoded and highly insecure. This is purely for demonstration purposes. **Do not use this pattern in production.**
*   **Demo Purposes Only:** This application is intended as a learning tool and demonstration. It lacks features essential for real-world secure storage, such as persistent storage, robust user authentication, and secure key management.

## Future Improvements (Ideas)

*   Implement persistent storage (e.g., using a database like SQLite, PostgreSQL, or saving encrypted files).
*   Develop a proper user authentication system instead of a hardcoded password.
*   Implement secure key management (e.g., deriving the encryption key from a user's master password using PBKDF2, storing keys securely).
*   Add functionality to delete stored data entries.
*   Improve error handling and user feedback.
