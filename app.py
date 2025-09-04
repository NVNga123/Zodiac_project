from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import json
import os
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from config import config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_google_credentials():
    """Setup Google credentials from environment variable for production"""
    try:
        creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
        
        if creds_json:
            # Parse JSON string và ghi vào file
            credentials_data = json.loads(creds_json)
            
            with open('google-credentials.json', 'w') as f:
                json.dump(credentials_data, f, indent=2)
            
            print("✅ Google credentials file created from environment variable")
            return True
        else:
            print("⚠️ No GOOGLE_CREDENTIALS_JSON found in environment variables")
            return False
            
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing GOOGLE_CREDENTIALS_JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Error setting up Google credentials: {e}")
        return False

# Setup credentials when app starts
if os.environ.get('FLASK_ENV') == 'production':
    setup_google_credentials()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Configuration constants
GEMINI_API_KEY = app.config['GEMINI_API_KEY']
OPENAI_API_KEY = app.config['OPENAI_API_KEY']
GOOGLE_SHEETS_CREDENTIALS_PATH = app.config['GOOGLE_CREDENTIALS_PATH']
GOOGLE_SHEET_ID = app.config['GOOGLE_SHEET_ID']
GOOGLE_SHEETS_ENABLED = app.config['GOOGLE_SHEETS_ENABLED']
HOROSCOPE_SYSTEM_ENABLED = app.config['HOROSCOPE_SYSTEM_ENABLED']

# Google Sheets setup
def get_google_sheets_client():
    """Initialize Google Sheets client"""
    try:
        if not GOOGLE_SHEETS_ENABLED:
            return None
            
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        
        if os.path.exists(GOOGLE_SHEETS_CREDENTIALS_PATH):
            creds = Credentials.from_service_account_file(
                GOOGLE_SHEETS_CREDENTIALS_PATH, scopes=scope)
            # Use new method instead of deprecated gspread.authorize
            client = gspread.Client(auth=creds)
            client.login()
            return client
        else:
            print("Google credentials file not found. Please add google-credentials.json")
            return None
    except Exception as e:
        print(f"Error initializing Google Sheets client: {e}")
        return None

def get_zodiac_sign(birth_date):
    """Determine zodiac sign from birth date"""
    if not birth_date:
        return 'aries'  # default
    
    try:
        from datetime import datetime
        if isinstance(birth_date, str):
            # Try different date formats
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y']:
                try:
                    date_obj = datetime.strptime(birth_date, fmt)
                    break
                except ValueError:
                    continue
            else:
                return 'aries'  # default if can't parse
        else:
            date_obj = birth_date
            
        month = date_obj.month
        day = date_obj.day
        
        # Zodiac date ranges
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return 'aries'
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return 'taurus'
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return 'gemini'
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return 'cancer'
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return 'leo'
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return 'virgo'
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return 'libra'
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return 'scorpio'
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return 'sagittarius'
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return 'capricorn'
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return 'aquarius'
        elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
            return 'pisces'
        else:
            return 'aries'  # default
    except:
        return 'aries'  # default

