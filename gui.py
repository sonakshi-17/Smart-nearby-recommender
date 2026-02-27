import tkinter as tk
from tkinter import ttk, END
from PIL import Image, ImageTk
from recommender import recommend_places

# -------- Window Setup --------
window = tk.Tk()
window.title("Smart Nearby Recommender")
window.geometry("720x520")
window.configure(bg="#1e1e2f")

# -------- Title --------
title = tk.Label(window, text="Smart Nearby Recommender",
                 font=("Arial", 20, "bold"),
                 bg="#1e1e2f", fg="white")
title.pack(pady=10)

# -------- Location Input --------
location_label = tk.Label(window, text="Enter Location:",
                          bg="#1e1e2f", fg="white",
                          font=("Arial", 12))
location_label.pack()

location_entry = tk.Entry(window, width=30)
location_entry.pack(pady=5)

# -------- Mood Selection --------
mood_label = tk.Label(window, text="Select Mood:",
                      bg="#1e1e2f", fg="white",
                      font=("Arial", 12))
mood_label.pack()

mood_combo = ttk.Combobox(window, values=["Work", "Date", "Quick Bite", "Budget"])
mood_combo.pack(pady=5)

# -------- LEFT OUTPUT PANEL --------
output_frame = tk.Frame(window, bg="#1e1e2f")
output_frame.place(x=20, y=180)

output_box = tk.Text(output_frame,
                     height=16,
                     width=45,
                     font=("Arial", 10),
                     bg="#2b2b3c",
                     fg="white",
                     wrap="word",
                     bd=0)
output_box.pack()

# -------- RIGHT IMAGE PANEL --------
image_frame = tk.Frame(window, bg="#1e1e2f")
image_frame.place(x=420, y=180)

image_label = tk.Label(image_frame, bg="#1e1e2f")
image_label.pack()

# -------- Mood Image Mapping --------
def get_mood_image(mood):

    mood_images = {
        "Work": "assets/work.png",
        "Date": "assets/date.gif",
        "Quick Bite": "assets/quick.png",
        "Budget": "assets/budget.png"
    }

    return mood_images.get(mood, "assets/default.png")

# -------- Update Image --------
def update_image(event=None):

    mood = mood_combo.get()
    img_path = get_mood_image(mood)

    try:
        img = Image.open(img_path)
        img = img.resize((220, 220))
        photo = ImageTk.PhotoImage(img)

        image_label.config(image=photo)
        image_label.image = photo
    except:
        pass

mood_combo.bind("<<ComboboxSelected>>", update_image)

# -------- Show Results --------
def show_results():

    location = location_entry.get()
    mood = mood_combo.get()

    results = recommend_places(location, mood)

    output_box.delete(1.0, END)

    if not results:
        output_box.insert(END, "No places found 😔")
        return

    for place in results:
        output_box.insert(END,
        f"""
🍽️ {place['name']}
📍 {place['area']}
🏠 {place['address']}
💰 {place['cost']}
----------------------------
""")

# -------- Button --------
search_button = tk.Button(window, text="Find Places",
                          command=show_results,
                          bg="#ff4d6d", fg="white")
search_button.pack(pady=10)

# -------- Start GUI --------
def start_gui():
    window.mainloop()