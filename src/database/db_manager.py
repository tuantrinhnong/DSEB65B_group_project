import json
import os
import streamlit as st
from src.auth.encryption import rsa_encrypt
# Đường dẫn đầy đủ tới file users.json trong thư mục database
USER_DAT
        'password': encrypted_password,
        'public_key': public_key,
        'private_key': private_key
    }

    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file)
    return "Đăng ký thành công!"