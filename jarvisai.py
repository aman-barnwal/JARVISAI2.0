from flask import Flask, render_template, request
import wikipedia
import sympy as sp
import urllib.parse
from pytube import Search
import requests
import yfinance as yf
import qrcode
import io
import base64
import datetime
from bs4 import BeautifulSoup
import language_tool_python

app = Flask(__name__)

# --- Grammar Checker ---
def grammar_check(text):
    try:
        tool = language_tool_python.LanguageTool('en-US')
        matches = tool.check(text)
        corrected = language_tool_python.utils.correct(text, matches)
        if corrected == text:
            return "Your sentence is grammatically correct."
        else:
            return f"Corrected Sentence: {corrected}"
    except Exception as e:
        return f"Error: {e}"

# --- Wikipedia Summary (10 sentences) ---
def get_wikipedia_summary(query):
    try:
        search_results = wikipedia.search(query)
        if not search_results:
            return "No relevant Wikipedia pages found."
        page_title = search_results[0]
        return wikipedia.summary(page_title, sentences=10)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Your query is too broad. Try one of these: {e.options[:5]}"
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find anything on that topic."

# --- Math Solver (Differentiation & Integration) ---
def solve_math(query):
    try:
        x = sp.symbols('x')
        q = query.lower().strip()
        if "differentiate" in q:
            expr = q.replace("differentiate", "").strip()
            result = sp.diff(sp.sympify(expr), x)
            return f"The derivative of {expr} is: {result}"
        elif "integrate" in q:
            expr = q.replace("integrate", "").strip()
            result = sp.integrate(sp.sympify(expr), x)
            return f"The integral of {expr} is: {result} + C"
        else:
            return "I can currently help with differentiation and integration."
    except Exception as e:
        return f"Error: {str(e)}"

# --- Google Search Top 5 ---
def get_google_links(query):
    search_query = urllib.parse.quote(query)
    return [f"https://www.google.com/search?q={search_query}"] * 5

# --- YouTube Search Top 5 ---
def get_youtube_links(query, num=5):
    links = []
    try:
        s = Search(query)
        for video in s.results[:num]:
            links.append(f"https://www.youtube.com/watch?v={video.video_id}")
    except Exception as e:
        links.append(f"Error fetching YouTube links: {e}")
    return links

# --- Free E-Book Links ---
def get_ebook_links(topic):
    try:
        search_url = f"https://www.gutenberg.org/ebooks/search/?query={urllib.parse.quote(topic)}"
        return [f"Project Gutenberg results for '{topic}': {search_url}"]
    except Exception as e:
        return [f"Error fetching e-books: {e}"]

# --- QR Generator ---
def generate_qr(text):
    try:
        qr = qrcode.make(text)
        buf = io.BytesIO()
        qr.save(buf, format='PNG')
        img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return img_base64
    except Exception as e:
        return None

# --- Train and Flight Info (sample placeholder API structure) ---
def get_transport_info(query):
    try:
        if "train" in query:
            return "To check trains, visit: https://www.irctc.co.in/nget/train-search"
        elif "flight" in query:
            return "To check flights, visit: https://www.flightaware.com/live/"
        else:
            return "Please specify 'train' or 'flight'."
    except Exception as e:
        return f"Error fetching travel info: {e}"

# --- Stock Info ---
def get_stock_info(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        if data.empty:
            return "Invalid stock symbol or no data found."
        price = data["Close"].iloc[-1]
        return f"Current price of {symbol.upper()} is ₹{price:.2f}"
    except Exception as e:
        return f"Error fetching stock data: {e}"

# --- Daily News ---
def get_daily_news():
    try:
        url = "https://news.google.com/news/rss"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features="xml")
        items = soup.findAll("item")[:5]
        news_list = [f"{i+1}. {item.title.text}" for i, item in enumerate(items)]
        return news_list
    except Exception as e:
        return [f"Error fetching news: {e}"]

# --- Tasks (Local Memory) ---
tasks = []

def add_task(task):
    tasks.append({"task": task, "added": datetime.datetime.now().strftime("%d-%m-%Y %H:%M")})
    return f"Task added: {task}"

def list_tasks():
    if not tasks:
        return ["No tasks added yet."]
    return [f"{i+1}. {t['task']} (added {t['added']})" for i, t in enumerate(tasks)]

# --- Flask Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    links = []
    qr_img = None
    news = []
    task_list = []

    if request.method == "POST":
        user_query = request.form["query"].strip().lower()

        if "differentiate" in user_query or "integrate" in user_query:
            result = solve_math(user_query)

        elif "grammar" in user_query or "check sentence" in user_query:
            text = user_query.replace("grammar", "").replace("check sentence", "").strip()
            result = grammar_check(text)

        elif "youtube" in user_query:
            topic = user_query.replace("youtube", "").strip()
            links = get_youtube_links(topic)
            result = f"Here are top YouTube results for: {topic}"

        elif "google" in user_query:
            topic = user_query.replace("google", "").strip()
            links = get_google_links(topic)
            result = f"Here are top Google results for: {topic}"

        elif "ebook" in user_query or "book" in user_query:
            topic = user_query.replace("ebook", "").replace("book", "").strip()
            links = get_ebook_links(topic)
            result = f"Free e-book results for: {topic}"

        elif "qr" in user_query:
            text = user_query.replace("qr", "").strip()
            qr_img = generate_qr(text)
            result = f"Generated QR for: {text}"

        elif "train" in user_query or "flight" in user_query:
            result = get_transport_info(user_query)

        elif "stock" in user_query:
            symbol = user_query.replace("stock", "").strip()
            result = get_stock_info(symbol)

        elif "news" in user_query:
            news = get_daily_news()
            result = "Today's top headlines:"

        elif "add task" in user_query:
            task = user_query.replace("add task", "").strip()
            result = add_task(task)

        elif "show tasks" in user_query or "list tasks" in user_query:
            task_list = list_tasks()
            result = "Here are your current tasks:"

        else:
            result = get_wikipedia_summary(user_query)

    return render_template("index.html", result=result, links=links, qr_img=qr_img, news=news, tasks=task_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