def create_comprehensive_horoscope(sign):
    """Generate dynamic horoscope data based on date and zodiac sign"""
    import hashlib
    from datetime import datetime
    
    # Get current date for dynamic content
    today = datetime.now()
    date_seed = f"{sign}_{today.strftime('%Y-%m-%d')}"
    
    # Create deterministic but changing data based on date + sign
    hash_obj = hashlib.md5(date_seed.encode())
    hash_hex = hash_obj.hexdigest()
    
    # Convert hash to numbers for selection
    seed_num = int(hash_hex[:8], 16)
    
    sign_names = {
        'aries': 'Bạch Dương', 'taurus': 'Kim Ngưu', 'gemini': 'Song Tử',
        'cancer': 'Cự Giải', 'leo': 'Sư Tử', 'virgo': 'Xử Nữ',
        'libra': 'Thiên Bình', 'scorpio': 'Hổ Cáp', 'sagittarius': 'Nhân Mã',
        'capricorn': 'Ma Kết', 'aquarius': 'Bao Bình', 'pisces': 'Song Ngư'
    }
    
    # Detailed descriptions for each sign with variations
    descriptions = {
        'aries': [
            "Hôm nay Bạch Dương tràn đầy năng lượng và sẵn sàng đương đầu với mọi thử thách. Sự dũng cảm của bạn sẽ được đền đáp xứng đáng.",
            "Tinh thần lãnh đạo của Bạch Dương được thể hiện rõ nét hôm nay. Đây là thời điểm tuyệt vời để khởi động những dự án mới.",
            "Bạch Dương cảm thấy tự tin và quyết đoán. Hãy tin tưởng vào bản năng và hành động theo trái tim mình.",
            "Năng lượng tích cực bao quanh Bạch Dương. Bạn sẽ tìm thấy động lực mạnh mẽ để theo đuổi những mục tiêu quan trọng."
        ],
        'taurus': [
            "Kim Ngưu tận hưởng sự ổn định và bình yên hôm nay. Đây là thời điểm tốt để tập trung vào những điều thực tế.",
            "Sự kiên nhẫn của Kim Ngưu sẽ được đền đáp. Những nỗ lực lâu dài cuối cùng cũng bắt đầu cho thấy kết quả.",
            "Kim Ngưu cảm thấy kết nối sâu sắc với thiên nhiên và vẻ đẹp. Hãy dành thời gian thưởng thức những điều đơn giản.",
            "Tính thực tế của Kim Ngưu giúp bạn đưa ra những quyết định sáng suốt trong công việc và tài chính."
        ],
        'gemini': [
            "Trí tuệ và sự tò mò của Song Tử được kích hoạt mạnh mẽ. Bạn sẽ học được nhiều điều thú vị hôm nay.",
            "Khả năng giao tiếp xuất sắc của Song Tử tỏa sáng. Đây là ngày tuyệt vời để kết nối và chia sẻ ý tưởng.",
            "Song Tử cảm thấy linh hoạt và thích ứng tốt với mọi tình huống. Sự đa tài của bạn được nhiều người ngưỡng mộ.",
            "Tâm trí nhanh nhạy của Song Tử giúp tìm ra giải pháp sáng tạo cho những vấn đề phức tạp."
        ],
        'cancer': [
            "Cự Giải cảm nhận được sự ấm áp từ gia đình và người thân. Tình cảm chân thành sẽ được đáp lại.",
            "Trực giác mạnh mẽ của Cự Giải dẫn dắt bạn đến những quyết định đúng đắn. Hãy tin tưởng vào cảm xúc của mình.",
            "Cự Giải thể hiện sự chăm sóc và bảo vệ những người quan trọng. Lòng nhân ái của bạn được nhiều người trân trọng.",
            "Khả năng đồng cảm của Cự Giải giúp hiểu sâu tâm tư của người khác và tạo nên những mối quan hệ bền chặt."
        ],
        'leo': [
            "Sư Tử tỏa sáng với sự tự tin và lôi cuốn không thể chối từ. Bạn là tâm điểm của mọi ánh nhìn.",
            "Tinh thần lãnh đạo của Sư Tử được thể hiện rõ nét. Khả năng truyền cảm hứng của bạn sẽ động viên nhiều người.",
            "Sư Tử cảm thấy được công nhận và trân trọng. Đây là thời điểm để thể hiện tài năng và sức sáng tạo.",
            "Lòng hào hiệp của Sư Tử được bộc lộ. Bạn sẵn sàng giúp đỡ và bảo vệ những người cần hỗ trợ."
        ],
        'virgo': [
            "Xử Nữ tập trung vào việc hoàn thiện và cải thiện mọi thứ xung quanh. Sự tỉ mỉ của bạn được đánh giá cao.",
            "Khả năng phân tích của Xử Nữ giúp nhìn rõ bản chất vấn đề. Bạn sẽ tìm ra cách giải quyết hiệu quả.",
            "Xử Nữ cảm thấy hài lòng khi giúp đỡ người khác. Sự chu đáo và tận tâm của bạn tạo nên khác biệt lớn.",
            "Tinh thần cầu tiến của Xử Nữ thúc đẩy bạn không ngừng học hỏi và phát triển bản thân."
        ],
        'libra': [
            "Thiên Bình tìm kiếm sự cân bằng và hài hòa trong mọi khía cạnh cuộc sống. Bạn là người hòa giải tuyệt vời.",
            "Khiếu thẩm mỹ của Thiên Bình được thể hiện rõ nét. Bạn có thể tạo ra vẻ đẹp và sự thanh lịch.",
            "Thiên Bình thể hiện sự công bằng và khách quan. Khả năng cân nhắc của bạn giúp đưa ra quyết định sáng suốt.",
            "Sự duyên dáng của Thiên Bình thu hút nhiều người. Bạn có thể xây dựng những mối quan hệ tích cực."
        ],
        'scorpio': [
            "Hổ Cáp đào sâu vào bản chất của mọi vấn đề. Trực giác mạnh mẽ của bạn không bao giờ lừa dối.",
            "Sức mạnh nội tại của Hổ Cáp được kích hoạt. Bạn có thể vượt qua mọi khó khăn và thử thách.",
            "Hổ Cáp thể hiện sự quyết tâm và bền bỉ. Không có gì có thể ngăn cản bạn đạt được mục tiêu.",
            "Khả năng tái sinh của Hổ Cáp giúp bạn biến những thách thức thành cơ hội phát triển."
        ],
        'sagittarius': [
            "Nhân Mã khao khát tự do và khám phá những chân trời mới. Tinh thần phiêu lưu dẫn dắt bạn đến thành công.",
            "Triết lý sống tích cực của Nhân Mã lan tỏa đến mọi người xung quanh. Bạn là nguồn cảm hứng cho nhiều người.",
            "Nhân Mã mở rộng tầm nhìn và kiến thức. Những trải nghiệm mới sẽ làm phong phú thế giới nội tâm.",
            "Sự lạc quan của Nhân Mã giúp vượt qua mọi trở ngại. Bạn luôn tìm thấy ánh sáng trong bóng tối."
        ],
        'capricorn': [
            "Ma Kết kiên định trên con đường đạt được mục tiêu. Sự chăm chỉ và kỷ luật sẽ được đền đáp xứng đáng.",
            "Tính thực tế của Ma Kết giúp xây dựng nền tảng vững chắc cho tương lai. Bạn là người đáng tin cậy.",
            "Ma Kết thể hiện sự trách nhiệm và cam kết. Khả năng lãnh đạo của bạn được nhiều người kính trọng.",
            "Sự kiên nhẫn của Ma Kết cuối cùng cũng được đền đáp. Những nỗ lực lâu dài bắt đầu cho thấy kết quả."
        ],
        'aquarius': [
            "Bao Bình tràn đầy ý tưởng sáng tạo và quan điểm độc đáo. Bạn có thể tạo ra những thay đổi tích cực.",
            "Tinh thần nhân đạo của Bao Bình được thể hiện rõ nét. Bạn muốn đóng góp cho cộng đồng và xã hội.",
            "Bao Bình thể hiện sự độc lập và tự do. Khả năng tư duy khác biệt giúp tìm ra giải pháp mới.",
            "Tầm nhìn tương lai của Bao Bình giúp dự đoán và chuẩn bị cho những thay đổi sắp tới."
        ],
        'pisces': [
            "Song Ngư kết nối sâu sắc với trực giác và cảm xúc. Khả năng đồng cảm của bạn chạm đến trái tim người khác.",
            "Sự nhạy cảm của Song Ngư giúp cảm nhận được những điều tinh tế. Bạn có thể hiểu được cảm xúc của mọi người.",
            "Song Ngư thể hiện sự từ bi và tha thứ. Tình yêu thương vô điều kiện của bạn chữa lành nhiều tổn thương.",
            "Trí tưởng tượng phong phú của Song Ngư tạo ra những ý tưởng tuyệt vời và nguồn cảm hứng bất tận."
        ]
    }
    
    # Colors for each sign
    colors = {
        'aries': ['Đỏ tươi', 'Cam rực', 'Đỏ thẫm'],
        'taurus': ['Xanh lục', 'Nâu đất', 'Hồng nhạt'],
        'gemini': ['Vàng', 'Bạc', 'Xanh nhạt'],
        'cancer': ['Bạc', 'Trắng ngọc trai', 'Xanh biển'],
        'leo': ['Vàng kim', 'Cam', 'Đỏ'],
        'virgo': ['Xanh navy', 'Nâu', 'Be'],
        'libra': ['Hồng', 'Xanh pastel', 'Trắng'],
        'scorpio': ['Đỏ thẫm', 'Đen', 'Tím'],
        'sagittarius': ['Tím', 'Xanh dương', 'Đỏ'],
        'capricorn': ['Nâu', 'Xanh đậm', 'Đen'],
        'aquarius': ['Xanh dương', 'Bạc', 'Tím'],
        'pisces': ['Xanh lam', 'Xanh lục biển', 'Tím nhạt']
    }
    
    # Moods for each sign
    moods = {
        'aries': ['Năng động và quyết đoán', 'Nhiệt huyết và dũng cảm', 'Tự tin và mạnh mẽ'],
        'taurus': ['Ổn định và thực tế', 'Bình yên và kiên nhẫn', 'Đáng tin cậy'],
        'gemini': ['Tò mò và linh hoạt', 'Thông minh và giao tiếp', 'Sáng tạo'],
        'cancer': ['Ấm áp và che chở', 'Nhạy cảm và trực giác', 'Yêu thương'],
        'leo': ['Tự tin và rạng rỡ', 'Hào hứng và tỏa sáng', 'Lãnh đạo'],
        'virgo': ['Tỉ mỉ và cẩn thận', 'Hoàn hảo và phân tích', 'Chu đáo'],
        'libra': ['Hòa hợp và công bằng', 'Thanh lịch và cân bằng', 'Hòa bình'],
        'scorpio': ['Mạnh mẽ và bí ẩn', 'Quyết tâm và sâu sắc', 'Trực giác'],
        'sagittarius': ['Tự do và phiêu lưu', 'Lạc quan và triết học', 'Khám phá'],
        'capricorn': ['Kỷ luật và có mục tiêu', 'Trách nhiệm và kiên định', 'Thực tế'],
        'aquarius': ['Sáng tạo và độc lập', 'Nhân đạo và tương lai', 'Độc đáo'],
        'pisces': ['Nhạy cảm và trực giác', 'Từ bi và nghệ thuật', 'Tưởng tượng']
    }
    
    # Lucky elements
    lucky_elements = [
        'một cuộc gặp gỡ quan trọng', 'tin tức tích cực', 'cơ hội mới',
        'sự hỗ trợ từ bạn bè', 'thành công trong công việc', 'tình yêu đẹp',
        'sức khỏe tốt', 'tài lộc', 'sự học hỏi', 'niềm vui bất ngờ'
    ]
    
    # Select variations based on seed
    desc_idx = seed_num % len(descriptions.get(sign, descriptions['aries']))
    color_idx = (seed_num >> 8) % len(colors.get(sign, colors['aries']))
    mood_idx = (seed_num >> 16) % len(moods.get(sign, moods['aries']))
    element_idx = (seed_num >> 24) % len(lucky_elements)
    
    return {
        "description": descriptions.get(sign, descriptions['aries'])[desc_idx],
        "compatibility": f"Cung {sign_names.get(sign, sign)} hôm nay có khả năng tương thích tốt, đặc biệt trong việc {lucky_elements[element_idx]}.",
        "mood": moods.get(sign, moods['aries'])[mood_idx],
        "color": colors.get(sign, colors['aries'])[color_idx],
        "lucky_number": str((seed_num % 9) + 1),
        "lucky_time": f"{10 + (seed_num % 6)}:00 AM - {2 + ((seed_num >> 4) % 4)}:00 PM",
                "current_date": today.strftime('%B %d, %Y')
    }

