import os
import json
from datetime import datetime, timedelta

# Đường dẫn tuyệt đối đến file schedule.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEDULE_FILE = os.path.join(BASE_DIR, "../database/schedule.json")

# Tải lịch từ file hoặc tạo mới nếu chưa tồn tại
# Tải lịch từ file hoặc tạo mới nếu chưa tồn tại
def load_schedule(filename=SCHEDULE_FILE):
    try:
        with open(filename, 'r') as file:
            data = file.read().strip()
            return json.loads(data) if data else {}
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        # Trả về dictionary rỗng nếu file không phải JSON hợp lệ
        return {}

# Lưu lịch vào file
def save_schedule(schedule, filename=SCHEDULE_FILE):
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    # Ghi dữ liệu vào file JSON
    with open(filename, 'w') as file:
        json.dump(schedule, file, indent=4)

# Thêm thời gian biểu và có tùy chọn lặp lại hàng tuần
def add_schedule(title, start_time, end_time, date, repeat_weekly=False, note=""):
    schedule = load_schedule()
    event_id = len(schedule) + 1
    schedule[event_id] = {
        "title": title,
        "start_time": start_time,
        "end_time": end_time,
        "date": date,
        "repeat_weekly": repeat_weekly,
        "note": note
    }
    if repeat_weekly:
        current_date = datetime.strptime(date, "%Y-%m-%d")
        for i in range(1, 5):
            next_date = current_date + timedelta(weeks=i)
            event_id += 1
            schedule[event_id] = {
                "title": title,
                "start_time": start_time,
                "end_time": end_time,
                "date": next_date.strftime("%Y-%m-%d"),
                "repeat_weekly": repeat_weekly,
                "note": note
            }
    save_schedule(schedule)
    return event_id

# Xóa thời gian biểu
def delete_schedule(event_id):
    schedule = load_schedule()
    if event_id in schedule:
        del schedule[event_id]
        save_schedule(schedule)
        return True
    return False

# Lấy thời gian biểu cho một hoặc nhiều ngày
def get_schedule(date=None, days=1):
    schedule = load_schedule()
    selected_schedules = []
    current_time = datetime.now()
    
    for event_id, event in schedule.items():
        event_date = datetime.strptime(event["date"], "%Y-%m-%d")
        if date:
            selected_date = datetime.strptime(date, "%Y-%m-%d")
            if selected_date <= event_date < selected_date + timedelta(days=days):
                event_with_id = {"ID": event_id}  # Thêm ID vào sự kiện
                event_with_id.update(event)
                selected_schedules.append(event_with_id)
        else:
            event_with_id = {"ID": event_id}
            event_with_id.update(event)
            selected_schedules.append(event_with_id)
    
    # Sắp xếp các sự kiện theo thời gian gần nhất hiện tại
    selected_schedules.sort(key=lambda x: datetime.strptime(x["date"] + " " + x["start_time"], "%Y-%m-%d %H:%M"))
    return selected_schedules
