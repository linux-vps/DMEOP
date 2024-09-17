from tkinter import Tk, Canvas, PhotoImage, Frame, Entry, Button
from pathlib import Path
from PIL import Image, ImageTk
import threading
import pickle
import subprocess
import sys

# Thêm thư mục gốc vào sys.path
sys.path.append(str(Path(__file__).parent.parent))

from automation.eop_manager import main

def create_gui():
    def relative_to_assets(path: str) -> Path:
        return Path(__file__).parent / "assets" / path

    login_info = Path("./eop_login_info.pkl")

    def initialize_window():
        window = Tk()
        window.title("ĐM EOP")
        icon_path = relative_to_assets("icon.ico")
        icon = Image.open(icon_path)
        icon = ImageTk.PhotoImage(icon)
        window.iconbitmap(icon_path)
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = 1444
        window_height = 670
        x = int(screen_width / 2 - window_width / 2)
        y = int(screen_height / 2 - window_height / 2)
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        window.configure(bg="#E8E8E8")
        
        return window
    
    def clearAll():
        for i in range(6):
            for field in ["username", "password", "name", "progress", "note"]:
                entries[i][field].delete(0, "end")
        save_info_to_storage()

    def save_info_to_storage():
        data = {}
        for i in range(6):
            for field in ["username", "password", "name", "progress", "note"]:
                entry = entries[i][field]
                data[f'{field}_{i}'] = entry.get()
        with open(login_info, 'wb') as f:
            pickle.dump(data, f)

    def runNow(username, password, randomFrom, randomTo):
        if not username or not password:
            return
        # print(username, password)
        save_info_to_storage()
        # truyền username, password vào bên xử lý tự động
        main(username, password, randomFrom, randomTo)
        return username, password

    def setup_canvas(window):
        canvas = Canvas(window, bg="#FFE1CC", height=780, width=1444, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        background_img_path = relative_to_assets("background.png")
        background_img = PhotoImage(file=background_img_path)
        canvas.create_image(0.0, 0.0, image=background_img, anchor="nw")
        canvas.background_img = background_img  # Keep a reference to avoid garbage collection

        return canvas

    def create_entries(frame, index, login_data):
        entries = {}
        fields = ["username", "password", "name", "progress", "note"]
        entry_widths = [125, 146, 187, 186, 296]  # Widths for each field
        x_positions = [55, 233, 445, 698, 950]  # X positions for each field
        
        for i, field in enumerate(fields):
            entry = Entry(frame, bd=0, bg="#EDEDED", fg="#000716", highlightthickness=0, show="*" if field == "password" else "")
            entry.place(x=x_positions[i], y=132.0 + index * 59, width=entry_widths[i], height=27.0)
            entry.insert(0, login_data.get(f'{field}_{index}', ''))
            entries[field] = entry
        return entries
    
    def create_buttons(frame, index):
        start_img = PhotoImage(file=relative_to_assets("start.png"))
        start_btn = Button(frame, image=start_img, borderwidth=0, highlightthickness=0,
                        command=lambda: threading.Thread(target=runNow,
                                                            args=(entries[index]["username"].get(), 
                                                                entries[index]["password"].get(),
                                                                globals()["randomFrom"].get(),
                                                                globals()["randomTo"].get(),
                                                                )).start(),

                        relief="flat")
        start_btn.place(x=1306.0, y=128.0 + index * 59, width=94, height=37.0)
        start_btn.start_img = start_img  # Keep a reference to avoid garbage collection
        return start_btn


    def create_clear_button(window):
        clear_img = PhotoImage(file=relative_to_assets("clear.png"))
        clear_btn = Button(window, image=clear_img, borderwidth=0, highlightthickness=0, command=clearAll, relief="flat")
        clear_btn.place(x=1229, y=11, width=124, height=37.0)
        clear_btn.clear_img = clear_img  # Keep a reference to avoid garbage collection
        return clear_btn

    def load_login_data():
        if login_info.exists():
            with open(login_info, 'rb') as f:
                return pickle.load(f)
        return {}

    window = initialize_window()
    canvas = setup_canvas(window)
    login_data = load_login_data()

    globals()["randomFrom"] = Entry(bd=0,bg="#fff",fg="#000716",highlightthickness=0)
    globals()["randomFrom"].place(x=936,y=27,width=45,height=25)
    globals()["randomFrom"].insert(0, 30)
    
    globals()["randomTo"] = Entry(bd=0,bg="#fff",fg="#000716",highlightthickness=0)
    globals()["randomTo"].place(x=1031,y=27,width=45,height=25)
    globals()["randomTo"].insert(0, 60)
    
    import webbrowser

    github_img = PhotoImage(file=relative_to_assets("github_in4.png"))
    github_btn = Button(window, image=github_img, borderwidth=0, highlightthickness=0,
                        command=lambda: webbrowser.open_new("https://github.com/linux-vps"),
                        )
    github_btn.place(x=960, y=530)
    github_btn.github_img = github_img  # Keep a reference to avoid garbage collection
    
    
    facebook_img = PhotoImage(file=relative_to_assets("facebook_in4.png"))
    facebook_btn = Button(window, image=facebook_img, borderwidth=0, highlightthickness=0,
                        command=lambda: webbrowser.open_new("https://www.facebook.com/groups/370817769403735"),
                        )
    facebook_btn.place(x=1200, y=530)
    facebook_btn.facebook_img = facebook_img  # Keep a reference to avoid garbage collection


    entries = []
    for i in range(6):
        frame = Frame(window, bg="#E8E8E8")
        frame.grid(row=i, column=0, sticky="nsew", padx=23, pady=23)
        window.grid_rowconfigure(i, weight=1)
        entries.append(create_entries(window, i, login_data))
        create_buttons(window, i)

    create_clear_button(window)
    
    window.resizable(False, False)
    window.mainloop()


