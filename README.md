# 🔮 Ứng Dụng Phân Tích Cung Hoàng Đạo

Một ứng dụng web hoàn chỉnh để phân tích mức độ tương thích giữa hai người dựa trên cung hoàng đạo, tích hợp AI và gợi ý sản phẩm phù hợp.

## ✨ Tính Năng Chính

- 📝 **Form thu thập thông tin**: Họ tên, ngày sinh, giới tính, địa chỉ, email, SĐT
- 🔮 **Phân tích cung hoàng đạo**: Tự động xác định cung hoàng đạo từ ngày sinh
- 🌟 **Tích hợp Aztro API**: Lấy thông tin horoscope hàng ngày
- 🤖 **AI Analysis**: Phân tích tính cách và mức độ tương thích
- 📊 **Google Sheets Integration**: Lưu trữ dữ liệu tự động
- 🎁 **Gợi ý sản phẩm**: Hiển thị sản phẩm phù hợp cho cặp đôi
- 📱 **Responsive Design**: Tương thích trên mọi thiết bị

## 🛠️ Công Nghệ Sử Dụng

### Frontend
- **HTML5**: Structure và semantic markup
- **CSS3**: Styling với Flexbox/Grid, animations
- **JavaScript (ES6+)**: Logic xử lý frontend
- **Responsive Design**: Mobile-first approach

### Backend
- **Python Flask**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **Requests**: HTTP client cho API calls
- **Google Sheets API**: Lưu trữ dữ liệu

### APIs & Services
- **Aztro API**: Dữ liệu horoscope
- **Google Gemini AI** (chính): Phân tích AI thông minh
- **OpenAI API** (fallback): Phân tích AI dự phòng
- **Google Sheets**: Database
- **Unsplash**: Hình ảnh sản phẩm

## 🚀 Cài Đặt và Chạy

### Yêu Cầu Hệ Thống
- Python 3.8+
- Git
- Trình duyệt web hiện đại

### 1. Clone Repository
```bash
git clone <repository-url>
cd "AI cung hoang dao"
```

### 2. Cài Đặt Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Cấu Hình Environment Variables
```bash
# Sao chép file template
copy .env.example .env

# Chỉnh sửa file .env với các thông tin thực tế
# - GEMINI_API_KEY: API key của Google Gemini (đã cấu hình sẵn)
# - GOOGLE_SHEET_ID: ID của Google Sheet để lưu dữ liệu (đã cấu hình sẵn)
# - Các cấu hình khác...
```

### 4. Thiết Lập Google Sheets (Tùy chọn)

