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
    <title>Smart Flashcard Pro - IELTS Master</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366F1;
            --primary-hover: #4F46E5;
            --accent: #EC4899;
            --success: #10B981;
            --danger: #EF4444;
        }

        * { box-sizing: border-box; }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: #0B0F19;
            /* GenZ Vibrant Mesh Gradient Background */
            background-image: 
                radial-gradient(at 10% 20%, rgba(99, 102, 241, 0.5) 0px, transparent 50%),
                radial-gradient(at 90% 10%, rgba(236, 72, 153, 0.45) 0px, transparent 50%),
                radial-gradient(at 50% 90%, rgba(14, 165, 233, 0.4) 0px, transparent 50%),
                radial-gradient(at 80% 80%, rgba(168, 85, 247, 0.4) 0px, transparent 50%);
            color: #F8FAFC;
            min-height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            overflow-x: hidden;
        }

        .main-container {
            position: relative;
            z-index: 10;
            background: rgba(15, 23, 42, 0.78);
            backdrop-filter: blur(28px);
            -webkit-backdrop-filter: blur(28px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 36px;
            padding: 32px 28px;
            width: 100%;
            max-width: 480px;
            box-shadow: 0 35px 70px -15px rgba(0, 0, 0, 0.7);
            text-align: center;
        }

        .nav-tabs {
            display: flex;
            background: rgba(255, 255, 255, 0.06);
            padding: 5px;
            border-radius: 18px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .tab-btn {
            flex: 1;
            padding: 11px;
            border: none;
            background: transparent;
            color: #94A3B8;
            font-size: 13px;
            font-weight: 700;
            border-radius: 14px;
            cursor: pointer;
            transition: all 0.25s;
            font-family: inherit;
        }

        .tab-btn.active {
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
            color: #FFFFFF;
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
        }

        select, input {
            width: 100%;
            padding: 13px 18px;
            border-radius: 16px;
            border: 1.5px solid rgba(255, 255, 255, 0.15);
            font-size: 14px;
            font-family: inherit;
            font-weight: 600;
            outline: none;
            transition: all 0.2s;
            margin-bottom: 14px;
            background: rgba(255, 255, 255, 0.07);
            color: #F8FAFC;
        }

        select option { background: #0F172A; color: #FFF; }

        select:focus, input:focus {
            border-color: #818CF8;
            background: rgba(255, 255, 255, 0.12);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.3);
        }

        .scene {
            width: 100%;
            height: 250px;
            perspective: 1000px;
            margin: 16px 0;
            cursor: pointer;
        }

        .card-flip {
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        .card-flip.is-flipped { transform: rotateY(180deg); }

        .card-face {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 26px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        }

        .card-front {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
        }

        .card-back {
            background: linear-gradient(145deg, rgba(49, 46, 129, 0.9) 0%, rgba(30, 27, 75, 0.95) 100%);
            transform: rotateY(180deg);
        }

        .word-title {
            font-size: 34px;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 2px;
            letter-spacing: -0.5px;
        }

        .word-ipa {
            font-size: 14px;
            color: #A5B4FC;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .badge-pos {
            background: rgba(99, 102, 241, 0.25);
            color: #A5B4FC;
            border: 1px solid rgba(99, 102, 241, 0.4);
            font-size: 11px;
            font-weight: 800;
            padding: 4px 12px;
            border-radius: 20px;
            text-transform: uppercase;
        }

        .word-meaning {
            font-size: 24px;
            font-weight: 800;
            color: #34D399;
            margin-bottom: 8px;
        }

        .word-example {
            font-size: 13px;
            color: #CBD5E1;
            font-style: italic;
            line-height: 1.4;
        }

        .audio-mic-group {
            display: flex;
            gap: 12px;
            margin-top: 12px;
        }

        .icon-btn {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            width: 44px;
            height: 44px;
            font-size: 18px;
            color: #FFF;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .icon-btn:hover {
            background: rgba(255, 255, 255, 0.25);
            transform: scale(1.1);
        }

        .icon-btn.recording {
            background: var(--danger);
            animation: pulseMic 1s infinite alternate;
        }

        @keyframes pulseMic {
            0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
            100% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
        }

        .speech-result {
            font-size: 12px;
            font-weight: 700;
            margin-top: 6px;
            min-height: 18px;
        }

        .controls { display: flex; gap: 12px; margin-top: 16px; }

        .btn {
            flex: 1;
            padding: 14px;
            border: none;
            border-radius: 16px;
            font-size: 14px;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.2s;
            font-family: inherit;
        }

        .btn-prev { background: rgba(255, 255, 255, 0.08); color: #CBD5E1; }
        .btn-prev:hover { background: rgba(255, 255, 255, 0.16); }

        .btn-next {
            background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
            color: white;
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.45);
        }
        .btn-next:hover { transform: translateY(-2px); }

        /* Quiz Mode Styles */
        .quiz-container { display: none; text-align: left; }
        .quiz-question { font-size: 18px; font-weight: 800; margin-bottom: 18px; text-align: center; color: #F8FAFC; }
        .quiz-options { display: flex; flex-direction: column; gap: 12px; }
        .quiz-opt-btn {
            padding: 15px;
            background: rgba(255, 255, 255, 0.06);
            border: 1.5px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            color: #FFF;
            font-weight: 700;
            font-size: 14px;
            cursor: pointer;
            text-align: left;
            transition: all 0.2s;
        }
        .quiz-opt-btn:hover { background: rgba(255, 255, 255, 0.15); border-color: rgba(255, 255, 255, 0.3); }
        .quiz-opt-btn.correct { background: rgba(16, 185, 129, 0.25) !important; border-color: var(--success) !important; color: #34D399 !important; }
        .quiz-opt-btn.wrong { background: rgba(239, 68, 68, 0.25) !important; border-color: var(--danger) !important; color: #F87171 !important; }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="nav-tabs">
            <button class="tab-btn active" onclick="switchTab('flashcard')">🃏 Flashcards</button>
            <button class="tab-btn" onclick="switchTab('quiz')">✍️ Bài tập Quiz</button>
        </div>

        <select id="categorySelect" onchange="changeCategory()">
            {% for cat in categories %}
            <option value="{{ cat }}">{{ cat }}</option>
            {% endfor %}
        </select>

        <!-- Flashcard Section -->
        <div id="flashcardSection">
            <input type="text" id="searchInput" placeholder="🔍 Tìm nhanh từ vựng..." onkeyup="filterCards()">

            <div id="cardCounter" style="font-size: 12px; font-weight: 700; color: #94A3B8; margin-bottom: 6px;">Thẻ 1 / 1</div>

            <div class="scene" onclick="flipCard()">
                <div class="card-flip" id="cardFlip">
                    <div class="card-face card-front">
                        <div class="word-title" id="wordFront">Loading...</div>
                        <div class="word-ipa" id="wordIpa">/.../</div>
                        <span class="badge-pos" id="wordPos">verb</span>

                        <div class="audio-mic-group" onclick="event.stopPropagation()">
                            <button class="icon-btn" onclick="speakWord()" title="Nghe phát âm">🔊</button>
                            <button class="icon-btn" id="micBtn" onclick="startSpeechRecognition()" title="Thử phát âm">🎤</button>
                        </div>
                        <div class="speech-result" id="speechResult"></div>
                    </div>
                    <div class="card-face card-back">
                        <div class="word-meaning" id="wordBack">Nghĩa tiếng Việt</div>
                        <div class="word-example" id="wordExample">Ví dụ...</div>
                    </div>
                </div>
            </div>
            <p style="font-size: 11px; color: #64748B; margin-top: -4px;">✨ Bấm vào thẻ để xoay lật mặt sau</p>

            <div class="controls">
                <button class="btn btn-prev" onclick="prevCard()">⬅️ Trước</button>
                <button class="btn btn-next" onclick="nextCard()">Tiếp theo 🚀</button>
            </div>
        </div>

        <!-- Quiz Section -->
        <div id="quizSection" class="quiz-container">
            <div class="quiz-question" id="quizQuestion">Từ nào có nghĩa là...</div>
            <div class="quiz-options" id="quizOptions"></div>
            <button class="btn btn-next" style="margin-top: 20px; width: 100%;" onclick="nextQuiz()">Câu tiếp theo ➔</button>
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

        async function renderCard() {
            document.getElementById("cardFlip").classList.remove("is-flipped");
            document.getElementById("speechResult").innerText = "";

            if (currentCards.length === 0) {
                document.getElementById("wordFront").innerText = "Không tìm thấy";
                document.getElementById("wordIpa").innerText = "";
                document.getElementById("wordPos").innerText = "N/A";
                document.getElementById("wordBack").innerText = "Hãy thử lại";
                document.getElementById("wordExample").innerText = "";
                return;
            }

            const card = currentCards[currentIndex];
            document.getElementById("wordFront").innerText = card.front;
            document.getElementById("wordPos").innerText = card.pos || "vocab";
            document.getElementById("wordBack").innerText = card.back;
            document.getElementById("wordExample").innerText = card.example ? `"${card.example}"` : "";
            document.getElementById("cardCounter").innerText = `Thẻ ${currentIndex + 1} / ${currentCards.length}`;

            if (card.ipa) {
                document.getElementById("wordIpa").innerText = card.ipa;
            } else {
                document.getElementById("wordIpa").innerText = "/.../";
                try {
                    const res = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${card.front}`);
                    const resData = await res.json();
                    if (resData && resData[0] && resData[0].phonetic) {
                        document.getElementById("wordIpa").innerText = resData[0].phonetic;
                    } else if (resData && resData[0] && resData[0].phonetics && resData[0].phonetics.length > 0) {
                        const ph = resData[0].phonetics.find(p => p.text);
                        if (ph) document.getElementById("wordIpa").innerText = ph.text;
                    }
                } catch(e) {
                    document.getElementById("wordIpa").innerText = "";
                }
            }
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
            if (document.getElementById("quizSection").style.display === "block") {
                nextQuiz();
            }
        }

        function filterCards() { loadCategoryCards(); }

        function speakWord() {
            if (currentCards.length === 0) return;
            const word = currentCards[currentIndex].front;
            const utterance = new SpeechSynthesisUtterance(word);
            utterance.lang = 'en-US';
            window.speechSynthesis.speak(utterance);
        }

        function startSpeechRecognition() {
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                alert("Trình duyệt chưa hỗ trợ nhận diện giọng nói.");
                return;
            }
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();
            recognition.lang = 'en-US';

            const micBtn = document.getElementById("micBtn");
            const speechResult = document.getElementById("speechResult");

            micBtn.classList.add("recording");
            speechResult.style.color = "#A5B4FC";
            speechResult.innerText = "🎙️ Đang nghe...";

            recognition.start();

            recognition.onresult = (event) => {
                micBtn.classList.remove("recording");
                const spokenText = event.results[0][0].transcript.toLowerCase().trim();
                const targetText = currentCards[currentIndex].front.toLowerCase().trim();

                if (spokenText === targetText) {
                    speechResult.style.color = "#34D399";
                    speechResult.innerText = `✅ Chuẩn xác: "${spokenText}"!`;
                } else {
                    speechResult.style.color = "#F87171";
                    speechResult.innerText = `❌ Nghe được: "${spokenText}"`;
                }
            };

            recognition.onerror = () => {
                micBtn.classList.remove("recording");
                speechResult.style.color = "#F87171";
                speechResult.innerText = "❌ Không nghe rõ. Vui lòng thử lại!";
            };
        }

        function switchTab(tab) {
            document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
            if (tab === 'flashcard') {
                document.querySelectorAll(".tab-btn")[0].classList.add("active");
                document.getElementById("flashcardSection").style.display = "block";
                document.getElementById("quizSection").style.display = "none";
            } else {
                document.querySelectorAll(".tab-btn")[1].classList.add("active");
                document.getElementById("flashcardSection").style.display = "none";
                document.getElementById("quizSection").style.display = "block";
                nextQuiz();
            }
        }

        // Quiz sạch sẽ, không lặp tên Band thừa thãi
        function nextQuiz() {
            const categoryWords = allData[currentCategory] || [];
            if (categoryWords.length < 2) {
                document.getElementById("quizQuestion").innerText = "Cần thêm từ vựng cho dải Band này!";
                document.getElementById("quizOptions").innerHTML = "";
                return;
            }

            const correctIdx = Math.floor(Math.random() * categoryWords.length);
            const correctCard = categoryWords[correctIdx];

            // Đã xóa bỏ cụm [Band] thừa thãi, chỉ giữ lại câu hỏi gọn gàng
            document.getElementById("quizQuestion").innerText = `Từ nào có nghĩa là: "${correctCard.back}"?`;

            let options = [correctCard];
            while (options.length < Math.min(4, categoryWords.length)) {
                let randCard = categoryWords[Math.floor(Math.random() * categoryWords.length)];
                if (!options.some(o => o.front === randCard.front)) {
                    options.push(randCard);
                }
            }
            options.sort(() => Math.random() - 0.5);

            const optionsContainer = document.getElementById("quizOptions");
            optionsContainer.innerHTML = "";

            options.forEach(opt => {
                const btn = document.createElement("button");
                btn.className = "quiz-opt-btn";
                btn.innerText = opt.front;
                btn.dataset.front = opt.front;

                btn.onclick = () => {
                    document.querySelectorAll(".quiz-opt-btn").forEach(b => {
                        b.disabled = true;
                        if (b.dataset.front === correctCard.front) {
                            b.classList.add("correct");
                            b.innerText += " ✅ (Đúng)";
                        }
                    });

                    if (opt.front !== correctCard.front) {
                        btn.classList.add("wrong");
                        btn.innerText += " ❌";
                    }
                };
                optionsContainer.appendChild(btn);
            });
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