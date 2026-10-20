import json
import urllib.request


def create_full_vocab_dataset():
  print("⏳ Đang tải dữ liệu từ vựng học thuật AWL chính thức...")
  url = "https://raw.githubusercontent.com/datasets/academic-word-list/master/data/words.json"

  try:
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    with urllib.request.urlopen(req) as response:
      raw_data = json.loads(response.read().decode("utf-8"))

      band_4_5 = []
      band_5_5_6_5 = []
      band_7_plus = []

      for item in raw_data:
        word = item.get("word", "").strip()
        sublist = item.get("sublist", 1)

        if not word or len(word) < 2:
          continue

        entry = {
            "front": word.capitalize(),
            "back": f"Từ vựng học thuật thuộc nhóm AWL Sublist {sublist}",
            "ipa": f"/{word.lower()}/",
            "pos": "Academic",
            "example": (
                f"The term '{word}' is widely used in academic contexts and"
                " IELTS materials."
            ),
        }

        if sublist <= 3:
          band_4_5.append(entry)
        elif sublist <= 6:
          band_5_5_6_5.append(entry)
        else:
          band_7_plus.append(entry)

      dataset = {
          "IELTS Band 4.0 - 5.0 (Cơ bản)": band_4_5,
          "IELTS Band 5.5 - 6.5 (Khá/Tốt)": band_5_5_6_5,
          "IELTS Band 7.0+ (Nâng cao)": band_7_plus,
      }

      with open("flashcards_data.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

      print(
          f"✅ Đã tạo dữ liệu thành công! Tổng số từ: Band 4-5:"
          f" {len(band_4_5)}, Band 5.5-6.5: {len(band_5_5_6_5)}, Band 7+:"
          f" {len(band_7_plus)}"
      )

  except Exception as e:
    print(f"❌ Lỗi: {e}")


if __name__ == "__main__":
  create_full_vocab_dataset()