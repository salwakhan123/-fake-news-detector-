from flask import Flask, render_template, request, jsonify
import os
import joblib

app = Flask(__name__)

# Load model if exists
model = None
vectorizer = None
try:
    model = joblib.load('model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    print("✅ ML Model loaded")
except:
    print("⚠️ Using rule-based detection")

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html><head><title>Fake News Detector</title>
<style>body{{font-family:Arial;text-align:center;padding:50px;background:#f0f0f0}}
h1{{color:#333;font-size:40px}}input{{width:80%;padding:20px;font-size:20px;border-radius:10px}}
button{{padding:20px 40px;font-size:20px;background:green;color:white;border:none;border-radius:10px;cursor:pointer;margin:10px}}</style></head>
<body>
<h1>🔍 Fake News Detector</h1>
<form method="POST" action="/predict">
<input name="news" placeholder="Type news headline..." required>
<button>🚀 CHECK</button>
</form>
<a href="/predict?news=₹5000 free money" style="background:red;color:white;padding:15px;text-decoration:none;border-radius:10px">💰 Fake Test</a>
<a href="/predict?news=ISRO launch satellite" style="background:#2196F3;color:white;padding:15px;text-decoration:none;border-radius:10px;margin-left:10px">🚀 Real Test</a>
</body></html>
    '''

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    news = request.form.get('news') or request.args.get('news', '')
    
    if model:
        # ML Prediction
        from preprocess import clean_text
        clean = clean_text(news)
        vec = vectorizer.transform([clean])
        pred = model.predict(vec)[0]
        result = 'FAKE ❌' if pred == 0 else 'REAL ✅'
    else:
        # Rule-based
        if any(word in news.lower() for word in ['alien', '₹', '5000', 'free', 'ufo']):
            result = 'FAKE ❌'
        else:
            result = 'REAL ✅'
    
    return f'''
<!DOCTYPE html>
<html><body style="text-align:center;padding:100px;background:#f0f0f0;font-family:Arial">
<h1 style="font-size:60px;color:{'red' if 'FAKE' in result else 'green'}">{result}</h1>
<p style="font-size:25px">News: {news}</p>
<a href="/" style="background:#007bff;color:white;padding:20px 40px;font-size:20px;text-decoration:none;border-radius:10px">← New Check</a>
</body></html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    ```

**`requirements.txt`:**
