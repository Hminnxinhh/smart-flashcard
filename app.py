import json
import os
import urllib.request
from flask import Flask, render_template_string

app = Flask(__name__)
DATA_FILE = "flashcards_data.json"


def get_vocab_data():
  # Nếu file chưa tồn tại hoặc dữ liệu bị thiếu, tự động cào trực tiếp kho AWL
  if not os.path.exists(DATA_FILE):
    download_awl_data()

  try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
      data = json.load(f)
      # Kiểm tra nếu dữ liệu quá ít (dưới 30 từ), tự nạp lại dữ liệu đầy đủ
      total_words = sum(len(v) for v in data.values())
      if total_words < 50:
        return download_awl_data()
      return data
  except Exception:
    return download_awl_data()


def download_awl_data():
  url = "https://raw.githubusercontent.com/datasets/academic-word-list/master/data/words.json"
  try:
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    with urllib.request.urlopen(req) as response:
      raw_data = json.loads(response.read().decode("utf-8"))

      band_1 = []
      band_2 = []
      band_3 = []

      for item in raw_data:
        word = item.get("word", "").strip()
        sublist = item.get("sublist", 1)
        if not word or len(word) < 2:
          continue

        entry = {
            "front": word.capitalize(),
            "back": f"Từ vựng học thuật nhóm AWL Sublist {sublist}",
            "ipa": f"/{word.lower()}/",
            "pos": "Academic",
            "example": (
                f"The academic word '{word}' frequently appears in reading and"
                " writing tasks."
            ),
        }

        if sublist <= 3:
          band_1.append(entry)
        elif sublist <= 6:
          band_2.append(entry)
        else:
          band_3.append(entry)

      dataset = {
          "IELTS Band 4.0 - 5.0 (Cơ bản)": band_1,
          "IELTS Band 5.5 - 6.5 (Khá/Tốt)": band_2,
          "IELTS Band 7.0+ (Nâng cao)": band_3,
      }

      with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

      return dataset
  except Exception as e:
    print(f"Lỗi nạp dữ liệu: {e}")
    return {}


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IELTS Vocab Master Pro</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #0B0F19;
            --card-bg: rgba(255, 255, 255, 0.06);
            --border-color: rgba(255, 255, 255, 0.12);
            --primary: #6366F1;
            --primary-glow: rgba(99, 102, 241, 0.4);
            --text-main: #F8FAFC;
            --text-sub: #94A3B8;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-dark);
            background-image: 
                radial-gradient(at 15% 15%, rgba(99, 102, 241, 0.25) 0px, transparent 50%),
                radial-gradient(at 85% 85%, rgba(236, 72, 153, 0.2) 0px, transparent 50%);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .app-container {
            width: 100%;
            max-width: 540px;
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(24px);
            border: 1px solid var(--border-color);
            border-radius: 32px;
            padding: 28px 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
        }

        header { text-align: center; margin-bottom: 20px; }
        h1 {
            font-size: 24px;
            font-weight: 800;
            background: linear-gradient(135deg, #818CF8 0%, #C084FC 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
        }
        .subtitle { font-size: 13px; color: var(--text-sub); }

        .band-selector {
            width: 100%;
            padding: 12px 16px;
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid var(--border-color);
            color: #FFF;
            font-size: 14px;
            font-weight: 700;
            outline: none;
            margin-bottom: 20px;
            cursor: pointer;
        }
        .band-selector option { background: #0F172A; color: #FFF; }

        .card-wrapper {
            perspective: 1000px;
            height: 260px;
            margin-bottom: 20px;
            cursor: pointer;
        }
        .card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            transform-style: preserve-3d;
        }
        .card-wrapper.flipped .card-inner { transform: rotateY(180deg); }

        .card-front, .card-back {
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
            text-align: center;
            border: 1px solid var(--border-color);
            background: var(--card-bg);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        .card-back {
            transform: rotateY(180deg);
            background: rgba(30, 41, 59, 0.95);
            border-color: rgba(99, 102, 241, 0.4);
        }

        .word-title { font-size: 28px; font-weight: 800; margin-bottom: 8px; color: #FFF; }
        .word-ipa { font-size: 15px; color: #818CF8; margin-bottom: 6px; font-weight: 600; }
        .word-pos {
            display: inline-block;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            padding: 4px 10px;
            border-radius: 20px;
            background: rgba(99, 102, 241, 0.2);
            color: #A5B4FC;
            margin-bottom: 12px;
        }
        .meaning-text { font-size: 18px; font-weight: 700; color: #F3F4F6; margin-bottom: 12px; }
        .example-text { font-size: 13px; color: var(--text-sub); font-style: italic; line-height: 1.4; }
        .tap-hint { position: absolute; bottom: 12px; font-size: 11px; color: rgba(255, 255, 255, 0.4); }

        .controls { display: flex; gap: 12px; }
        .btn {
            flex: 1;
            padding: 14px;
            border: none;
            border-radius: 16px;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
        }
        .btn-prev { background: rgba(255, 255, 255, 0.08); color: var(--text-main); border: 1px solid var(--border-color); }
        .btn-next { background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%); color: #FFF; box-shadow: 0 4px 15px var(--primary-glow); }
        .btn:hover { transform: translateY(-2px); }

        .progress-text { text-align: center; font-size: 13px; color: #818CF8; margin-top: 14px; font-weight: 700; }
    </style>
</head>
<body>
    <div class="app-container">
        <header>
            <h1>IELTS Vocab Master</h1>
            <div class="subtitle">Kho từ vựng học thuật AWL đầy đủ theo Band</div>
        </header>

        <select class="band-selector" id="bandSelect" onchange="changeBand()"></select>

        <div class="card-wrapper" id="cardWrapper" onclick="flipCard()">
            <div class="card-inner">
                <div class="card-front">
                    <span class="word-pos" id="wordPos">Academic</span>
                    <div class="word-title" id="wordFront">Loading...</div>
                    <div class="word-ipa" id="wordIpa">/.../</div>
                    <div class="tap-hint">💡 Chạm vào thẻ để xem nghĩa</div>
                </div>
                <div class="card-back">
                    <div class="meaning-text" id="wordMeaning">---</div>
                    <div class="example-text" id="wordExample">---</div>
                    <div class="tap-hint">💡 Chạm vào thẻ để lật lại</div>
                </div>
            </div>
        </div>

        <div class="controls">
            <button class="btn btn-prev" onclick="prevCard()">◄ Từ trước</button>
            <button class="btn btn-next" onclick="nextCard()">Từ tiếp ►</button>
        </div>

        <div class="progress-text" id="progressText">0 / 0</div>
    </div>

    <script>
        const vocabData = {{ data | tojson }};
        let currentBand = "";
        let currentIndex = 0;

        function initApp() {
            const bands = Object.keys(vocabData);
            if (bands.length === 0) return;

            const select = document.getElementById("bandSelect");
            select.innerHTML = "";
            bands.forEach(band => {
                const opt = document.createElement("option");
                opt.value = band;
                opt.innerText = `${band} (${vocabData[band].length} từ)`;
                select.appendChild(opt);
            });

            currentBand = bands[0];
            currentIndex = 0;
            renderCard();
        }

        function renderCard() {
            const list = vocabData[currentBand] || [];
            if (list.length === 0) return;

            const item = list[currentIndex];
            document.getElementById("wordFront").innerText = item.front || item.word || "N/A";
            document.getElementById("wordIpa").innerText = item.ipa || "/.../";
            document.getElementById("wordPos").innerText = item.pos || "Academic";
            document.getElementById("wordMeaning").innerText = item.back || item.meaning || "---";
            document.getElementById("wordExample").innerText = item.example ? `"${item.example}"` : "";
            
            document.getElementById("progressText").innerText = `Từ ${currentIndex + 1} / ${list.length} từ`;
            document.getElementById("cardWrapper").classList.remove("flipped");
        }

        function flipCard() { document.getElementById("cardWrapper").classList.toggle("flipped"); }
        function nextCard() {
            const list = vocabData[currentBand] || [];
            if (currentIndex < list.length - 1) { currentIndex++; renderCard(); }
        }
        function prevCard() {
            if (currentIndex > 0) { currentIndex--; renderCard(); }
        }
        function changeBand() {
            currentBand = document.getElementById("bandSelect").value;
            currentIndex = 0;
            renderCard();
        }

        initApp();
    </script>
</body>
</html>
"""


@app.route("/")
def index():
  data = get_vocab_data()
  return render_template_string(HTML_TEMPLATE, data=data)


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)