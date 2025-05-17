import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os
import subprocess
import logging
import sys

logging.basicConfig(filename='menu_dashboard.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

DB_CONFIG = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'qismet_cafe',
    'raise_on_warnings': True
}

class MenuDashboard(tk.Toplevel):
    def __init__(self, master=None, pin=None, user_id=None):
        super().__init__(master)
        self.title("Qismet Cafe - Menu")
        self.geometry("1000x760")
        self.configure(bg="white")
        self.resizable(False, False)

        # Center the window on the screen
        self.update_idletasks()  # Update geometry to get accurate screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 1000
        window_height = 760
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        if len(sys.argv) > 2:
            self.pin = sys.argv[1]
            self.user_id = int(sys.argv[2])
        else:
            self.pin = pin if pin else "2345"
            self.user_id = user_id if user_id else 2

        self.base_dir = r"C:\Users\ADMIN\Desktop\School Files\PythonProjects\Qismet_Cafe"
        self.selected_item = None
        self.quantity = 1
        self.temp = "HOT"
        self.size = "MEDIUM"
        self.flavor = tk.StringVar(value="")
        self.selected_category = "Coffee"
        self.dine_option = "Dine In"
        self.cart_data = []
        self.python_exec = os.path.join(self.base_dir, ".venv", "Scripts", "python.exe")

        self.products = []
        self.load_products()

        self.create_widgets()
        self.left_frame.pack_forget()

    def load_products(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT m.menu_id, m.name, m.price, m.size, m.image, m.flavors, c.name AS category
                FROM Menu m
                JOIN Categories c ON m.category_id = c.category_id
                WHERE m.is_hidden = FALSE
            """)
            menu_items = cursor.fetchall()
            cursor.close()
            conn.close()

            product_dict = {}
            for item in menu_items:
                name = item['name']
                if name not in product_dict:
                    # Split flavors if they exist, otherwise use empty list
                    flavors = item['flavors'].split(',') if item['flavors'] else []
                    product_dict[name] = {
                        "name": name,
                        "category": item['category'],
                        "image": item['image'],
                        "price": {},
                        "flavors": flavors
                    }
                if item['size']:
                    product_dict[name]["price"][item['size']] = item['price']
                else:
                    product_dict[name]["price"] = item['price']

            self.products = list(product_dict.values())
            for product in self.products:
                logging.info(
                    f"Loaded product: {product['name']}, Category: {product['category']}, Flavors: {product['flavors']}")
        except mysql.connector.Error as e:
            messagebox.showwarning("Warning", f"Failed to load products: {e}")
            logging.error(f"Database error: {e}")
            self.products = []

    def create_widgets(self):
        # Left frame with scrollable canvas
        self.left_frame = tk.Frame(self, bg="black", width=400, height=700)
        self.left_frame.pack_propagate(False)

        self.left_canvas = tk.Canvas(self.left_frame, bg="black", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.left_frame, orient="vertical", command=self.left_canvas.yview)
        self.left_content = tk.Frame(self.left_canvas, bg="black", width=400)

        self.left_content.bind("<Configure>",
                               lambda e: self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all")))
        self.left_canvas.create_window((200, 0), window=self.left_content, anchor="n")
        self.left_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.left_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Logo (emoji label)
        logo_frame = tk.Frame(self.left_content, bg="black")
        logo_frame.pack(pady=10, padx=170)
        tk.Label(logo_frame, text=" ", bg="black", fg="white", font=("Poppins", 16)).pack()

        # Item Title
        self.item_title = tk.Label(self.left_content, text="", bg="black", fg="white", font=("Poppins", 24, "bold"))
        self.item_title.pack(pady=10, padx=20)

        # Item Image (200x200)
        self.item_image_label = tk.Label(self.left_content, bg="black")
        self.item_image_label.pack(pady=10, padx=100)

        # Temperature Options (only for Coffee)
        self.temp_label = tk.Label(self.left_content, text="Temperature", bg="black", fg="white",
                                   font=("Poppins", 12, "bold"))
        self.temp_var = tk.StringVar(value="HOT")
        self.temp_frame = tk.Frame(self.left_content, bg="black")
        for temp in ["HOT", "ICED"]:
            btn = tk.Button(self.temp_frame, text=temp, command=lambda t=temp: self.temp_var.set(t),
                            font=("Poppins", 12, "bold"), bg="#808080", fg="white", width=10,
                            activebackground="#D0021B", activeforeground="white")
            btn.pack(side="left", padx=5, pady=5)
        self.temp_frame.pack(pady=5, padx=85)

        # Size Options (for Coffee and Non-Coffee)
        self.size_label = tk.Label(self.left_content, text="Size", bg="black", fg="white", font=("Poppins", 12, "bold"))
        self.size_frame = tk.Frame(self.left_content, bg="black")
        self.size_var = tk.StringVar(value="MEDIUM")
        for size in ["SMALL", "MEDIUM", "LARGE"]:
            btn = tk.Button(self.size_frame, text=size, command=lambda s=size: self.size_var.set(s),
                            font=("Poppins", 12, "bold"), bg="#808080", fg="white", width=10,
                            activebackground="#D0021B", activeforeground="white")
            btn.pack(side="left", padx=5, pady=5)
        self.size_frame.pack(pady=5, padx=25)

        # Flavor Label (for Pastries)
        self.flavor_label = tk.Label(self.left_content, text="Flavor", bg="black", fg="white",
                                     font=("Poppins", 12, "bold"))
        self.flavor_frame = tk.Frame(self.left_content, bg="black")

        # Quantity Controls
        tk.Label(self.left_content, text="Quantity", bg="black", fg="white", font=("Poppins", 12, "bold")).pack(pady=5,
                                                                                                                padx=160)
        qty_frame = tk.Frame(self.left_content, bg="black")
        qty_frame.pack(padx=125)
        minus_btn = tk.Button(qty_frame, text="-", font=("Poppins", 12, "bold"), bg="#D0021B", fg="white",
                              command=self.decrease_qty, width=5)
        minus_btn.pack(side="left", padx=5)
        self.qty_label = tk.Label(qty_frame, text=str(self.quantity), font=("Poppins", 12, "bold"),
                                  bg="white", fg="black", width=5, relief="sunken")
        self.qty_label.pack(side="left", padx=5)
        plus_btn = tk.Button(qty_frame, text="+", font=("Poppins", 12, "bold"), bg="#D0021B", fg="white",
                             command=self.increase_qty, width=5)
        plus_btn.pack(side="left", padx=5)

        # Price Labels
        self.price_label = tk.Label(self.left_content, text="", bg="black", fg="white", font=("Poppins", 12))
        self.price_label.pack(pady=5, padx=20)

        self.total_price_label = tk.Label(self.left_content, text="", bg="black", fg="white",
                                          font=("Poppins", 15, "bold"))
        self.total_price_label.pack(pady=5, padx=20)

        # Add to Cart Button (Fixed: Added command=self.add_to_cart)
        self.add_cart_btn = tk.Button(self.left_content, text="Add to Cart", bg="#D0021B", fg="white",
                                      font=("Poppins", 16, "bold"), height=2, command=self.add_to_cart)
        self.add_cart_btn.pack(fill="x", pady=10, padx=20)

        # Right frame
        self.right_frame = tk.Frame(self, bg="white", width=600, height=700)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Header Frame (Cart and Logo Icons)
        header_frame = tk.Frame(self.right_frame, bg="white")
        header_frame.pack(fill="x", pady=10, padx=15)
        try:
            cart_icon = ImageTk.PhotoImage(Image.open(os.path.join(self.base_dir, "cart.png")).resize((40, 40)))
            cart_button = tk.Button(header_frame, image=cart_icon, bg="white", bd=0, command=self.open_cart)
            cart_button.image = cart_icon
            cart_button.pack(side="right", padx=10)
        except Exception as e:
            logging.error(f"Cart icon load error: {e}")
            tk.Button(header_frame, text="Cart", bg="white", font=("Poppins", 12), command=self.open_cart).pack(
                side="right", padx=10)
        try:
            logo_icon = ImageTk.PhotoImage(Image.open(os.path.join(self.base_dir, "menulogo.png")).resize((40, 40)))
            logo_button = tk.Button(header_frame, image=logo_icon, bg="white", bd=0)
            logo_button.image = logo_icon
            logo_button.pack(side="right", padx=10)
        except Exception as e:
            logging.error(f"Logo icon load error: {e}")
            tk.Button(header_frame, text="Logo", bg="white", font=("Poppins", 12)).pack(side="right", padx=10)

        # Category Frame (Centered)
        category_frame = tk.Frame(self.right_frame, bg="white")
        category_frame.pack(pady=10, anchor="center")
        category_inner_frame = tk.Frame(category_frame, bg="white")
        category_inner_frame.pack()
        for cat in ["Coffee", "Non-Coffee", "Pastries"]:
            btn = tk.Button(category_inner_frame, text=cat, font=("Poppins", 12, "bold"),
                            bg="black", fg="white", width=12, relief="flat",
                            command=lambda c=cat: self.filter_by_category(c))
            btn.pack(side="left", padx=10, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#D0021B"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="black"))

        # Grid Frame (Centered Product Grid)
        self.grid_frame = tk.Frame(self.right_frame, bg="white")
        self.grid_frame.pack(pady=10, padx=15, anchor="center")

        # Dine Frame (Centered)
        self.dine_frame = tk.Frame(self.right_frame, bg="white")
        self.dine_frame.pack(pady=10, anchor="center")
        dine_inner_frame = tk.Frame(self.dine_frame, bg="white")
        dine_inner_frame.pack()

        # Dine In/Take Out buttons with pressed state
        self.dine_in_btn = tk.Button(dine_inner_frame, text="Dine In", font=("Poppins", 12), bg="#D3D3D3", fg="black",
                                     width=10, relief="raised", command=lambda: self.set_dine_option("Dine In"))
        self.dine_in_btn.pack(side="left", padx=5)
        self.take_out_btn = tk.Button(dine_inner_frame, text="Take Out", font=("Poppins", 12), bg="#D3D3D3", fg="black",
                                      width=10, relief="raised", command=lambda: self.set_dine_option("Take Out"))
        self.take_out_btn.pack(side="left", padx=5)

        # Set initial pressed state for "Dine In"
        self.dine_in_btn.config(relief="sunken", bg="#A9A9A9")

        # Log Out Button (Centered)
        logout_btn = tk.Button(self.right_frame, text="Log Out", font=("Poppins", 14, "bold"),
                               bg="#D0021B", fg="white", command=self.log_out,
                               padx=15, pady=8, relief="flat")
        logout_btn.pack(side="bottom", pady=10, anchor="center")
        logout_btn.bind("<Enter>", lambda e: logout_btn.config(bg="#B00217"))
        logout_btn.bind("<Leave>", lambda e: logout_btn.config(bg="#D0021B"))

        self.display_products()

    def set_dine_option(self, option):
        self.dine_option = option
        # Update dine_option in cart_data
        for item in self.cart_data:
            item["dine_option"] = self.dine_option
        logging.info(f"Dine option set to: {self.dine_option}")
        # Update UI buttons if needed
        if option == "Dine In":
            self.dine_in_btn.config(relief="sunken", bg="#A9A9A9")
            self.take_out_btn.config(relief="raised", bg="#D3D3D3")
        else:
            self.dine_in_btn.config(relief="raised", bg="#D3D3D3")
            self.take_out_btn.config(relief="sunken", bg="#A9A9A9")

    def filter_by_category(self, category):
        self.selected_category = category
        self.display_products()

    def display_products(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        row = col = 0
        products_in_category = [p for p in self.products if p["category"] == self.selected_category]
        total_products = len(products_in_category)

        if total_products == 1:
            col = 1
        elif total_products == 2:
            col = 0
        else:
            col = 0

        for i, product in enumerate(products_in_category):
            try:
                frame = tk.Frame(self.grid_frame, bg="#D3D3D3", padx=5, pady=5)
                frame.grid(row=row, column=col, padx=10, pady=10)
                inner_frame = tk.Frame(frame, bg="white", padx=10, pady=10)
                inner_frame.pack()

                img = Image.open(os.path.join(self.base_dir, product["image"])).resize((120, 120), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(inner_frame, image=photo, bg="white")
                img_label.image = photo
                img_label.pack(pady=5)

                tk.Label(inner_frame, text=product["name"], font=("Poppins", 12, "bold"),
                         bg="white", fg="#D0021B", wraplength=120).pack(pady=5)
                price = product["price"]["MEDIUM"] if isinstance(product["price"], dict) else product["price"]
                tk.Label(inner_frame, text=f"₱ {price}", font=("Poppins", 10, "bold"),
                         bg="white", fg="black").pack()

                img_label.bind("<Button-1>", lambda e, p=product: self.update_preview(p))
                inner_frame.bind("<Button-1>", lambda e, p=product: self.update_preview(p))

                col += 1
                if col >= 3 or (total_products == 2 and col >= 2):
                    col = 0 if total_products >= 3 else 1
                    row += 1
            except Exception as e:
                logging.error(f"Image load error for {product['image']}: {e}")
                continue

    def update_preview(self, product):
        self.selected_item = product
        self.left_frame.pack(side="left", fill="y")
        self.item_title.config(text=product["name"])
        try:
            img = Image.open(os.path.join(self.base_dir, product["image"])).resize((200, 200), Image.LANCZOS)
            self.item_img = ImageTk.PhotoImage(img)
            self.item_image_label.config(image=self.item_img)
        except Exception as e:
            logging.error(f"Preview image load error for {product['image']}: {e}")
            self.item_image_label.config(image="")

        self.quantity = 1
        self.temp_var.set("HOT")
        self.size_var.set("MEDIUM")
        self.qty_label.config(text=str(self.quantity))

        self.temp_frame.pack_forget()
        self.size_frame.pack_forget()
        self.flavor_frame.pack_forget()
        self.flavor_label.pack_forget()
        self.temp_label.pack_forget()
        self.size_label.pack_forget()

        if product["category"] == "Coffee":
            self.temp_label.pack(pady=5, padx=160)
            self.temp_frame.pack(pady=5, padx=85)
            self.size_label.pack(pady=5, padx=175)
            self.size_frame.pack(pady=5, padx=25)
        elif product["category"] == "Non-Coffee":
            self.size_label.pack(pady=5, padx=175)
            self.size_frame.pack(pady=5, padx=25)
        elif product["category"] == "Pastries":
            self.flavor_label.pack(pady=5, padx=165)
            self.flavor_frame.pack(pady=5, padx=30)  # Adjusted for larger radio buttons
            for widget in self.flavor_frame.winfo_children():
                widget.destroy()
            self.flavor.set("")
            if product["flavors"]:
                for flavor in product["flavors"]:
                    tk.Radiobutton(self.flavor_frame, text=flavor, variable=self.flavor, value=flavor,
                                   bg="black", fg="white", selectcolor="#D0021B", font=("Poppins", 16),
                                   activebackground="black", activeforeground="white").pack(anchor="w", padx=10, pady=5)
                if product["flavors"]:
                    self.flavor.set(product["flavors"][0])
            else:
                tk.Label(self.flavor_frame, text="No flavors available", bg="black", fg="gray",
                         font=("Poppins", 12)).pack(pady=5)

        self.update_price_labels()
        self.left_canvas.yview_moveto(0)

    def update_price_labels(self):
        if not self.selected_item:
            return
        unit_price = self.selected_item["price"][self.size_var.get()] if isinstance(self.selected_item["price"],
                                                                                    dict) else self.selected_item[
            "price"]
        total_price = unit_price * self.quantity
        self.price_label.config(text=f"Unit Price: ₱ {unit_price}")
        self.total_price_label.config(text=f"Total: ₱ {total_price}")

    def increase_qty(self):
        self.quantity += 1
        self.qty_label.config(text=str(self.quantity))
        self.update_price_labels()

    def decrease_qty(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.qty_label.config(text=str(self.quantity))
        self.update_price_labels()

    def add_to_cart(self):
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select an item to add to cart.")
            return

        cart_item = {
            "name": self.selected_item["name"],
            "category": self.selected_item["category"],
            "size": self.size_var.get() if self.selected_item["category"] in ["Coffee", "Non-Coffee"] else None,
            "temperature": self.temp_var.get() if self.selected_item["category"] == "Coffee" else None,
            "flavor": self.flavor.get() if self.selected_item["category"] == "Pastries" else None,
            "price": float(
                self.selected_item["price"][self.size_var.get()] if isinstance(self.selected_item["price"], dict) else
                self.selected_item["price"]),
            "quantity": self.quantity,
            "dine_option": self.dine_option,
            "image": self.selected_item["image"]
        }

        for existing_item in self.cart_data:
            if (existing_item["name"] == cart_item["name"] and
                    existing_item["size"] == cart_item["size"] and
                    existing_item["temperature"] == cart_item["temperature"] and
                    existing_item["flavor"] == cart_item["flavor"]):
                existing_item["quantity"] += cart_item["quantity"]
                break
        else:
            self.cart_data.append(cart_item)

        messagebox.showinfo("Success", f"{cart_item['name']} added to cart!")
        self.left_frame.pack_forget()
        logging.info(f"Added to cart: {cart_item}")

    def open_cart(self):
        try:
            logging.info(f"Opening cart for PIN: {self.pin} with {len(self.cart_data)} items, user_id: {self.user_id}")
            from CartScreen import CartScreen
            cart_screen = CartScreen(master=self, pin=self.pin, cart_data=self.cart_data, user_id=self.user_id)
            cart_screen.update()
        except Exception as e:
            logging.error(f"Error opening cart: {e}")
            messagebox.showerror("Error", f"Failed to open cart: {str(e)}")

    def log_out(self):
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
    root = tk.Tk()
    root.withdraw()
    app = MenuDashboard(master=root, pin="2345")
    app.mainloop()