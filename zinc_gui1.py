# === Zinc.inc Pharmacy Management System ===
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os, json, datetime, webbrowser
from collections import defaultdict
import tempfile
import csv

# ==== GLOBAL DATA ====
INVENTORY_FILE = "inventory.json"
SALES_FILE = "sales.json"
PATIENTS_FILE = "patients.json"
SUPPLIERS_FILE = "suppliers.json"
USERS = {"admin": "admin123"}
current_user = None
inventory = {}
sales_data = []
patients_data = {}
suppliers_data = {}
today = datetime.datetime.now().strftime("%Y-%m-%d")

# ==== DATA HANDLING ====
def load_data():
    global inventory, sales_data, patients_data, suppliers_data
    
    # Load inventory (unchanged)
    # ...
    
    # Load patients data
    if os.path.exists(PATIENTS_FILE):
        with open(PATIENTS_FILE, "r") as f:
            patients_data = json.load(f)
    else:
        patients_data = {
            "PAT001": {
                "name": "John Doe",
                "age": "35",
                "gender": "Male",
                "phone": "555-0101",
                "address": "123 Main St",
                "medical_history": "Hypertension",
                "purchases": [{"date": today, "items": ["paracetamol"]}]
            }
        }
    
    # Load suppliers data
    if os.path.exists(SUPPLIERS_FILE):
        with open(SUPPLIERS_FILE, "r") as f:
            suppliers_data = json.load(f)
    else:
        suppliers_data = {
            "SUPP001": {
                "name": "MediCorp Distributors",
                "contact": "555-0202",
                "email": "sales@medicorp.com",
                "address": "456 Pharma Ave"
            },
            "SUPP002": {
                "name": "Global Pharma Supply",
                "contact": "555-0303",
                "email": "orders@globalpharma.com",
                "address": "789 Healthcare Blvd"
            }
        }
    
    # Load suppliers data
    if os.path.exists(SUPPLIERS_FILE):
        with open(SUPPLIERS_FILE, "r") as f:
            suppliers_data = json.load(f)
    else:
        suppliers_data = {
            "default": {
                "name": "Default Supplier",
                "contact": "9999999999",
                "email": "supplier@example.com",
                "address": "123 Supplier Street"
            }
        }

def save_data():
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=2)
    with open(SALES_FILE, "w") as f:
        json.dump(sales_data, f, indent=2)
    with open(PATIENTS_FILE, "w") as f:
        json.dump(patients_data, f, indent=2)
    with open(SUPPLIERS_FILE, "w") as f:
        json.dump(suppliers_data, f, indent=2)

load_data()

# ==== GUI SETUP ====
root = tk.Tk()
root.title("Zinc.inc Pharmacy Management System")
root.geometry("1400x850")
root.state('zoomed')  # Start maximized

# Styling
BG_COLOR = "#ffffff"
ACCENT_COLOR = "#2c3e50"
CHART_COLORS = ['#1abc9c', '#3498db', '#9b59b6', '#e74c3c', '#f1c40f']

sidebar = tk.Frame(root, bg=ACCENT_COLOR, width=220)
sidebar.pack(fill=tk.Y, side=tk.LEFT)
main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(fill=tk.BOTH, expand=True)

# ==== UTILITY FUNCTIONS ====
def clear_main_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"

def print_receipt(text):
    """Create a temporary HTML file and print it"""
    html_content = f"""
    <html>
        <head>
            <title>Pharmacy Receipt</title>
            <style>
                body {{ font-family: Arial; width: 80mm; margin: 0 auto; }}
                .header {{ text-align: center; margin-bottom: 15px; }}
                .info {{ margin: 10px 0; }}
                .items {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                .items th {{ text-align: left; border-bottom: 1px solid #000; }}
                .items td {{ padding: 5px 0; }}
                .total {{ text-align: right; font-weight: bold; margin-top: 10px; }}
                .footer {{ text-align: center; margin-top: 20px; font-size: 0.8em; }}
            </style>
        </head>
        <body>
            <div class='header'>
                <h2>Zinc.inc Pharmacy</h2>
                <p>123 Medical Street, Pharma City</p>
            </div>
            {text.replace("\n", "<br>")}
            <div class='footer'>
                <p>Thank you for your purchase!</p>
                <p>{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            </div>
        </body>
    </html>
    """
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html') as f:
        f.write(html_content)
        temp_path = f.name
    
    webbrowser.open(temp_path)

def export_to_csv(data, headers, filename):
    """Export data to CSV file"""
    filepath = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile=filename
    )
    if filepath:
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(data)
        messagebox.showinfo("Success", f"Data exported to {filepath}")

