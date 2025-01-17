from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
from database import connessione
from cryptography.hazmat.primitives import padding



class Encryption:
    ENCRYPTION_KEY  = b"super_secret_encryption_key_32by"
    
    # Function to encrypt the user key using AES
    def encrypt_key(key):
        #Encrypt key with AES-GCM
        iv = os.urandom(12)  
        cipher = Cipher(algorithms.AES(Encryption.ENCRYPTION_KEY), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(key) + encryptor.finalize()
        return iv + encryptor.tag + ciphertext  

    # Function to decrypt the user key
    def decrypt_key(encrypted_key):
        iv = encrypted_key[:12]  
        tag = encrypted_key[12:28]  
        ciphertext = encrypted_key[28:] 
        cipher = Cipher(algorithms.AES(Encryption.ENCRYPTION_KEY), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        key = decryptor.update(ciphertext) + decryptor.finalize()
        return key


    # Function to save the file encryption key to database
    def save_key_to_database(user_id, key, overwrite=False):
        try:
            if connessione.is_connected():
                cursor = connessione.cursor()
                encrypted_key = Encryption.encrypt_key(key)
                if overwrite:
                    query = "UPDATE users SET mykey = %s WHERE id = %s"
                    cursor.execute(query, (encrypted_key, user_id))
                else:
                    query = """
                    INSERT INTO users (id, mykey) 
                    SELECT %s, %s 
                    WHERE NOT EXISTS (SELECT 1 FROM users WHERE id = %s)
                    """
                    cursor.execute(query, (user_id, encrypted_key, user_id))
                connessione.commit()
                print(f">> Key saved successfully for user ID {user_id}.")
            else:
                print(">> Error: Database connection is not active.")
        except Exception as e:
            print(f">> Error saving key to database: {e}")


    # Directly related to save_key function, it allows to generate a new key if we want a new key
    def generate_and_save_key(user_id, force_regeneration=False):
        if not force_regeneration:
            existing_key = Encryption.get_user_key(user_id)
            if existing_key:
                print(f">> Key already exists for user ID {user_id}.")
                return existing_key
            
        new_key = os.urandom(32)
        Encryption.save_key_to_database(user_id, new_key, overwrite=True)
        print(f">> New key generated and saved for user ID {user_id}.")
        return new_key

    
    def get_user_key(user_id):
        if connessione.is_connected():
            try:
                cursor = connessione.cursor()
                query = "SELECT mykey FROM users WHERE ID = %s;"
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()
                if not result or not result[0]:
                    print(f">> Error: No key found for user ID {user_id}.")
                    return None
                
                encrypted_key = result[0]
                key = Encryption.decrypt_key(encrypted_key)
                return key
            
            except Exception as e:
                print(f">> Error fetching key: {e}")
                return None
            finally:
                cursor.close()
        else:
            print(">> Error: Database connection failed.")
            return None

    # Encrypt the shards with the retrieved key
    def encrypt_file_with_user_key(file_content, user_id):
        key = Encryption.get_user_key(user_id)
        if len(key) not in [16, 24, 32]:  
            print(">> Invalid key length. Must be 16, 24, or 32 bytes.")
            return False
        
        iv = os.urandom(12)  
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
 
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(file_content) + padder.finalize()
 
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return iv + encryptor.tag + ciphertext  
 
    # Decrypt the shards with the key
    def decrypt_file_with_user_key(encrypted_data, user_id):
        try:
            key = Encryption.get_user_key(user_id)
            if len(key) not in [16, 24, 32]:
                print(">> Invalid key length. Must be 16, 24, or 32 bytes.")
                return None
 
            iv = encrypted_data[:12]
            tag = encrypted_data[12:28]
            ciphertext = encrypted_data[28:]
 
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
            decryptor = cipher.decryptor()
 
            plaintext_padded = decryptor.update(ciphertext) + decryptor.finalize()
 
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            plaintext = unpadder.update(plaintext_padded) + unpadder.finalize()
 
            return plaintext
        except Exception as e:
            print(f">> Error during decryption: {e}")
            return None
