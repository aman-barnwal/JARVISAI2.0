# 🧠 Hyper JARVISAI

**Hyper JARVISAI** is an intelligent multi-functional AI assistant built using **Flask**, designed to perform a variety of real-world tasks — all from a single web interface.  

It combines the power of **Wikipedia, YouTube, Google Search, QR Generation, Math Engine, Stock Updates, and Daily News APIs** to create a futuristic experience inspired by J.A.R.V.I.S from Iron Man.

---

## 🚀 Features

- 🔍 **Smart Google Search** — Fetches top Google results instantly.  
- 🎬 **YouTube Integration** — Displays top videos based on your query.  
- 📚 **Free E-Book Finder** — Search and access free educational resources.  
- ➗ **Mathematics Engine** — Solves differentiation and integration queries.  
- 💹 **Live Stock Updates** — Get real-time data of companies and prices.  
- 🗞️ **Daily News Fetcher** — Displays latest trending headlines.  
- 🧾 **Task Manager** — Keep track of quick tasks and ideas.  
- 🔗 **QR Generator** — Generates scannable QR codes for any link or text.  

---

## 🖥️ Tech Stack

- **Frontend:** HTML5, CSS3, Jinja2  
- **Backend:** Python (Flask)  
- **Libraries Used:**
  - `wikipedia`
  - `sympy`
  - `pytube`
  - `requests`
  - `yfinance`
  - `qrcode`
  - `newsapi-python`

---

## 💡 Example Queries

You can ask JARVISAI in plain English, for example:

| Category | Example Query |
|-----------|----------------|
| 🔍 Google | `Google AI in 2025` |
| 🎬 YouTube | `YouTube tutorials for Python` |
| ➗ Math | `Differentiate x^3 + 2x` |
| 💹 Stocks | `Stock price of Tesla` |
| 🗞️ News | `Show me daily news of India` |
| 📚 E-Books | `Free e-books for Machine Learning` |
| 🔗 QR | `Generate QR for https://github.com` |

---

## 🧠 How It Works

1. The user enters a query on the web interface.  
2. Flask routes it to a specific function (Wikipedia / YouTube / Math / Stock / QR / etc.).  
3. The backend processes and returns structured results dynamically.  

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR-USERNAME/HyperJarvisAI.git
cd HyperJarvisAI

