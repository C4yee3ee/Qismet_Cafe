import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import logging

logging.basicConfig(filename='admin_dashboard.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

try:
    from MenuAndSales import MenuManagement, SalesReport
except ImportError as e:
    logging.error(f"Failed to import MenuAndSales: {e}")
    messagebox.showerror("Error", f"Cannot import MenuAndSales: {e}")
    raise

class AdminDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.base_dir = r"C:\Users\ADMIN\Desktop\School Files\PythonProjects\Qismet_Cafe"
        self.python_exec = os.path.join(self.base_dir, ".venv", "Scripts", "python.exe")
        logging.debug("Initializing AdminDashboard")
        self.title("Qismet Cafe - Admin Dashboard")

        window_width = 1200
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.configure(bg="#d0021b")
        self.current_button = None
        try:
            self.create_widgets()
        except Exception as e:
            logging.error(f"Failed to create widgets: {e}")
            messagebox.showerror("Error", f"Failed to initialize dashboard: {e}")
            self.create_fallback_ui()

    def create_fallback_ui(self):
        logging.debug("Creating fallback UI")
        self.sidebar = tk.Frame(self, bg="#1c2526", width=100)
        self.sidebar.pack(side="left", fill="y")
        self.main_area = tk.Frame(self, bg="#d0021b")
        self.main_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        tk.Label(self.sidebar, text="Admin Dashboard", font=("Poppins", 18, "bold"),
                 bg="#1c2526", fg="white").pack(pady=30)
        tk.Label(self.main_area, text="Dashboard failed to load. Check logs.",
                 font=("Poppins", 12), fg="white", bg="#d0021b").pack(pady=20)

    def create_widgets(self):
        logging.debug("Creating widgets")
        self.sidebar = tk.Frame(self, bg="#1c2526", width=100)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)

        self.main_area = tk.Frame(self, bg="#d0021b")
        self.main_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        tk.Label(self.sidebar, text="Admin Dashboard", font=("Poppins", 18, "bold"),
                 bg="#1c2526", fg="white").pack(pady=30)

        button_style = {
            "font": ("Poppins", 14),
            "bg": "#333333",
            "fg": "white",
            "activebackground": "#222222",
            "activeforeground": "white",
            "bd": 0,
            "relief": "flat",
            "padx": 15,
            "pady": 10
        }

        self.menu_button = tk.Button(self.sidebar, text="Menu Management",
                                     command=lambda: self.show_menu(self.menu_button), **button_style)
        self.menu_button.pack(fill="x", padx=20, pady=10)

        self.sales_button = tk.Button(self.sidebar, text="Sales Report",
                                      command=lambda: self.show_sales(self.sales_button), **button_style)
        self.sales_button.pack(fill="x", padx=20, pady=10)

        self.logout_btn = tk.Button(self.sidebar, text="Log Out",
                                       command=self.logout, **button_style)
        self.logout_btn.pack(fill="x", padx=20, pady=10)

        self.content_frame = None
        self.show_menu(self.menu_button)

    def reset_button_colors(self):
        default_bg = "#333333"
        for button in [self.menu_button, self.sales_button, self.logout_btn]:
            button.config(bg=default_bg)

    def show_menu(self, button):
        logging.debug("Menu Management button clicked")
        self.reset_button_colors()
        button.config(bg="#2a2a2a")
        self.current_button = button
        if self.content_frame:
            self.content_frame.destroy()
        try:
            self.content_frame = MenuManagement(self.main_area)
            self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        except Exception as e:
            logging.error(f"Failed to load MenuManagement: {e}")
            self.content_frame = tk.Frame(self.main_area, bg="#d0021b")
            tk.Label(self.content_frame, text=f"Menu Management failed to load: {e}",
                     font=("Poppins", 12), fg="white").pack(pady=20)
            self.content_frame.pack(fill="both", expand=True)

    def show_sales(self, button):
        logging.debug("Sales Report button clicked")
        self.reset_button_colors()
        button.config(bg="#2a2a2a")
        self.current_button = button
        if self.content_frame:
            self.content_frame.destroy()
        try:
            self.content_frame = SalesReport(self.main_area)
            self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        except Exception as e:
            logging.error(f"Failed to load SalesReport: {e}")
            self.content_frame = tk.Frame(self.main_area, bg="#d0021b")
            tk.Label(self.content_frame, text=f"Sales Report failed to load: {e}",
                     font=("Poppins", 12), fg="white").pack(pady=20)
            self.content_frame.pack(fill="both", expand=True)

    def logout(self):
        login_path = os.path.join(self.base_dir, "LogIn.py")
        if not os.path.exists(login_path):
            logging.error(f"LogIn.py not found at: {login_path}")
            messagebox.showerror("Error", "Cannot find LogIn.py")
            return
        try:
            subprocess.Popen([self.python_exec, login_path], cwd=self.base_dir)
            logging.info("Logged out, launching LogIn.py")
            self.destroy()
        except Exception as e:
            logging.error(f"Failed to launch LogIn.py: {e}")
            messagebox.showerror("Error", f"Failed to launch LogIn.py: {e}")

if __name__ == "__main__":
    try:
        app = AdminDashboard()
        app.mainloop()
    except Exception as e:
        logging.error(f"Application failed to start: {e}")
        print(f"ERROR: Application failed to start: {e}")