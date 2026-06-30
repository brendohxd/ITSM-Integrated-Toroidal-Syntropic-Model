import os
import sys
import zipfile
import shutil
import getpass

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import base64
except ImportError:
    print("ERROR: Missing 'cryptography' library. Please run: pip install cryptography")
    sys.exit(1)

TARGET_DIR = "Endgame_Applications"
TARGET_FILE = ".local_build_notes.md"
VAULT_NAME = "build_notes_backup.cachebin"
ZIP_TEMP = "temp_sync.zip"

def get_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def lock():
    print(f"🔒 Locking '{TARGET_DIR}' and '{TARGET_FILE}' into '{VAULT_NAME}'...")
    if not os.path.exists(TARGET_DIR) and not os.path.exists(TARGET_FILE):
        print("Error: Targets do not exist to lock.")
        return

    pwd = getpass.getpass("Enter password to lock vault: ")
    pwd2 = getpass.getpass("Confirm password: ")
    if pwd != pwd2:
        print("Passwords do not match. Aborting.")
        return

    # Zip the targets
    with zipfile.ZipFile(ZIP_TEMP, 'w', zipfile.ZIP_DEFLATED) as zipf:
        if os.path.exists(TARGET_FILE):
            zipf.write(TARGET_FILE)
        if os.path.exists(TARGET_DIR):
            for root, dirs, files in os.walk(TARGET_DIR):
                for file in files:
                    zipf.write(os.path.join(root, file))

    # Encrypt the zip
    salt = os.urandom(16)
    key = get_key(pwd, salt)
    f = Fernet(key)
    
    with open(ZIP_TEMP, 'rb') as file:
        original = file.read()
    encrypted = f.encrypt(original)
    
    with open(VAULT_NAME, 'wb') as file:
        file.write(salt + encrypted)

    # Clean up
    os.remove(ZIP_TEMP)
    # SECURITY OVERRIDE: We no longer permanently delete local files.
    # We rely on .gitignore to prevent accidental GitHub pushes, and 
    # keep the local files intact so Git can track them if placed in a local branch.
    # if os.path.exists(TARGET_FILE):
    #     os.remove(TARGET_FILE)
    # if os.path.exists(TARGET_DIR):
    #     shutil.rmtree(TARGET_DIR)
        
    print("✅ Vault secured. The encrypted .cachebin has been created as a safe backup.")

def unlock():
    print(f"🔓 Unlocking '{VAULT_NAME}'...")
    if not os.path.exists(VAULT_NAME):
        print("Error: No vault found.")
        return

    pwd = getpass.getpass("Enter password to unlock vault: ")
    
    with open(VAULT_NAME, 'rb') as file:
        data = file.read()
        
    salt = data[:16]
    encrypted = data[16:]
    key = get_key(pwd, salt)
    f = Fernet(key)
    
    try:
        decrypted = f.decrypt(encrypted)
    except Exception:
        print("❌ Invalid password or corrupted vault!")
        return

    with open(ZIP_TEMP, 'wb') as file:
        file.write(decrypted)
        
    with zipfile.ZipFile(ZIP_TEMP, 'r') as zipf:
        zipf.extractall()
        
    os.remove(ZIP_TEMP)
    os.remove(VAULT_NAME)
    print("✅ Vault unlocked and files restored to the disk.")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ["lock", "unlock"]:
        print("Usage: python local_env_sync.py [lock|unlock]")
        sys.exit(1)
        
    if sys.argv[1] == "lock":
        lock()
    else:
        unlock()
