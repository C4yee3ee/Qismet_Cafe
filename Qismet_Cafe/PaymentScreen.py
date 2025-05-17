import tkinter as tk
from tkinter import messagebox
import json
import os
import DbConfig
import mysql.connector
from datetime import datetime
from PIL import Image, ImageTk
import logging

logging.basicConfig(filename='menu_sales.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class PaymentScreen(tk.Toplevel):
    def __init__(self, master, cart_data, pin, user_id, dine_option=None):
        super().__init__(master)
        self.title("Qismet Cafe - Payment")
        self.configure(bg="red")
        window_width = 500
        window_height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.order_type = dine_option if dine_option in ["Dine In", "Take Out"] else "Dine In"
        self.payment_method = None
        self.cart_data = cart_data
        self.user_id = user_id
        self.pin = pin
        self.master = master
        self.base_dir = r"C:\Users\ADMIN\Desktop\School Files\PythonProjects\Qismet_Cafe"
        self.qr_images = {}
        self.payment_buttons = {}
        self.create_widgets()
        logging.debug(f"Initialized PaymentScreen with cart_data={cart_data}, user_id={user_id}, pin={pin}, dine_option={self.order_type}")

    def create_widgets(self):
        header = tk.Frame(self, bg="black", height=100)
        header.pack(fill="x")

        tk.Label(header, text="QISMET CAFE", font=("Poppins", 18, "bold"), bg="black", fg="white").pack(pady=(25, 50))

        option_frame = tk.Frame(self, bg="red")
        option_frame.pack(pady=40)

        def set_payment(method, button):
            self.payment_method = method
            self.reset_button_colors()
            button.config(bg="#d5d5d5")
            logging.debug(f"Payment method set to {method}")

        btn_style = {
            "width": 18,
            "height": 3,
            "font": ("Poppins", 14, "bold"),
            "bg": "#eeeeee",
            "fg": "black",
            "activebackground": "#cccccc",
            "activeforeground": "black",
            "bd": 0,
            "relief": "flat"
        }

        cash_button = tk.Button(option_frame, text="Cash", command=lambda: set_payment("Cash", cash_button),
                                **btn_style)
        cash_button.grid(row=0, column=0, padx=10, pady=10)
        self.payment_buttons["Cash"] = cash_button

        ewallet_button = tk.Button(option_frame, text="E-Wallet",
                                   command=lambda: set_payment("E-Wallet", ewallet_button), **btn_style)
        ewallet_button.grid(row=0, column=1, padx=10, pady=10)
        self.payment_buttons["E-Wallet"] = ewallet_button

        place_order_style = {
            "font": ("Poppins", 16, "bold"),
            "bg": "white",
            "fg": "black",
            "activebackground": "#d0d0d0",
            "activeforeground": "black",
            "width": 20,
            "height": 2,
            "bd": 0,
            "relief": "flat"
        }

        place_order_btn = tk.Button(self, text="Place Order", command=self.place_order, **place_order_style)
        place_order_btn.pack(pady=30)

        back_btn_style = {
            "font": ("Poppins", 16, "bold"),
            "bg": "#ff5555",
            "fg": "white",
            "activebackground": "#cc4444",
            "activeforeground": "white",
            "width": 20,
            "height": 2,
            "bd": 0,
            "relief": "flat"
        }

        back_btn = tk.Button(self, text="Back", command=self.destroy, **back_btn_style)
        back_btn.pack(pady=10)

    def reset_button_colors(self):
        default_bg = "#eeeeee"
        for button in self.payment_buttons.values():
            button.config(bg=default_bg)

    def place_order(self):
        logging.debug("Attempting to place order")
        if not self.payment_method:
            messagebox.showwarning("Select Payment", "Please select a payment method.")
            logging.warning("No payment method selected")
            return

        if not self.cart_data:
            messagebox.showerror("Error", "Cart is empty.")
            logging.error("Cart is empty")
            return

        conn = None
        cursor = None
        try:
            logging.debug(f"Cart data: {self.cart_data}")
            conn = DbConfig.connect()
            cursor = conn.cursor(buffered=True)
            logging.debug("Database connection established")

            total = sum(item["price"] * item["quantity"] for item in self.cart_data)
            vat_total = round(total * 0.12, 2)
            logging.debug(f"Total={total}, VAT={vat_total}, Order Type={self.order_type}")

            if vat_total > 99999999.99:
                raise ValueError("VAT total exceeds maximum allowed value")

            # Insert into Orders
            cursor.execute("""
                INSERT INTO Orders (user_id, order_date, order_type, status)
                VALUES (%s, %s, %s, %s)
            """, (self.user_id, datetime.now(), self.order_type, "Preparing"))
            order_id = cursor.lastrowid
            logging.debug(f"Inserted order_id={order_id}")

            # Insert OrderItems and update SalesReport
            items_processed = 0
            for item in self.cart_data:
                logging.debug(f"Processing item: {item}")
                cursor.execute("""
                    SELECT menu_id FROM Menu WHERE name = %s AND (size = %s OR size IS NULL)
                """, (item["name"], item.get("size")))
                menu_id = cursor.fetchone()
                logging.debug(f"Queried menu_id for {item['name']}, size={item.get('size')}: {menu_id}")

                if not menu_id:
                    logging.warning(f"No menu_id found for {item['name']}, size={item.get('size')}")
                    continue

                menu_id = menu_id[0]
                cursor.execute("""
                    INSERT INTO OrderItems (order_id, menu_id, quantity)
                    VALUES (%s, %s, %s)
                """, (order_id, menu_id, item["quantity"]))
                logging.debug(f"Inserted OrderItem: order_id={order_id}, menu_id={menu_id}, quantity={item['quantity']}")

                order_date = datetime.now().date()
                item_name = item["name"]
                quantity = item["quantity"]
                item_total = item["price"] * quantity
                vat = round(item_total * 0.12, 2)
                total_sales = round(item_total + vat, 2)
                logging.debug(f"Item={item_name}, Item_Total={item_total}, VAT={vat}, Total_Sales={total_sales}")

                if vat > 99999999.99 or total_sales > 99999999.99:
                    raise ValueError(f"SalesReport values for {item_name} exceed maximum allowed")

                cursor.execute("""
                    SELECT report_id, total_orders, total_qty
                    FROM SalesReport
                    WHERE order_date = %s AND item_name = %s
                """, (order_date, item_name))
                existing = cursor.fetchone()
                cursor.fetchall()
                logging.debug(f"SalesReport existing record: {existing}")

                if existing:
                    new_orders = existing[1] + 1
                    new_qty = existing[2] + quantity
                    cursor.execute("""
                        UPDATE SalesReport
                        SET total_orders = %s, total_qty = %s, total_vat = total_vat + %s, total_sales = total_sales + %s
                        WHERE report_id = %s
                    """, (new_orders, new_qty, vat, total_sales, existing[0]))
                    logging.debug(f"Updated SalesReport: report_id={existing[0]}")
                else:
                    cursor.execute("""
                        INSERT INTO SalesReport (order_date, item_name, total_orders, total_qty, total_vat, total_sales)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (order_date, item_name, 1, quantity, vat, total_sales))
                    logging.debug(f"Inserted new SalesReport record for {item_name}")
                cursor.fetchall()

                items_processed += 1

            if items_processed == 0:
                raise ValueError("No valid items were processed for the order")

            # Insert into Payments
            cursor.execute("""
                INSERT INTO Payments (order_id, method, vat_total)
                VALUES (%s, %s, %s)
            """, (order_id, self.payment_method, vat_total))
            logging.debug(f"Inserted Payment: order_id={order_id}, method={self.payment_method}, vat_total={vat_total}")

            conn.commit()
            logging.debug(f"Order {order_id} committed successfully")

        except (mysql.connector.Error, ValueError) as e:
            messagebox.showerror("Error", f"Failed to place order: {e}")
            logging.error(f"Failed to place order: {e}")
            if conn and conn.is_connected():
                conn.rollback()
                logging.debug("Transaction rolled back")
            return
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
            logging.debug("Database connection closed")

        if hasattr(self.master, 'cart_data'):
            self.master.cart_data.clear()
        self.cart_data.clear()

        if self.payment_method == "E-Wallet":
            self.show_qr_screen(order_id)
        else:
            messagebox.showinfo("Success", f"Order placed successfully! Order #{order_id}")
            self.destroy()

    def show_qr_screen(self, order_id):
        logging.debug(f"Showing QR code for Order #{order_id}")
        qr_window = tk.Toplevel(self)
        qr_window.title("Scan QR Code")
        qr_window.configure(bg="red")
        qr_window.geometry("400x500")
        qr_window.transient(self)
        qr_window.grab_set()

        content_frame = tk.Frame(qr_window, bg="red")
        content_frame.pack(expand=True)

        tk.Label(content_frame, text=f"QR Code for Order #{order_id}", font=("Poppins", 16, "bold"), bg="red", fg="white").pack(pady=20)

        qr_image_path = os.path.join(self.base_dir, "qrcode.jpg")
        try:
            qr_img = Image.open(qr_image_path).convert("L").resize((200, 200), Image.Resampling.LANCZOS)
            qr_photo = ImageTk.PhotoImage(qr_img)
            self.qr_images[order_id] = qr_photo
            qr_label = tk.Label(content_frame, image=qr_photo, bg="red")
            qr_label.pack(pady=20)
            logging.debug(f"QR code loaded from {qr_image_path}")
        except Exception as e:
            tk.Label(content_frame, text=f"Failed to load QR code: {str(e)}", font=("Poppins", 12), bg="red", fg="white").pack(pady=20)
            logging.error(f"Failed to load QR code: {e}")

        ok_btn = tk.Button(content_frame, text="OK", font=("Poppins", 14, "bold"),
                           bg="#4CAF50", fg="white", command=lambda: self.close_qr_and_return(qr_window),
                           width=10, height=2, bd=0, relief="flat")
        ok_btn.pack(pady=20)

        self.wait_window(qr_window)

    def close_qr_and_return(self, qr_window):
        if hasattr(self.master, 'cart_data'):
            self.master.cart_data.clear()
        self.cart_data.clear()
        qr_window.destroy()
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = PaymentScreen(master=root, cart_data=[], pin="2345", user_id=1, dine_option="Dine In")
    app.mainloop()