def get_horoscope_data(sign):
    """Generate comprehensive horoscope data locally without external APIs"""
    print(f"Generating local horoscope data for {sign}")
    return create_comprehensive_horoscope(sign)

def create_fallback_horoscope(sign):
    """Create enhanced fallback horoscope data when API fails"""
    sign_names = {
        'aries': 'Bạch Dương', 'taurus': 'Kim Ngưu', 'gemini': 'Song Tử',
        'cancer': 'Cự Giải', 'leo': 'Sư Tử', 'virgo': 'Xử Nữ',
        'libra': 'Thiên Bình', 'scorpio': 'Hổ Cáp', 'sagittarius': 'Nhân Mã',
        'capricorn': 'Ma Kết', 'aquarius': 'Bao Bình', 'pisces': 'Song Ngư'
    }
    
    # Enhanced descriptions for each sign
    sign_descriptions = {
        'aries': 'Hôm nay là ngày tuyệt vời để Bạch Dương thể hiện sự năng động và dẫn dắt. Bạn sẽ cảm thấy tràn đầy năng lượng và sẵn sàng đối mặt với mọi thử thách.',
        'taurus': 'Kim Ngưu sẽ có một ngày ổn định và thu hoạch những thành quả từ sự kiên nhẫn. Đây là thời điểm tốt để tập trung vào công việc và tài chính.',
        'gemini': 'Song Tử sẽ có cơ hội giao tiếp và học hỏi nhiều điều mới. Trí óc nhanh nhạy của bạn sẽ giúp giải quyết hiệu quả các vấn đề.',
        'cancer': 'Cự Giải cảm thấy kết nối sâu sắc với gia đình và người thân. Hôm nay là ngày tốt để nuôi dưỡng các mối quan hệ quan trọng.',
        'leo': 'Sư Tử tỏa sáng với sự tự tin và lôi cuốn. Bạn sẽ thu hút sự chú ý và có cơ hội thể hiện tài năng của mình.',
        'virgo': 'Xử Nữ tập trung vào việc hoàn thiện và cải thiện. Sự tỉ mỉ và cẩn thận sẽ mang lại kết quả tích cực trong công việc.',
        'libra': 'Thiên Bình tìm kiếm sự cân bằng và hòa hợp. Khả năng ngoại giao của bạn sẽ giúp giải quyết các xung đột một cách suôn sẻ.',
        'scorpio': 'Hổ Cáp đào sâu vào bản chất của vấn đề. Trực giác mạnh mẽ sẽ dẫn dắt bạn đến những phát hiện quan trọng.',
        'sagittarius': 'Nhân Mã khao khát tự do và khám phá. Hôm nay mang đến cơ hội mở rộng tầm nhìn và học hỏi điều mới.',
        'capricorn': 'Ma Kết kiên định trên con đường đạt được mục tiêu. Sự chăm chỉ và kỷ luật sẽ đưa bạn tiến gần hơn đến thành công.',
        'aquarius': 'Bao Bình tràn đầy ý tưởng sáng tạo và quan điểm độc đáo. Bạn có thể đóng góp những giải pháp mới mẻ cho cộng đồng.',
        'pisces': 'Song Ngư kết nối với trực giác và cảm xúc sâu sắc. Khả năng đồng cảm và sự nhạy cảm sẽ giúp bạn hiểu rõ hơn về người khác.'
    }
    
    sign_colors = {
        'aries': 'Đỏ', 'taurus': 'Xanh lục', 'gemini': 'Vàng',
        'cancer': 'Bạc', 'leo': 'Vàng kim', 'virgo': 'Xanh navy',
        'libra': 'Hồng', 'scorpio': 'Đỏ thẫm', 'sagittarius': 'Tím',
        'capricorn': 'Nâu', 'aquarius': 'Xanh dương', 'pisces': 'Xanh lam'
    }
    
    sign_moods = {
        'aries': 'Năng động và quyết đoán', 'taurus': 'Ổn định và thực tế',
        'gemini': 'Tò mò và linh hoạt', 'cancer': 'Ấm áp và che chở',
        'leo': 'Tự tin và rạng rỡ', 'virgo': 'Tỉ mỉ và cẩn thận',
        'libra': 'Hòa hợp và công bằng', 'scorpio': 'Mạnh mẽ và bí ẩn',
        'sagittarius': 'Tự do và phiêu lưu', 'capricorn': 'Kỷ luật và có mục tiêu',
        'aquarius': 'Sáng tạo và độc lập', 'pisces': 'Nhạy cảm và trực giác'
    }
    
    return {
        "description": sign_descriptions.get(sign, f"Hôm nay là ngày tích cực cho cung {sign_names.get(sign, sign)}"),
        "compatibility": f"Cung {sign_names.get(sign, sign)} có khả năng tương thích tốt với những cung có tính cách bổ trợ và hỗ trợ lẫn nhau.",
        "mood": sign_moods.get(sign, "Tích cực và lạc quan"),
        "color": sign_colors.get(sign, "Xanh dương"),
        "lucky_number": str(hash(sign) % 9 + 1),
        "lucky_time": f"{10 + hash(sign) % 6}:00 AM - {2 + hash(sign) % 4}:00 PM",
        "current_date": datetime.now().strftime('%B %d, %Y')
    }