# ==== PAGE FUNCTIONS ====
def show_invoice_page():
    clear_main_frame()
    
    # Header
    header_frame = tk.Frame(main_frame, bg=BG_COLOR)
    header_frame.pack(fill=tk.X, pady=10)
    
    tk.Label(header_frame, text="Zinc.inc Invoice System", 
            font=("Helvetica", 20, "bold"), bg=BG_COLOR).pack(side=tk.LEFT, padx=20)
    
    # Customer Info Frame
    customer_frame = tk.LabelFrame(main_frame, text="Customer Information", bg=BG_COLOR)
    customer_frame.pack(fill=tk.X, padx=20, pady=10)
    
    # Customer Name
    tk.Label(customer_frame, text="Customer Name:", bg=BG_COLOR).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    customer_entry = tk.Entry(customer_frame)
    customer_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    customer_entry.bind("<Return>", focus_next_widget)
    
    # Patient ID (new field)
    tk.Label(customer_frame, text="Patient ID:", bg=BG_COLOR).grid(row=0, column=2, padx=5, pady=5, sticky="e")
    patient_id_entry = tk.Entry(customer_frame)
    patient_id_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")
    patient_id_entry.bind("<Return>", focus_next_widget)
    
    # GST Number
    tk.Label(customer_frame, text="GST Number:", bg=BG_COLOR).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    gst_entry = tk.Entry(customer_frame)
    gst_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    gst_entry.insert(0, "22AAAAA0000A1Z5")  # Sample GST
    gst_entry.bind("<Return>", focus_next_widget)
    
    # Doctor Info
    tk.Label(customer_frame, text="Doctor Name:", bg=BG_COLOR).grid(row=1, column=2, padx=5, pady=5, sticky="e")
    doctor_entry = tk.Entry(customer_frame)
    doctor_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")
    doctor_entry.bind("<Return>", focus_next_widget)
    
    # Medicine Entry Frame
    medicine_frame = tk.LabelFrame(main_frame, text="Add Medicine", bg=BG_COLOR)
    medicine_frame.pack(fill=tk.X, padx=20, pady=10)
    
    # Medicine Selection
    tk.Label(medicine_frame, text="Medicine:", bg=BG_COLOR).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    med_combo = ttk.Combobox(medicine_frame, values=list(inventory.keys()), width=30)
    med_combo.grid(row=0, column=1, padx=5, pady=5)
    med_combo.bind("<Return>", focus_next_widget)
    
    # Stock Info
    stock_label = tk.Label(medicine_frame, text="Available: ", bg=BG_COLOR)
    stock_label.grid(row=0, column=2, padx=5, pady=5)
    
    # Quantity
    tk.Label(medicine_frame, text="Quantity:", bg=BG_COLOR).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    qty_entry = tk.Entry(medicine_frame)
    qty_entry.grid(row=1, column=1, padx=5, pady=5)
    qty_entry.bind("<Return>", focus_next_widget)
    
    # Price
    tk.Label(medicine_frame, text="Price:", bg=BG_COLOR).grid(row=1, column=2, padx=5, pady=5, sticky="e")
    price_label = tk.Label(medicine_frame, text="₹0.00", bg=BG_COLOR)
    price_label.grid(row=1, column=3, padx=5, pady=5, sticky="w")
    
    # Cart Frame
    cart_frame = tk.LabelFrame(main_frame, text="Current Cart", bg=BG_COLOR)
    cart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    # Cart Treeview
    cart_tree = ttk.Treeview(cart_frame, columns=("Medicine", "Qty", "Price", "Total"), show="headings")
    cart_tree.heading("Medicine", text="Medicine")
    cart_tree.heading("Qty", text="Quantity")
    cart_tree.heading("Price", text="Price (₹)")
    cart_tree.heading("Total", text="Total (₹)")
    cart_tree.column("Medicine", width=200)
    cart_tree.column("Qty", width=80, anchor='center')
    cart_tree.column("Price", width=100, anchor='e')
    cart_tree.column("Total", width=120, anchor='e')
    cart_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Totals Frame
    totals_frame = tk.Frame(main_frame, bg=BG_COLOR)
    totals_frame.pack(fill=tk.X, padx=20, pady=10)
    
    tk.Label(totals_frame, text="Subtotal:", bg=BG_COLOR, font=("Arial", 10)).grid(row=0, column=0, padx=5, sticky="e")
    subtotal_label = tk.Label(totals_frame, text="₹0.00", bg=BG_COLOR, font=("Arial", 10))
    subtotal_label.grid(row=0, column=1, padx=5, sticky="w")
    
    tk.Label(totals_frame, text="GST (18%):", bg=BG_COLOR, font=("Arial", 10)).grid(row=1, column=0, padx=5, sticky="e")
    gst_amount_label = tk.Label(totals_frame, text="₹0.00", bg=BG_COLOR, font=("Arial", 10))
    gst_amount_label.grid(row=1, column=1, padx=5, sticky="w")
    
    tk.Label(totals_frame, text="Total:", bg=BG_COLOR, font=("Arial", 12, "bold")).grid(row=2, column=0, padx=5, sticky="e")
    total_label = tk.Label(totals_frame, text="₹0.00", bg=BG_COLOR, font=("Arial", 12, "bold"))
    total_label.grid(row=2, column=1, padx=5, sticky="w")
    
    # Button Frame
    button_frame = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame.pack(fill=tk.X, padx=20, pady=10)
    
    # Cart operations
    cart = []
    
    def update_stock_display(event=None):
        med = med_combo.get().strip().lower()
        if med in inventory:
            stock_label.config(text=f"Available: {inventory[med]['quantity']}")
            price_label.config(text=f"₹{inventory[med]['price']:.2f}")
        else:
            stock_label.config(text="Not found")
            price_label.config(text="₹0.00")
    
    def add_to_cart():
        med = med_combo.get().strip().lower()
        qty = qty_entry.get().strip()
        
        if not med or not qty:
            messagebox.showwarning("Missing Fields", "Please select medicine and enter quantity")
            return
            
        try:
            qty = int(qty)
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Quantity must be a positive integer")
            return
            
        if med not in inventory:
            messagebox.showerror("Error", "Medicine not found in inventory")
            return
            
        if qty > inventory[med]['quantity']:
            messagebox.showerror("Stock Error", f"Only {inventory[med]['quantity']} available")
            return
            
        price = inventory[med]['price']
        total = price * qty
        cart.append({"medicine": med, "quantity": qty, "price": price, "total": total})
        
        # Update cart display
        cart_tree.insert("", tk.END, values=(med.title(), qty, f"₹{price:.2f}", f"₹{total:.2f}"))
        update_totals()
        
        # Clear inputs
        med_combo.set('')
        qty_entry.delete(0, tk.END)
        med_combo.focus()
    
    def remove_from_cart():
        selected = cart_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an item to remove")
            return
            
        index = cart_tree.index(selected[0])
        cart.pop(index)
        cart_tree.delete(selected[0])
        update_totals()
    
    def update_totals():
        subtotal = sum(item['total'] for item in cart)
        gst = subtotal * 0.18
        total = subtotal + gst
        
        subtotal_label.config(text=f"₹{subtotal:.2f}")
        gst_amount_label.config(text=f"₹{gst:.2f}")
        total_label.config(text=f"₹{total:.2f}")
    
    def generate_invoice():
        if not cart:
            messagebox.showwarning("Empty Cart", "Please add items to cart first")
            return
            
        customer = customer_entry.get().strip()
        if not customer:
            messagebox.showwarning("Missing Info", "Please enter customer name")
            return
            
        # Get patient ID if provided
        patient_id = patient_id_entry.get().strip()
        if patient_id and patient_id in patients_data:
            # Update patient's purchase history
            if "purchases" not in patients_data[patient_id]:
                patients_data[patient_id]["purchases"] = []
            patients_data[patient_id]["purchases"].append({
                "date": today,
                "items": [item["medicine"] for item in cart]
            })
            save_data()
            
        # Calculate totals
        subtotal = sum(item['total'] for item in cart)
        gst = subtotal * 0.18
        total = subtotal + gst
        
        # Calculate profit
        profit = sum((item['price'] - inventory[item['medicine']]['cost']) * item['quantity'] for item in cart)
        
        # Update inventory
        for item in cart:
            med = item['medicine']
            inventory[med]['quantity'] -= item['quantity']
            
        # Record sale
        sale = {
            "date": today,
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "customer": customer,
            "patient_id": patient_id if patient_id else None,
            "doctor": doctor_entry.get(),
            "gst_number": gst_entry.get(),
            "items": cart.copy(),
            "subtotal": subtotal,
            "gst": gst,
            "total": total,
            "profit": profit
        }
        sales_data.append(sale)
        save_data()
        
        # Generate receipt text
        receipt_text = f"Customer: {customer}\n"
        if patient_id:
            receipt_text += f"Patient ID: {patient_id}\n"
        receipt_text += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        receipt_text += f"Doctor: {doctor_entry.get()}\n"
        receipt_text += f"GST: {gst_entry.get()}\n\n"
        receipt_text += "ITEM\tQTY\tPRICE\tTOTAL\n"
        receipt_text += "-"*40 + "\n"
        
        for item in cart:
            receipt_text += f"{item['medicine'].title()}\t{item['quantity']}\t₹{item['price']:.2f}\t₹{item['total']:.2f}\n"
        
        receipt_text += "-"*40 + "\n"
        receipt_text += f"Subtotal: ₹{subtotal:.2f}\n"
        receipt_text += f"GST (18%): ₹{gst:.2f}\n"
        receipt_text += f"TOTAL: ₹{total:.2f}\n"
        
        # Show receipt in new window
        show_receipt(receipt_text)
        
        # Clear cart
        cart.clear()
        cart_tree.delete(*cart_tree.get_children())
        update_totals()
        customer_entry.delete(0, tk.END)
        patient_id_entry.delete(0, tk.END)
        doctor_entry.delete(0, tk.END)
        customer_entry.focus()
    
    def show_receipt(text):
        receipt_window = tk.Toplevel(root)
        receipt_window.title("Invoice Receipt")
        receipt_window.geometry("600x700")
        
        receipt_text = tk.Text(receipt_window, wrap=tk.WORD, font=("Courier New", 12))
        receipt_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        receipt_text.insert(tk.END, text)
        receipt_text.config(state=tk.DISABLED)
        
        button_frame = tk.Frame(receipt_window)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Print Receipt", command=lambda: print_receipt(text), 
                 bg="#3498db", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Close", command=receipt_window.destroy,
                 bg="#e74c3c", fg="white").pack(side=tk.LEFT, padx=10)
    
    # Bindings
    med_combo.bind("<<ComboboxSelected>>", update_stock_display)
    
    # Buttons
    tk.Button(button_frame, text="Add to Cart", command=add_to_cart, bg="#3498db", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Remove Selected", command=remove_from_cart, bg="#e74c3c", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Generate Invoice", command=generate_invoice, bg="#2ecc71", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Clear Cart", command=lambda: [cart.clear(), cart_tree.delete(*cart_tree.get_children()), update_totals()], 
             bg="#f39c12", fg="white").pack(side=tk.LEFT, padx=5)

