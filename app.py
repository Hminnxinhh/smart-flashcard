import json
import os
from flask import Flask, render_template_string

app = Flask(__name__)
DATA_FILE = "flashcards_data.json"


def load_data():
  if os.path.exists(DATA_FILE):
    try:
      with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    except Exception:
      pass
  return {}


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Flashcard - GenZ IELTS Pro 🚀</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366F1;
            --primary-hover: #4F46E5;
            --accent: #EC4899;
            --bg-gradient: linear-gradient(135deg, #0EA5E9 0%, #6366F1 50%, #A855F7 100%);
        }

        * { box-sizing: border-box; }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: var(--bg-gradient);
            min-height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 16px;
        }

        .card-container {
            background: rgba(255, 255, 255, 0.96);
            backdrop-filter: blur(16px);
            border-radius: 28px;
            padding: 28px 24px;
            width: 100%;
            max-width: 440px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            text-align: center;
        }

        .header-title {
            font-size: 26px;
            font-weight: 800;
            background: linear-gradient(90deg, #6366F1, #EC4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0 0 4px 0;
        }

        .header-sub {
            font-size: 13px;
            color: #64748B;
            font-weight: 700;
            margin-bottom: 20px;
        }

        select, input {
            width: 100%;
            padding: 12px 16px;
            border-radius: 14px;
            border: 2px solid #E2E8F0;
            font-size: 14px;
            font-family: inherit;
            font-weight: 700;
            outline: none;
            transition: all 0.2s;
            margin-bottom: 12px;
            background: #F8FAFC;
        }

        select:focus, input:focus {
            border-color: var(--primary);
            background: #FFF;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15);
        }

        /* Flashcard 3D Flip */
        .scene {
            width: 100%;
            height: 220px;
            perspective: 1000px;
            margin: 16px 0;
            cursor: pointer;
        }

        .card-flip {
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1);
        }

        .card-flip.is-flipped {
            transform: rotateY(180deg);
        }

        .card-face {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 20px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border: 2px solid #EEF2FF;
            box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.1);
        }

        .card-front {
            background: #FFFFFF;
        }

        .card-back {
            background: linear-gradient(135deg, #EEF2FF 0%, #F5F3FF 100%);
            transform: rotateY(180deg);
            border-color: #C7D2FE;
        }

        .word-title {
            font-size: 32px;
            font-weight: 800;
            color: #0F172A;
            margin-bottom: 6px;
        }

        .badge-pos {
            background: #EEF2FF;
            color: #4F46E5;
            font-size: 11px;
            font-weight: 800;
            padding: 4px 12px;
            border-radius: 20px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .word-meaning {
            font-size: 24px;
            font-weight: 800;
            color: #059669;
            margin-bottom: 8px;
        }

        .word-example {
            font-size: 13px;
            color: #475569;
            font-style: italic;
            line-height: 1.4;
        }

        .btn-audio {
            background: #F1F5F9;
            border: none;
            border-radius: 50%;
            width: 44px;
            height: 44px;
            font-size: 20px;
            cursor: pointer;
            margin-top: 12px;
            transition: all 0.2s;
        }

        .btn-audio:hover {
            background: #E2E8F0;
            transform: scale(1.1);
        }

        .progress-bar {
            height: 8px;
            background: #F1F5F9;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 8px;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #EC4899, #8B5CF6);
            width: 0%;
            transition: width 0.3s;
        }

        .controls {
            display: flex;
            gap: 12px;
            margin-top: 16px;
        }

        .btn {
            flex: 1;
            padding: 14px;
            border: none;
            border-radius: 14px;
            font-size: 15px;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.2s;
            font-family: inherit;
        }

        .btn-prev { background: #F1F5F9; color: #334155; }
        .btn-prev:hover { background: #E2E8F0; }

        .btn-next {
            background: var(--primary);
            color: white;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
        }
        .btn-next:hover {
            background: var(--primary-hover);
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="card-container">
        <h1 class="header-title">⚡ Smart Flashcard</h1>
        <div class="header-sub">IELTS Band 2.5 ➔ 6.5 GenZ Edition 🔥</div>

        <select id="categorySelect" onchange="changeCategory()">
            {% for cat in categories %}
            <option value="{{ cat }}">{{ cat }}</option>
            {% endfor %}
        </select>

        <input type="text" id="searchInput" placeholder="🔍 Tìm nhanh từ vựng..." onkeyup="filterCards()">

        <div class="progress-bar">
            <div class="progress-fill" id="progressFill"></div>
        </div>
        <div id="cardCounter" style="font-size: 12px; font-weight: 700; color: #64748B;">Thẻ 1 / 1</div>

        <!-- Khung 3D Flip -->
        <div class="scene" onclick="flipCard()">
            <div class="card-flip" id="cardFlip">
                <div class="card-face card-front">
                    <div class="word-title" id="wordFront">Loading...</div>
                    <span class="badge-pos" id="wordPos">verb</span>
                    <button class="btn-audio" onclick="event.stopPropagation(); speakWord()">🔊</button>
                </div>
                <div class="card-face card-back">
                    <div class="word-meaning" id="wordBack">Nghĩa tiếng Việt</div>
                    <div class="word-example" id="wordExample">Ví dụ...</div>
                </div>
            </div>
        </div>
        <p style="font-size: 11px; color: #94A3B8; margin-top: -6px;">✨ Bấm vào thẻ để xoay lật mặt sau</p>

        <div class="controls">
            <button class="btn btn-prev" onclick="prevCard()">⬅️ Trước</button>
            <button class="btn btn-next" onclick="nextCard()">Tiếp theo 🚀</button>
        </div>
    </div>

    <script>
        const allData = {{ data | tojson }};
        let currentCategory = Object.keys(allData)[0] || "";
        let currentCards = [];
        let currentIndex = 0;

        function loadCategoryCards() {
            const searchVal = document.getElementById("searchInput").value.toLowerCase().trim();
            let original = allData[currentCategory] || [];
            if (searchVal) {
                currentCards = original.filter(c => c.front.toLowerCase().includes(searchVal) || c.back.toLowerCase().includes(searchVal));
            } else {
                currentCards = original;
            }
            currentIndex = 0;
            renderCard();
        }

        function renderCard() {
            const cardFlip = document.getElementById("cardFlip");
            cardFlip.classList.remove("is-flipped");

            if (currentCards.length === 0) {
                document.getElementById("wordFront").innerText = "Không tìm thấy!";
                document.getElementById("wordPos").innerText = "N/A";
                document.getElementById("wordBack").innerText = "Hãy nhập từ khác";
                document.getElementById("wordExample").innerText = "";
                document.getElementById("cardCounter").innerText = "0 / 0";
                document.getElementById("progressFill").style.width = "0%";
                return;
            }

            const card = currentCards[currentIndex];
            document.getElementById("wordFront").innerText = card.front;
            document.getElementById("wordPos").innerText = card.pos || "vocab";
            document.getElementById("wordBack").innerText = card.back;
            document.getElementById("wordExample").innerText = card.example ? `"${card.example}"` : "";

            const progress = ((currentIndex + 1) / currentCards.length) * 100;
            document.getElementById("progressFill").style.width = progress + "%";
            document.getElementById("cardCounter").innerText = `Thẻ ${currentIndex + 1} / ${currentCards.length}`;
        }

        function flipCard() {
            if (currentCards.length === 0) return;
            document.getElementById("cardFlip").classList.toggle("is-flipped");
        }

        function nextCard() {
            if (currentCards.length === 0) return;
            currentIndex = (currentIndex + 1) % currentCards.length;
            renderCard();
        }

        function prevCard() {
            if (currentCards.length === 0) return;
            currentIndex = (currentIndex - 1 + currentCards.length) % currentCards.length;
            renderCard();
        }

        function changeCategory() {
            currentCategory = document.getElementById("categorySelect").value;
            loadCategoryCards();
        }

        function filterCards() {
            loadCategoryCards();
        }

        function speakWord() {
            if (currentCards.length === 0) return;
            const word = currentCards[currentIndex].front;
            const utterance = new SpeechSynthesisUtterance(word);
            utterance.lang = 'en-US';
            window.speechSynthesis.speak(utterance);
        }

        loadCategoryCards();
    </script>
</body>
</html>
"""


@app.route("/")
def index():
  data = load_data()
  categories = list(data.keys())
  return render_template_string(
      HTML_TEMPLATE, data=data, categories=categories
  )


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)