def calculate_compatibility_score(sign1, sign2):
    """Calculate compatibility score based on element and modality compatibility"""
    
    # Element mapping
    element_map = {
        'aries': 'fire', 'leo': 'fire', 'sagittarius': 'fire',
        'taurus': 'earth', 'virgo': 'earth', 'capricorn': 'earth', 
        'gemini': 'air', 'libra': 'air', 'aquarius': 'air',
        'cancer': 'water', 'scorpio': 'water', 'pisces': 'water'
    }
    
    # Modality mapping  
    modality_map = {
        'aries': 'cardinal', 'cancer': 'cardinal', 'libra': 'cardinal', 'capricorn': 'cardinal',
        'taurus': 'fixed', 'leo': 'fixed', 'scorpio': 'fixed', 'aquarius': 'fixed',
        'gemini': 'mutable', 'virgo': 'mutable', 'sagittarius': 'mutable', 'pisces': 'mutable'
    }
    
    element1 = element_map.get(sign1.lower(), 'fire')
    element2 = element_map.get(sign2.lower(), 'fire') 
    modality1 = modality_map.get(sign1.lower(), 'cardinal')
    modality2 = modality_map.get(sign2.lower(), 'cardinal')
    
    # Base score by element compatibility
    base_score = 50  # default
    
    # Element compatibility rules
    if element1 == element2:
        # Same element - high compatibility
        base_score = 82
    elif (element1 == 'fire' and element2 == 'air') or (element1 == 'air' and element2 == 'fire'):
        # Fire + Air (complementary) - very high
        base_score = 90
    elif (element1 == 'earth' and element2 == 'water') or (element1 == 'water' and element2 == 'earth'):
        # Earth + Water (complementary) - very high
        base_score = 88
    elif (element1 == 'fire' and element2 == 'water') or (element1 == 'water' and element2 == 'fire'):
        # Fire + Water (opposing) - challenging
        base_score = 35
    elif (element1 == 'earth' and element2 == 'air') or (element1 == 'air' and element2 == 'earth'):
        # Earth + Air (square) - moderate challenge
        base_score = 45
    else:
        # Other combinations - neutral
        base_score = 55
    
    # Modality adjustments
    modality_adjustment = 0
    
    if (modality1 == 'cardinal' and modality2 == 'mutable') or (modality1 == 'mutable' and modality2 == 'cardinal'):
        modality_adjustment = 8
    elif (modality1 == 'fixed' and modality2 == 'mutable') or (modality1 == 'mutable' and modality2 == 'fixed'):
        modality_adjustment = 5
    elif modality1 == 'cardinal' and modality2 == 'cardinal':
        modality_adjustment = -2
    elif modality1 == 'fixed' and modality2 == 'fixed':
        modality_adjustment = -5
    # Cardinal + Fixed = 0, Mutable + Mutable = +3
    elif modality1 == 'mutable' and modality2 == 'mutable':
        modality_adjustment = 3
    
    final_score = max(0, min(100, base_score + modality_adjustment))
    return final_score

def get_compatibility_tier(score):
    """Get compatibility tier based on score according to instruction"""
    if score >= 85:
        return "Hợp duyên trời định"
    elif score >= 70:
        return "Có duyên, cần thời gian vun đắp"  
    elif score >= 40:
        return "Có duyên nhưng cần nỗ lực nhiều"
    else:
        return "Có sự khác biệt, cần thấu hiểu nhiều hơn"

def get_tier_description(tier):
    """Get tier description according to instruction"""
    descriptions = {
        "Hợp duyên trời định": "Hai bạn như mảnh ghép vừa khít – dễ đồng điệu cả trong tính cách lẫn cảm xúc. Chỉ cần một cái nhìn cũng đủ hiểu nhau.",
        "Có duyên, cần thời gian vun đắp": "Giữa hai bạn có sự hấp dẫn nhau tự nhiên, nhưng vẫn cần trải nghiệm, chia sẻ thêm về suy nghĩ và cảm xúc để gắn bó lâu dài.",
        "Có duyên nhưng cần nỗ lực nhiều": "Sự khác biệt có thể dẫn đến mâu thuẫn, nhưng nếu đủ kiên nhẫn thì đây lại là cơ hội để học cách dung hòa và trưởng thành, biết chấp nhận và tôn trọng sự khác biệt của người khác.",
        "Có sự khác biệt, cần thấu hiểu nhiều hơn": "Hai bạn có nhiều điểm khác biệt, nhưng chính điều đó có thể giúp mỗi người soi chiếu và hiểu rõ bản thân hơn, biết rằng mình cần điều chỉnh gì để hài hòa mối quan hệ."
    }
    return descriptions.get(tier, "")

