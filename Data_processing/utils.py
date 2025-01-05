import re
import json

# Hàm đọc file json và trả về dữ liệu
def read_json_file(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        data = json.load(file)
    return data


# Hàm viết và lưu dữ liệu đã xử lý vào file json
def write_json_file(data, file_path):
    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)