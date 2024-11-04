import streamlit as st
import pandas as pd
from datetime import datetime
from src.schedule.scheduler import add_schedule, get_schedule, delete_schedule

def display_schedule():
    st.header("Quản lý Thời gian biểu")

    # Form thêm thời gian biểu mới
    with st.form("add_schedule_form"):
        title = st.text_input("Tiêu đề sự kiện")
        start_time = st.time_input("Giờ bắt đầu")
        end_time = st.time_input("Giờ kết thúc")
        date = st.date_input("Ngày")
        repeat_weekly = st.checkbox("Lặp lại hàng tuần")
        note = st.text_area("Ghi chú")
        submit_button = st.form_submit_button(label="Thêm Thời gian biểu")

        if submit_button:
            add_schedule(title, start_time.strftime("%H:%M"), end_time.strftime("%H:%M"), date.strftime("%Y-%m-%d"), repeat_weekly, note)
            st.success("Đã thêm thời gian biểu!")

    # Hiển thị lịch trình
    st.subheader("Lịch trình")
    view_date = st.date_input("Chọn ngày để xem lịch trình", value=datetime.today())
    days = st.slider("Số ngày muốn xem", 1, 7, 1)
    schedules = get_schedule(date=view_date.strftime("%Y-%m-%d"), days=days)

    if schedules:
        # Đảm bảo rằng mỗi sự kiện đều có trường "note" và thêm "ID" cho từng sự kiện
        for i, event in enumerate(schedules):
            event["ID"] = i + 1  # Gán ID cho từng sự kiện
            if "note" not in event:
                event["note"] = ""

        # Chuyển đổi dữ liệu thành DataFrame
        schedule_table = pd.DataFrame(schedules)

        # Sắp xếp lại các cột và đặt tên cột
        schedule_table = schedule_table[["ID", "title", "date", "start_time", "end_time", "note"]]
        schedule_table.columns = ["ID", "Tiêu đề", "Ngày", "Giờ bắt đầu", "Giờ kết thúc", "Ghi chú"]

        # Đặt `ID` làm chỉ mục và đặt tên cho chỉ mục là "ID"
        schedule_table.set_index("ID", inplace=True)
        schedule_table.index.name = "ID"

        # Hiển thị bảng
        st.table(schedule_table)

        # Chọn sự kiện để xóa
        delete_id = st.number_input("Nhập ID sự kiện để xóa", min_value=1, step=1)
        if st.button("Xóa Thời gian biểu"):
            if delete_schedule(delete_id):
                st.success("Đã xóa sự kiện!")
            else:
                st.error("ID không tồn tại.")
    else:
        st.write("Không có thời gian biểu nào cho ngày đã chọn.")