def analyze_compatibility_with_ai(person1_data, person2_data, horoscope1, horoscope2):
    """Use OpenAI to analyze compatibility based on detailed instruction scenarios"""
    
    # Calculate score using the new formula
    sign1 = person1_data['zodiacSign'].lower()
    sign2 = person2_data['zodiacSign'].lower()
    compatibility_score = calculate_compatibility_score(sign1, sign2)
    compatibility_tier = get_compatibility_tier(compatibility_score)
    tier_description = get_tier_description(compatibility_tier)
    
    # Build detailed prompt based on instruction
    prompt = f"""
    Bạn là chuyên gia chiêm tinh chuyên nghiệp với 20 năm kinh nghiệm. Hãy phân tích tương thích giữa 2 người theo CHÍNH XÁC kịch bản "{compatibility_tier}":

    Người 1: {person1_data['name']} - Cung {person1_data['zodiacSign']} - {person1_data['gender']}
    Người 2: {person2_data['name']} - Cung {person2_data['zodiacSign']} - {person2_data['gender']}

    Kết quả đánh giá: {compatibility_tier}
    Mô tả: {tier_description}
    
    VIẾT PHÂN TÍCH CHI TIẾT THEO CHÍNH XÁC KỊCH BẢN "{compatibility_tier}" với cấu trúc:

    1. ZODIAC_SUMMARY: Mô tả chi tiết về tính cách cung hoàng đạo của từng người dựa trên thông tin nguồn (đoạn văn 200-300 chữ)

    2. PERSONALITY_ANALYSIS: Phân tích chi tiết, vô cùng chi tiết về tính cách và cung hoàng đạo của từng người (đoạn văn liền mạch 200-300 chữ mỗi người)

    3. DIFFERENCES (theo tier): 
    - Tier "Có duyên, cần thời gian vun đắp": điểm khác biệt không quá gay gắt, dễ dung hòa với ví dụ cụ thể (200-300 chữ mỗi người)
    - Tier "Có duyên nhưng cần nỗ lực nhiều": điểm khác biệt có thể sửa được để cùng phát triển với ví dụ cụ thể (200-300 chữ)  
    - Tier "Có sự khác biệt, cần thấu hiểu nhiều hơn": khác biệt về trọng tâm, giá trị, quan điểm sống với ví dụ cụ thể (200-300 chữ)

    4. STRENGTHS: 
    - Tier "Hợp duyên trời định": tương đồng tính cách, giá trị sống (200-300 chữ)
    - Tier "Có duyên, cần thời gian vun đắp": tương đồng tính cách, giá trị sống (200-300 chữ)
    - Tier "Có duyên nhưng cần nỗ lực nhiều": lợi ích khi cân bằng tính cách đối lập với ví dụ (200-300 chữ)
    - Tier "Có sự khác biệt, cần thấu hiểu nhiều hơn": bài học và giá trị nhận được với ví dụ (200-300 chữ)

    5. LIFE_BENEFITS: Vẽ bối cảnh chi tiết về lợi ích trong đời sống (200-300 chữ)
    6. WORK_BENEFITS: Vẽ bối cảnh chi tiết về lợi ích trong công việc (200-300 chữ)
    7. LOVE_BENEFITS: Vẽ bối cảnh chi tiết về lợi ích trong tình cảm (200-300 chữ)

    8. ADVICE: Lời khuyên chi tiết (400-500 chữ) theo đúng cấu trúc tier:
    
    - Tier "Hợp duyên trời định" & "Có duyên, cần thời gian vun đắp":
    Bước 1: Hai bạn có rất nhiều giá trị tương đồng để có thể tìm hiểu, làm quen lâu dài
    Bước 2: Tại sao không thử mở cánh cửa cơ hội cho mình nhỉ, cùng làm quen, đi chơi
    Bước 3: Nếu trong buổi hẹn đầu tiên mà đã có một món quà nhỏ cho đối phương thì chắc chắn sẽ để lại ấn tượng rất sâu sắc
    Bước 4: Như một vài món quà sau đây, chúng không quá đắt để đối phương thấy ngại khi nhận, nhưng cũng đủ giá trị để thể hiện sự quan tâm
    
    - Tier "Có duyên nhưng cần nỗ lực nhiều":
    Bước 1: Tạo đồng cảm (khác biệt là tất yếu → học cách chấp nhận → đừng từ bỏ cơ hội)
    Bước 2: Giới thiệu quà (kết nối → ấn tượng → không quá đắt nhưng đủ giá trị)
    
    - Tier "Có sự khác biệt, cần thấu hiểu nhiều hơn":
    Bước 1: Bẻ lại tư tưởng (chiêm tinh chỉ là công cụ → thấu hiểu là nền tảng → link: https://afamily.vn/gioi-tre-trung-quoc-mat-niem-tin-vao-cung-hoang-dao-sau-khi-chiem-tinh-gia-noi-tieng-19-trieu-follower-ly-hon-20250810140654261.chn → đừng bỏ lỡ người → tạo niềm tin kết nối)
    Bước 2: Giới thiệu quà (kết nối → ấn tượng → không quá đắt nhưng đủ giá trị)

    9. PRODUCT_RECOMMENDATIONS: 3 sản phẩm phù hợp với cặp đôi

    Trả về JSON với keys: compatibility_tier, tier_description, zodiac_summary, personality_analysis, differences, strengths, life_benefits, work_benefits, love_benefits, advice, product_recommendations
    
    Viết bằng tiếng Việt, mỗi đoạn văn liền mạch, chi tiết và chuyên nghiệp theo CHÍNH XÁC instruction.
    """

    try:
        # Use OpenAI API first
        if OPENAI_API_KEY and OPENAI_API_KEY != 'your-openai-api-key-here':
            headers = {
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'gpt-5',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 4000,
                'temperature': 0.7
            }
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # Clean up the response to extract JSON
                ai_response = ai_response.strip()
                if ai_response.startswith('```json'):
                    ai_response = ai_response[7:-3].strip()
                elif ai_response.startswith('```'):
                    ai_response = ai_response[3:-3].strip()
                
                try:
                    return json.loads(ai_response)
                except json.JSONDecodeError:
                    print(f"Failed to parse OpenAI JSON response: {ai_response}")
                    return generate_fallback_analysis(person1_data, person2_data)
            else:
                print(f"OpenAI API error: {response.status_code}")
                return generate_fallback_analysis(person1_data, person2_data)
        
        # COMMENT OUT GEMINI FOR NOW - CAN UNCOMMENT LATER
        # elif GEMINI_API_KEY and GEMINI_API_KEY != 'your-gemini-api-key-here':
        #     headers = {
        #         'Content-Type': 'application/json',
        #         'X-goog-api-key': GEMINI_API_KEY
        #     }
        #     
        #     data = {
        #         'contents': [{
        #             'parts': [{
        #                 'text': prompt
        #             }]
        #         }],
        #         'generationConfig': {
        #             'temperature': 0.7,
        #             'maxOutputTokens': 8192,
        #         }
        #     }
        #     
        #     response = requests.post(
        #         'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent',
        #         headers=headers,
        #         json=data,
        #         timeout=60
        #     )
        #     
        #     if response.status_code == 200:
        #         result = response.json()
        #         if 'candidates' in result and len(result['candidates']) > 0:
        #             ai_response = result['candidates'][0]['content']['parts'][0]['text']
        #             ai_response = ai_response.strip()
        #             if ai_response.startswith('```json'):
        #                 ai_response = ai_response[7:-3].strip()
        #             elif ai_response.startswith('```'):
        #                 ai_response = ai_response[3:-3].strip()
        #             
        #             try:
        #                 return json.loads(ai_response)
        #             except json.JSONDecodeError:
        #                 print(f"Failed to parse Gemini JSON response: {ai_response}")
        #                 return generate_fallback_analysis(person1_data, person2_data)
        #     else:
        #         print(f"Gemini API error: {response.status_code}")
        #         return generate_fallback_analysis(person1_data, person2_data)
        
        # Fallback analysis if no AI API is available
        return generate_fallback_analysis(person1_data, person2_data)
        
    except Exception as e:
        print(f"Error in AI analysis: {e}")
        return generate_fallback_analysis(person1_data, person2_data)

