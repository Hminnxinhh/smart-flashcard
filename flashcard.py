import json
import os
import tkinter as tk
from tkinter import messagebox

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
        {"front": "Fintech", "back": "Công nghệ tài chính"}
    ]

def save_data(cards_data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(cards_data, f, ensure_ascii=False, indent=4)

cards = load_data()
current_index = 0
showing_front = True

def flip_card(event=None):
    global showing_front
    showing_front = not showing_front
    if showing_front:
        card_label.config(text=cards[current_index]['front'], fg="#333333")
    else:
        card_label.config(text=cards[current_index]['back'], fg="#1890ff")

def next_card():
    global current_index, showing_front
    if not cards:
        return
    showing_front = True
    current_index = (current_index + 1) % len(cards)
    card_label.config(text=cards[current_index]['front'], fg="#333333")
    progress_label.config(text=f"Thẻ {current_index + 1} / {len(cards)}")

def add_new_card():
    front_text = entry_front.get().strip()
    back_text = entry_back.get().strip()
    
    if not front_text or not back_text:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ từ vựng và nghĩa!")
        return
        
    cards.append({"front": front_text, "back": back_text})
    save_data(cards)
    
    entry_front.delete(0, tk.END)
    entry_back.delete(0, tk.END)
    
    progress_label.config(text=f"Thẻ {current_index + 1} / {len(cards)}")
    messagebox.showinfo("Thành công", "Đã lưu từ vựng mới vào hệ thống!")

root = tk.Tk()
root.title("Smart Flashcard - Học từ vựng thông minh")
root.geometry("450x530")
root.config(bg="#f0f2f5")

title_label = tk.Label(root, text="🧠 SMART FLASHCARD", font=("Arial", 16, "bold"), bg="#f0f2f5", fg="#333")
title_label.pack(pady=10)

progress_label = tk.Label(root, text=f"Thẻ 1 / {len(cards)}", font=("Arial", 12), bg="#f0f2f5", fg="#666")
progress_label.pack(pady=2)

card_label = tk.Label(root, text=cards[0]['front'], font=("Arial", 22, "bold"), bg="white", fg="#333", width=18, height=3, relief="raised", bd=2)
card_label.pack(pady=8)
card_label.bind("<Button-1>", flip_card)

hint_label = tk.Label(root, text="(Bấm vào thẻ để lật xem nghĩa)", font=("Arial", 9, "italic"), bg="#f0f2f5", fg="#888")
hint_label.pack(pady=2)

btn_next = tk.Button(root, text="Đã nhớ / Thẻ tiếp theo ➔", font=("Arial", 11, "bold"), bg="#52c41a", fg="white", padx=10, pady=6, command=next_card)
btn_next.pack(pady=8)

# --- KHUNG NHẬP TỪ VỰNG TỐI ƯU GIAO DIỆN ---
frame_add = tk.LabelFrame(root, text=" Thêm từ vựng mới ", font=("Arial", 10, "bold"), bg="#ffffff", fg="#333", padx=15, pady=10)
frame_add.pack(pady=10, fill="x", padx=30)

tk.Label(frame_add, text="Từ vựng (Mặt trước):", font=("Arial", 9), bg="#ffffff", fg="#333").pack(anchor="w")
entry_front = tk.Entry(frame_add, font=("Arial", 11), bg="#ffffff", fg="#000000", insertbackground="#000000", width=30)
entry_front.pack(pady=3, fill="x")

tk.Label(frame_add, text="Nghĩa (Mặt sau):", font=("Arial", 9), bg="#ffffff", fg="#333").pack(anchor="w")
entry_back = tk.Entry(frame_add, font=("Arial", 11), bg="#ffffff", fg="#000000", insertbackground="#000000", width=30)
entry_back.pack(pady=3, fill="x")

btn_add = tk.Button(frame_add, text="Thêm & Lưu vào hệ thống ➕", font=("Arial", 10, "bold"), bg="#1890ff", fg="white", command=add_new_card)
btn_add.pack(pady=8)

root.mainloop()