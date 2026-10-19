import json
import os
from flask import Flask, render_template_string

app = Flask(__name__)
STORY_FILE = "story_data.json"


def load_story():
  if os.path.exists(STORY_FILE):
    try:
      with open(STORY_FILE, "r", encoding="utf-8") as f:
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
    <title>Detective Game Pro - Căn Phòng Khóa Cấm</title>
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
            background-image: 
                radial-gradient(at 10% 20%, rgba(99, 102, 241, 0.4) 0px, transparent 50%),
                radial-gradient(at 90% 10%, rgba(236, 72, 153, 0.35) 0px, transparent 50%),
                radial-gradient(at 50% 90%, rgba(14, 165, 233, 0.3) 0px, transparent 50%);
            color: #F8FAFC;
            min-height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .main-container {
            position: relative;
            z-index: 10;
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(28px);
            -webkit-backdrop-filter: blur(28px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 36px;
            padding: 32px 28px;
            width: 100%;
            max-width: 520px;
            box-shadow: 0 35px 70px -15px rgba(0, 0, 0, 0.7);
        }

        h1 {
            font-size: 22px;
            font-weight: 800;
            margin-bottom: 8px;
            color: #FFFFFF;
            text-align: center;
        }

        .case-desc {
            font-size: 13px;
            color: #94A3B8;
            text-align: center;
            margin-bottom: 24px;
            line-height: 1.5;
        }

        .progress-bar {
            display: flex;
            gap: 6px;
            margin-bottom: 24px;
            justify-content: center;
        }

        .step-dot {
            width: 35px;
            height: 6px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
            transition: all 0.3s;
        }

        .step-dot.active { background: var(--primary); box-shadow: 0 0 10px rgba(99, 102, 241, 0.6); }
        .step-dot.completed { background: var(--success); }

        .puzzle-box {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 16px;
        }

        .puzzle-title {
            font-size: 16px;
            font-weight: 700;
            color: #818CF8;
            margin-bottom: 10px;
        }

        .hint-text {
            font-size: 13px;
            color: #CBD5E1;
            font-style: italic;
            margin-bottom: 16px;
            line-height: 1.5;
            background: rgba(0, 0, 0, 0.2);
            padding: 12px;
            border-radius: 12px;
            border-left: 3px solid var(--primary);
        }

        input[type="text"] {
            width: 100%;
            padding: 13px 16px;
            border-radius: 14px;
            border: 1.5px solid rgba(255, 255, 255, 0.2);
            background: rgba(255, 255, 255, 0.07);
            color: #FFF;
            font-size: 14px;
            font-weight: 600;
            outline: none;
            margin-bottom: 14px;
            transition: all 0.2s;
        }

        input[type="text"]:focus {
            border-color: var(--primary);
            background: rgba(255, 255, 255, 0.12);
        }

        .btn {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 14px;
            background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
            color: #FFF;
            font-size: 14px;
            font-weight: 800;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
            transition: transform 0.2s;
        }

        .btn:hover { transform: translateY(-2px); }

        .result-msg {
            font-size: 13px;
            font-weight: 700;
            margin-top: 12px;
            text-align: center;
            min-height: 20px;
        }

        .suspect-grid {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 16px;
        }

        .suspect-card {
            padding: 14px 16px;
            background: rgba(255, 255, 255, 0.05);
            border: 1.5px solid rgba(255, 255, 255, 0.1);
            border-radius: 14px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .suspect-card:hover { background: rgba(255, 255, 255, 0.1); }
        .suspect-card.selected {
            background: rgba(99, 102, 241, 0.25);
            border-color: var(--primary);
            box-shadow: 0 0 15px rgba(99, 102, 241, 0.3);
        }

        .suspect-name { font-weight: 700; font-size: 14px; color: #FFF; margin-bottom: 2px; }
        .suspect-desc { font-size: 12px; color: #94A3B8; }
    </style>
</head>
<body>
    <div class="main-container">
        <h1 id="gameTitle">Đang tải vụ án...</h1>
        <div class="case-desc" id="gameDesc"></div>

        <div class="progress-bar">
            <div class="step-dot active" id="dot1"></div>
            <div class="step-dot" id="dot2"></div>
            <div class="step-dot" id="dot3"></div>
        </div>

        <div id="puzzleArea"></div>
    </div>

    <script>
        const storyData = {{ story | tojson }};
        let currentStage = 1;
        let selectedSuspect = null;

        function initGame() {
            if (!storyData.chapter_info) return;
            document.getElementById("gameTitle").innerText = storyData.chapter_info.title;
            document.getElementById("gameDesc").innerText = storyData.chapter_info.description;
            renderStage();
        }

        function renderStage() {
            const area = document.getElementById("puzzleArea");
            area.innerHTML = "";

            document.getElementById("dot1").className = currentStage === 1 ? "step-dot active" : (currentStage > 1 ? "step-dot completed" : "step-dot");
            document.getElementById("dot2").className = currentStage === 2 ? "step-dot active" : (currentStage > 2 ? "step-dot completed" : "step-dot");
            document.getElementById("dot3").className = currentStage === 3 ? "step-dot active" : "step-dot";

            if (currentStage === 1) {
                const p1 = storyData.puzzles.puzzle_1;
                area.innerHTML = `
                    <div class="puzzle-box">
                        <div class="puzzle-title">${p1.title}</div>
                        <div class="hint-text">${p1.hint_text}</div>
                        <input type="text" id="answerInput" placeholder="Nhập mã 4 chữ số...">
                        <button class="btn" onclick="checkPuzzle1()">Xác nhận mật mã ➔</button>
                        <div class="result-msg" id="resMsg"></div>
                    </div>
                `;
            } else if (currentStage === 2) {
                const p2 = storyData.puzzles.puzzle_2;
                area.innerHTML = `
                    <div class="puzzle-box">
                        <div class="puzzle-title">${p2.title}</div>
                        <div class="hint-text">💡 Manh mối tin nhắn nhắc đến từ khóa: 'Giao dịch lúc RẠNG ĐÔNG' (4 ký tự tiếng Anh).</div>
                        <input type="text" id="answerInput" placeholder="Nhập từ khóa...">
                        <button class="btn" onclick="checkPuzzle2()">Giải mã file ➔</button>
                        <div class="result-msg" id="resMsg"></div>
                    </div>
                `;
            } else if (currentStage === 3) {
                const p3 = storyData.puzzles.puzzle_3;
                let suspectsHtml = storyData.suspects.map(s => `
                    <div class="suspect-card" id="suspect-${s.id}" onclick="selectSuspect('${s.id}')">
                        <div class="suspect-name">${s.name}</div>
                        <div class="suspect-desc">${s.desc}</div>
                    </div>
                `).join('');

                area.innerHTML = `
                    <div class="puzzle-box">
                        <div class="puzzle-title">Thử thách 3: Chỉ định Thủ phạm</div>
                        <div class="hint-text">🔍 Dựa vào các bằng chứng, ai là kẻ dàn dựng vụ mất tích?</div>
                        <div class="suspect-grid">${suspectsHtml}</div>
                        <button class="btn" onclick="checkPuzzle3()">Kết luận vụ án 🏆</button>
                        <div class="result-msg" id="resMsg"></div>
                    </div>
                `;
            }
        }

        function checkPuzzle1() {
            const val = document.getElementById("answerInput").value.trim();
            const p1 = storyData.puzzles.puzzle_1;
            const msg = document.getElementById("resMsg");
            if (val === p1.answer) {
                msg.style.color = "#34D399";
                msg.innerText = p1.success_msg;
                setTimeout(() => { currentStage = 2; renderStage(); }, 1500);
            } else {
                msg.style.color = "#F87171";
                msg.innerText = "❌ Mật mã không chính xác. Hãy kiểm tra lại!";
            }
        }

        function checkPuzzle2() {
            const val = document.getElementById("answerInput").value.trim().toUpperCase();
            const p2 = storyData.puzzles.puzzle_2;
            const msg = document.getElementById("resMsg");
            if (val === p2.answer) {
                msg.style.color = "#34D399";
                msg.innerText = p2.success_msg;
                setTimeout(() => { currentStage = 3; renderStage(); }, 1500);
            } else {
                msg.style.color = "#F87171";
                msg.innerText = "❌ Từ khóa sai. Thử lại nhé!";
            }
        }

        function selectSuspect(id) {
            selectedSuspect = id;
            document.querySelectorAll('.suspect-card').forEach(c => c.classList.remove('selected'));
            document.getElementById(`suspect-${id}`).classList.add('selected');
        }

        function checkPuzzle3() {
            const msg = document.getElementById("resMsg");
            const p3 = storyData.puzzles.puzzle_3;
            if (!selectedSuspect) {
                msg.style.color = "#F87171";
                msg.innerText = "⚠️ Vui lòng chọn một nghi phạm!";
                return;
            }
            if (selectedSuspect === p3.answer) {
                msg.style.color = "#34D399";
                msg.innerText = p3.success_msg;
                setTimeout(() => {
                    alert("🎉 CHÚC MỪNG BẠN ĐÃ PHÁ ÁN THÀNH CÔNG!");
                    currentStage = 1;
                    renderStage();
                }, 2000);
            } else {
                msg.style.color = "#F87171";
                msg.innerText = "❌ Sai rồi! Kẻ này vô tội. Hãy suy luận lại!";
            }
        }

        initGame();
    </script>
</body>
</html>
"""


@app.route("/")
def index():
  story = load_story()
  return render_template_string(HTML_TEMPLATE, story=story)


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)