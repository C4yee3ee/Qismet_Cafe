import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import logging
import os
try:
    from PaymentScreen import PaymentScreen
except ImportError:
    PaymentScreen = None

logging.basicConfig(filename='cart.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class CartScreen(tk.Toplevel):
    def __init__(self, master=None, pin=None, cart_data=None, user_id=None):
        super().__init__(master)
        self.title("Qismet Cafe - Cart")
        self.geometry("610x800")  # Initial size
        self.configure(bg="white")
        self.base_dir = r"C:\Users\ADMIN\Desktop\School Files\PythonProjects\Qismet_Cafe"
        self.pin = pin if pin else "2345"
        self.user_id = user_id if user_id else 2
        self.cart_data = cart_data or []
        self.cart_images = {}
        logging.info(f"CartScreen initialized with PIN: {self.pin}, user_id: {self.user_id}, items: {len(self.cart_data)}")
        self.create_ui()

        # Center the window
        self.update_idletasks()  # Ensure geometry is calculated
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 610
        window_height = 800
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    def create_ui(self):
        # Header
        header_frame = tk.Frame(self, bg="white")
        header_frame.pack(fill="x", pady=10)
        tk.Label(header_frame, text="Your Cart", font=("Poppins", 20, "bold"), bg="white", fg="black").pack()

        # Canvas Frame (to isolate canvas and scrollbar)
        canvas_frame = tk.Frame(self, bg="white")
        canvas_frame.pack(fill="both", expand=True)

        # Scrollable canvas
        canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg="white")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if not self.cart_data:
            tk.Label(self.scroll_frame, text="No items in cart", font=("Poppins", 14), bg="white", fg="gray").pack(pady=20)
        else:
            for item in self.cart_data:
                self.add_item_to_ui(self.scroll_frame, item)

        # Bottom Frame (Total and Buttons)
        bottom_frame = tk.Frame(self, bg="white")
        bottom_frame.pack(fill="x", pady=5)

        total_frame = tk.Frame(bottom_frame, bg="white")
        total_frame.pack(fill="x", padx=20, pady=5)
        self.total_label = tk.Label(total_frame, text=f"Total:\t\t\t\t\t₱{self.calculate_total():.2f}", font=("Poppins", 16, "bold"), bg="white", fg="black")
        self.total_label.pack(pady=10)

        # Button Frame with Grid Layout
        button_frame = tk.Frame(bottom_frame, bg="white")
        button_frame.pack(fill="x", pady=5)

        # Use grid to control button placement
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        back_btn = tk.Button(button_frame, text="Back to Menu", font=("Poppins", 14, "bold"),
                             bg="#D0021B", fg="white", command=self.go_back,
                             padx=10, pady=5, bd=0, relief="flat")
        back_btn.grid(row=0, column=0, sticky="w", padx=(20, 0))
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#B00217"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#D0021B"))

        place_order_btn = tk.Button(button_frame, text="Place Order", font=("Poppins", 14, "bold"),
                                    bg="#4CAF50", fg="white", command=self.open_payment_screen,
                                    padx=10, pady=5, bd=0, relief="flat")
        place_order_btn.grid(row=0, column=1, sticky="e", padx=(0, 20))
        place_order_btn.bind("<Enter>", lambda e: place_order_btn.config(bg="#45A049"))
        place_order_btn.bind("<Leave>", lambda e: place_order_btn.config(bg="#4CAF50"))

    def add_item_to_ui(self, parent, item):
        frame = tk.Frame(parent, bg="white", padx=10, pady=10, relief="groove", bd=1)
        frame.pack(fill="x", pady=5)

        # Configure column weights to reduce white space
        frame.grid_columnconfigure(0, weight=1)  # Image
        frame.grid_columnconfigure(1, weight=3)  # Details
        frame.grid_columnconfigure(2, weight=1)  # Price
        frame.grid_columnconfigure(3, weight=1)  # Quantity
        frame.grid_columnconfigure(4, weight=1)  # Remove

        # Image
        image_path = os.path.join(self.base_dir, item.get('image', '')) if item.get('image') else None
        logging.info(f"Attempting to load image: {image_path}")
        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path).resize((80, 80))
                photo = ImageTk.PhotoImage(img)
                self.cart_images[item['name']] = photo
                img_label = tk.Label(frame, image=photo, bg="white")
            except Exception as e:
                logging.error(f"Image load error for {item.get('image', 'unknown')}: {e}")
                img_label = tk.Label(frame, text="No Image", bg="white", font=("Poppins", 12))
        else:
            logging.warning(f"Image path does not exist: {image_path}")
            img_label = tk.Label(frame, text="No Image", bg="white", font=("Poppins", 12))
        img_label.grid(row=0, column=0, padx=5)

        # Item Details
        details_frame = tk.Frame(frame, bg="white")
        details_frame.grid(row=0, column=1, sticky="w")

        name_label = tk.Label(details_frame, text=item['name'], font=("Poppins", 14, "bold"), bg="white", fg="#D0021B", anchor="w")
        name_label.pack(anchor="w")

        desc = []
        if item.get("category") == "Coffee":
            if item.get("temperature"): desc.append(item["temperature"])
            if item.get("size"): desc.append(item["size"])
        elif item.get("category") == "Non-Coffee":
            if item.get("size"): desc.append(item["size"])
        elif item.get("category") == "Pastries":
            if item.get("flavor"): desc.append(item["flavor"])
        if item.get("dine_option"): desc.append(item["dine_option"])
        desc_text = ", ".join(desc)
        desc_label = tk.Label(details_frame, text=desc_text, font=("Poppins", 12), bg="white", fg="gray", anchor="w")
        desc_label.pack(anchor="w")

        # Price
        price = item.get("price", 0.0)
        price_label = tk.Label(frame, text=f"₱{price * item.get('quantity', 1):.2f}", font=("Poppins", 14), bg="white", fg="black")
        price_label.grid(row=0, column=2, padx=10)

        # Quantity Controls
        qty_frame = tk.Frame(frame, bg="white")
        qty_frame.grid(row=0, column=3)

        minus_btn = tk.Button(qty_frame, text="−", font=("Poppins", 12), width=3, bg="#808080", fg="white",
                              command=lambda i=item: self.update_quantity(i, -1))
        minus_btn.pack(side="left", padx=2)
        minus_btn.bind("<Enter>", lambda e: minus_btn.config(bg="#D0021B"))
        minus_btn.bind("<Leave>", lambda e: minus_btn.config(bg="#808080"))

        qty_label = tk.Label(qty_frame, text=str(item.get("quantity", 1)), font=("Poppins", 12), width=4, bg="white", fg="black", relief="sunken")
        qty_label.pack(side="left", padx=2)

        plus_btn = tk.Button(qty_frame, text="+", font=("Poppins", 12), width=3, bg="#808080", fg="white",
                             command=lambda i=item: self.update_quantity(i, 1))
        plus_btn.pack(side="left", padx=2)
        plus_btn.bind("<Enter>", lambda e: plus_btn.config(bg="#D0021B"))
        plus_btn.bind("<Leave>", lambda e: plus_btn.config(bg="#808080"))

        # Remove Button
        remove_btn = tk.Button(frame, text="Remove", font=("Poppins", 12, "bold"),
                               bg="#808080", fg="white", relief="flat",
                               command=lambda i=item: self.remove_item(i))
        remove_btn.grid(row=0, column=4, padx=5)
        remove_btn.bind("<Enter>", lambda e: remove_btn.config(bg="#D0021B"))
        remove_btn.bind("<Leave>", lambda e: remove_btn.config(bg="#808080"))

        item["_qty_label"] = qty_label

    def update_quantity(self, item, delta):
        new_quantity = item.get("quantity", 1) + delta
        if new_quantity < 1:
            return
        item["quantity"] = new_quantity
        item["_qty_label"].config(text=str(new_quantity))
        self.total_label.config(text=f"Total:\t\t\t\t\t₱{self.calculate_total():.2f}")
        logging.info(f"Updated quantity for item {item['name']} to {new_quantity}")

    def remove_item(self, item):
        self.cart_data.remove(item)
        self.reload_ui()
        self.total_label.config(text=f"Total:\t\t\t\t\t₱{self.calculate_total():.2f}")
        logging.info(f"Removed item {item['name']} from cart")

    def calculate_total(self):
        total = sum(item.get("price", 0.0) * item.get("quantity", 1) for item in self.cart_data)
        return total

    def reload_ui(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.create_ui()

    def open_payment_screen(self):
        if not self.cart_data:
            messagebox.showwarning("Warning", "Cart is empty. Nothing to order.")
            return
        try:
            # Extract dine_option from the first item (assuming consistency)
            dine_option = self.cart_data[0].get("dine_option", "Dine In")
            if dine_option not in ["Dine In", "Take Out"]:
                logging.warning(f"Invalid dine_option: {dine_option}, defaulting to 'Dine In'")
                dine_option = "Dine In"
            logging.info(f"Passing dine_option to PaymentScreen: {dine_option}")
            self.destroy()
            payment_screen = PaymentScreen(master=self.master, cart_data=self.cart_data, pin=self.pin,
                                          user_id=self.user_id, dine_option=dine_option)
            payment_screen.update()
        except Exception as e:
            logging.error(f"Error opening PaymentScreen: {e}")
            messagebox.showerror("Error", f"Failed to open PaymentScreen: {str(e)}")

    def go_back(self):
        # Pass cart_data back to MenuDashboard
        if hasattr(self.master, 'cart_data'):
            self.master.cart_data = self.cart_data
        logging.info("Returning to MenuDashboard with updated cart_data")
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = CartScreen(master=root, pin="2345", cart_data=[])
    root.mainloop()