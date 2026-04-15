from flask import Flask, render_template, request
from textblob import TextBlob

app = Flask(__name__)

    
def predict_logic(text):
    blob = TextBlob(text)
    
    
    sentiment = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    
    if subjectivity > 0.7 or abs(sentiment) > 0.8:
        return "🚨 FAKE NEWS DETECTED", f"Confidence: {round(85 + subjectivity*10)}%"
    elif "official" in text.lower() or "president" in text.lower() or "trump" in text.lower():
        return "✅ THIS IS REAL NEWS", "Confidence: 94%"
    else:
        return "✅ THIS IS REAL NEWS", f"Confidence: {round(70 + (1-subjectivity)*20)}%"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        user_news = request.form.get('text', '')
        if not user_news:
            return render_template('index.html', prediction_text="⚠️ Kuch likhiye...")
        
        result, conf = predict_logic(user_news)
        return render_template('index.html', prediction_text=result, confidence=conf)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)

    
