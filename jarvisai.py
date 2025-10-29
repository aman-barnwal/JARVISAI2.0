from flask import Flask, render_template, request, jsonify
import wikipedia
import sympy as sp
import qrcode
import io
import base64
import requests
from pytube import Search

app = Flask(__name__)

# --- Helper Functions ---

def search_youtube(query):
    try:
        s = Search(query)
        results = [f"https://www.youtube.com/watch?v={v.video_id}" for v in s.results[:5]]
        return results if results else ["No YouTube results found."]
    except Exception as e:
        return [f"Error: {str(e)}"]

def solve_math(expression):
    try:
        x = sp.Symbol('x')
        result = sp.sympify(expression)
        return str(sp.simplify(result))
    except Exception as e:
        return f"Error solving math: {str(e)}"

def search_books(query):
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
        data = requests.get(url).json()
        books = []
        for item in data.get("items", [])[:5]:
            info = item.get("volumeInfo", {})
            title = info.get("title", "Unknown Title")
            link = info.get("infoLink", "#")
            books.append(f"{title} - {link}")
        return books if books else ["No books found."]
    except Exception as e:
        return [f"Error fetching books: {str(e)}"]

def generate_qr(url):
    try:
        qr = qrcode.make(url)
        buf = io.BytesIO()
        qr.save(buf, format='PNG')
        qr_str = base64.b64encode(buf.getvalue()).decode('utf-8')
        return qr_str
    except Exception as e:
        return None

def fetch_stock(query):
    try:
        company = query.replace("stock", "").strip()
        info = wikipedia.summary(company, sentences=2)
        return [info]
    except Exception:
        return [f"No stock data found for '{query}'. Try 'Tesla stock price'."]

def fetch_news(query):
    try:
        url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey=YOUR_NEWS_API_KEY"
        data = requests.get(url).json()
        articles = [f"{a['title']} - {a['url']}" for a in data.get('articles', [])[:5]]
        return articles if articles else ["No news found."]
    except Exception as e:
        return [f"Error fetching news: {str(e)}"]


# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    query = request.form['query'].lower().strip()
    results = []

    if query.startswith("youtube"):
        results = search_youtube(query.replace("youtube", "").strip())

    elif query.startswith("math") or query.startswith("integrate") or query.startswith("differentiate"):
        expr = query.replace("math", "").replace("integrate", "").replace("differentiate", "").strip()
        results = [solve_math(expr)]

    elif query.startswith("book") or query.startswith("get me books") or query.startswith("free books"):
        results = search_books(query.replace("book", "").replace("get me books", "").strip())

    elif query.startswith("generate qr for"):
        url = query.replace("generate qr for", "").strip()
        qr_img = generate_qr(url)
        if qr_img:
            results = [f"<img src='data:image/png;base64,{qr_img}' alt='QR Code' width='200'>"]
        else:
            results = ["Failed to generate QR code."]

    elif query.startswith("stock"):
        results = fetch_stock(query)

    elif query.startswith("news") or query.startswith("update news") or query.startswith("latest news"):
        results = fetch_news(query.replace("news", "").strip())

    else:
        try:
            summary = wikipedia.summary(query, sentences=3)
            results = [summary]
        except Exception:
            results = ["No relevant information found. Try rephrasing your query."]

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)

