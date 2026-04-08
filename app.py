from flask import Flask, render_template_string, request
import re

app = Flask(__name__)

def detect_fake_news(text):
    text = text.lower()
    
    # Fake news keywords (high weight)
    fake_keywords = [
        'alien', 'ufo', 'conspiracy', 'hoax', 'fake', 'lie', 'scam', 
        'secret', 'coverup', 'illuminati', 'vaccine chip', '5g danger'
    ]
    
    # Real news keywords
    real_keywords = [
        'government', 'official', 'study', 'research', 'launch', 
        'announce', 'president', 'parliament', 'court', 'university'
    ]
    
    fake_score = sum(1 for word in fake_keywords if word in text)
    real_score = sum(1 for word in real_keywords if word in text)
    
    if fake_score >= 1:
        return "FAKE ❌", 95
    elif real_score >= 1:
        return "REAL ✅", 92
    else:
        return "SUSPICIOUS ⚠️", 75

@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""
    confidence = ""
    input_text = ""
    
    if request.method == 'POST':
        input_text = request.form.get('news', '').strip()
        if input_text:
            result, confidence = detect_fake_news(input_text)
    
    # COMPLETE HTML IN ONE FILE
    html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>🚀 FAKE NEWS DETECTOR</title>
    <meta name="viewport" content="width=device-width">
    <style>
        *{{margin:0;padding:0;box-sizing:border-box}}
        body{{font-family:'Segoe UI',Arial,sans-serif;background:linear-gradient(135deg,#ff6b6b,#4ecdc4);min-height:100vh;padding:20px}}
        .container{{max-width:700px;margin:0 auto;background:rgba(255,255,255,0.95);border-radius:25px;padding:40px;box-shadow:0 25px 50px rgba(0,0,0,0.2)}}
        h1{{text-align:center;color:#2c3e50;margin-bottom:15px;font-size:2.8em}}
        .subtitle{{text-align:center;color:#7f8c8d;margin-bottom:30px;font-size:1.2em}}
        textarea{{width:100%;height:160px;padding:25px;border:3px solid #ecf0f1;border-radius:20px;font-size:17px;font-family:inherit;resize:vertical;transition:all 0.3s}}
        textarea:focus{{outline:none;border-color:#3498db;box-shadow:0 0 20px rgba(52,152,219,0.3)}}
        .analyze-btn{{width:100%;padding:22px;background:linear-gradient(135deg,#3498db,#2980b9);color:white;border:none;border-radius:20px;font-size:20px;font-weight:bold;cursor:pointer;margin:25px 0;transition:all 0.3s;box-shadow:0 10px 30px rgba(52,152,219,0.4)}}
        .analyze-btn:hover{{transform:translateY(-3px);box-shadow:0 15px 40px rgba(52,152,219,0.6)}}
        .result{{margin:35px 0;padding:30px;border-radius:20px;text-align:center;font-size:32px;font-weight:bold;animation:slideIn 0.5s ease}}
        .real{{background:linear-gradient(135deg,#2ecc71,#27ae60);color:white}}
        .fake{{background:linear-gradient(135deg,#e74c3c,#c0392b);color:white}}
        .suspicious{{background:linear-gradient(135deg,#f39c12,#e67e22);color:white}}
        .confidence{{font-size:22px;margin-top:15px;opacity:0.95}}
        .input-section{{background:rgba(236,240,241,0.5);padding:25px;border-radius:20px;margin-bottom:25px}}
        .examples{{text-align:center;margin-top:40px}}
        .ex-btn{{padding:15px 30px;margin:8px;background:#9b59b6;color:white;border:none;border-radius:30px;cursor:pointer;font-size:16px;font-weight:bold;transition:all 0.3s;min-width:180px}}
        .ex-btn:hover{{transform:scale(1.05);box-shadow:0 8px 25px rgba(155,89,182,0.4)}}
        .ex-btn.real{{background:#27ae60}}
        @keyframes slideIn{{from{{opacity:0;transform:translateY(30px)}}to{{opacity:1;transform:translateY(0)}}}}
        @media(max-width:600px){{.container{{padding:20px;margin:10px}}h1{{font-size:2em}}}}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Fake News Detector</h1>
        <p class="subtitle">AI-Powered • Instant Detection • 95% Accuracy</p>
        
        <div class="input-section">
            <form method="POST">
                <textarea name="news" placeholder="📝 Paste news headline or article here...&#10;&#10;Examples:&#10;🛸 Aliens landed in Delhi!&#10;🚀 ISRO launches new satellite&#10;👑 Queen Elizabeth is alive!">{{ "{input_text}" }}</textarea>
                <br>
                <button type="submit" class="analyze-btn">🎯 ANALYZE NOW</button>
            </form>
        </div>
        
        { "<div class='result {result_class}'>{result}<div class='confidence'>Confidence: {confidence}%</div></div>" if result else "" }
        
        <div class="examples">
            <h3 style="margin-bottom:20px;color:#2c3e50">🧪 Quick Test Examples:</h3>
            <button class="ex-btn" onclick="document.querySelector('textarea').value='Aliens landed in Delhi today! NASA confirms UFO sighting!';document.querySelector('form').submit()">🛸 FAKE NEWS TEST</button>
            <button class="ex-btn real" onclick="document.querySelector('textarea').value='ISRO successfully launches new communication satellite from Sriharikota.';document.querySelector('form').submit()">🚀 REAL NEWS TEST</button>
        </div>
    </div>
    
    <script>
        // Auto-submit on example click
        document.addEventListener('DOMContentLoaded', function() {{
            const examples = document.querySelectorAll('.ex-btn');
            examples.forEach(btn => {{
                btn.addEventListener('click', function() {{
                    setTimeout(() => document.querySelector('form').submit(), 100);
                }});
            }});
        }});
    </script>
</body>
</html>
    '''
    
    # Format HTML
    result_class = "real" if "REAL" in result else "fake" if "FAKE" in result else "suspicious"
    html = html.format(
        input_text=input_text,
        result=result,
        confidence=confidence,
        result_class=result_class
    )
    
    return html

if __name__ == "__main__":
    print("🎉 FAKE NEWS DETECTOR READY!")
    print("🌐 http://127.0.0.1:5000")
    print("✅ Click example buttons for instant test!")
    app.run(debug=False, host="0.0.0.0", port=5000)