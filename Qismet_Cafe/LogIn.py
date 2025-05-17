import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
from PIL import Image, ImageTk, ImageDraw
import os
import subprocess
import mysql.connector
import logging

logging.basicConfig(filename='login.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

DB_CONFIG = {
    'user': 'root',
    'password': '',  # Update with your MySQL password if needed
    'host': '127.0.0.1',
    'database': 'qismet_cafe',
    'raise_on_warnings': True
}

IMAGES = {
    "Admin": "admin.jpg",
    "Customer": "customer.jpg",
    "Barista": "barista.jpg"
}

LOGO_IMAGE = "logo.jpg"

BASE_DIR = r"C:\Users\ADMIN\Desktop\School Files\PythonProjects\Qismet_Cafe"
PYTHON_EXEC = os.path.join(BASE_DIR, ".venv", "Scripts", "python.exe")

def load_custom_font(font_path="Poppins-Regular.ttf", font_family="Poppins"):
    font_path = os.path.join(BASE_DIR, font_path)
    if os.path.exists(font_path):
        try:
            tkFont.Font(family=font_family, size=12)
            return font_family
        except Exception as e:
            logging.error(f"Font load error: {e}")
    return "Helvetica"

def circular_crop(img_path, size):
    img_path = os.path.join(BASE_DIR, img_path)
    try:
        img = Image.open(img_path).resize(size).convert("RGBA")
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        img.putalpha(mask)
        border_size = 6
        bordered_size = (size[0] + border_size * 2, size[1] + border_size * 2)
        bordered_img = Image.new("RGBA", bordered_size, (0, 0, 0, 0))
        border_draw = ImageDraw.Draw(bordered_img)
        border_draw.ellipse((0, 0, bordered_size[0], bordered_size[1]), fill="green")
        bordered_img.paste(img, (border_size, border_size), mask=img)
        return ImageTk.PhotoImage(bordered_img)
    except Exception as e:
        logging.error(f"Image processing error for {img_path}: {e}")
        return None

class QismetCafe:
    def __init__(self, root):
        self.root = root
        self.root.title("QISMET Operator Login")
        self.root.configure(bg="white")
        # Set window size
        window_width = 500
        window_height = 550
        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.current_operator = None
        self.pin_input = ""
        self.font_family = load_custom_font()
        self.pin_display = None
        self.keypad_buttons = []
        self.app_running = True
        self.create_operator_screen()

    def clear_window(self):
        if not self.app_running:
            return
        for widget in self.root.winfo_children():
            widget.destroy()
        self.pin_display = None
        self.keypad_buttons = []

    def create_operator_screen(self):
        if not self.app_running:
            return
        self.clear_window()
        header = tk.Frame(self.root, bg="black", height=30)
        header.pack(fill="x")
        try:
            logo = Image.open(os.path.join(BASE_DIR, LOGO_IMAGE)).resize((300, 250))
            logo_photo = ImageTk.PhotoImage(logo)
            logo_label = tk.Label(header, image=logo_photo, bg="black")
            logo_label.image = logo_photo
            logo_label.pack(pady=20)
        except Exception as e:
            logging.error(f"Logo load error: {e}")
            tk.Label(header, text="LOGO", bg="black", fg="white", font=(self.font_family, 18)).pack(pady=30)

        body = tk.Frame(self.root, bg="red")
        body.pack(expand=True, fill="both")
        tk.Label(body, text="Select Operator", font=(self.font_family, 18, "italic"), fg="white", bg="red").pack(
            pady=10)
        btn_frame = tk.Frame(body, bg="red")
        btn_frame.pack(pady=20)
        for operator in ["Admin", "Customer", "Barista"]:
            image = circular_crop(IMAGES[operator], (100, 100))
            if image:
                op_frame = tk.Frame(btn_frame, bg="red")
                op_frame.pack(side="left", padx=20)
                btn = tk.Button(op_frame, image=image, bg="red", bd=0,
                                activebackground="red",
                                command=lambda op=operator: self.create_pin_screen(op))
                btn.image = image
                btn.pack()

    def create_pin_screen(self, operator):
        if not self.app_running:
            return
        self.current_operator = operator
        self.pin_input = ""
        self.clear_window()
        image = circular_crop(IMAGES[operator], (120, 120))
        if image:
            tk.Label(self.root, image=image).pack(pady=15)
            self.image_ref = image
        tk.Label(self.root, text="Please enter the 4 digit PIN",
                 font=(self.font_family, 12, "bold")).pack(pady=10)
        self.pin_display = tk.Entry(self.root, font=(self.font_family, 24), justify="center",
                                    show="*", width=10, bd=2, relief="solid")
        self.pin_display.pack(pady=10)
        keypad_frame = tk.Frame(self.root)
        keypad_frame.pack()
        buttons = [
            ["1", "2", "3", "4"],
            ["5", "6", "7", "8"],
            ["⌫", "9", "0", "Enter"]
        ]
        self.keypad_buttons = []
        for row in buttons:
            row_frame = tk.Frame(keypad_frame)
            row_frame.pack(pady=5)
            for char in row:
                btn = tk.Button(row_frame, text=char, font=(self.font_family, 18),
                                bg="red", fg="white", width=4, height=2,
                                command=lambda c=char: self.handle_key(c))
                btn.pack(side="left", padx=5)
                self.keypad_buttons.append(btn)

    def handle_key(self, char):
        if not self.app_running or not self.pin_display or not self.pin_display.winfo_exists():
            logging.warning("PIN display widget is invalid or application is destroyed")
            return
        try:
            if char == "⌫":
                self.pin_input = self.pin_input[:-1]
            elif char == "Enter":
                self.verify_pin()
            elif char.isdigit() and len(self.pin_input) < 4:
                self.pin_input += char
            if self.pin_display.winfo_exists():
                self.pin_display.delete(0, tk.END)
                self.pin_display.insert(0, "*" * len(self.pin_input))
        except tk.TclError as e:
            logging.error(f"TclError in handle_key: {e}")
            if self.app_running:
                messagebox.showerror("Error", "An error occurred while processing input. Please try again.")
                self.create_operator_screen()

    def verify_pin(self):
        if not self.app_running:
            return
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, role FROM Users WHERE pin = %s", (self.pin_input,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result:
                user_id, role = result
                if role.lower() == self.current_operator.lower():
                    for btn in self.keypad_buttons:
                        btn.config(state="disabled")
                    self.launch_dashboard(role, user_id)
                else:
                    messagebox.showerror("Access Denied", "PIN does not match selected operator!")
                    self.create_operator_screen()
            else:
                messagebox.showerror("Access Denied", "Invalid PIN!")
                self.create_operator_screen()
        except mysql.connector.Error as e:
            logging.error(f"Database error: {e}")
            messagebox.showerror("Error", f"Database error: {e}")
            self.create_operator_screen()

    def launch_dashboard(self, role, user_id):
        self.app_running = False
        dashboard_files = {
            "customer": "MenuDashboard.py",
            "barista": "BaristaDashboard.py",
            "admin": "AdminDashboard.py"
        }
        dashboard_file = dashboard_files.get(role.lower())
        dashboard_path = os.path.join(BASE_DIR, dashboard_file)

        if not os.path.exists(dashboard_path):
            logging.error(f"Dashboard file not found: {dashboard_path}")
            messagebox.showerror("Error", f"Cannot launch {dashboard_file}: File not found in {BASE_DIR}")
            self.create_operator_screen()
            self.app_running = True
            return

        if not os.path.exists(PYTHON_EXEC):
            logging.error(f"Python executable not found: {PYTHON_EXEC}")
            messagebox.showerror("Error", f"Python executable not found at {PYTHON_EXEC}")
            self.create_operator_screen()
            self.app_running = True
            return

        try:
            logging.info(f"Launching {dashboard_file} with {PYTHON_EXEC}")
            if role.lower() == "customer":
                subprocess.Popen([PYTHON_EXEC, dashboard_path, self.pin_input, str(user_id)], cwd=BASE_DIR)
            else:
                subprocess.Popen([PYTHON_EXEC, dashboard_path], cwd=BASE_DIR)
            logging.info(f"Launched {dashboard_file} for role: {role}, PIN: {self.pin_input}, user_id: {user_id}")
            self.root.after(1000, self.root.destroy)  # Delay destruction to ensure subprocess starts
        except Exception as e:
            logging.error(f"Failed to launch {dashboard_file}: {e}")
            messagebox.showerror("Error", f"Failed to launch {dashboard_file}: {e}")
            self.create_operator_screen()
            self.app_running = True


if __name__ == "__main__":
    root = tk.Tk()
    app = QismetCafe(root)
    root.mainloop()