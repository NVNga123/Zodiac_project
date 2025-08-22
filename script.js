// Zodiac sign mapping từ ngày sinh
const zodiacSigns = {
    "aries": { name: "Bạch Dương", dates: [[3, 21], [4, 19]], symbol: "♈" },
    "taurus": { name: "Kim Ngưu", dates: [[4, 20], [5, 20]], symbol: "♉" },
    "gemini": { name: "Song Tử", dates: [[5, 21], [6, 20]], symbol: "♊" },
    "cancer": { name: "Cự Giải", dates: [[6, 21], [7, 22]], symbol: "♋" },
    "leo": { name: "Sư Tử", dates: [[7, 23], [8, 22]], symbol: "♌" },
    "virgo": { name: "Xử Nữ", dates: [[8, 23], [9, 22]], symbol: "♍" },
    "libra": { name: "Thiên Bình", dates: [[9, 23], [10, 22]], symbol: "♎" },
    "scorpio": { name: "Hổ Cáp", dates: [[10, 23], [11, 21]], symbol: "♏" },
    "sagittarius": { name: "Nhân Mã", dates: [[11, 22], [12, 21]], symbol: "♐" },
    "capricorn": { name: "Ma Kết", dates: [[12, 22], [12, 31], [1, 1], [1, 19]], symbol: "♑" },
    "aquarius": { name: "Bao Bình", dates: [[1, 20], [2, 18]], symbol: "♒" },
    "pisces": { name: "Song Ngư", dates: [[2, 19], [3, 20]], symbol: "♓" }
};

// Hàm xác định cung hoàng đạo từ ngày sinh
function getZodiacSign(birthDate) {
    const date = new Date(birthDate);
    const month = date.getMonth() + 1;
    const day = date.getDate();
    
    for (const [sign, info] of Object.entries(zodiacSigns)) {
        const dates = info.dates;
        for (let i = 0; i < dates.length; i += 2) {
            const startMonth = dates[i][0];
            const startDay = dates[i][1];
            const endMonth = dates[i + 1] ? dates[i + 1][0] : dates[i][0];
            const endDay = dates[i + 1] ? dates[i + 1][1] : dates[i][1];
            
            if ((month === startMonth && day >= startDay) || 
                (month === endMonth && day <= endDay) ||
                (startMonth === 12 && endMonth === 1 && (month === 12 || month === 1))) {
                return sign;
            }
        }
    }
    return "aries"; // default
}

