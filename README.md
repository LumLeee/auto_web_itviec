# ITviec Crawler

## 📋 Mô tả
TTự động truy cập trang [itviec.com](https://itviec.com), thu thập thông tin tuyển dụng tại Đà Nẵng: tiêu đề, mô tả, công ty, địa chỉ mỗi ngày lúc 6h sáng.

## 📄 Thư viện
- **setuptools**: Công cụ hỗ trợ cài đặt **undetected-chromedriver**
- **undetected-chromedriver**: Tránh bị phát hiện là bot khi dùng trình duyệt tự động.
- **selenium**: Điều khiển trình duyệt để tự động duyệt web và lấy dữ liệu.
- **pandas**: Xử lý và lưu dữ liệu thành bảng, xuất ra file Excel.
- **schedule**: Hẹn giờ tự động chạy script theo lịch định sẵn.

## ⚙️ Cài đặt môi trường
```bash
pip install -r requirements.txt
```
## 📂 Cấu trúc thư mục
```
.
├── auto_web_itviec.py      # Mã nguồn chính
├── requirements.txt        # Thư viện cần cài
├── README.md               # Hướng dẫn sử dụng
└── itviec.xlsx             # File kết quả sau khi crawl
```

## 📝 Ghi chú
- Kiểm tra đường dẫn lưu file excel tại :
```bash
df.to_excel(r"D:\Desktop\itviec.xlsx", index=False)
```
- Nhập tài khoản và mật khẩu trước khi dùng tại :
```bash
username=""
password=""
```

## 🚀 Cách sử dụng

```bash
python auto_web_itviec.py
```

Kết quả sẽ được lưu thành file `itviec.xlsx` trong thư mục chỉ định.