def show_restock_page():
    clear_main_frame()
    
    tk.Label(main_frame, text="Restock Inventory", 
            font=("Helvetica", 18, "bold"), bg=BG_COLOR).pack(pady=20)
    
    form = tk.Frame(main_frame, bg=BG_COLOR)
    form.pack(pady=10)

    # Medicine Selection
    tk.Label(form, text="Medicine:", bg=BG_COLOR).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    med_combo = ttk.Combobox(form, values=list(inventory.keys()), width=30)
    med_combo.grid(row=0, column=1, padx=5, pady=5)
    med_combo.bind("<Return>", focus_next_widget)
    
    # Current Stock
    tk.Label(form, text="Current Stock:", bg=BG_COLOR).grid(row=0, column=2, padx=5, pady=5, sticky="e")
    stock_label = tk.Label(form, text="0", bg=BG_COLOR)
    stock_label.grid(row=0, column=3, padx=5, pady=5, sticky="w")
    
    # Supplier Selection
    tk.Label(form, text="Supplier:", bg=BG_COLOR).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    supplier_combo = ttk.Combobox(form, values=list(suppliers_data.keys()), width=30)
    supplier_combo.grid(row=1, column=1, padx=5, pady=5)
    
    # Quantity to Add
    tk.Label(form, text="Quantity to Add:", bg=BG_COLOR).grid(row=2, column=0, padx=5, pady=5, sticky="e")
    qty_entry = tk.Entry(form)
    qty_entry.grid(row=2, column=1, padx=5, pady=5)
    qty_entry.bind("<Return>", lambda e: restock_medicine())
    
    # Cost Price
    tk.Label(form, text="Cost Price:", bg=BG_COLOR).grid(row=2, column=2, padx=5, pady=5, sticky="e")
    cost_entry = tk.Entry(form)
    cost_entry.grid(row=2, column=3, padx=5, pady=5, sticky="w")
    
    def update_stock_display(event=None):
        med = med_combo.get().strip().lower()
        if med in inventory:
            stock_label.config(text=str(inventory[med]['quantity']))
            supplier_combo.set(inventory[med]['supplier'])
            cost_entry.delete(0, tk.END)
            cost_entry.insert(0, str(inventory[med]['cost']))
        else:
            stock_label.config(text="Not found")
            supplier_combo.set('')
            cost_entry.delete(0, tk.END)
    
    def restock_medicine():
        med = med_combo.get().strip().lower()
        qty = qty_entry.get().strip()
        supplier = supplier_combo.get().strip()
        cost = cost_entry.get().strip()
        
        if not med:
            messagebox.showwarning("Missing Info", "Please select a medicine")
            return
            
        try:
            qty = int(qty)
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid quantity")
            return
            
        try:
            cost = float(cost)
            if cost <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid cost price")
            return
            
        if med not in inventory:
            # Add new medicine to inventory
            inventory[med] = {
                "quantity": qty,
                "price": cost * 1.3,  # 30% markup by default
                "cost": cost,
                "supplier": supplier
            }
        else:
            # Update existing medicine
            inventory[med]['quantity'] += qty
            inventory[med]['cost'] = cost
            inventory[med]['supplier'] = supplier
        
        save_data()
        messagebox.showinfo("Success", f"Added {qty} units of {med}")
        update_stock_display()
        med_combo.set('')
        qty_entry.delete(0, tk.END)
        cost_entry.delete(0, tk.END)
        med_combo.focus()
    
    # Bindings
    med_combo.bind("<<ComboboxSelected>>", update_stock_display)
    
    # Button
    tk.Button(main_frame, text="Restock Medicine", command=restock_medicine, 
             bg="#2ecc71", fg="white").pack(pady=10)

def show_statistics_page():
    clear_main_frame()
    
    # Header
    tk.Label(main_frame, text="Pharmacy Analytics Dashboard", 
            font=("Helvetica", 18, "bold"), bg=BG_COLOR).pack(pady=10)

    # Create figure with 2x2 grid
    fig = Figure(figsize=(12, 9), dpi=100)
    gs = fig.add_gridspec(2, 2)
    ax1 = fig.add_subplot(gs[0, 0])  # Sales Trend
    ax2 = fig.add_subplot(gs[0, 1])  # Top Products
    ax3 = fig.add_subplot(gs[1, 0])  # Profit Analysis
    ax4 = fig.add_subplot(gs[1, 1])  # Inventory Health

    # Process sales data
    daily_sales = defaultdict(float)
    product_sales = defaultdict(lambda: {'qty': 0, 'profit': 0})
    profit_trend = defaultdict(float)
    
    for sale in sales_data:
        date = sale['date']
        daily_sales[date] += sale['total']
        profit_trend[date] += sale['profit']
        
        for item in sale['items']:
            med = item['medicine']
            product_sales[med]['qty'] += item['quantity']
            product_sales[med]['profit'] += (item['price'] - inventory[med]['cost']) * item['quantity']

    # Chart 1: Sales Trend
    if daily_sales:
        dates = sorted(daily_sales.keys())
        sales = [daily_sales[d] for d in dates]
        ax1.plot(dates, sales, marker='o', color=CHART_COLORS[0])
        ax1.set_title("Daily Sales Trend", fontweight='bold')
        ax1.set_ylabel("Sales Amount (₹)")
        ax1.tick_params(axis='x', rotation=45)
    else:
        ax1.text(0.5, 0.5, 'No sales data available', ha='center')

    # Chart 2: Top Selling Products
    if product_sales:
        top_meds = sorted(product_sales.items(), key=lambda x: x[1]['qty'], reverse=True)[:5]
        medicines = [med[0].title() for med in top_meds]
        quantities = [med[1]['qty'] for med in top_meds]
        ax2.bar(medicines, quantities, color=CHART_COLORS[1])
        ax2.set_title("Top Selling Medicines (Quantity)", fontweight='bold')
        ax2.set_ylabel("Units Sold")
        ax2.tick_params(axis='x', rotation=45)
    else:
        ax2.text(0.5, 0.5, 'No sales data available', ha='center')

    # Chart 3: Profit Analysis
    if profit_trend:
        dates = sorted(profit_trend.keys())
        profits = [profit_trend[d] for d in dates]
        ax3.fill_between(dates, profits, color=CHART_COLORS[2], alpha=0.4)
        ax3.plot(dates, profits, marker='o', color=CHART_COLORS[2])
        ax3.set_title("Profit Trend Analysis", fontweight='bold')
        ax3.set_ylabel("Profit (₹)")
        ax3.tick_params(axis='x', rotation=45)
    else:
        ax3.text(0.5, 0.5, 'No profit data available', ha='center')

    # Chart 4: Inventory Health
    low_stock = {k:v for k,v in inventory.items() if v['quantity'] < 20}
    healthy_stock = {k:v for k,v in inventory.items() if v['quantity'] >= 20}
    
    sizes = [len(low_stock), len(healthy_stock)]
    labels = ['Low Stock', 'Healthy Stock']
    colors = [CHART_COLORS[3], CHART_COLORS[0]]
    
    if any(sizes):
        ax4.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                startangle=90, wedgeprops={'edgecolor': 'white'})
        ax4.set_title("Inventory Health Status", fontweight='bold')
    else:
        ax4.text(0.5, 0.5, 'No inventory data', ha='center')

    # Adjust layout
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Embed chart in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Export and Refresh buttons
    button_frame = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame.pack(side=tk.BOTTOM, pady=10)
    
    if sales_data:
        tk.Button(button_frame, text="Export Sales Data", command=lambda: export_sales_data(),
                 bg="#3498db", fg="white").pack(side=tk.LEFT, padx=10)
    
    tk.Button(button_frame, text="🔄 Refresh Data", command=show_statistics_page,
             bg=ACCENT_COLOR, fg="white").pack(side=tk.LEFT, padx=10)

def export_sales_data():
    """Export sales data to CSV"""
    headers = ["Date", "Time", "Customer", "Patient ID", "Doctor", "Items", "Subtotal", "GST", "Total", "Profit"]
    data = []
    
    for sale in sales_data:
        items = ", ".join(f"{item['medicine']}({item['quantity']})" for item in sale['items'])
        data.append([
            sale['date'],
            sale['time'],
            sale['customer'],
            sale.get('patient_id', ''),
            sale.get('doctor', ''),
            items,
            f"₹{sale['subtotal']:.2f}",
            f"₹{sale['gst']:.2f}",
            f"₹{sale['total']:.2f}",
            f"₹{sale['profit']:.2f}"
        ])
    
    export_to_csv(data, headers, "pharmacy_sales_report.csv")