// Function to display results
function displayResults(data) {
    const compatibility = data.compatibility_analysis || data.analysis || data;
    
    if (!compatibility) {
        console.error('No compatibility data received:', data);
        alert('Không nhận được dữ liệu phân tích. Vui lòng thử lại!');
        return;
    }
    
    const score = compatibility.compatibility_score || 50;
    let levelClass = 'level-low';
    if (score >= 85) levelClass = 'level-perfect';
    else if (score >= 70) levelClass = 'level-high';
    else if (score >= 40) levelClass = 'level-medium';
    
    const resultContainer = document.getElementById('analysisContent');
    
    // Build detailed content according to instruction format
    let detailedContent = '';
    
    // Add zodiac description if available
    if (compatibility.zodiac_summary) {
        detailedContent += `
            <div class="zodiac-description">
                <p><em>${compatibility.zodiac_summary}</em></p>
            </div>
        `;
    }
    
    // Add personality analysis
    if (compatibility.personality_analysis) {
        detailedContent += `
            <div class="analysis-section">
                <h4>🌟 Tính cách và cung hoàng đạo của 2 người</h4>
                <div class="analysis-content">
                    ${compatibility.personality_analysis}
                </div>
            </div>
        `;
    }
    
    // Add differences analysis if available
    if (compatibility.differences) {
        detailedContent += `
            <div class="analysis-section">
                <h4>⚖️ Điểm khác biệt của 2 người</h4>
                <div class="analysis-content">
                    ${compatibility.differences}
                </div>
            </div>
        `;
    }
    
    // Add strengths analysis
    if (compatibility.strengths) {
        detailedContent += `
            <div class="analysis-section">
                <h4>💪 Điểm mạnh khi kết nối</h4>
                <div class="analysis-content">
                    ${compatibility.strengths}
                </div>
            </div>
        `;
    }
    
    // Add life areas analysis - check for different possible field names
    const hasLifeAreas = compatibility.life_benefits || compatibility.work_benefits || compatibility.love_benefits;
    if (hasLifeAreas) {
        detailedContent += `
            <div class="analysis-section">
                <h4>🌈 Lợi ích khi kết hợp</h4>
                <div class="life-areas">
        `;
        
        if (compatibility.life_benefits) {
            detailedContent += `
                <div class="life-area">
                    <h5>🏠 Đời sống</h5>
                    <p>${compatibility.life_benefits}</p>
                </div>
            `;
        }
        
        if (compatibility.work_benefits) {
            detailedContent += `
                <div class="life-area">
                    <h5>💼 Công việc</h5>
                    <p>${compatibility.work_benefits}</p>
                </div>
            `;
        }
        
        if (compatibility.love_benefits) {
            detailedContent += `
                <div class="life-area">
                    <h5>💕 Tình cảm</h5>
                    <p>${compatibility.love_benefits}</p>
                </div>
            `;
        }
        
        detailedContent += `
                </div>
            </div>
        `;
    }
    
    // Add advice if available
    if (compatibility.advice) {
        detailedContent += `
            <div class="analysis-section">
                <h4>💡 Lời khuyên</h4>
                <div class="analysis-content">
                    ${compatibility.advice}
                </div>
            </div>
        `;
    }
    
    // If no detailed content, use fallback
    if (!detailedContent) {
        detailedContent = `
            <div class="analysis-section">
                <h4>👥 Phân tích chi tiết</h4>
                <div class="analysis-content">
                    ${compatibility.personality_analysis || compatibility.description || compatibility.analysis || 'Đang phân tích...'}
                </div>
            </div>
        `;
    }
    
    // Build products section
    let productsContent = '';
    if (compatibility.product_recommendations && Array.isArray(compatibility.product_recommendations)) {
        compatibility.product_recommendations.forEach(product => {
            productsContent += `
                <div class="product-item">
                    ${product.image_url ? `<img src="${product.image_url}" alt="${product.name}" class="product-image">` : ''}
                    <div class="product-info">
                        <h4>${product.name}</h4>
                        <p class="product-description">${product.description}</p>
                        ${product.price ? `<div class="product-price">${product.price}</div>` : ''}
                        <a href="${product.shop_url || '#'}" class="product-link" target="_blank">Xem sản phẩm</a>
                    </div>
                </div>
            `;
        });
    } else {
        // Default products with demo images
        productsContent = `
            <div class="product-item">
                <img src="https://via.placeholder.com/300x200/FFB6C1/FFFFFF?text=Nhẫn+Đôi" alt="Nhẫn đôi cung hoàng đạo" class="product-image">
                <div class="product-info">
                    <h4>Nhẫn đôi cung hoàng đạo</h4>
                    <p class="product-description">Nhẫn đôi thiết kế theo cung hoàng đạo của hai bạn</p>
                    <a href="#" class="product-link">Xem sản phẩm</a>
                </div>
            </div>
            <div class="product-item">
                <img src="https://via.placeholder.com/300x200/87CEEB/FFFFFF?text=Vòng+Tay" alt="Vòng tay may mắn" class="product-image">
                <div class="product-info">
                    <h4>Vòng tay may mắn</h4>
                    <p class="product-description">Vòng tay đá quý phù hợp với cung hoàng đạo</p>
                    <a href="#" class="product-link">Xem sản phẩm</a>
                </div>
            </div>
            <div class="product-item">
                <img src="https://via.placeholder.com/300x200/F0E68C/FFFFFF?text=Dây+Chuyền" alt="Dây chuyền cặp đôi" class="product-image">
                <div class="product-info">
                    <h4>Dây chuyền cặp đôi</h4>
                    <p class="product-description">Dây chuyền symbol cung hoàng đạo của hai bạn</p>
                    <a href="#" class="product-link">Xem sản phẩm</a>
                </div>
            </div>
            <div class="product-item">
                <img src="https://via.placeholder.com/300x200/DDA0DD/FFFFFF?text=Tranh+Canvas" alt="Tranh canvas cung hoàng đạo" class="product-image">
                <div class="product-info">
                    <h4>Tranh canvas cung hoàng đạo</h4>
                    <p class="product-description">Tranh nghệ thuật về sự kết hợp của hai cung</p>
                    <a href="#" class="product-link">Xem sản phẩm</a>
                </div>
            </div>
        `;
    }
    
    resultContainer.innerHTML = `
        <div class="result-container ${levelClass}">
            <div class="compatibility-header">
                <div class="score-circle">
                    <span class="score">${score}%</span>
                </div>
                <h2 class="compatibility-title">${compatibility.compatibility_level || compatibility.title || 'Phân tích tương thích'}</h2>
            </div>
            
            <div class="personality-section">
                <h3>👥 Phân tích chi tiết</h3>
                ${detailedContent}
            </div>
            
            <div class="products-section">
                <h3>🛍️ Gợi ý sản phẩm cho cặp đôi</h3>
                <div class="products-grid">
                    ${productsContent}
                </div>
            </div>
        </div>
    `;
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('zodiacForm');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const analyzeText = document.getElementById('analyzeText');
    const loadingText = document.getElementById('loadingText');
    const resultsSection = document.getElementById('results');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading state
        analyzeBtn.disabled = true;
        analyzeText.style.display = 'none';
        loadingText.style.display = 'inline';
        
        try {
            // Collect form data
            const formData = {
                person1: {
                    name: document.getElementById('name1').value,
                    birthdate: document.getElementById('birth1').value,
                    gender: document.getElementById('gender1').value,
                    phone: document.getElementById('phone1').value,
                    email: document.getElementById('email1').value,
                    address: document.getElementById('address1').value,
                    zodiacSign: getZodiacSign(document.getElementById('birth1').value)
                },
                person2: {
                    name: document.getElementById('name2').value,
                    birthdate: document.getElementById('birth2').value,
                    gender: document.getElementById('gender2').value,
                    phone: document.getElementById('phone2').value,
                    email: document.getElementById('email2').value,
                    address: document.getElementById('address2').value,
                    zodiacSign: getZodiacSign(document.getElementById('birth2').value)
                }
            };

            // Call backend API for analysis
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            if (!result.success) {
                throw new Error(result.error || 'Analysis failed');
            }

            // Display results using backend data
            displayResults(result);

            // Show results section
            resultsSection.style.display = 'block';
            resultsSection.scrollIntoView({ behavior: 'smooth' });

        } catch (error) {
            console.error('Error during analysis:', error);
            alert('Có lỗi xảy ra trong quá trình phân tích. Vui lòng thử lại!');
        } finally {
            // Reset button state
            analyzeBtn.disabled = false;
            analyzeText.style.display = 'inline';
            loadingText.style.display = 'none';
        }
    });
});

// Share and restart functions
function shareResults() {
    if (navigator.share) {
        navigator.share({
            title: 'Kết quả phân tích cung hoàng đạo',
            text: 'Tôi vừa phân tích mức độ tương thích cung hoàng đạo. Cùng thử xem kết quả của bạn nhé!',
            url: window.location.href
        });
    } else {
        const url = window.location.href;
        navigator.clipboard.writeText(url).then(() => {
            alert('Đã copy link để chia sẻ!');
        });
    }
}

function analyzeAgain() {
    document.getElementById('results').style.display = 'none';
    document.getElementById('analysisContent').innerHTML = '';
    
    // Reset forms
    const forms = document.querySelectorAll('.person-form form');
    forms.forEach(form => form.reset());
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
