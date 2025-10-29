from flask import Flask, render_template, request
import wikipedia, sympy as sp, urllib.parse, qrcode, os, io, yfinance as yf, language_tool_python, requests
from pytube import Search
from datetime import datetime
from newsapi import NewsApiClient
from flask import send_file

app = Flask(__name__)

# Initialize tools
tool = language_tool_python.LanguageTool('en-US')
newsapi = NewsApiClient(api_key='YOUR_NEWS_API_KEY')  # ← replace with your NewsAPI key

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    user_input = request.form['query'].strip()
    query = user_input.lower()
    
    # --- Natural Language Command Detection ---
    try:
        # YouTube Search
        if "youtube" in query or "video" in query:
            topic = user_input.replace("give me links for", "").replace("on youtube", "").strip()
            results = Search(topic).results
            links = [f"https://www.youtube.com/watch?v={r.video_id}" for r in results[:5]]
            return render_template('index.html', result="<br>".join(links))

        # Wikipedia Summary
        elif "who is" in query or "what is" in query or "tell me about" in query:
            topic = user_input.replace("who is", "").replace("what is", "").replace("tell me about", "").strip()
            return render_template('index.html', result=wikipedia.summary(topic, sentences=5))

        # Grammar Check
        elif "check" in query and "grammar" in query or "check" in query:
            text = user_input.replace("check", "").strip()
            matches = tool.check(text)
            corrected = language_tool_python.utils.correct(text, matches)
            return render_template('index.html', result=f"✅ Corrected: {corrected}")

        # QR Code
        elif "generate a qr" in query or "qr for" in query:
            text = user_input.replace("generate a qr for", "").replace("qr for", "").strip()
            img = qrcode.make(text)
            buf = io.BytesIO()
            img.save(buf, 'PNG')
            buf.seek(0)
            return send_file(buf, mimetype='image/png')

        # Math Integration / Differentiation
        elif "integrate" in query or "differentiate" in query:
            expr = query.replace("integrate", "").replace("differentiate", "").strip()
            x = sp.symbols('x')
            expression = sp.sympify(expr)
            result = sp.integrate(expression, x) if "integrate" in query else sp.diff(expression, x)
            return render_template('index.html', result=f"Result: {result}")

        # Stock Data
        elif "data for" in query or "stock" in query:
            stock_name = user_input.replace("data for", "").replace("stock", "").strip()
            stock = yf.Ticker(stock_name)
            data = stock.history(period="5d")
            return render_template('index.html', result=data.tail(5).to_html())

        # Train Number
        elif "train number" in query:
            num = ''.join(filter(str.isdigit, query))
            return render_template('index.html', result=f"🚆 Train {num}: Feature coming soon!")

        # Flight Number
        elif "flight number" in query:
            num = ''.join(filter(str.isdigit, query))
            return render_template('index.html', result=f"✈️ Flight {num}: Feature coming soon!")

        # News
        elif "news" in query or "update news" in query:
            country = "in" if "india" in query else "us"
            top_headlines = newsapi.get_top_headlines(country=country)
            headlines = [article['title'] for article in top_headlines['articles'][:5]]
            return render_template('index.html', result="<br>".join(headlines))

        # Task Suggestions
        elif "recommend me tasks" in query or "tasks for today" in query:
            tasks = [
                "🧠 Study one new C programming concept",
                "💻 Push one GitHub commit",
                "📚 Read 10 pages of a finance book",
                "🧘 Meditate for 10 minutes",
                "🚀 Work 30 minutes on Legend Pyramids idea"
            ]
            return render_template('index.html', result="<br>".join(tasks))

        else:
            return render_template('index.html', result="❌ Sorry, I didn’t understand that command yet.")
    
    except Exception as e:
        return render_template('index.html', result=f"⚠️ Error: {e}")

if __name__ == "__main__":
    app.run(debug=True)

