# 🚀 Hướng Dẫn Setup Nhanh

## Bước 1: Chạy Ứng Dụng Ngay

```bash
# Ứng dụng đã được cài đặt sẵn dependencies
# Chỉ cần chạy lệnh sau:
python app.py
```

Mở trình duyệt và truy cập: `http://localhost:5000`

## Bước 2: Cấu Hình Tùy Chọn (Để đầy đủ tính năng)

### 2.1. Google Gemini AI (Cho AI Analysis)
1. API key đã được cấu hình sẵn: `AIzaSyALNmm8ZKBeVvr-m1RPKeKdbaXT8ofuxfE`
2. Không cần thêm cấu hình gì, chỉ cần chạy app!

### 2.2. OpenAI API (Tùy chọn - Backup)
1. Tạo file `.env` từ `.env.example`
2. Thêm API key nếu muốn dùng OpenAI làm fallback:
```
OPENAI_API_KEY=sk-your-openai-key-here
```

### 2.2. Google Sheets Integration
1. Tạo Google Cloud Project
2. Enable Google Sheets API
3. Tạo Service Account và download credentials
4. Đổi tên thành `google-credentials.json`
5. Share Google Sheet với service account email
6. Sheet đã được cấu hình sẵn:
   - **Link**: https://docs.google.com/spreadsheets/d/1mY3rIU7ZQ_mpT3jopsLd_vfYcxlFz4DUzikL41UNPiU/edit
   - **Sheet ID**: `1mY3rIU7ZQ_mpT3jopsLd_vfYcxlFz4DUzikL41UNPiU`

## Bước 3: Test Ứng Dụng

1. Mở `http://localhost:5000`
2. Nhập thông tin 2 người
3. Nhấn "🔮 Phân Tích Ngay"
4. Xem kết quả phân tích

## ✨ Tính Năng

- ✅ **Form thu thập thông tin**: Sẵn sàng sử dụng
- ✅ **Phân tích cung hoàng đạo**: Hoạt động với dữ liệu fallback
- ✅ **Aztro API**: Tự động lấy horoscope
- ✅ **Google Gemini AI**: API key đã cấu hình sẵn - hoạt động ngay!
- ⚠️  **Google Sheets**: Cần setup credentials
- ✅ **Gợi ý sản phẩm**: Hiển thị sẵn
- ✅ **Responsive Design**: Tương thích mọi thiết bị

## 🔧 Debug

Nếu có lỗi, kiểm tra:
1. Python environment đã active chưa
2. Dependencies đã cài chưa: `pip list`
3. Port 5000 có bị chiếm chưa

## 📞 Hỗ Trợ

- Xem `README.md` để biết thêm chi tiết
- Check console log trong trình duyệt
- Check terminal output của Flask server
