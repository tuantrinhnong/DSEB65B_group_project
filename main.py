import streamlit as st
from src.auth.auth import login, register

def main():
    st.title("RSA Đăng Nhập và Đăng Ký")

    option = st.sidebar.selectbox("Chọn chức năng", ("Đăng Nhập", "Đăng Ký"))

    if option == "Đăng Ký":
        register()
    elif option == "Đăng Nhập":
        login()

if __name__ == "__main__":
    main()