#### Bước 1: Tạo Google Cloud Project
1. Truy cập [Google Cloud Console](https://console.cloud.google.com/)
2. Tạo project mới hoặc chọn project hiện có
3. Enable Google Sheets API và Google Drive API

#### Bước 2: Tạo Service Account
1. Vào **IAM & Admin > Service Accounts**
2. Tạo service account mới
3. Download file JSON credentials
4. Đổi tên thành `google-credentials.json` và đặt vào thư mục gốc

#### Bước 3: Tạo Google Sheet
1. Tạo Google Sheet mới hoặc sử dụng sheet có sẵn: https://docs.google.com/spreadsheets/d/1mY3rIU7ZQ_mpT3jopsLd_vfYcxlFz4DUzikL41UNPiU/edit
2. Share với email của service account (với quyền Editor)
3. Sheet ID đã được cấu hình sẵn: `1mY3rIU7ZQ_mpT3jopsLd_vfYcxlFz4DUzikL41UNPiU`

### 5. Chạy Ứng Dụng
```bash
# Chạy Flask development server
python app.py

# Hoặc sử dụng flask command
flask run
```

Ứng dụng sẽ chạy tại: `http://localhost:5000`

## 📋 Cách Sử Dụng

### 1. Nhập Thông Tin
- Điền đầy đủ thông tin của hai người
- Ngày sinh sẽ được dùng để xác định cung hoàng đạo

### 2. Phân Tích
- Nhấn nút "🔮 Phân Tích Ngay"
- Hệ thống sẽ:
  - Gọi Aztro API lấy thông tin horoscope
  - Phân tích tương thích qua AI (nếu có)
  - Tạo gợi ý sản phẩm phù hợp

### 3. Xem Kết Quả
- **Phân tích cá nhân**: Tính cách từng người
- **Mức độ tương thích**: Điểm số và phân tích chi tiết
- **Gợi ý sản phẩm**: Danh sách sản phẩm với hình ảnh và link

### 4. Lưu Trữ Dữ Liệu
- Thông tin tự động lưu vào Google Sheets
- Có thể xem và quản lý dữ liệu từ Google Sheets

## 🎨 Tùy Chỉnh

### Thêm Sản Phẩm Mới
Chỉnh sửa function `generateProductRecommendations()` trong `script.js`:

```javascript
const products = [
    {
        name: "Tên sản phẩm",
        image: "URL hình ảnh",
        description: "Mô tả sản phẩm",
        link: "Link sản phẩm", 
        price: "Giá"
    }
    // Thêm sản phẩm mới...
];
```

### Tùy Chỉnh Phân Tích AI
Chỉnh sửa prompt trong `app.py` function `analyze_compatibility_with_ai()`:

```python
prompt = f"""
Tùy chỉnh prompt theo ý bạn...
"""
```

### Thay Đổi Giao Diện
- **CSS**: Chỉnh sửa `style.css` để thay đổi màu sắc, layout
- **HTML**: Cập nhật cấu trúc trong `index.html`
- **JavaScript**: Thêm tính năng mới trong `script.js`

## 🔧 API Endpoints

### POST `/api/analyze`
Phân tích tương thích cung hoàng đạo

**Request Body:**
```json
{
    "person1": {
        "name": "Tên người 1",
        "birth": "2000-01-15",
        "gender": "Nam",
        "phone": "0123456789",
        "email": "email1@example.com",
        "address": "Địa chỉ 1",
        "zodiacSign": "capricorn"
    },
    "person2": {
        // Thông tin tương tự người 2
    }
}
```

**Response:**
```json
{
    "analysis": {
        "compatibility_score": 85,
        "compatibility_analysis": "Phân tích chi tiết...",
        "person1_traits": ["Tính cách 1", "Tính cách 2"],
        "person2_traits": ["Tính cách 1", "Tính cách 2"],
        "product_recommendations": [...]
    },
    "timestamp": "2025-01-01T12:00:00"
}
```

### GET `/health`
Kiểm tra trạng thái server

## 🚀 Deployment

### Heroku
```bash
# Cài Heroku CLI và login
heroku create your-app-name
git push heroku main
heroku config:set GEMINI_API_KEY=AIzaSyALNmm8ZKBeVvr-m1RPKeKdbaXT8ofuxfE
heroku config:set GOOGLE_SHEET_ID=1mY3rIU7ZQ_mpT3jopsLd_vfYcxlFz4DUzikL41UNPiU
```

### Railway/Render
1. Connect GitHub repository
2. Set environment variables
3. Deploy automatically

### VPS/Server
```bash
# Sử dụng Gunicorn cho production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🐛 Troubleshooting

### Lỗi API
- **Aztro API**: Nếu API không hoạt động, app sẽ dùng dữ liệu fallback
- **OpenAI API**: Có thể skip nếu không có API key
- **Google Sheets**: Kiểm tra credentials và permissions

### Lỗi CORS
- Đảm bảo Flask-CORS được cài đặt
- Kiểm tra CORS_ORIGINS trong config

### Lỗi Dependencies
```bash
# Cập nhật pip
python -m pip install --upgrade pip

# Cài lại dependencies
pip install -r requirements.txt --force-reinstall
```

## 🤝 Đóng Góp

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch  
5. Tạo Pull Request

## 📄 License

MIT License - xem file LICENSE để biết thêm chi tiết.

## 📞 Liên Hệ

- **Email**: your-email@example.com
- **GitHub**: your-github-username
- **Website**: your-website.com

## 🙏 Cảm Ơn

- **Aztro API**: Cung cấp dữ liệu horoscope
- **OpenAI**: AI analysis capabilities  
- **Google**: Sheets API cho data storage
- **Unsplash**: Hình ảnh miễn phí cho sản phẩm

---

*Được phát triển với ❤️ cho cộng đồng yêu thích chiêm tinh*
