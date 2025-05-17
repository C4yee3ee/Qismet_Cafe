import logging
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import DbConfig

class BaristaDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.base_dir = r"C:\Users\ADMIN\Desktop\School Files\PythonProjects\Qismet_Cafe"
        self.python_exec = os.path.join(self.base_dir, ".venv", "Scripts", "python.exe")
        self.title("Qismet Cafe - Barista Dashboard")
        # Set window size
        window_width = 600
        window_height = 700
        # Center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.configure(bg="white")

        header_frame = tk.Frame(self, bg="black")
        header_frame.pack(fill="x")

        tk.Label(header_frame, text="BARISTA DASHBOARD", font=("Poppins", 18, "bold"),
                 bg="black", fg="white", pady=10).pack(side="left", padx=10)

        tk.Button(header_frame, text="Logout", font=("Poppins", 10), bg="red", fg="white",
                  command=self.logout).pack(side="right", padx=10, pady=5)

        container = tk.Frame(self, bg="white")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg="white")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.load_orders()
        self.auto_refresh()

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

    def load_orders(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        try:
            conn = DbConfig.connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT order_id, order_date, order_type, status
                FROM Orders
                WHERE status IN ('Preparing', 'Ready')
                ORDER BY order_date DESC
            """)
            orders = cursor.fetchall()

            # Fetch order items for each order
            order_items = {}
            for order in orders:
                cursor.execute("""
                    SELECT m.name, oi.quantity
                    FROM OrderItems oi
                    JOIN Menu m ON oi.menu_id = m.menu_id
                    WHERE oi.order_id = %s
                """, (order['order_id'],))
                order_items[order['order_id']] = cursor.fetchall()

            cursor.close()
            conn.close()

            if not orders:
                tk.Label(self.scroll_frame, text="No orders in 'Preparing' or 'Ready' status", font=("Poppins", 12), bg="white").pack()
                return

            for order in orders:
                frame = tk.Frame(self.scroll_frame, bd=2, relief="groove", bg="#f8f8f8", padx=10, pady=10)
                frame.pack(fill="x", pady=8)

                order_id = order['order_id']
                timestamp = order['order_date'].strftime("%Y-%m-%d %H:%M:%S") if order['order_date'] else "N/A"
                status = order['status']
                items = order_items.get(order['order_id'], [])
                order_type = order['order_type']

                tk.Label(frame, text=f"Order #{order_id}", font=("Poppins", 14, "bold"), bg="#f8f8f8").pack(anchor="w")
                tk.Label(frame, text=f"Time: {timestamp}", font=("Poppins", 10), bg="#f8f8f8").pack(anchor="w")
                tk.Label(frame, text=f"Type: {order_type}", font=("Poppins", 10), bg="#f8f8f8").pack(anchor="w")

                items_text = "\n".join([f"- {item['name']} x{item['quantity']}" for item in items])
                tk.Label(frame, text=items_text, font=("Poppins", 10), bg="#f8f8f8", justify="left").pack(anchor="w", pady=5)

                tk.Label(frame, text=f"Status: {status}", font=("Poppins", 10, "bold"), fg="green", bg="#f8f8f8").pack(anchor="w")

                btn_frame = tk.Frame(frame, bg="#f8f8f8")
                btn_frame.pack(anchor="e", pady=5)

                if status == 'Preparing':
                    tk.Button(btn_frame, text="Mark Ready", font=("Poppins", 10), bg="orange", fg="white",
                              command=lambda oid=order['order_id']: self.update_status(oid, "Ready")).pack(side="left", padx=5)
                if status == 'Ready':
                    tk.Button(btn_frame, text="Mark Completed", font=("Poppins", 10), bg="green", fg="white",
                              command=lambda oid=order['order_id']: self.update_status(oid, "Completed")).pack(side="left", padx=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load orders: {e}")

    def update_status(self, order_id, new_status):
        try:
            conn = DbConfig.connect()
            cursor = conn.cursor()

            # Update Orders table
            cursor.execute("""
                UPDATE Orders
                SET status = %s
                WHERE order_id = %s
            """, (new_status, order_id))

            # Log the status update in OrderStatusLog
            cursor.execute("SELECT user_id FROM Users WHERE role = 'Barista' LIMIT 1")
            result = cursor.fetchone()
            if not result:
                raise Exception("No barista user found in database")
            barista_id = result[0]
            cursor.execute("""
                INSERT INTO OrderStatusLog (order_id, updated_by, new_status)
                VALUES (%s, %s, %s)
            """, (order_id, barista_id, new_status))

            conn.commit()
            cursor.close()
            conn.close()

            self.load_orders()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update order status: {e}")

    def auto_refresh(self):
        self.load_orders()
        self.after(5000, self.auto_refresh)  # Refresh every 5 seconds

if __name__ == "__main__":
    app = BaristaDashboard()
    app.mainloop()