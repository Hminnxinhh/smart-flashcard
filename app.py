import json
import os
from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)
DATA_FILE = "flashcards_data.json"


def load_data():
  if os.path.exists(DATA_FILE):
    try:
      with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    except Exception:
      pass
  return [
      {"front": "Apple", "back": "Quả táo"},
      {"front": "Developer", "back": "Lập trình viên"},
      {"front": "Fintech", "back": "Công nghệ tài chính"},
  ]


def save_data(cards_data):
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(cards_data, f, ensure_ascii=False, indent=4)


# Giao diện HTML trực quan chạy thẳng trên trình duyệt
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Smart Flashcard Online</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card-box { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 400px; text-align: center; }
        .card { font-size: 24px; font-weight: bold; color: #333; padding: 40px 20px; background: #fafafa; border: 2px dashed #d9d9d9; border-radius: 8px; margin: 20px 0; cursor: pointer; min-height: 60px; display: flex; align-items: center; justify-content: center; }
        .btn { background: #1890ff; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 6px; cursor: pointer; width: 100%; margin-top: 10px; }
        .btn-success { background: #52c41a; }
        input { width: 100%; padding: 8px; margin: 5px 0 15px 0; border: 1px solid #d9d9d9; border-radius: 4px; box-sizing: border-box; }
        .form-group { text-align: left; margin-top: 15px; border-top: 1px solid #eee; padding-top: 10px; }
    </style>
</head>
<body>
    <div class="card-box">
        <h2>🧠 Smart Flashcard</h2>
        <p>Thẻ {{ index + 1 }} / {{ total }}</p>
        
        <div class="card" onclick="location.href='{{ url_for('flip') }}'">
            {{ current_text }}
        </div>
        <p style="color: #888; font-size: 13px;">(Bấm vào thẻ để lật xem nghĩa)</p>

        <form action="{{ url_for('next_card') }}" method="post">
            <button type="submit" class="btn btn-success">Đã nhớ / Thẻ tiếp theo ➔</button>
        </form>

        <div class="form-group">
            <h4 style="margin: 5px 0;">➕ Thêm từ vựng mới</h4>
            <form action="{{ url_for('add') }}" method="post">
                <label style="font-size: 12px;">Từ vựng (Mặt trước):</label>
                <input type="text" name="front" required>
                <label style="font-size: 12px;">Nghĩa (Mặt sau):</label>
                <input type="text" name="back" required>
                <button type="submit" class="btn">Thêm & Lưu vào hệ thống</button>
            </form>
        </div>
    </div>
</body>
</html>
"""

# Biến trạng thái đơn giản
current_index = 0
showing_front = True


@app.route("/")
def index():
  global current_index, showing_front
  cards = load_data()
  if not cards:
    return "Chưa có từ vựng nào!"
  current_index = current_index % len(cards)
  card = cards[current_index]
  current_text = card["front"] if showing_front else f"💡 {card['back']}"
  return render_template_string(
      HTML_TEMPLATE,
      index=current_index,
      total=len(cards),
      current_text=current_text,
  )


@app.route("/flip")
def flip():
  global showing_front
  showing_front = not showing_front
  return redirect(url_for("index"))


@app.route("/next", methods=["POST"])
def next_card():
  global current_index, showing_front
  cards = load_data()
  if cards:
    current_index = (current_index + 1) % len(cards)
  showing_front = True
  return redirect(url_for("index"))


@app.route("/add", methods=["POST"])
def add():
  global current_index, showing_front
  front = request.form.get("front", "").strip()
  back = request.form.get("back", "").strip()
  if front and back:
    cards = load_data()
    cards.append({"front": front, "back": back})
    save_data(cards)
  return redirect(url_for("index"))


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)