def generate_fallback_analysis(person1_data, person2_data):
    """Generate fallback analysis without AI using instruction format"""
    
    # Calculate compatibility using the same system as AI function
    compatibility_score = calculate_compatibility_score(
        person1_data['zodiacSign'], 
        person2_data['zodiacSign']
    )
    compatibility_tier = get_compatibility_tier(compatibility_score)
    
    # Define personality traits for each sign
    personality_traits = {
        'aries': ['Năng động và đầy nhiệt huyết', 'Dám dấn thân và không sợ thử thách', 'Có khả năng lãnh đạo tự nhiên', 'Đôi khi hơi nóng tính'],
        'taurus': ['Ổn định và đáng tin cậy', 'Yêu thích sự thoải mái và an toàn', 'Kiên nhẫn và bền bỉ', 'Có thể hơi cố chấp'],
        'gemini': ['Thông minh và linh hoạt', 'Giao tiếp tốt và hòa đồng', 'Luôn tò mò học hỏi', 'Có thể thay đổi suy nghĩ nhanh'],
        'cancer': ['Tình cảm sâu sắc và quan tâm người khác', 'Trực giác tốt và nhạy cảm', 'Yêu gia đình và bảo vệ người thân', 'Đôi khi quá nhạy cảm'],
        'leo': ['Tự tin và có sức hút', 'Hào phóng và ấm áp', 'Sáng tạo và đầy cảm hứng', 'Thích được chú ý và ngưỡng mộ'],
        'virgo': ['Tỉ mỉ và cầu toàn', 'Thực tế và có logic', 'Luôn muốn giúp đỡ người khác', 'Có thể quá khắt khe với bản thân'],
        'libra': ['Cân bằng và hài hòa', 'Có gu thẩm mỹ tốt', 'Công bằng và khách quan', 'Đôi khi hay do dự'],
        'scorpio': ['Sâu sắc và bí ẩn', 'Có ý chí mạnh mẽ', 'Trung thành và chung thủy', 'Có thể hay ghen tuông'],
        'sagittarius': ['Yêu tự do và phiêu lưu', 'Lạc quan và tích cực', 'Thích khám phá và du lịch', 'Đôi khi thiếu kiên nhẫn'],
        'capricorn': ['Có trách nhiệm và thực tế', 'Tham vọng và quyết tâm', 'Kiên trì theo đuổi mục tiêu', 'Có thể quá nghiêm túc'],
        'aquarius': ['Độc lập và sáng tạo', 'Quan tâm đến vấn đề xã hội', 'Tư duy tiến bộ', 'Đôi khi xa cách về mặt cảm xúc'],
        'pisces': ['Nhạy cảm và giàu cảm xúc', 'Trực giác mạnh và sáng tạo', 'Đồng cảm và hiểu biết', 'Có thể quá mơ mộng']
    }
    
    sign1 = person1_data['zodiacSign'].lower()
    sign2 = person2_data['zodiacSign'].lower()
    
    # Generate advice based on compatibility tier 
    advice_by_tier = {
        "Hợp duyên trời định": f"Hai bạn có rất nhiều giá trị tương đồng để có thể tìm hiểu, làm quen lâu dài. Sự hòa hợp giữa cung {sign1.title()} và {sign2.title()} tạo nên một mối quan hệ đầy tiềm năng. Tại sao không thử mở cánh cửa cơ hội cho mình nhỉ, cùng làm quen, đi chơi? Nếu trong buổi hẹn đầu tiên mà đã có một món quà nhỏ cho đối phương thì chắc chắn sẽ để lại ấn tượng rất sâu sắc.",
        
        "Có duyên cần thời gian vun đắp": f"Hai bạn có rất nhiều giá trị tương đồng để có thể tìm hiểu, làm quen lâu dài. Mối quan hệ giữa cung {sign1.title()} và {sign2.title()} có tiềm năng phát triển lâu dài. Tại sao không thử mở cánh cửa cơ hội cho mình nhỉ, cùng làm quen, đi chơi? Nếu trong buổi hẹn đầu tiên mà đã có một món quà nhỏ cho đối phương thì chắc chắn sẽ để lại ấn tượng rất sâu sắc.",
        
        "Có duyên nhưng cần nỗ lực nhiều": f"Mỗi người lớn lên trong môi trường giáo dục khác nhau, nên điểm khác biệt là điều tất yếu trong cuộc sống. Sự khác biệt có mặt ở mọi nơi, không chỉ bạn và bạn này mà sau này bạn và bạn khác cũng sẽ có sự khác biệt. Vậy nên điểm mấu chốt nhất là các bạn học cách chấp nhận và tôn trọng điều khác biệt ở nhau để cùng phát triển, cùng trở nên hợp hơn. Nên là đừng vì có một chút khác biệt mà từ bỏ cơ hội, hãy cứ thử sức, hãy cho mình cơ hội để hiểu bản thân và hiểu người khác hơn.",
        
        "Có sự khác biệt, cần thấu hiểu nhiều hơn": f"Tuy nhiên, bạn hãy nhớ một điều rằng tất cả các loại hình chiêm tinh chỉ là công cụ giúp bạn thấu hiểu bản thân, chứ không phải kim chỉ nam của mọi mối quan hệ. Mà trên hết, sự thấu hiểu và trưởng thành cảm xúc mới là nền tảng quan trọng nhất để duy trì một mối quan hệ. Vì đến ngay cả cặp Kim Ngưu – Thiên Yết (Bọ Cạp) được đánh giá rất cao về độ phù hợp nhưng vẫn đổ vỡ vì chưa có đủ sự thấu hiểu, cảm thông và trưởng thành cảm xúc. Vậy nên đừng vì sự đánh giá sơ bộ của bất kỳ công cụ chiêm tinh nào mà bỏ lỡ một người."
    }
    
    return {
        "compatibility_tier": compatibility_tier,
        "tier_description": compatibility_tier,
        "zodiac_summary": f"Cung {sign1.title()} và cung {sign2.title()} đại diện cho hai phong cách sống và tư duy khác nhau. {sign1.title()} thường {personality_traits.get(sign1, ['có tính cách riêng biệt'])[0].lower()}, trong khi {sign2.title()} {personality_traits.get(sign2, ['có tính cách riêng biệt'])[0].lower()}. Sự kết hợp này tạo nên một bức tranh tổng thể đa dạu và phong phú, mang đến những trải nghiệm thú vị trong hành trình tìm hiểu nhau.",
        
        "personality_analysis": f"{person1_data['name']} thuộc cung {sign1.title()} - một người {personality_traits.get(sign1, ['tính cách độc đáo'])[0].lower()}, {personality_traits.get(sign1, ['tính cách độc đáo'])[1].lower() if len(personality_traits.get(sign1, [''])) > 1 else 'có cách nhìn riêng về cuộc sống'}. Trong giao tiếp, {person1_data['name']} thường thể hiện sự {personality_traits.get(sign1, ['tính cách độc đáo'])[2].lower() if len(personality_traits.get(sign1, [''])) > 2 else 'chân thành và cởi mở'}. Về mặt cảm xúc, những người cung {sign1.title()} thường có xu hướng {personality_traits.get(sign1, ['tính cách độc đáo'])[-1].lower() if len(personality_traits.get(sign1, [''])) > 3 else 'thể hiện cảm xúc một cách trực tiếp'}.\n\nTrong khi đó, {person2_data['name']} thuộc cung {sign2.title()} lại {personality_traits.get(sign2, ['tính cách độc đáo'])[0].lower()}, {personality_traits.get(sign2, ['tính cách độc đáo'])[1].lower() if len(personality_traits.get(sign2, [''])) > 1 else 'có phong cách riêng'}. {person2_data['name']} thường {personality_traits.get(sign2, ['tính cách độc đáo'])[2].lower() if len(personality_traits.get(sign2, [''])) > 2 else 'xử lý tình huống một cách khéo léo'}, và có khuynh hướng {personality_traits.get(sign2, ['tính cách độc đáo'])[-1].lower() if len(personality_traits.get(sign2, [''])) > 3 else 'lắng nghe và thấu hiểu'}. Sự kết hợp giữa hai tính cách này tạo nên những trải nghiệm phong phú, trong đó mỗi người đều có thể học hỏi và khám phá những khía cạnh mới về bản thân qua con mắt của người kia.",
        
        "differences": "Những khác biệt chính giữa hai người nằm ở cách tiếp cận cuộc sống và thể hiện cảm xúc. Trong khi một người có thể thích sự ổn định và kế hoạch chi tiết, người kia lại ưa thích sự linh hoạt và tự phát. Điều này có thể dẫn đến những cuộc thảo luận thú vị về cách tổ chức thời gian, lựa chọn hoạt động giải trí, hoặc đưa ra quyết định quan trọng. Tuy nhiên, những khác biệt này không phải là rào cản mà là cơ hội để cả hai mở rộng tầm nhìn và học cách uyển chuyển trong các tình huống khác nhau.",
        
        "strengths": "Điểm mạnh lớn nhất của mối quan hệ này chính là khả năng bổ sung và hỗ trợ lẫn nhau. Khi một người mạnh về khả năng phân tích và lập kế hoạch, người kia có thể mang đến sự sáng tạo và linh hoạt. Trong những khoảnh khắc khó khăn, sự kết hợp này giúp cả hai tìm ra giải pháp tốt nhất bằng cách nhìn vấn đề từ nhiều góc độ khác nhau. Họ có thể cùng nhau xây dựng một môi trường hỗ trợ, nơi mỗi người đều cảm thấy được trân trọng và hiểu biết.",
        
        "life_benefits": "Trong cuộc sống hàng ngày, hai người có thể tạo ra một nhịp sống cân bằng và thú vị. Họ có thể chia sẻ những công việc nhà dựa trên sở thích và khả năng của mỗi người - một người có thể đảm nhận việc lập kế hoạch và quản lý tài chính, trong khi người kia có thể tập trung vào việc tạo ra không gian sống ấm cúng và sáng tạo. Khi đi chơi hoặc du lịch, họ có thể kết hợp giữa những hoạt động được lên kế hoạch kỹ lưỡng và những trải nghiệm tự phát thú vị.",
        
        "work_benefits": "Trong môi trường công việc, sự kết hợp này có thể mang lại hiệu quả cao đáng kể. Một người có thể đảm nhận vai trò lập kế hoạch chi tiết và theo dõi tiến độ, trong khi người kia có thể đóng góp những ý tưởng sáng tạo và giải pháp linh hoạt. Khi đối mặt với dự án khó khăn, họ có thể bổ sung cho nhau - một người đảm bảo chất lượng và deadline, người kia tìm kiếm những cách tiếp cận mới và đột phá.",
        
        "love_benefits": "Về mặt tình cảm, mối quan hệ này có tiềm năng phát triển sâu sắc và bền vững. Hai người có thể học cách yêu thương theo những cách khác nhau - một người thể hiện tình cảm qua những hành động cụ thể và chu đáo, trong khi người kia có thể bày tỏ qua lời nói ngọt ngào và những cử chỉ tự nhiên. Sự khác biệt này giúp cả hai hiểu được rằng tình yêu có thể được thể hiện qua nhiều hình thức khác nhau.",
        
        "advice": advice_by_tier.get(compatibility_tier, advice_by_tier["Có sự khác biệt, cần thấu hiểu nhiều hơn"]),
        
        "product_recommendations": [
            {
                "name": "Nhẫn đôi cung hoàng đạo bạc cao cấp",
                "description": f"Nhẫn đôi được thiết kế riêng cho cặp {sign1.title()} - {sign2.title()}, chế tác từ bạc 925 với biểu tượng cung hoàng đạo tinh xảo",
                "image_url": "https://i.pinimg.com/736x/ea/87/51/ea8751f3816013dfcca04c796e09e6de.jpg",
                "price": "1,500,000 - 3,200,000 VNĐ"
            },
            {
                "name": "Vòng tay đá quý phong thủy couple",
                "description": f"Vòng tay đôi với đá phong thủy phù hợp cung {sign1.title()} và {sign2.title()}, mang lại năng lượng tích cực và hạnh phúc",
                "image_url": "https://i.pinimg.com/736x/ea/87/51/ea8751f3816013dfcca04c796e09e6de.jpg",
                "price": "800,000 - 1,800,000 VNĐ"
            },
            {
                "name": "Tranh canvas cung hoàng đạo custom",
                "description": "Tranh nghệ thuật được thiết kế riêng theo hai cung hoàng đạo, in trên canvas cao cấp, trang trí phòng ngủ hoặc phòng khách",
                "image_url": "https://i.pinimg.com/736x/ea/87/51/ea8751f3816013dfcca04c796e09e6de.jpg",
                "price": "450,000 - 900,000 VNĐ"
            }
        ]
    }

