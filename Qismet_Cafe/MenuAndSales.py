import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from tkinter import font as tkFont
import os
import mysql.connector
import logging
import shutil

logging.basicConfig(filename='menu_sales.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

DB_CONFIG = {
    'user': 'root',
    'password': '',  # Update with your MySQL password if required
    'host': '127.0.0.1',
    'database': 'qismet_cafe',
    'raise_on_warnings': True
}

class MenuManagement(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        self.base_dir = r"C:\Users\ADMIN\Desktop\School Files\PythonProjects\Qismet_Cafe"
        # Ensure base_dir exists
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
            logging.debug(f"Created base_dir: {self.base_dir}")
        self.selected_category = tk.StringVar(value="Coffee")
        self.search_var = tk.StringVar()
        self.products = []
        self.load_products()
        self.build_ui()
        self.render_products()

    def load_products(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT m.menu_id, m.name, m.price, m.size, m.image, m.flavors, m.is_hidden, c.name AS category
                FROM Menu m
                JOIN Categories c ON m.category_id = c.category_id
            """)
            menu_items = cursor.fetchall()
            cursor.close()
            conn.close()

            product_dict = {}
            for item in menu_items:
                name = item['name']
                if name not in product_dict:
                    flavors = item['flavors'].split(',') if item['flavors'] else []
                    product_dict[name] = {
                        "menu_ids": [],
                        "name": name,
                        "category": item['category'],
                        "image": item['image'],
                        "price": {},
                        "flavors": flavors,
                        "is_hidden": item['is_hidden']
                    }
                    logging.debug(f"Loaded product {name} with flavors: {flavors}")
                product_dict[name]["menu_ids"].append(item['menu_id'])
                if item['size']:
                    product_dict[name]["price"][item['size']] = item['price']
                else:
                    product_dict[name]["price"] = item['price']

            self.products = list(product_dict.values())
            logging.debug(f"Loaded {len(self.products)} products")
        except mysql.connector.Error as e:
            logging.error(f"Database error in load_products: {e}")
            messagebox.showwarning("Warning", f"Failed to load products: {e}")
            self.products = []

    def build_ui(self):
        tk.Label(self, text="MENU MANAGEMENT", font=("Poppins", 20, "bold"), bg="white").pack(pady=20)

        control_frame = tk.Frame(self, bg="white")
        control_frame.pack(fill="x", padx=20, pady=10)

        for category in ["Coffee", "Non-Coffee", "Pastries"]:
            btn = tk.Radiobutton(control_frame, text=category, variable=self.selected_category,
                                 value=category, indicatoron=0, width=12, command=self.render_products,
                                 font=("Poppins", 12), bg="#ececec", selectcolor="#d5d5d5")
            btn.pack(side="left", padx=5, pady=5)

        tk.Entry(control_frame, textvariable=self.search_var, width=30, font=("Poppins", 12)).pack(side="left", padx=10)
        tk.Button(control_frame, text="Search", font=("Poppins", 12), bg="#333333", fg="white",
                  command=self.render_products).pack(side="left")
        tk.Button(control_frame, text="Create", font=("Poppins", 12), bg="blue", fg="white",
                  command=self.open_create_popup).pack(side="right")

        self.list_frame = tk.Frame(self, bg="white")
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.canvas = tk.Canvas(self.list_frame, bg="white")
        self.scrollbar = tk.Scrollbar(self.list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def render_products(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        keyword = self.search_var.get().lower()
        for index, product in enumerate(self.products):
            if product["category"] != self.selected_category.get():
                continue
            if keyword and keyword not in product["name"].lower():
                continue

            frame = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="solid")
            frame.pack(fill="x", padx=5, pady=5)

            try:
                img_path = os.path.join(self.base_dir, product["image"])
                if not os.path.exists(img_path):
                    raise FileNotFoundError(f"Image file {img_path} not found")
                img = Image.open(img_path)
                img = img.resize((60, 60))
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(frame, image=photo, bg="white")
                img_label.image = photo
            except Exception as e:
                logging.error(f"Image load error for {product['image']} at {img_path}: {e}")
                img_label = tk.Label(frame, text="[No Image]", width=10, bg="white")
            img_label.pack(side="left", padx=10)

            info_text = f"{product['name']}\n"
            if isinstance(product['price'], dict):
                price_list = ", ".join([f"{k}: ₱{v}" for k, v in product['price'].items()])
            else:
                price_list = f"₱{product['price']}"
            info_text += f"Price: {price_list}"
            if product['flavors']:
                info_text += f"\nFlavors: {', '.join(product['flavors'])}"
            if product['is_hidden']:
                info_text += f"\n[Hidden]"

            tk.Label(frame, text=info_text, bg="white", justify="left", font=("Poppins", 12)).pack(side="left", padx=10)

            tk.Button(frame, text="Hide" if not product['is_hidden'] else "Unhide", bg="#333333", fg="white",
                      font=("Poppins", 10),
                      command=lambda i=index: self.toggle_hide(i)).pack(side="right", padx=5)
            tk.Button(frame, text="Edit", bg="gray", fg="white", font=("Poppins", 10),
                      command=lambda i=index: self.open_edit_popup(i)).pack(side="right", padx=5)
            tk.Button(frame, text="Delete", bg="#d0021b", fg="white", font=("Poppins", 10),
                      command=lambda i=index: self.prompt_delete(i)).pack(side="right")

    def open_create_popup(self):
        self.open_product_popup()

    def open_edit_popup(self, index):
        self.open_product_popup(index)

    def open_product_popup(self, index=None):
        popup = tk.Toplevel(self)
        popup.title("Create Product" if index is None else "Edit Product")
        popup.geometry("450x650")
        popup.configure(bg="white")
        popup.resizable(False, False)

        product = self.products[index] if index is not None else {}
        custom_font = tkFont.Font(family="Poppins", size=12)

        main_frame = tk.Frame(popup, bg="white", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        tk.Label(main_frame, text="Product Name*", bg="white", font=custom_font).pack(anchor="w")
        name_var = tk.StringVar(value=product.get("name", ""))
        name_entry = tk.Entry(main_frame, textvariable=name_var, font=custom_font, width=30)
        name_entry.pack(fill="x", pady=5)

        tk.Label(main_frame, text="Category*", bg="white", font=custom_font).pack(anchor="w", pady=(10, 0))
        category_var = tk.StringVar(value=product.get("category", "Coffee"))
        category_cb = ttk.Combobox(main_frame, values=["Coffee", "Non-Coffee", "Pastries"],
                                  textvariable=category_var, font=custom_font, state="readonly", width=28)
        category_cb.pack(fill="x", pady=5)

        tk.Label(main_frame, text="Product Image*", bg="white", font=custom_font).pack(anchor="w", pady=(10, 0))
        img_frame = tk.Frame(main_frame, bg="white")
        img_frame.pack(fill="x", pady=5)
        img_path = tk.StringVar(value=product.get("image", ""))
        img_entry = tk.Entry(img_frame, textvariable=img_path, font=custom_font, width=22)
        img_entry.pack(side="left", fill="x", expand=True)
        tk.Button(img_frame, text="Browse", font=custom_font, bg="#333333", fg="white",
                  command=lambda: img_path.set(filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")]))).pack(side="right", padx=5)

        price_frame = tk.Frame(main_frame, bg="white")
        price_entries = {}
        tk.Label(price_frame, text="Prices (Coffee/Non-Coffee)*", bg="white", font=custom_font).pack(anchor="w")
        for size in ["SMALL", "MEDIUM", "LARGE"]:
            frame = tk.Frame(price_frame, bg="white")
            frame.pack(fill="x", pady=2)
            tk.Label(frame, text=size, bg="white", font=custom_font, width=10).pack(side="left")
            val = product.get("price", {}).get(size, "") if isinstance(product.get("price"), dict) else ""
            entry = tk.Entry(frame, font=custom_font, width=15)
            entry.insert(0, val)
            entry.pack(side="left", fill="x", expand=True)
            price_entries[size] = entry

        single_price_frame = tk.Frame(main_frame, bg="white")
        single_price_var = tk.StringVar(value=str(product.get("price", ""))
                                       if not isinstance(product.get("price"), dict) else "")
        tk.Label(single_price_frame, text="Price (Pastries)*", bg="white", font=custom_font).pack(anchor="w")
        single_price_entry = tk.Entry(single_price_frame, textvariable=single_price_var,
                                    font=custom_font, width=15)
        single_price_entry.pack(fill="x", pady=5)

        flavor_frame = tk.Frame(main_frame, bg="white")
        tk.Label(flavor_frame, text="Flavors (comma-separated)", bg="white", font=custom_font).pack(anchor="w")
        flavor_entry = tk.Entry(flavor_frame, font=custom_font, width=30)
        flavor_entry.insert(0, ", ".join(product.get("flavors", [])))
        flavor_entry.pack(fill="x", pady=5)

        tk.Label(main_frame, text="* Required fields", bg="white", font=("Poppins", 10, "italic")).pack(anchor="w", pady=5)

        def update_ui(*args):
            is_pastry = category_var.get() == "Pastries"
            if is_pastry:
                price_frame.pack_forget()
                single_price_frame.pack(fill="x", pady=10)
                flavor_frame.pack(fill="x", pady=10)
            else:
                price_frame.pack(fill="x", pady=10)
                single_price_frame.pack_forget()
                flavor_frame.pack_forget()

        category_var.trace("w", update_ui)
        update_ui()

        def save():
            name = name_var.get().strip()
            category = category_var.get()
            image = img_path.get()

            # Validate inputs
            if not name:
                messagebox.showerror("Error", "Product name is required")
                return
            if not image:
                messagebox.showerror("Error", "Product image is required")
                return
            if not os.path.exists(image):
                messagebox.showerror("Error", "Selected image file does not exist")
                return

            # Handle image copying
            image_basename = os.path.basename(image)
            target_path = os.path.join(self.base_dir, image_basename)
            if os.path.abspath(image) != os.path.abspath(target_path):
                try:
                    shutil.copy2(image, target_path)
                    logging.debug(f"Copied image from {image} to {target_path}")
                except (IOError, OSError) as e:
                    logging.error(f"Failed to copy image {image} to {target_path}: {e}")
                    messagebox.showerror("Error", f"Failed to copy image: {e}")
                    return

            # Database operations
            conn = None
            cursor = None
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()

                # Get category_id
                cursor.execute("SELECT category_id FROM categories WHERE name = %s", (category,))
                category_id = cursor.fetchone()
                if not category_id:
                    messagebox.showerror("Error", f"Category {category} not found")
                    return
                category_id = category_id[0]

                if category == "Pastries":
                    # Validate price for Pastries
                    try:
                        price = float(single_price_var.get()) if single_price_var.get().strip() else 0
                        if price <= 0:
                            messagebox.showerror("Error", "Valid price is required for pastries")
                            return
                    except ValueError:
                        messagebox.showerror("Error", "Price must be a valid number")
                        return
                    flavors = [f.strip() for f in flavor_entry.get().split(",") if f.strip()]
                    flavors_str = ",".join(flavors) if flavors else None

                    if index is not None:
                        # Update existing Pastry
                        menu_id = self.products[index]["menu_ids"][0]
                        cursor.execute("""
                            UPDATE menu
                            SET category_id = %s, name = %s, price = %s, size = NULL, image = %s, flavors = %s, is_hidden = 0
                            WHERE menu_id = %s
                        """, (category_id, name, price, image_basename, flavors_str, menu_id))
                        logging.debug(f"Updated pastry {name} with menu_id {menu_id}")
                    else:
                        # Insert new Pastry
                        cursor.execute("""
                            INSERT INTO menu (category_id, name, price, size, image, flavors, vat_percent, is_hidden)
                            VALUES (%s, %s, %s, NULL, %s, %s, 12.00, 0)
                        """, (category_id, name, price, image_basename, flavors_str))
                        logging.debug(f"Inserted new pastry {name}")
                else:
                    # Validate prices for Coffee/Non-Coffee
                    prices = {}
                    for size in ["SMALL", "MEDIUM", "LARGE"]:
                        if price_entries[size].get().strip():
                            try:
                                price = float(price_entries[size].get())
                                if price <= 0:
                                    messagebox.showerror("Error", f"Valid price required for {size}")
                                    return
                                prices[size] = price
                            except ValueError:
                                messagebox.showerror("Error", f"Price for {size} must be a valid number")
                                return
                    if not prices:
                        messagebox.showerror("Error", "At least one valid price is required")
                        return

                    if index is not None:
                        # Update existing Coffee/Non-Coffee
                        existing_menu_ids = self.products[index]["menu_ids"]
                        menu_id_to_size = {}
                        if existing_menu_ids:  # Check if there are any menu_ids
                            # Dynamically create placeholders for IN clause
                            placeholders = ','.join(['%s'] * len(existing_menu_ids))
                            query = f"SELECT menu_id, size FROM menu WHERE menu_id IN ({placeholders})"
                            cursor.execute(query, existing_menu_ids)
                            menu_id_to_size = {row[0]: row[1] for row in cursor.fetchall()}

                        for size, price in prices.items():
                            menu_id = next((mid for mid, s in menu_id_to_size.items() if s == size), None)
                            if menu_id:
                                # Update existing entry
                                cursor.execute("""
                                    UPDATE menu
                                    SET category_id = %s, name = %s, price = %s, size = %s, image = %s, flavors = NULL, is_hidden = 0
                                    WHERE menu_id = %s
                                """, (category_id, name, price, size, image_basename, menu_id))
                                logging.debug(f"Updated {name} size {size} with menu_id {menu_id}")
                            else:
                                # Insert new size
                                cursor.execute("""
                                    INSERT INTO menu (category_id, name, price, size, image, flavors, vat_percent, is_hidden)
                                    VALUES (%s, %s, %s, %s, %s, NULL, 12.00, 0)
                                """, (category_id, name, price, size, image_basename))
                                logging.debug(f"Inserted new size {size} for {name}")

                        # Mark removed sizes as hidden
                        for menu_id, size in menu_id_to_size.items():
                            if size not in prices:
                                cursor.execute("UPDATE menu SET is_hidden = 1 WHERE menu_id = %s", (menu_id,))
                                logging.debug(f"Marked size {size} for {name} as hidden")
                    else:
                        # Insert new Coffee/Non-Coffee
                        for size, price in prices.items():
                            cursor.execute("""
                                INSERT INTO menu (category_id, name, price, size, image, flavors, vat_percent, is_hidden)
                                VALUES (%s, %s, %s, %s, %s, NULL, 12.00, 0)
                            """, (category_id, name, price, size, image_basename))
                            logging.debug(f"Inserted new size {size} for {name}")

                # Commit changes
                conn.commit()

                # Verify changes
                cursor.execute("SELECT COUNT(*) FROM menu WHERE name = %s", (name,))
                if cursor.fetchone()[0] == 0 and index is None:
                    logging.error(f"Failed to verify insertion of product {name}")
                    messagebox.showerror("Error", "Failed to save product: Verification failed")
                    return

            except mysql.connector.Error as e:
                logging.error(f"Database error while saving product {name}: {e}")
                messagebox.showerror("Error", f"Database error: {e}")
                if conn and conn.is_connected():
                    conn.rollback()
                return
            except Exception as e:
                logging.error(f"Unexpected error while saving product {name}: {e}", exc_info=True)
                messagebox.showerror("Error", f"Unexpected error: {e}")
                if conn and conn.is_connected():
                    conn.rollback()
                return
            finally:
                if cursor:
                    cursor.close()
                if conn and conn.is_connected():
                    conn.close()

            # Refresh UI and close popup
            try:
                self.load_products()
                self.render_products()
                popup.destroy()
                logging.debug(f"Saved product: {name} with image {image_basename}")
                messagebox.showinfo("Success",
                                    f"Product {name} {'created' if index is None else 'updated'} successfully")
            except Exception as e:
                logging.error(f"Error refreshing UI or closing popup: {e}", exc_info=True)
                messagebox.showerror("Error", f"Failed to refresh UI: {e}")

                conn.commit()
                cursor.close()
                conn.close()

                self.load_products()
                self.render_products()
                logging.debug(f"Saved product: {name} with image {image_basename}")
                messagebox.showinfo("Success",
                                    f"Product {name} {'created' if index is None else 'updated'} successfully")

            except mysql.connector.Error as e:
                logging.error(f"Failed to save product: {e}")
                messagebox.showerror("Error", f"Database error: {e}")

        button_frame = tk.Frame(main_frame, bg="white")
        button_frame.pack(fill="x", pady=20)
        tk.Button(button_frame, text="Save", bg="#4CAF50", fg="white", font=custom_font, width=10,
                 command=save).pack(side="left", padx=5)
        tk.Button(button_frame, text="Cancel", bg="#d0021b", fg="white", font=custom_font, width=10,
                 command=popup.destroy).pack(side="right", padx=5)

    def prompt_delete(self, index):
        popup = tk.Toplevel(self)
        popup.title("Admin PIN Verification")
        popup.geometry("300x150")
        popup.configure(bg="white")

        tk.Label(popup, text="Enter Admin PIN:", bg="white", font=("Poppins", 12)).pack(pady=10)
        pin_var = tk.StringVar()
        pin_entry = tk.Entry(popup, textvariable=pin_var, font=("Poppins", 12), show="*")
        pin_entry.pack(pady=5)

        def verify_and_delete():
            pin = pin_var.get()
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                cursor.execute("SELECT user_id FROM Users WHERE role = 'Admin' AND pin = %s", (pin,))
                result = cursor.fetchone()
                cursor.close()
                conn.close()
                if result:
                    self.delete_product(index)
                    popup.destroy()
                    logging.debug("Returned to admin dashboard after deletion")
                else:
                    messagebox.showerror("Error", "Invalid Admin PIN")
            except mysql.connector.Error as e:
                logging.error(f"PIN verification error: {e}")
                messagebox.showerror("Error", f"PIN verification failed: {e}")

        tk.Button(popup, text="Verify", bg="green", fg="white", font=("Poppins", 12), command=verify_and_delete).pack(pady=10)

    def delete_product(self, index):
        product_name = self.products[index]["name"]
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            for menu_id in self.products[index]["menu_ids"]:
                cursor.execute("UPDATE menu SET is_hidden = 1 WHERE menu_id = %s", (menu_id,))
            conn.commit()
            cursor.close()
            conn.close()
            self.load_products()
            self.render_products()
            logging.debug(f"Marked product {product_name} as hidden")
            messagebox.showinfo("Success", f"Product {product_name} marked as hidden")
        except mysql.connector.Error as e:
            logging.error(f"Failed to hide product {product_name}: {e}")
            messagebox.showerror("Error", f"Failed to hide product: {e}")

    def toggle_hide(self, index):
        product = self.products[index]
        new_hidden_state = not product['is_hidden']
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            for menu_id in product["menu_ids"]:
                cursor.execute("UPDATE Menu SET is_hidden = %s WHERE menu_id = %s", (new_hidden_state, menu_id))
            conn.commit()
            cursor.close()
            conn.close()
            self.load_products()
            self.render_products()
            logging.debug(f"Product {product['name']} {'hidden' if new_hidden_state else 'unhidden'}")
        except mysql.connector.Error as e:
            logging.error(f"Failed to toggle hide for product {product['name']}: {e}")
            messagebox.showerror("Error", f"Failed to update hide status: {e}")

class SalesReport(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#d0021b")
        self.custom_font = tkFont.Font(family="Poppins", size=12)
        self.header_font = tkFont.Font(family="Poppins", size=20, weight="bold")
        self.sales_data = []
        self.create_sales_report()

    def create_sales_report(self):
        logging.debug("Initializing Sales Report UI")
        header = tk.Frame(self, bg="#d0021b")
        header.pack(side="top", fill="x", pady=(20, 0), padx=20)

        title = tk.Label(header, text="Sales Report", font=self.header_font, bg="#1c2526", fg="white", padx=20, pady=15)
        title.pack(side="top", fill="x")

        controls = tk.Frame(header, bg="#d0021b")
        controls.pack(fill="x", pady=15)

        tk.Label(controls, text="Sort by", font=self.custom_font, bg="#d0021b", fg="white").pack(side="left", padx=10)
        sort_dropdown = ttk.Combobox(controls, values=["Date", "Qty", "Total Sales"], font=self.custom_font, width=15)
        sort_dropdown.set("Date")
        sort_dropdown.pack(side="left")
        sort_dropdown.bind("<<ComboboxSelected>>", self.sort_sales)

        search_var = tk.StringVar()
        search_entry = tk.Entry(controls, textvariable=search_var, font=self.custom_font, width=30)
        search_entry.insert(0, "Search")
        search_entry.pack(side="right", padx=10)
        search_entry.bind("<KeyRelease>", lambda e: self.search_sales(search_var.get()))

        table_canvas = tk.Canvas(self, bg="#d0021b", highlightthickness=0)
        table_scrollbar = tk.Scrollbar(self, orient="vertical", command=table_canvas.yview)
        scrollable_frame = tk.Frame(table_canvas, bg="#d0021b")

        scrollable_frame.bind("<Configure>", lambda e: table_canvas.configure(scrollregion=table_canvas.bbox("all")))
        table_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        table_canvas.configure(yscrollcommand=table_scrollbar.set)

        table_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        table_scrollbar.pack(side="right", fill="y")

        self.columns = ["Report ID", "Date", "Item", "Total Orders", "Qty", "VAT", "Total Sales"]
        self.tree = ttk.Treeview(scrollable_frame, columns=self.columns, show="headings")

        style = ttk.Style()
        style.configure("Custom.Treeview", font=self.custom_font, rowheight=40, background="#f5f5f5",
                        foreground="black")
        style.configure("Custom.Treeview.Heading", font=self.custom_font, background="#1c2526", foreground="Black")
        style.map("Custom.Treeview",
                  background=[('selected', '#d0021b'), ('!selected', '#f5f5f5')],
                  foreground=[('selected', 'white'), ('!selected', 'black')])
        style.configure("Custom.Treeview", fieldbackground="#f5f5f5")

        self.tree.tag_configure('oddrow', background='#ffffff')
        self.tree.tag_configure('evenrow', background='#f0f0f0')

        self.tree.configure(style="Custom.Treeview")

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=125, anchor="center")

        self.tree.pack(fill="both", expand=True)
        logging.debug("Treeview packed")
        self.load_sales()

    def load_sales(self):
        logging.debug("Loading sales data")
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT report_id, order_date, item_name, total_orders, total_qty, total_vat, total_sales
                FROM SalesReport
                ORDER BY order_date DESC
            """)
            sales = cursor.fetchall()
            cursor.close()
            conn.close()
            logging.debug(f"Fetched {len(sales)} sales records")

            self.sales_data = []
            if not sales:
                tk.Label(self.tree, text="No sales data available", font=self.custom_font, fg="white").pack(pady=20)
                return

            for idx, sale in enumerate(sales):
                self.sales_data.append({
                    "report_id": sale['report_id'],
                    "date": sale['order_date'].strftime("%Y-%m-%d") if sale['order_date'] else "N/A",
                    "item": sale['item_name'],
                    "total_orders": sale['total_orders'],
                    "quantity": sale['total_qty'],
                    "vat": sale['total_vat'],
                    "total_sales": sale['total_sales']
                })

            for idx, sale in enumerate(self.sales_data):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                logging.debug(f"Inserting sale: {sale}")
                self.tree.insert("", "end", values=(
                    sale["report_id"],
                    sale["date"],
                    sale["item"],
                    sale["total_orders"],
                    sale["quantity"],
                    f"₱{sale['vat']:.2f}",
                    f"₱{sale['total_sales']:.2f}"
                ), tags=(tag,))
            self.tree.update_idletasks()
        except mysql.connector.Error as e:
            logging.error(f"Database error in load_sales: {e}")
            messagebox.showwarning("Warning", f"Failed to load sales: {e}")
            self.sales_data = []
            tk.Label(self.tree, text="Error loading sales data", font=self.custom_font, fg="white").pack(pady=20)

    def sort_sales(self, event):
        sort_by = event.widget.get()
        logging.debug(f"Sorting by {sort_by}")
        if sort_by == "Date":
            self.sales_data.sort(key=lambda x: x["date"], reverse=True)
        elif sort_by == "Qty":
            self.sales_data.sort(key=lambda x: x["quantity"], reverse=True)
        elif sort_by == "Total Sales":
            self.sales_data.sort(key=lambda x: x["total_sales"], reverse=True)
        for item in self.tree.get_children():
            self.tree.delete(item)
        for idx, sale in enumerate(self.sales_data):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=(
                sale["report_id"],
                sale["date"],
                sale["item"],
                sale["total_orders"],
                sale["quantity"],
                f"₱{sale['vat']:.2f}",
                f"₱{sale['total_sales']:.2f}"
            ), tags=(tag,))
        self.tree.update_idletasks()

    def search_sales(self, keyword):
        logging.debug(f"Searching for {keyword}")
        for item in self.tree.get_children():
            self.tree.delete(item)
        keyword = keyword.lower()
        for idx, sale in enumerate(self.sales_data):
            if keyword in sale["item"].lower() or str(sale["report_id"]).lower() in keyword:
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree.insert("", "end", values=(
                    sale["report_id"],
                    sale["date"],
                    sale["item"],
                    sale["total_orders"],
                    sale["quantity"],
                    f"₱{sale['vat']:.2f}",
                    f"₱{sale['total_sales']:.2f}"
                ), tags=(tag,))
        self.tree.update_idletasks()