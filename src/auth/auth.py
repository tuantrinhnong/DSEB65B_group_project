# src/auth/auth.py

import streamlit as st
from src.database.db_manager import load_users  # Giả sử bạn đã tạo load_users trong db_manager
from src.auth.encryption import rsa_decrypt

def login():
    st.subheader("Đăng Nhập")
    username = st.text_input("Tên đăng nhập", key="login_username").strip()
    password = st.text_input("Mật khẩu", type="password", key="login_password")
    
    if st.button("Đăng Nhập"):
        users = load_users()
        
        if username in users:
            stored_data = users[username]
            stored_cipher = stored_data['password']
            stored_private_key = stored_data['private_key']
            
            decrypted_password = rsa_decrypt(stored_cipher, stored_private_key)
            
            if decrypted_password == password:
                st.success("Đăng nhập thành công!")
                return True
            else:
                st.error("Sai mật khẩu.")
                return False
        else:
            st.error("Người dùng không tồn tại.")
            return False


def register():
    st.subheader("Đăng Ký")
    username = st.text_input("Tên đăng nhập", key="register_username").strip()
    password = st.text_input("Mật khẩu", type="password", key="register_password")
    
    if st.button("Đăng Ký"):
        from src.auth.encryption import generate_rsa_keys
        from src.database.db_manager import save_user

        public_key, private_key = generate_rsa_keys()
        save_user(username, password, public_key, private_key)
        st.success("Đăng ký thành công!")