def save_to_google_sheets(data):
    """Save form data and analysis to Google Sheets with improved error handling"""
    try:
        if not GOOGLE_SHEETS_ENABLED:
            print("Google Sheets is disabled - data not saved")
            return False
            
        client = get_google_sheets_client()
        if not client:
            print("Google Sheets client not available - data not saved to sheets")
            return False
            
        # Open the Google Sheet
        sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1
        
        # Extract data safely with fallbacks
        person1 = data.get('person1', {})
        person2 = data.get('person2', {})
        compatibility = data.get('compatibility_analysis') or data.get('analysis', {})
        
        # Prepare row data with safe access
        row_data = [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Timestamp
            person1.get('name', ''),
            person1.get('birthdate', '') or person1.get('birth', ''),
            person1.get('gender', ''),
            person1.get('zodiacSign', ''),
            person2.get('name', ''),
            person2.get('birthdate', '') or person2.get('birth', ''),
            person2.get('gender', ''),
            person2.get('zodiacSign', ''),
            compatibility.get('compatibility_score', 0) if isinstance(compatibility, dict) else 0,
            str(compatibility.get('compatibility_level', '')) if isinstance(compatibility, dict) else str(compatibility)[:100]
        ]
        
        # Add headers if sheet is empty
        try:
            all_records = sheet.get_all_records()
            if len(all_records) == 0:
                headers = [
                    'Thời gian', 'Tên 1', 'Ngày sinh 1', 'Giới tính 1', 'Cung hoàng đạo 1',
                    'Tên 2', 'Ngày sinh 2', 'Giới tính 2', 'Cung hoàng đạo 2',
                    'Điểm tương thích', 'Phân tích'
                ]
                sheet.insert_row(headers, 1)
        except Exception as header_error:
            print(f"Warning: Could not check/add headers: {header_error}")
        
        # Insert data
        sheet.append_row(row_data)
        print(f"Successfully saved data to Google Sheets for {person1.get('name', 'Unknown')} and {person2.get('name', 'Unknown')}")
        return True
        
    except Exception as e:
        print(f"Error saving to Google Sheets: {e}")
        return False

