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
    <title>Smart Flashcard</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #4F46E5;
            --primary-hover: #4338CA;
            --accent: #F43F5E;
        }

        * { box-sizing: border-box; }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #0F172A;
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.35) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(236, 72, 153, 0.3) 0px, transparent 50%),
                radial-gradient(at 50% 100%, rgba(56, 189, 248, 0.25) 0px, transparent 50%);
            min-height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .card-container {
            background: rgba(255, 255, 255, 0.92);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            border-radius: 32px;
            padding: 32px 28px;
            width: 100%;
            max-width: 450px;
            box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.3);
            text-align: center;
        }

        .header-title {
            font-size: 28px;
            font-weight: 800;
            color: #0F172A;
            margin: 0 0 20px 0;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            letter-spacing: -0.5px;
        }

        select, input {
            width: 100%;
            padding: 13px 18px;
            border-radius: 16px;
            border: 1.5px solid #E2E8F0;
            font-size: 14px;
            font-family: inherit;
            font-weight: 600;
            outline: none;
            transition: all 0.2s ease;
            margin-bottom: 12px;
            background: #FFFFFF;
            color: #1E293B;
        }

        select:focus, input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.12);
        }

        /* Flashcard 3D Flip */
        .scene {
            width: 100%;
            height: 230px;
            perspective: 1000px;
            margin: 18px 0;
            cursor: pointer;
        }

        .card-flip {
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        .card-flip.is-flipped {
            transform: rotateY(180deg);
        }

        .card-face {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 24px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border: 1px solid rgba(226, 232, 240, 0.8);
            box-shadow: 0 12px 28px -6px rgba(15, 23, 42, 0.06);
        }

        .card-front {
            background: #FFFFFF;
        }

        .card-back {
            background: linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 100%);
            transform: rotateY(180deg);
            border-color: #C7D2FE;
        }

        .word-title {
            font-size: 34px;
            font-weight: 800;
            color: #0F172A;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }

        .badge-pos {
            background: #EEF2FF;
            color: var(--primary);
            font-size: 11px;
            font-weight: 800;
            padding: 5px 14px;
            border-radius: 20px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }

        .word-meaning {
            font-size: 25px;
            font-weight: 800;
            color: #10B981;
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
            font-size: 18px;
            cursor: pointer;
            margin-top: 14px;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .btn-audio:hover {
            background: #E2E8F0;
            transform: scale(1.08);
        }

        .progress-bar {
            height: 6px;
            background: #E2E8F0;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 8px;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #6366F1, #EC4899);
            width: 0%;
            transition: width 0.3s;
        }

        .controls {
            display: flex;
            gap: 12px;
            margin-top: 18px;
        }

        .btn {
            flex: 1;
            padding: 14px;
            border: none;
            border-radius: 16px;
            font-size: 15px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
            font-family: inherit;
        }

        .btn-prev { background: #F1F5F9; color: #475569; }
        .btn-prev:hover { background: #E2E8F0; }

        .btn-next {
            background: var(--primary);
            color: white;
            box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3);
        }
        .btn-next:hover {
            background: var(--primary-hover);
            transform: translateY(-1px);
        }
    </style>
</head>
<body>
    <div class="card-container">
        <h1 class="header-title">⚡ Smart Flashcard</h1>

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
        <p style="font-size: 11px; color: #64748B; margin-top: -6px; font-weight: 600;">✨ Bấm vào thẻ để xoay lật mặt sau</p>

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