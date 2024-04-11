#!/usr/bin/env python
# coding: utf-8

# In[5]:


import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "pycryptodome"])


# In[9]:


from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os
import pandas as pd

# Function to encrypt a file
def encrypt_file(file_path, key):
    # Initialize cipher in CBC mode with a random IV
    cipher = AES.new(key, AES.MODE_CBC)
    
    # Read the content of the file
    with open(file_path, 'rb') as f:
        file_data = f.read()
        
    # Encrypt the file data
    encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))
    
    # Save the IV and the encrypted data to a file
    encrypted_file_path = file_path + '.encrypted'
    with open(encrypted_file_path, 'wb') as f:
        f.write(cipher.iv)
        f.write(encrypted_data)
    
    return encrypted_file_path

# Function to decrypt a file
def decrypt_file(encrypted_file_path, key):
    # Read the IV and encrypted data
    with open(encrypted_file_path, 'rb') as f:
        iv = f.read(16)  # AES block size is 16 bytes
        encrypted_data = f.read()
        
    # Initialize cipher in CBC mode with the saved IV
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    
    # Decrypt and unpad the data
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    
    # Save the decrypted data to a new file
    decrypted_file_path = encrypted_file_path + '.decrypted'
    with open(decrypted_file_path, 'wb') as f:
        f.write(decrypted_data)
    
    return decrypted_file_path

# Your secret key (use a secure method to generate and store this key!)
key = b'1234567891234567'  # Key must be 16, 24, or 32 bytes long

dataset_path = 'past-data.csv'
#dataset = pd.read_csv(dataset_path)

#dataset.head()

# Encrypt the CSV file
encrypted_file_path = encrypt_file(dataset_path, key)
print(f'Encrypted file saved to: {encrypted_file_path}')

# Decrypt the file (for demonstration)
decrypted_file_path = decrypt_file(encrypted_file_path, key)
print(f'Decrypted file saved to: {decrypted_file_path}')


# In[ ]:




