from cryptography.fernet import Fernet, InvalidToken
import os

# -----------------------------
# Key File Location
# -----------------------------
KEY_FILE = "secret.key"


# -----------------------------
# Generate Encryption Key
# -----------------------------
def generate_key():
    """
    Generates a new encryption key and saves it to file
    """
    key = Fernet.generate_key()

    with open(KEY_FILE, "wb") as f:
        f.write(key)

    return key


# -----------------------------
# Load Encryption Key
# -----------------------------
def load_key():
    """
    Loads encryption key from file.
    If key does not exist, it generates one automatically.
    """

    if not os.path.exists(KEY_FILE):
        print("Encryption key not found. Generating new key...")
        return generate_key()

    with open(KEY_FILE, "rb") as f:
        key = f.read()

    # Validate key length (Fernet keys must be 44 bytes)
    if len(key) != 44:
        raise ValueError(
            "Invalid encryption key detected. Key file may be corrupted.")

    return key


# -----------------------------
# Initialize Cipher
# -----------------------------
try:
    key = load_key()
    cipher = Fernet(key)
except Exception as e:
    raise RuntimeError(f"Encryption system failed to initialize: {e}")


# -----------------------------
# Encrypt Data
# -----------------------------
def encrypt_data(data):
    """
    Encrypts sensitive data before storing in database
    """

    try:

        if isinstance(data, str):
            data = data.encode("utf-8")

        encrypted = cipher.encrypt(data)

        return encrypted

    except Exception as e:
        raise RuntimeError(f"Encryption failed: {e}")


# -----------------------------
# Decrypt Data
# -----------------------------
def decrypt_data(encrypted_data):
    """
    Decrypts stored data when detokenizing
    """

    try:

        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode("utf-8")

        decrypted = cipher.decrypt(encrypted_data)

        return decrypted.decode("utf-8")

    except InvalidToken:
        raise ValueError(
            "Decryption failed: Invalid or corrupted encrypted data.")

    except Exception as e:
        raise RuntimeError(f"Decryption error: {e}")