def show_transaction_history():
    clear_main_frame()
    
    tk.Label(main_frame, text="Transaction History", 
            font=("Helvetica", 18, "bold"), bg=BG_COLOR).pack(pady=10)
    
    # Filter Frame
    filter_frame = tk.Frame(main_frame, bg=BG_COLOR)
    filter_frame.pack(fill=tk.X, padx=20, pady=10)
    
    tk.Label(filter_frame, text="Filter by Date:", bg=BG_COLOR).pack(side=tk.LEFT, padx=5)
    date_combo = ttk.Combobox(filter_frame, values=sorted({sale['date'] for sale in sales_data}, reverse=True))
    date_combo.pack(side=tk.LEFT, padx=5)
    date_combo.bind("<<ComboboxSelected>>", lambda e: update_transaction_list(date_combo.get()))
    
    tk.Button(filter_frame, text="Show All", command=lambda: update_transaction_list(), 
             bg="#3498db", fg="white").pack(side=tk.LEFT, padx=10)
    
    # Transaction Treeview
    tree_frame = tk.Frame(main_frame, bg=BG_COLOR)
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    scroll_y = tk.Scrollbar(tree_frame)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    
    transaction_tree = ttk.Treeview(tree_frame, columns=("ID", "Date", "Time", "Customer", "Patient ID", "Items", "Total"), 
                                  yscrollcommand=scroll_y.set, height=20)
    scroll_y.config(command=transaction_tree.yview)
    
    transaction_tree.heading("#0", text="")
    transaction_tree.heading("ID", text="ID")
    transaction_tree.heading("Date", text="Date")
    transaction_tree.heading("Time", text="Time")
    transaction_tree.heading("Customer", text="Customer")
    transaction_tree.heading("Patient ID", text="Patient ID")
    transaction_tree.heading("Items", text="Items")
    transaction_tree.heading("Total", text="Total (₹)")
    
    transaction_tree.column("#0", width=0, stretch=tk.NO)
    transaction_tree.column("ID", width=50, anchor='center')
    transaction_tree.column("Date", width=100, anchor='center')
    transaction_tree.column("Time", width=80, anchor='center')
    transaction_tree.column("Customer", width=150)
    transaction_tree.column("Patient ID", width=100)
    transaction_tree.column("Items", width=200)
    transaction_tree.column("Total", width=100, anchor='e')
    
    transaction_tree.pack(fill=tk.BOTH, expand=True)
    
    def update_transaction_list(date=None):
        transaction_tree.delete(*transaction_tree.get_children())
        for i, sale in enumerate(reversed(sales_data)):
            if date and sale['date'] != date:
                continue
                
            items = ", ".join(f"{item['medicine']}({item['quantity']})" for item in sale['items'])
            transaction_tree.insert("", tk.END, values=(
                len(sales_data)-i,
                sale['date'],
                sale['time'],
                sale['customer'],
                sale.get('patient_id', ''),
                items,
                f"₹{sale['total']:.2f}"
            ))
    
    update_transaction_list()
    
    # View Details Button
    def view_transaction_details():
        selected = transaction_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a transaction")
            return
            
        index = len(sales_data) - int(transaction_tree.item(selected[0])['values'][0])
        sale = sales_data[index]
        
        details_window = tk.Toplevel(root)
        details_window.title(f"Transaction Details - {sale['date']}")
        details_window.geometry("600x500")
        
        details_text = tk.Text(details_window, wrap=tk.WORD, font=("Courier New", 12))
        details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text = f"Transaction ID: {len(sales_data)-index}\n"
        text += f"Date: {sale['date']} {sale['time']}\n"
        text += f"Customer: {sale['customer']}\n"
        if sale.get('patient_id'):
            text += f"Patient ID: {sale['patient_id']}\n"
        text += f"Doctor: {sale.get('doctor', 'N/A')}\n"
        text += f"GST: {sale.get('gst_number', 'N/A')}\n\n"
        text += "ITEMS PURCHASED:\n"
        text += "-"*50 + "\n"
        
        for item in sale['items']:
            text += f"{item['medicine'].title():<20} {item['quantity']:>3} x ₹{item['price']:>6.2f} = ₹{item['total']:>7.2f}\n"
        
        text += "-"*50 + "\n"
        text += f"Subtotal: ₹{sale['subtotal']:.2f}\n"
        text += f"GST (18%): ₹{sale['gst']:.2f}\n"
        text += f"TOTAL: ₹{sale['total']:.2f}\n"
        text += f"Profit: ₹{sale['profit']:.2f}\n"
        
        details_text.insert(tk.END, text)
        details_text.config(state=tk.DISABLED)
        
        tk.Button(details_window, text="Close", command=details_window.destroy,
                 bg="#3498db", fg="white").pack(pady=10)
    
    tk.Button(main_frame, text="View Details", command=view_transaction_details,
             bg="#2ecc71", fg="white").pack(pady=10)