@app.route('/')
def index():
    """Serve the main HTML page"""
    try:
        with open('index.html', 'r', encoding='utf-8') as file:
            return file.read(), 200, {'Content-Type': 'text/html; charset=utf-8'}
    except FileNotFoundError:
        return "index.html not found", 404

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    try:
        if filename.endswith('.css'):
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read(), 200, {'Content-Type': 'text/css'}
        elif filename.endswith('.js'):
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read(), 200, {'Content-Type': 'application/javascript'}
        else:
            return "File not found", 404
    except FileNotFoundError:
        return "File not found", 404

@app.route('/api/analyze', methods=['POST'])
def analyze_compatibility():
    """Main API endpoint for compatibility analysis with improved error handling"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract person data
        person1_data = data.get('person1', {})
        person2_data = data.get('person2', {})
        
        if not person1_data or not person2_data:
            return jsonify({'error': 'Missing person data'}), 400
        
        # Get zodiac signs - handle both birthdate and birth field names
        sign1 = person1_data.get('zodiacSign') or get_zodiac_sign(person1_data.get('birthdate') or person1_data.get('birth', ''))
        sign2 = person2_data.get('zodiacSign') or get_zodiac_sign(person2_data.get('birthdate') or person2_data.get('birth', ''))
        
        # Update person data with zodiac signs
        person1_data['zodiacSign'] = sign1
        person2_data['zodiacSign'] = sign2
        
        # Get horoscope data with fallback handling
        try:
            horoscope1 = get_horoscope_data(sign1)
            horoscope2 = get_horoscope_data(sign2)
        except Exception as horoscope_error:
            print(f"Error getting horoscope data: {horoscope_error}")
            # Use fallback horoscopes
            horoscope1 = create_fallback_horoscope(sign1)
            horoscope2 = create_fallback_horoscope(sign2)
        
        # Analyze compatibility with AI
        try:
            compatibility_analysis = analyze_compatibility_with_ai(person1_data, person2_data, horoscope1, horoscope2)
        except Exception as ai_error:
            print(f"Error in AI analysis: {ai_error}")
            # Use fallback analysis
            compatibility_analysis = generate_fallback_analysis(person1_data, person2_data)
        
        # Prepare response data
        response_data = {
            'success': True,
            'person1': person1_data,
            'person2': person2_data,
            'horoscope1': horoscope1,
            'horoscope2': horoscope2,
            'compatibility_analysis': compatibility_analysis,
            'timestamp': datetime.now().isoformat()
        }
        
        # Save to Google Sheets (non-blocking)
        try:
            if GOOGLE_SHEETS_ENABLED:
                save_to_google_sheets(response_data)
        except Exception as e:
            print(f"Warning: Could not save to Google Sheets: {e}")
            # Continue without failing the request
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error in analyze endpoint: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/horoscope/<sign>')
def get_horoscope_api(sign):
    """API endpoint to get horoscope for a specific sign"""
    try:
        if sign.lower() not in ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
                               'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']:
            return jsonify({'error': 'Invalid zodiac sign'}), 400
        
        horoscope_data = get_horoscope_data(sign.lower())
        return jsonify({
            'success': True,
            'sign': sign.lower(),
            'data': horoscope_data
        })
        
    except Exception as e:
        print(f"Error in horoscope endpoint: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/test-horoscope')
def test_horoscope_system():
    """Test local horoscope system"""
    try:
        # Test with all zodiac signs
        test_signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
                     'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
        
        results = {}
        for sign in test_signs:
            horoscope_data = get_horoscope_data(sign)
            results[sign] = {
                'has_description': bool(horoscope_data.get('description')),
                'has_mood': bool(horoscope_data.get('mood')),
                'has_color': bool(horoscope_data.get('color')),
                'has_lucky_number': bool(horoscope_data.get('lucky_number')),
                'sample': horoscope_data.get('description', '')[:50] + '...'
            }
        
        return jsonify({
            'success': True,
            'system_status': 'Local horoscope system working',
            'total_signs': len(results),
            'all_working': all(r['has_description'] for r in results.values()),
            'test_results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'type': type(e).__name__
        })

@app.route('/api/test-aztro')
def test_aztro_api():
    """Deprecated: Aztro API no longer used"""
    return jsonify({
        'success': False,
        'message': 'Aztro API is no longer used. This application now uses a local horoscope system.',
        'redirect': '/api/test-horoscope'
    })

@app.route('/api/test-sheets')
def test_sheets():
    """Test Google Sheets connection"""
    try:
        client = get_google_sheets_client()
        if not client:
            return jsonify({
                'status': 'error',
                'message': 'Google Sheets credentials not found',
                'solution': 'Add google-credentials.json file to connect to Google Sheets'
            })
        
        # Try to open the sheet
        sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1
        sheet_info = {
            'title': sheet.title,
            'row_count': sheet.row_count,
            'col_count': sheet.col_count
        }
        
        return jsonify({
            'status': 'success',
            'message': 'Google Sheets connection successful!',
            'sheet_info': sheet_info,
            'sheet_url': f'https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/edit'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Google Sheets connection failed: {str(e)}',
            'sheet_id': GOOGLE_SHEET_ID
        })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/test-credentials')
def test_credentials():
    """Test endpoint để kiểm tra credentials setup"""
    return jsonify({
        "environment": os.environ.get('FLASK_ENV'),
        "has_credentials_file": os.path.exists(app.config['GOOGLE_CREDENTIALS_PATH']),
        "credentials_path": app.config['GOOGLE_CREDENTIALS_PATH'],
        "google_sheets_enabled": app.config['GOOGLE_SHEETS_ENABLED'],
        "has_sheet_id": bool(app.config.get('GOOGLE_SHEET_ID')),
        "has_gemini_key": bool(app.config.get('GEMINI_API_KEY'))
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)