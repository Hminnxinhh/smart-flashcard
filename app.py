import json
import os
from flask import Flask, render_template_string, request

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
    <title>Smart Flashcard - IELTS GenZ Edition 🚀</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #6EE7B7 0%, #3B82F6 50%, #9333EA 100%);
            --card-bg: rgba(255, 255, 255, 0.95);
            --primary-color: #4F46E5;
            --accent-color: #EC4899;
        }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: var(--bg-gradient);
            min-height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            box-sizing: border-box;
        }

        .container {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 32px;
            width: 100%;
            max-width: 480px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            text-align: center;
        }

        .logo { font-size: 28px; font-weight: 800; color: #1E293B; margin-bottom: 4px; }
        .tagline { font-size: 14px; color: #64748B; margin-bottom: 24px; font-weight: 600; }

        select, input {
            width: 100%;
            padding: 12px 16px;
            border-radius: 12px;
            border: 2px solid #E2E8F0;
            font-size: 14px;
            font-family: inherit;
            font-weight: 600;
            margin-bottom: 16px;
            box-sizing: border-box;
            outline: none;
            transition: all 0.2s;
        }

        select:focus, input:focus { border-color: var(--primary-color); }

        /* Style Flashcard */
        .card-wrapper {
            perspective: 1000px;
            margin: 20px 0;
        }

        .flashcard {
            background: #FFFFFF;
            border-radius: 20px;
            padding: 30px 20px;
            min-height: 180px;
            border: 3px solid #F1F5F9;
            box-shadow: 0 10px 25px rgba(79, 70, 229, 0.08);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            position: relative;
        }

        .flashcard:hover {
            transform: translateY(-4px);
            box-shadow: 0 15px 30px rgba(79, 70, 229, 0.15);
        }

        .word-front { font-size: 32px; font-weight: 800; color: #0F172A; }
        .word-pos { font-size: 12px; font-weight: 700; color: #6366F1; text-transform: uppercase; background: #EEF2FF; padding: 4px 10px; border-radius: 20px; margin-top: 8px; }
        .word-back { font-size: 26px; font-weight: 700; color: #059669; margin-top: 8px; }
        .word-example { font-size: 13px; color: #475569; font-style: italic; margin-top: 12px; line-height: 1.4; }

        .audio-btn {
            background: #F3F4F6;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            font-size: 18px;
            cursor: pointer;
            margin-top: 10px;
            transition: background 0.2s;
        }
        .audio-btn:hover { background: #E5E7EB; }

        .btn-group { display: flex; gap: 12px; margin-top: 20px; }
        
        .btn {
            flex: 1;
            padding: 14px;
            border: none;
            border-radius: 14px;
            font-size: 15px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
            font-family: inherit;
        }

        .btn-primary { background: var(--primary-color); color: white; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3); }
        .btn-primary:hover { opacity: 0.9; transform: scale(1.02); }

        .btn-secondary { background: #F1F5F9; color: #334155; }
        .btn-secondary:hover { background: #E2E8F0; }

        .progress-bar {
            height: 8px;
            background: #E2E8F0;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 12px;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #EC4899, #8B5CF6);
            width: 0%;
            transition: width 0.3s;
        }

        .hidden { display: none !important; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">⚡ Smart Flashcard</div>
        <div class="tagline">Bứt phá IELTS Band từ 2.5 ➔ 6.5 🔥</div>

        <!-- Chọn danh mục -->
        <select id="categorySelect" onchange="changeCategory()">
            {% for cat in categories %}
            <option value="{{ cat }}">{{ cat }}</option>
            {% endfor %}
        </select>

        <!-- Thanh tìm kiếm -->
        <input type="text" id="searchInput" placeholder="🔍 Tìm kiếm từ vựng nhanh..." onkeyup="filterCards()">

        <!-- Tiến trình -->
        <div class="progress-bar">
            <div class="progress-fill" id="progressFill"></div>
        </div>
        <div id="cardCounter" style="font-size: 12px; font-weight: 700; color: #64748B;">Thẻ 1 / 1</div>

        <!-- Khung Flashcard -->
        <div class="card-wrapper">
            <div class="flashcard" onclick="flipCard()">
                <div id="cardFront">
                    <div class="word-front" id="wordFront">Loading...</div>
                    <span class="word-pos" id="wordPos">verb</span>
                    <div>
                        <button class="audio-btn" onclick="event.stopPropagation(); speakWord()">🔊</button>
                    </div>
                </div>
                <div id="cardBack" class="hidden">
                    <div class="word-back" id="wordBack">Nghĩa tiếng Việt</div>
                    <div class="word-example" id="wordExample">Ví dụ...</div>
                </div>
            </div>
        </div>
        <p style="font-size: 12px; color: #94A3B8; margin-top: -10px;">(Chạm vào thẻ để lật xem nghĩa ✨)</p>

        <!-- Điều hướng -->
        <div class="btn-group">
            <button class="btn btn-secondary" onclick="prevCard()">⬅️ Trước</button>
            <button class="btn btn-primary" onclick="nextCard()">Tiếp theo 🚀</button>
        </div>
    </div>

    <script>
        const allData = {{ data | tojson }};
        let currentCategory = Object.keys(allData)[0] || "";
        let currentCards = [];
        let currentIndex = 0;
        let isFront = true;

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
            if (currentCards.length === 0) {
                document.getElementById("wordFront").innerText = "Không tìm thấy từ!";
                document.getElementById("wordPos").innerText = "N/A";
                document.getElementById("wordBack").innerText = "Vui lòng nhập từ khác";
                document.getElementById("wordExample").innerText = "";
                document.getElementById("cardCounter").innerText = "0 / 0";
                document.getElementById("progressFill").style.width = "0%";
                return;
            }

            const card = currentCards[currentIndex];
            document.getElementById("wordFront").innerText = card.front;
            document.getElementById("wordPos").innerText = card.pos || "vocab";
            document.getElementById("wordBack").innerText = "💡 " + card.back;
            document.getElementById("wordExample").innerText = card.example ? `"${card.example}"` : "";

            // Cập nhật tiến trình
            const progress = ((currentIndex + 1) / currentCards.length) * 100;
            document.getElementById("progressFill").style.width = progress + "%";
            document.getElementById("cardCounter").innerText = `Thẻ ${currentIndex + 1} / ${currentCards.length}`;

            // Reset mặt thẻ
            isFront = true;
            document.getElementById("cardFront").classList.remove("hidden");
            document.getElementById("cardBack").classList.add("hidden");
        }

        function flipCard() {
            if (currentCards.length === 0) return;
            isFront = !isFront;
            if (isFront) {
                document.getElementById("cardFront").classList.remove("hidden");
                document.getElementById("cardBack").classList.add("hidden");
            } else {
                document.getElementById("cardFront").classList.add("hidden");
                document.getElementById("cardBack").classList.remove("hidden");
            }
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

        // Khởi chạy ban đầu
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