def show_patient_management():
    clear_main_frame()
    
    tk.Label(main_frame, text="Patient Management System", 
            font=("Helvetica", 18, "bold"), bg=BG_COLOR).pack(pady=10)
    
    # Search Frame
    search_frame = tk.Frame(main_frame, bg=BG_COLOR)
    search_frame.pack(fill=tk.X, padx=20, pady=10)
    
    tk.Label(search_frame, text="Search Patient:", bg=BG_COLOR).pack(side=tk.LEFT, padx=5)
    search_entry = tk.Entry(search_frame, width=30)
    search_entry.pack(side=tk.LEFT, padx=5)
    search_entry.bind("<Return>", lambda e: search_patient())
    
    tk.Button(search_frame, text="Search", command=search_patient, 
             bg="#3498db", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(search_frame, text="Add New Patient", command=add_patient_dialog, 
             bg="#2ecc71", fg="white").pack(side=tk.LEFT, padx=5)
    
    # Patient Treeview
    tree_frame = tk.Frame(main_frame, bg=BG_COLOR)
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    scroll_y = tk.Scrollbar(tree_frame)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    
    patient_tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Age", "Gender", "Phone", "Last Visit"), 
                              yscrollcommand=scroll_y.set, height=15)
    scroll_y.config(command=patient_tree.yview)
    
    patient_tree.heading("#0", text="")
    patient_tree.heading("ID", text="Patient ID")
    patient_tree.heading("Name", text="Name")
    patient_tree.heading("Age", text="Age")
    patient_tree.heading("Gender", text="Gender")
    patient_tree.heading("Phone", text="Phone")
    patient_tree.heading("Last Visit", text="Last Visit")
    
    patient_tree.column("#0", width=0, stretch=tk.NO)
    patient_tree.column("ID", width=100, anchor='center')
    patient_tree.column("Name", width=150)
    patient_tree.column("Age", width=50, anchor='center')
    patient_tree.column("Gender", width=80, anchor='center')
    patient_tree.column("Phone", width=100, anchor='center')
    patient_tree.column("Last Visit", width=100, anchor='center')
    
    patient_tree.pack(fill=tk.BOTH, expand=True)
    
    # View/Edit/Delete buttons
    button_frame = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame.pack(fill=tk.X, padx=20, pady=10)
    
    tk.Button(button_frame, text="View Details", command=lambda: view_patient_details(patient_tree),
             bg="#3498db", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Edit Patient", command=lambda: edit_patient_dialog(patient_tree),
             bg="#f39c12", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Delete Patient", command=lambda: delete_patient(patient_tree),
             bg="#e74c3c", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Export Patients", command=export_patients,
             bg="#9b59b6", fg="white").pack(side=tk.LEFT, padx=5)
    
    def search_patient():
        query = search_entry.get().strip().lower()
        patient_tree.delete(*patient_tree.get_children())
        
        if not query:
            # Show all patients if search is empty
            for patient_id, data in patients_data.items():
                last_visit = "Never" if "purchases" not in data or not data["purchases"] else data["purchases"][-1]["date"]
                patient_tree.insert("", tk.END, values=(
                    patient_id,
                    data.get("name", ""),
                    data.get("age", ""),
                    data.get("gender", ""),
                    data.get("phone", ""),
                    last_visit
                ))
        else:
            # Filter patients based on search query
            for patient_id, data in patients_data.items():
                if (query in patient_id.lower() or 
                    query in data.get("name", "").lower() or 
                    query in data.get("phone", "")):
                    
                    last_visit = "Never" if "purchases" not in data or not data["purchases"] else data["purchases"][-1]["date"]
                    patient_tree.insert("", tk.END, values=(
                        patient_id,
                        data.get("name", ""),
                        data.get("age", ""),
                        data.get("gender", ""),
                        data.get("phone", ""),
                        last_visit
                    ))
    
    def add_patient_dialog():
        dialog = tk.Toplevel(root)
        dialog.title("Add New Patient")
        dialog.geometry("400x400")
        
        tk.Label(dialog, text="Patient ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        id_entry = tk.Entry(dialog)
        id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(dialog, text="Full Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(dialog)
        name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(dialog, text="Age:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        age_entry = tk.Entry(dialog)
        age_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(dialog, text="Gender:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        gender_combo = ttk.Combobox(dialog, values=["Male", "Female", "Other"])
        gender_combo.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(dialog, text="Phone:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        phone_entry = tk.Entry(dialog)
        phone_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(dialog, text="Address:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        address_entry = tk.Entry(dialog)
        address_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(dialog, text="Medical History:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        history_entry = tk.Text(dialog, height=5, width=30)
        history_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        
        def save_patient():
            patient_id = id_entry.get().strip()
            if not patient_id:
                messagebox.showwarning("Error", "Patient ID is required")
                return
                
            patients_data[patient_id] = {
                "name": name_entry.get().strip(),
                "age": age_entry.get().strip(),
                "gender": gender_combo.get().strip(),
                "phone": phone_entry.get().strip(),
                "address": address_entry.get().strip(),
                "medical_history": history_entry.get("1.0", tk.END).strip()
            }
            save_data()
            messagebox.showinfo("Success", "Patient added successfully")
            search_patient()  # Refresh the list
            dialog.destroy()
        
        tk.Button(dialog, text="Save", command=save_patient, 
                 bg="#2ecc71", fg="white").grid(row=7, column=1, pady=10, sticky="e")
    
    def view_patient_details(tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a patient")
            return
            
        patient_id = tree.item(selected[0])['values'][0]
        data = patients_data.get(patient_id, {})
        
        details_window = tk.Toplevel(root)
        details_window.title(f"Patient Details - {patient_id}")
        details_window.geometry("600x500")
        
        details_text = tk.Text(details_window, wrap=tk.WORD, font=("Arial", 12))
        details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text = f"Patient ID: {patient_id}\n"
        text += f"Name: {data.get('name', '')}\n"
        text += f"Age: {data.get('age', '')}\n"
        text += f"Gender: {data.get('gender', '')}\n"
        text += f"Phone: {data.get('phone', '')}\n"
        text += f"Address: {data.get('address', '')}\n\n"
        text += "Medical History:\n"
        text += "-"*50 + "\n"
        text += f"{data.get('medical_history', '')}\n\n"
        
        if "purchases" in data and data["purchases"]:
            text += "Purchase History:\n"
            text += "-"*50 + "\n"
            for purchase in data["purchases"]:
                text += f"{purchase['date']}: {', '.join(purchase['items'])}\n"
        else:
            text += "No purchase history\n"
        
        details_text.insert(tk.END, text)
        details_text.config(state=tk.DISABLED)
        
        tk.Button(details_window, text="Close", command=details_window.destroy,
                 bg="#3498db", fg="white").pack(pady=10)
    
    def edit_patient_dialog(tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a patient")
            return
            
        patient_id = tree.item(selected[0])['values'][0]
        data = patients_data.get(patient_id, {})
        
        dialog = tk.Toplevel(root)
        dialog.title(f"Edit Patient - {patient_id}")
        dialog.geometry("400x400")
        
        tk.Label(dialog, text="Patient ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(dialog, text=patient_id).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(dialog, text="Full Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(dialog)
        name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        name_entry.insert(0, data.get("name", ""))
        
        tk.Label(dialog, text="Age:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        age_entry = tk.Entry(dialog)
        age_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        age_entry.insert(0, data.get("age", ""))
        
        tk.Label(dialog, text="Gender:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        gender_combo = ttk.Combobox(dialog, values=["Male", "Female", "Other"])
        gender_combo.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        gender_combo.set(data.get("gender", ""))
        
        tk.Label(dialog, text="Phone:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        phone_entry = tk.Entry(dialog)
        phone_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        phone_entry.insert(0, data.get("phone", ""))
        
        tk.Label(dialog, text="Address:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        address_entry = tk.Entry(dialog)
        address_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        address_entry.insert(0, data.get("address", ""))
        
        tk.Label(dialog, text="Medical History:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        history_entry = tk.Text(dialog, height=5, width=30)
        history_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        history_entry.insert(tk.END, data.get("medical_history", ""))
        
        def update_patient():
            patients_data[patient_id] = {
                "name": name_entry.get().strip(),
                "age": age_entry.get().strip(),
                "gender": gender_combo.get().strip(),
                "phone": phone_entry.get().strip(),
                "address": address_entry.get().strip(),
                "medical_history": history_entry.get("1.0", tk.END).strip(),
                "purchases": data.get("purchases", [])  # Preserve purchase history
            }
            save_data()
            messagebox.showinfo("Success", "Patient updated successfully")
            search_patient()  # Refresh the list
            dialog.destroy()
        
        tk.Button(dialog, text="Update", command=update_patient, 
                 bg="#2ecc71", fg="white").grid(row=7, column=1, pady=10, sticky="e")
    
    def delete_patient(tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a patient")
            return
            
        patient_id = tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete patient {patient_id}?"):
            del patients_data[patient_id]
            save_data()
            search_patient()  # Refresh the list
            messagebox.showinfo("Success", "Patient deleted successfully")
    
    def export_patients():
        """Export patient data to CSV"""
        headers = ["Patient ID", "Name", "Age", "Gender", "Phone", "Address", "Last Visit"]
        data = []
        
        for patient_id, details in patients_data.items():
            last_visit = "Never" if "purchases" not in details or not details["purchases"] else details["purchases"][-1]["date"]
            data.append([
                patient_id,
                details.get("name", ""),
                details.get("age", ""),
                details.get("gender", ""),
                details.get("phone", ""),
                details.get("address", ""),
                last_visit
            ])
        
        export_to_csv(data, headers, "patient_records.csv")
    
    # Initial load of patients
    search_patient()

def show_supplier_management():
    clear_main_frame()
    
    tk.Label(main_frame, text="Supplier Management System", 
            font=("Helvetica", 18, "bold"), bg=BG_COLOR).pack(pady=10)
    
    # Search Frame
    search_frame = tk.Frame(main_frame, bg=BG_COLOR)
    search_frame.pack(fill=tk.X, padx=20, pady=10)
    
    tk.Label(search_frame, text="Search Supplier:", bg=BG_COLOR).pack(side=tk.LEFT, padx=5)
    search_entry = tk.Entry(search_frame, width=30)
    search_entry.pack(side=tk.LEFT, padx=5)
    search_entry.bind("<Return>", lambda event: search_supplier())  # Fixed binding
    
    # ... rest of the function remains the same ...
    
    tk.Button(search_frame, text="Search", command=search_supplier, 
             bg="#3498db", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(search_frame, text="Add New Supplier", command=add_supplier_dialog, 
             bg="#2ecc71", fg="white").pack(side=tk.LEFT, padx=5)
    
    # Supplier Treeview
    tree_frame = tk.Frame(main_frame, bg=BG_COLOR)
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    scroll_y = tk.Scrollbar(tree_frame)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    
    supplier_tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Contact", "Email", "Address"), 
                               yscrollcommand=scroll_y.set, height=15)
    scroll_y.config(command=supplier_tree.yview)
    
    supplier_tree.heading("#0", text="")
    supplier_tree.heading("ID", text="Supplier ID")
    supplier_tree.heading("Name", text="Supplier Name")
    supplier_tree.heading("Contact", text="Contact")
    supplier_tree.heading("Email", text="Email")
    supplier_tree.heading("Address", text="Address")
    
    supplier_tree.column("#0", width=0, stretch=tk.NO)
    supplier_tree.column("ID", width=100, anchor='center')
    supplier_tree.column("Name", width=150)
    supplier_tree.column("Contact", width=100, anchor='center')
    supplier_tree.column("Email", width=150)
    supplier_tree.column("Address", width=200)
    
    supplier_tree.pack(fill=tk.BOTH, expand=True)
    
    # View/Edit/Delete buttons
    button_frame = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame.pack(fill=tk.X, padx=20, pady=10)
    
    tk.Button(button_frame, text="View Details", command=lambda: view_supplier_details(supplier_tree),
             bg="#3498db", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Edit Supplier", command=lambda: edit_supplier_dialog(supplier_tree),
             bg="#f39c12", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Delete Supplier", command=lambda: delete_supplier(supplier_tree),
             bg="#e74c3c", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Export Suppliers", command=export_suppliers,
             bg="#9b59b6", fg="white").pack(side=tk.LEFT, padx=5)
    
    def search_supplier():
     query = search_entry.get().strip().lower()
    supplier_tree.delete(*supplier_tree.get_children())
    
    if not query: # type: ignore
        # Show all suppliers if search is empty
        for supplier_id, data in suppliers_data.items():
            supplier_tree.insert("", tk.END, values=(
                supplier_id,
                data.get("name", ""),
                data.get("contact", ""),
                data.get("email", ""),
                data.get("address", "")
            ))
    else:
        # Filter suppliers based on search query
        for supplier_id, data in suppliers_data.items():
            if (query in supplier_id.lower() or  # type: ignore
                query in data.get("name", "").lower() or  # type: ignore
                query in data.get("contact", "").lower() or # type: ignore
                query in data.get("email", "").lower()): # type: ignore
                
                supplier_tree.insert("", tk.END, values=(
                    supplier_id,
                    data.get("name", ""),
                    data.get("contact", ""),
                    data.get("email", ""),
                    data.get("address", "")
                ))
    
    def add_supplier_dialog():
        dialog = tk.Toplevel(root)
        dialog.title("Add New Supplier")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="Supplier ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        id_entry = tk.Entry(dialog)
        id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(dialog, text="Supplier Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(dialog)
        name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(dialog, text="Contact:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        contact_entry = tk.Entry(dialog)
        contact_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(dialog, text="Email:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        email_entry = tk.Entry(dialog)
        email_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(dialog, text="Address:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        address_entry = tk.Entry(dialog)
        address_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        def save_supplier():
            supplier_id = id_entry.get().strip()
            if not supplier_id:
                messagebox.showwarning("Error", "Supplier ID is required")
                return
                
            suppliers_data[supplier_id] = {
                "name": name_entry.get().strip(),
                "contact": contact_entry.get().strip(),
                "email": email_entry.get().strip(),
                "address": address_entry.get().strip()
            }
            save_data()
            messagebox.showinfo("Success", "Supplier added successfully")
            search_supplier()  # Refresh the list
            dialog.destroy()
        
        tk.Button(dialog, text="Save", command=save_supplier, 
                 bg="#2ecc71", fg="white").grid(row=5, column=1, pady=10, sticky="e")
    
    def view_supplier_details(tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a supplier")
            return
            
        supplier_id = tree.item(selected[0])['values'][0]
        data = suppliers_data.get(supplier_id, {})
        
        details_window = tk.Toplevel(root)
        details_window.title(f"Supplier Details - {supplier_id}")
        details_window.geometry("500x300")
        
        details_text = tk.Text(details_window, wrap=tk.WORD, font=("Arial", 12))
        details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text = f"Supplier ID: {supplier_id}\n"
        text += f"Name: {data.get('name', '')}\n"
        text += f"Contact: {data.get('contact', '')}\n"
        text += f"Email: {data.get('email', '')}\n"
        text += f"Address: {data.get('address', '')}\n\n"
        
        # Get medicines supplied by this supplier
        supplied_meds = [med for med, details in inventory.items() if details.get('supplier') == supplier_id]
        if supplied_meds:
            text += "Supplied Medicines:\n"
            text += "-"*50 + "\n"
            text += "\n".join(supplied_meds)
        else:
            text += "No medicines supplied by this supplier\n"
        
        details_text.insert(tk.END, text)
        details_text.config(state=tk.DISABLED)
        
        tk.Button(details_window, text="Close", command=details_window.destroy,
                 bg="#3498db", fg="white").pack(pady=10)
    
    def edit_supplier_dialog(tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a supplier")
            return
            
        supplier_id = tree.item(selected[0])['values'][0]
        data = suppliers_data.get(supplier_id, {})
        
        dialog = tk.Toplevel(root)
        dialog.title(f"Edit Supplier - {supplier_id}")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="Supplier ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(dialog, text=supplier_id).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(dialog, text="Supplier Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(dialog)
        name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        name_entry.insert(0, data.get("name", ""))
        
        tk.Label(dialog, text="Contact:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        contact_entry = tk.Entry(dialog)
        contact_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        contact_entry.insert(0, data.get("contact", ""))
        
        tk.Label(dialog, text="Email:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        email_entry = tk.Entry(dialog)
        email_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        email_entry.insert(0, data.get("email", ""))
        
        tk.Label(dialog, text="Address:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        address_entry = tk.Entry(dialog)
        address_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        address_entry.insert(0, data.get("address", ""))
        
        def update_supplier():
            suppliers_data[supplier_id] = {
                "name": name_entry.get().strip(),
                "contact": contact_entry.get().strip(),
                "email": email_entry.get().strip(),
                "address": address_entry.get().strip()
            }
            save_data()
            messagebox.showinfo("Success", "Supplier updated successfully")
            search_supplier()  # Refresh the list
            dialog.destroy()
        
        tk.Button(dialog, text="Update", command=update_supplier, 
                 bg="#2ecc71", fg="white").grid(row=5, column=1, pady=10, sticky="e")
    
    def delete_supplier(tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a supplier")
            return
            
        supplier_id = tree.item(selected[0])['values'][0]
        
        # Check if any medicines are supplied by this supplier
        supplied_meds = [med for med, details in inventory.items() if details.get('supplier') == supplier_id]
        if supplied_meds:
            messagebox.showerror("Error", 
                f"Cannot delete supplier. {len(supplied_meds)} medicines are supplied by this supplier.")
            return
            
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete supplier {supplier_id}?"):
            del suppliers_data[supplier_id]
            save_data()
            search_supplier()  # Refresh the list
            messagebox.showinfo("Success", "Supplier deleted successfully")
    
    def export_suppliers():
        """Export supplier data to CSV"""
        headers = ["Supplier ID", "Name", "Contact", "Email", "Address"]
        data = []
        
        for supplier_id, details in suppliers_data.items():
            data.append([
                supplier_id,
                details.get("name", ""),
                details.get("contact", ""),
                details.get("email", ""),
                details.get("address", "")
            ])
        
        export_to_csv(data, headers, "supplier_records.csv")
    
    # Initial load of suppliers
    search_supplier()

def show_financial_tools():
    clear_main_frame()
    
    tk.Label(main_frame, text="Financial Tools", 
            font=("Helvetica", 18, "bold"), bg=BG_COLOR).pack(pady=10)
    
    # Financial Summary Frame
    summary_frame = tk.LabelFrame(main_frame, text="Financial Summary", bg=BG_COLOR)
    summary_frame.pack(fill=tk.X, padx=20, pady=10)
    
    # Calculate financial data
    total_sales = sum(sale['total'] for sale in sales_data)
    total_profit = sum(sale['profit'] for sale in sales_data)
    total_gst = sum(sale['gst'] for sale in sales_data)
    inventory_value = sum(item['quantity'] * item['cost'] for item in inventory.values())
    
    # Display summary
    tk.Label(summary_frame, text="Total Sales:", bg=BG_COLOR).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tk.Label(summary_frame, text=f"₹{total_sales:.2f}", bg=BG_COLOR, font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5, pady=5, sticky="w")
    
    tk.Label(summary_frame, text="Total Profit:", bg=BG_COLOR).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    tk.Label(summary_frame, text=f"₹{total_profit:.2f}", bg=BG_COLOR, font=("Arial", 10, "bold")).grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    tk.Label(summary_frame, text="Total GST Collected:", bg=BG_COLOR).grid(row=2, column=0, padx=5, pady=5, sticky="e")
    tk.Label(summary_frame, text=f"₹{total_gst:.2f}", bg=BG_COLOR, font=("Arial", 10, "bold")).grid(row=2, column=1, padx=5, pady=5, sticky="w")
    
    tk.Label(summary_frame, text="Inventory Value:", bg=BG_COLOR).grid(row=3, column=0, padx=5, pady=5, sticky="e")
    tk.Label(summary_frame, text=f"₹{inventory_value:.2f}", bg=BG_COLOR, font=("Arial", 10, "bold")).grid(row=3, column=1, padx=5, pady=5, sticky="w")
    
    # Date Range Filter Frame
    filter_frame = tk.LabelFrame(main_frame, text="Date Range Filter", bg=BG_COLOR)
    filter_frame.pack(fill=tk.X, padx=20, pady=10)
    
    tk.Label(filter_frame, text="From:", bg=BG_COLOR).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    from_date = tk.Entry(filter_frame)
    from_date.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    
    tk.Label(filter_frame, text="To:", bg=BG_COLOR).grid(row=0, column=2, padx=5, pady=5, sticky="e")
    to_date = tk.Entry(filter_frame)
    to_date.grid(row=0, column=3, padx=5, pady=5, sticky="w")
    
    # Results Frame
    results_frame = tk.LabelFrame(main_frame, text="Filtered Results", bg=BG_COLOR)
    results_frame.pack(fill=tk.X, padx=20, pady=10)
    
    tk.Label(results_frame, text="Filtered Sales:", bg=BG_COLOR).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    filtered_sales_label = tk.Label(results_frame, text="₹0.00", bg=BG_COLOR)
    filtered_sales_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    
    tk.Label(results_frame, text="Filtered Profit:", bg=BG_COLOR).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    filtered_profit_label = tk.Label(results_frame, text="₹0.00", bg=BG_COLOR)
    filtered_profit_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    tk.Label(results_frame, text="Filtered GST:", bg=BG_COLOR).grid(row=2, column=0, padx=5, pady=5, sticky="e")
    filtered_gst_label = tk.Label(results_frame, text="₹0.00", bg=BG_COLOR)
    filtered_gst_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    
    # Button Frame
    button_frame = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame.pack(fill=tk.X, padx=20, pady=10)
    
    def calculate_filtered():
        from_dt = from_date.get().strip()
        to_dt = to_date.get().strip()
        
        if not from_dt or not to_dt:
            messagebox.showwarning("Error", "Please enter both from and to dates")
            return
            
        filtered_sales = 0
        filtered_profit = 0
        filtered_gst = 0
        
        for sale in sales_data:
            if from_dt <= sale['date'] <= to_dt:
                filtered_sales += sale['total']
                filtered_profit += sale['profit']
                filtered_gst += sale['gst']
        
        filtered_sales_label.config(text=f"₹{filtered_sales:.2f}")
        filtered_profit_label.config(text=f"₹{filtered_profit:.2f}")
        filtered_gst_label.config(text=f"₹{filtered_gst:.2f}")
    
    def export_financial_report():
        """Export financial report to CSV"""
        headers = ["Date", "Sales", "Profit", "GST"]
        data = []
        
        # Group by date
        daily_sales = defaultdict(lambda: {'sales': 0, 'profit': 0, 'gst': 0})
        for sale in sales_data:
            date = sale['date']
            daily_sales[date]['sales'] += sale['total']
            daily_sales[date]['profit'] += sale['profit']
            daily_sales[date]['gst'] += sale['gst']
        
        # Prepare data for export
        for date, values in sorted(daily_sales.items()):
            data.append([
                date,
                f"₹{values['sales']:.2f}",
                f"₹{values['profit']:.2f}",
                f"₹{values['gst']:.2f}"
            ])
        
        # Add totals row
        data.append([
            "TOTAL",
            f"₹{sum(sale['total'] for sale in sales_data):.2f}",
            f"₹{sum(sale['profit'] for sale in sales_data):.2f}",
            f"₹{sum(sale['gst'] for sale in sales_data):.2f}"
        ])
        
        export_to_csv(data, headers, "financial_report.csv")
    
    tk.Button(button_frame, text="Calculate", command=calculate_filtered, 
             bg="#3498db", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Export Report", command=export_financial_report,
             bg="#2ecc71", fg="white").pack(side=tk.LEFT, padx=5)

def show_reporting_system():
    clear_main_frame()
    
    tk.Label(main_frame, text="Reporting System", 
            font=("Helvetica", 18, "bold"), bg=BG_COLOR).pack(pady=10)
    
    # Report Selection Frame
    report_frame = tk.LabelFrame(main_frame, text="Select Report Type", bg=BG_COLOR)
    report_frame.pack(fill=tk.X, padx=20, pady=10)
    
    report_var = tk.StringVar()
    report_var.set("sales")  # default selection
    
    tk.Radiobutton(report_frame, text="Sales Report", variable=report_var, 
                  value="sales", bg=BG_COLOR).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    tk.Radiobutton(report_frame, text="Inventory Report", variable=report_var, 
                  value="inventory", bg=BG_COLOR).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    tk.Radiobutton(report_frame, text="Patient Report", variable=report_var, 
                  value="patients", bg=BG_COLOR).grid(row=2, column=0, padx=5, pady=5, sticky="w")
    tk.Radiobutton(report_frame, text="Supplier Report", variable=report_var, 
                  value="suppliers", bg=BG_COLOR).grid(row=3, column=0, padx=5, pady=5, sticky="w")
    
    # Date Range Frame (for sales report)
    date_frame = tk.LabelFrame(main_frame, text="Date Range (for Sales Report)", bg=BG_COLOR)
    date_frame.pack(fill=tk.X, padx=20, pady=10)
    
    tk.Label(date_frame, text="From:", bg=BG_COLOR).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    from_date = tk.Entry(date_frame)
    from_date.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    
    tk.Label(date_frame, text="To:", bg=BG_COLOR).grid(row=0, column=2, padx=5, pady=5, sticky="e")
    to_date = tk.Entry(date_frame)
    to_date.grid(row=0, column=3, padx=5, pady=5, sticky="w")
    
    # Preview Frame
    preview_frame = tk.LabelFrame(main_frame, text="Report Preview", bg=BG_COLOR)
    preview_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    scroll_y = tk.Scrollbar(preview_frame)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    
    report_text = tk.Text(preview_frame, wrap=tk.WORD, yscrollcommand=scroll_y.set)
    report_text.pack(fill=tk.BOTH, expand=True)
    scroll_y.config(command=report_text.yview)
    
    # Button Frame
    button_frame = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame.pack(fill=tk.X, padx=20, pady=10)
    
    def generate_report():
        report_type = report_var.get()
        report_text.delete(1.0, tk.END)
        
        if report_type == "sales":
            from_dt = from_date.get().strip()
            to_dt = to_date.get().strip()
            
            if not from_dt or not to_dt:
                messagebox.showwarning("Error", "Please enter both from and to dates for sales report")
                return
                
            # Filter sales by date range
            filtered_sales = [sale for sale in sales_data if from_dt <= sale['date'] <= to_dt]
            
            if not filtered_sales:
                report_text.insert(tk.END, "No sales data found for the selected date range")
                return
                
            # Generate sales report
            report_text.insert(tk.END, f"SALES REPORT ({from_dt} to {to_dt})\n")
            report_text.insert(tk.END, "="*50 + "\n\n")
            
            total_sales = 0
            total_profit = 0
            total_gst = 0
            
            # Group by date
            daily_sales = defaultdict(lambda: {'sales': 0, 'profit': 0, 'gst': 0})
            for sale in filtered_sales:
                date = sale['date']
                daily_sales[date]['sales'] += sale['total']
                daily_sales[date]['profit'] += sale['profit']
                daily_sales[date]['gst'] += sale['gst']
                total_sales += sale['total']
                total_profit += sale['profit']
                total_gst += sale['gst']
            
            # Add daily sales to report
            for date, values in sorted(daily_sales.items()):
                report_text.insert(tk.END, f"Date: {date}\n")
                report_text.insert(tk.END, f"Total Sales: ₹{values['sales']:.2f}\n")
                report_text.insert(tk.END, f"Total Profit: ₹{values['profit']:.2f}\n")
                report_text.insert(tk.END, f"Total GST: ₹{values['gst']:.2f}\n")
                report_text.insert(tk.END, "-"*50 + "\n")
            
            # Add summary
            report_text.insert(tk.END, "\nSUMMARY\n")
            report_text.insert(tk.END, "="*50 + "\n")
            report_text.insert(tk.END, f"Total Sales: ₹{total_sales:.2f}\n")
            report_text.insert(tk.END, f"Total Profit: ₹{total_profit:.2f}\n")
            report_text.insert(tk.END, f"Total GST: ₹{total_gst:.2f}\n")
            
        elif report_type == "inventory":
            # Generate inventory report
            report_text.insert(tk.END, "INVENTORY REPORT\n")
            report_text.insert(tk.END, "="*50 + "\n\n")
            
            low_stock = {k:v for k,v in inventory.items() if v['quantity'] < 20}
            healthy_stock = {k:v for k,v in inventory.items() if v['quantity'] >= 20}
            
            report_text.insert(tk.END, f"Total Medicines: {len(inventory)}\n")
            report_text.insert(tk.END, f"Low Stock Items: {len(low_stock)}\n")
            report_text.insert(tk.END, f"Healthy Stock Items: {len(healthy_stock)}\n\n")
            
            report_text.insert(tk.END, "LOW STOCK ITEMS:\n")
            report_text.insert(tk.END, "-"*50 + "\n")
            for med, details in low_stock.items():
                report_text.insert(tk.END, f"{med.title()}: {details['quantity']} units (Supplier: {details['supplier']})\n")
            
            report_text.insert(tk.END, "\nINVENTORY VALUE:\n")
            report_text.insert(tk.END, "-"*50 + "\n")
            inventory_value = sum(item['quantity'] * item['cost'] for item in inventory.values())
            report_text.insert(tk.END, f"Total Inventory Value: ₹{inventory_value:.2f}\n")
            
        elif report_type == "patients":
            # Generate patient report
            report_text.insert(tk.END, "PATIENT REPORT\n")
            report_text.insert(tk.END, "="*50 + "\n\n")
            
            report_text.insert(tk.END, f"Total Patients: {len(patients_data)}\n\n")
            
            # Patients with purchases
            patients_with_purchases = [p for p in patients_data.values() if "purchases" in p and p["purchases"]]
            report_text.insert(tk.END, f"Patients with purchases: {len(patients_with_purchases)}\n")
            report_text.insert(tk.END, f"Patients without purchases: {len(patients_data) - len(patients_with_purchases)}\n\n")
            
            # Top patients by purchases
            if patients_with_purchases:
                patient_purchase_counts = []
                for patient_id, data in patients_data.items():
                    if "purchases" in data:
                        patient_purchase_counts.append((patient_id, data.get("name", ""), len(data["purchases"])))
                
                # Sort by purchase count descending
                patient_purchase_counts.sort(key=lambda x: x[2], reverse=True)
                
                report_text.insert(tk.END, "TOP PATIENTS BY PURCHASES:\n")
                report_text.insert(tk.END, "-"*50 + "\n")
                for patient_id, name, count in patient_purchase_counts[:5]:  # Top 5
                    report_text.insert(tk.END, f"{name} (ID: {patient_id}): {count} purchases\n")
            
        elif report_type == "suppliers":
            # Generate supplier report
            report_text.insert(tk.END, "SUPPLIER REPORT\n")
            report_text.insert(tk.END, "="*50 + "\n\n")
            
            report_text.insert(tk.END, f"Total Suppliers: {len(suppliers_data)}\n\n")
            
            # Supplier statistics
            supplier_med_counts = defaultdict(int)
            for med, details in inventory.items():
                supplier_med_counts[details['supplier']] += 1
            
            report_text.insert(tk.END, "SUPPLIERS AND THEIR MEDICINES:\n")
            report_text.insert(tk.END, "-"*50 + "\n")
            for supplier_id, count in sorted(supplier_med_counts.items(), key=lambda x: x[1], reverse=True):
                supplier_name = suppliers_data.get(supplier_id, {}).get("name", "Unknown")
                report_text.insert(tk.END, f"{supplier_name} (ID: {supplier_id}): {count} medicines\n")
    
    def export_report():
        report_type = report_var.get()
        content = report_text.get(1.0, tk.END)
        
        if not content.strip():
            messagebox.showwarning("Error", "Please generate a report first")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"{report_type}_report.txt"
        )
        
        if filepath:
            with open(filepath, 'w') as f:
                f.write(content)
            messagebox.showinfo("Success", f"Report exported to {filepath}")
    
    tk.Button(button_frame, text="Generate Report", command=generate_report, 
             bg="#3498db", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Export Report", command=export_report,
             bg="#2ecc71", fg="white").pack(side=tk.LEFT, padx=5)

def show_login_page():
    clear_main_frame()
    
    login_frame = tk.Frame(main_frame, bg=BG_COLOR)
    login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    tk.Label(login_frame, text="Zinc.inc Pharmacy", 
            font=("Helvetica", 24, "bold"), bg=BG_COLOR).grid(row=0, column=0, columnspan=2, pady=20)
    
    tk.Label(login_frame, text="Username:", bg=BG_COLOR).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    user_entry = tk.Entry(login_frame)
    user_entry.grid(row=1, column=1, padx=5, pady=5)
    user_entry.bind("<Return>", lambda e: pass_entry.focus())
    
    tk.Label(login_frame, text="Password:", bg=BG_COLOR).grid(row=2, column=0, padx=5, pady=5, sticky="e")
    pass_entry = tk.Entry(login_frame, show="*")
    pass_entry.grid(row=2, column=1, padx=5, pady=5)
    pass_entry.bind("<Return>", lambda e: login())
    
    def login():
        global current_user
        username = user_entry.get()
        password = pass_entry.get()
        
        if username in USERS and USERS[username] == password:
            current_user = username
            show_invoice_page()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    tk.Button(login_frame, text="Login", command=login, 
             bg="#3498db", fg="white", width=15).grid(row=3, column=0, columnspan=2, pady=20)

# ==== SIDEBAR BUTTONS ====
sidebar_buttons = [
    ("🧾 Invoice", "#1abc9c", show_invoice_page),
    ("📦 Restock", "#16a085", show_restock_page),
    ("👨‍⚕️ Patients", "#3498db", show_patient_management),
    ("🏭 Suppliers", "#9b59b6", show_supplier_management),
    ("💰 Finance", "#f1c40f", show_financial_tools),
    ("📊 Reports", "#2c3e50", show_reporting_system),
    ("📈 Statistics", "#2980b9", show_statistics_page),
    ("📋 Transactions", "#8e44ad", show_transaction_history),
    ("🔐 Logout", "#e74c3c", show_login_page)
]

for text, color, command in sidebar_buttons:
    btn = tk.Button(sidebar, text=text, font=("Segoe UI", 12, "bold"),
                   bg=color, fg="white", command=command, anchor='w')
    btn.pack(fill=tk.X, padx=5, pady=5)

# ==== START APPLICATION ====
show_login_page()
root.mainloop()