import json
import urllib.request


def generate_local_data():
  print("⏳ Đang tải và xử lý dữ liệu Academic Word List...")
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

      with open("flashcards_data.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

      print(
          f"✅ Đã tạo thành công file flashcards_data.json với tổng số từ:"
          f" {len(band_1) + len(band_2) + len(band_3)} từ!"
      )
  except Exception as e:
    print(f"❌ Lỗi: {e}")


if __name__ == "__main__":
  generate_local_data()