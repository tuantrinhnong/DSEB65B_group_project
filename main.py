import streamlit as st
from src.auth.auth import login, register
from src.schedule.schedule_display import display_schedule  # Import display_schedule

def main():
    st.title("Quản lý thời gian và công việc")

    # Kiểm tra trạng thái đăng nhập
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False

    # Lựa chọn chức năng
    if st.session_state.is_logged_in:
        option = st.sidebar.selectbox("Chọn chức năng", ("Quản lý Thời gian biểu", "Đăng Xuất"))
    else:
        option = st.sidebar.selectbox("Chọn chức năng", ("Đăng Nhập", "Đăng Ký"))

    # Xử lý các chức năng
    if option == "Đăng Nhập":
        if login():
            st.session_state.is_logged_in = True

    elif option == "Đăng Ký":
        register()

    elif option == "Quản lý Thời gian biểu":
        if not st.session_state.is_logged_in:
            st.warning("Bạn cần phải đăng nhập để truy cập vào tính năng này.")
        else:
            # Gọi hàm hiển thị lịch trình từ file khác
            display_schedule()

    elif option == "Đăng Xuất":
        st.session_state.is_logged_in = False
        st.success("Đăng xuất thành công!")

if __name__ == "__main__":
    main()
