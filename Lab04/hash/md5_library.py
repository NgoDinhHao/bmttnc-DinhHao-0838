import hashlib

def calculate_md5(input_string):
    md5_hash = hashlib.md5()  # Khởi tạo đối tượng MD5
    md5_hash.update(input_string.encode('utf-8'))  # Mã hóa và cập nhật dữ liệu
    return md5_hash.hexdigest()  # Trả về chuỗi hex (mã băm)

# Nhập từ người dùng
input_string = input("Nhập chuỗi cần băm: ")
md5_hash = calculate_md5(input_string)

print("Mã băm MD5 của chuỗi '{}' là: {}".format(input_string, md5_hash))
