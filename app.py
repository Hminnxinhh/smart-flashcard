import json
import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Dữ liệu từ vựng IELTS AWL nhúng trực tiếp trong code (Đảm bảo 100% không lo thiếu file JSON)
DEFAULT_VOCAB_DATA = {
    "IELTS Band 4.0 - 5.0 (Cơ bản)": [
        {
            "front": "Analyse",
            "ipa": "/ˈæn.əl.aɪz/",
            "pos": "Verb",
            "back": "Phân tích (nghiên cứu chi tiết cấu trúc)",
            "example": (
                "Researchers need to analyse the data before reaching a"
                " conclusion."
            ),
        },
        {
            "front": "Approach",
            "ipa": "/əˈprəʊtʃ/",
            "pos": "Noun / Verb",
            "back": "Tiếp cận / Phương pháp giải quyết",
            "example": "We need a new approach to solve this complex problem.",
        },
        {
            "front": "Area",
            "ipa": "/ˈeə.ri.ə/",
            "pos": "Noun",
            "back": "Lĩnh vực / Khu vực",
            "example": (
                "This study focuses on the area of environmental science."
            ),
        },
        {
            "front": "Assess",
            "ipa": "/əˈses/",
            "pos": "Verb",
            "back": "Đánh giá / Định giá",
            "example": (
                "The exam is designed to assess students' writing skills."
            ),
        },
        {
            "front": "Assume",
            "ipa": "/əˈsjuːm/",
            "pos": "Verb",
            "back": "Cho rằng / Giả định",
            "example": "It is incorrect to assume that all results are equal.",
        },
        {
            "front": "Authority",
            "ipa": "/ɔːˈθɒr.ə.ti/",
            "pos": "Noun",
            "back": "Chính quyền / Quyền lực / Chuyên gia",
            "example": "She is a leading authority on international law.",
        },
        {
            "front": "Benefit",
            "ipa": "/ˈben.ɪ.fɪt/",
            "pos": "Noun / Verb",
            "back": "Lợi ích / Thu lợi từ",
            "example": "Regular study brings great benefits to students.",
        },
        {
            "front": "Concept",
            "ipa": "/ˈkɒn.sept/",
            "pos": "Noun",
            "back": "Khái niệm / Ý tưởng",
            "example": (
                "Understanding the basic concept is vital for this course."
            ),
        },
        {
            "front": "Context",
            "ipa": "/ˈkɒn.tekst/",
            "pos": "Noun",
            "back": "Bối cảnh / Ngữ cảnh",
            "example": (
                "Words must be understood in their original context."
            ),
        },
        {
            "front": "Create",
            "ipa": "/kriˈeɪt/",
            "pos": "Verb",
            "back": "Tạo ra / Sáng tạo",
            "example": "The campaign aims to create job opportunities.",
        },
        {
            "front": "Data",
            "ipa": "/ˈdeɪ.tə/",
            "pos": "Noun",
            "back": "Dữ liệu / Thông tin",
            "example": "The collected data supports our main hypothesis.",
        },
        {
            "front": "Definition",
            "ipa": "/ˌdef.ɪˈnɪʃ.ən/",
            "pos": "Noun",
            "back": "Định nghĩa",
            "example": (
                "Can you provide a clear definition of this academic term?"
            ),
        },
        {
            "front": "Derived",
            "ipa": "/dɪˈraɪvd/",
            "pos": "Adjective",
            "back": "Bắt nguồn từ / Bị chiết xuất từ",
            "example": (
                "Many English words are derived from ancient Latin roots."
            ),
        },
        {
            "front": "Distribution",
            "ipa": "/ˌdɪs.trɪˈbjuː.ʃən/",
            "pos": "Noun",
            "back": "Sự phân phối / Phân bố",
            "example": "The global distribution of wealth remains unequal.",
        },
        {
            "front": "Economic",
            "ipa": "/ˌiː.kəˈnɒm.ɪk/",
            "pos": "Adjective",
            "back": "Thuộc về kinh tế",
            "example": "The country experienced rapid economic growth.",
        },
    ],
    "IELTS Band 5.5 - 6.5 (Khá/Tốt)": [
        {
            "front": "Acquire",
            "ipa": "/əˈkwaɪər/",
            "pos": "Verb",
            "back": "Lĩnh hội / Đạt được (kỹ năng, kiến thức)",
            "example": (
                "Students must acquire language skills through continuous"
                " practice."
            ),
        },
        {
            "front": "Category",
            "ipa": "/ˈkæt.ə.ɡri/",
            "pos": "Noun",
            "back": "Hạng / Loại / Danh mục",
            "example": (
                "The books are divided into separate academic categories."
            ),
        },
        {
            "front": "Complex",
            "ipa": "/ˈkɒm.pleks/",
            "pos": "Adjective",
            "back": "Phức tạp / Rắc rối",
            "example": (
                "The human brain is an extraordinarily complex organ."
            ),
        },
        {
            "front": "Consequence",
            "ipa": "/ˈkɒn.sɪ.kwəns/",
            "pos": "Noun",
            "back": "Hậu quả / Kết quả",
            "example": "Global warming is a direct consequence of pollution.",
        },
        {
            "front": "Construct",
            "ipa": "/kənˈstrʌkt/",
            "pos": "Verb",
            "back": "Xây dựng / Kiến tạo",
            "example": (
                "Engineers plan to construct a sustainable infrastructure."
            ),
        },
        {
            "front": "Evaluate",
            "ipa": "/ɪˈvæl.ju.eɪt/",
            "pos": "Verb",
            "back": "Đánh giá / Ước lượng giá trị",
            "example": "Professors will evaluate your research proposal.",
        },
        {
            "front": "Impact",
            "ipa": "/ˈɪm.pækt/",
            "pos": "Noun / Verb",
            "back": "Tác động mạnh mẽ / Ảnh hưởng",
            "example": "Technology has a profound impact on modern education.",
        },
        {
            "front": "Obtain",
            "ipa": "/əbˈteɪn/",
            "pos": "Verb",
            "back": "Đạt được / Lấy được",
            "example": "You need to obtain permission before conducting the survey.",
        },
        {
            "front": "Primary",
            "ipa": "/ˈpraɪ.mər.i/",
            "pos": "Adjective",
            "back": "Chính / Chủ yếu / Sơ cấp",
            "example": "The primary goal of this initiative is public health.",
        },
        {
            "front": "Relevant",
            "ipa": "/ˈrel.ə.vənt/",
            "pos": "Adjective",
            "back": "Lên quan / Thích hợp",
            "example": "Please include only relevant details in your essay.",
        },
    ],
    "IELTS Band 7.0+ (Nâng cao)": [
        {
            "front": "Coversely",
            "ipa": "/ˈkɒn.vɜːs.li/",
            "pos": "Adverb",
            "back": "Ngược lại / Trái lại",
            "example": (
                "Some thrive under stress; conversely, others lose focus."
            ),
        },
        {
            "front": "Differentiate",
            "ipa": "/ˌdɪf.əˈren.ʃi.eɪt/",
            "pos": "Verb",
            "back": "Phân biệt / Nhận dạng sự khác biệt",
            "example": (
                "It is critical to differentiate between opinion and fact."
            ),
        },
        {
            "front": "Implementation",
            "ipa": "/ˌɪm.plɪ.menˈteɪ.ʃən/",
            "pos": "Noun",
            "back": "Sự thực thi / Triển khai áp dụng",
            "example": (
                "The successful implementation of policy requires funding."
            ),
        },
        {
            "front": "Inevitably",
            "ipa": "/ɪnˈev.ɪ.tə.bli/",
            "pos": "Adverb",
            "back": "Tất yếu / Không thể tránh khỏi",
            "example": "Rapid industrial development inevitably leads to waste.",
        },
        {
            "front": "Predominantly",
            "ipa": "/prɪˈdɒm.ɪ.nənt.li/",
            "pos": "Adverb",
            "back": "Phần lớn / Chủ yếu",
            "example": "The city population is predominantly young professionals.",
        },
        {
            "front": "Subsequent",
            "ipa": "/ˈsʌb.sɪ.kwənt/",
            "pos": "Adjective",
            "back": "Xảy ra sau đó / Theo sau",
            "example": "Subsequent studies supported the original findings.",
        },
    ],
}


def get_vocab_data():
  DATA_FILE = "flashcards_data.json"
  if os.path.exists(DATA_FILE):
    try:
      with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        if data and sum(len(v) for v in data.values()) > 0:
          return data
    except Exception:
      pass
  return DEFAULT_VOCAB_DATA


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