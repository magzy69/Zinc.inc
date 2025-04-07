import csv
import os
from datetime import datetime

def load_inventory():
    inventory = []
    with open('inventory.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            inventory.append({
                'name': row['name'].strip().lower(),
                'quantity': int(row['quantity']),
                'price': float(row['price']),
                'cost_price': float(row['cost_price'])
            })
    return inventory

def save_inventory(inventory):
    with open('inventory.csv', 'w', newline='') as file:
        fieldnames = ['name', 'quantity', 'price', 'cost_price']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in inventory:
            writer.writerow(item)

def view_inventory(inventory):
    print("\n📦 Current Inventory:")
    print("{:<20} {:<10} {:<10} {:<10}".format("Medicine", "Qty", "Price(₹)", "Cost(₹)"))
    print("-" * 55)
    for item in inventory:
        print("{:<20} {:<10} {:<10} {:<10}".format(item['name'].title(), item['quantity'], item['price'], item['cost_price']))

def sell_medicines(inventory):
    buyer_name = input("\nEnter buyer's name: ").strip().title()
    cart = []
    while True:
        medicine_name = input("\nEnter medicine name to sell (or 'done' to finish): ").strip().lower()
        if medicine_name == 'done':
            break
        found = False
        for item in inventory:
            if item['name'] == medicine_name:
                found = True
                print(f"Available: {item['quantity']} units at ₹{item['price']} each")
                qty = int(input("Enter quantity to dispense: "))
                if qty <= item['quantity']:
                    item['quantity'] -= qty
                    cart.append((item, qty))
                else:
                    print("❌ Not enough stock.")
                break
        if not found:
            print("❌ Medicine not found in inventory.")

    if not cart:
        print("🛒 No items sold.")
        return

    gst_input = input("Enter GST rate (leave empty for 18% default): ")
    try:
        gst_rate = float(gst_input) if gst_input else 18.0
    except ValueError:
        gst_rate = 18.0

    total_amount = 0
    total_profit = 0
    invoice_lines = []

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile('sales.csv')
    is_empty = not file_exists or os.stat('sales.csv').st_size == 0

    with open('sales.csv', 'a', newline='') as sales_file:
        fieldnames = ['timestamp', 'buyer', 'medicine', 'quantity', 'price_per_unit', 'cost_price', 'total', 'profit']
        writer = csv.DictWriter(sales_file, fieldnames=fieldnames)
        if is_empty:
            writer.writeheader()

        for item, qty in cart:
            total = qty * item['price']
            profit = (item['price'] - item['cost_price']) * qty
            total_amount += total
            total_profit += profit

            writer.writerow({
                'timestamp': timestamp,
                'buyer': buyer_name,
                'medicine': item['name'].title(),
                'quantity': qty,
                'price_per_unit': item['price'],
                'cost_price': item['cost_price'],
                'total': total,
                'profit': profit
            })

            invoice_lines.append(
                f"{item['name'].title()} x{qty} @ ₹{item['price']} = ₹{total} (Profit: ₹{profit})"
            )

    gst_amount = (total_amount * gst_rate) / 100
    grand_total = total_amount + gst_amount

    invoice_name = f"invoice_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    with open(invoice_name, 'w', encoding='utf-8') as invoice:
        invoice.write("Zinc.inc Pharmacy Invoice\n")
        invoice.write("------------------------------\n")
        invoice.write(f"Date: {timestamp}\n")
        invoice.write(f"Buyer: {buyer_name}\n")
        invoice.write(f"GST Rate: {gst_rate}%\n")
        invoice.write("------------------------------\n")
        for line in invoice_lines:
            invoice.write(line + "\n")
        invoice.write("------------------------------\n")
        invoice.write(f"Subtotal: ₹{total_amount}\n")
        invoice.write(f"GST: ₹{gst_amount}\n")
        invoice.write(f"Grand Total: ₹{grand_total}\n")
        invoice.write(f"Total Profit: ₹{total_profit}\n")
        invoice.write("------------------------------\n")
        invoice.write("Thank you for your purchase!\n")

    print(f"📄 Invoice saved as: {invoice_name}")
    print(f"✅ Total Sale: ₹{grand_total} | Profit: ₹{total_profit}")

def restock_inventory(inventory):
    medicine_name = input("\nEnter medicine name to restock (or add new): ").strip().lower()
    qty = int(input("Enter quantity to add: "))
    price = float(input("Enter selling price per unit (₹): "))
    cost_price = float(input("Enter cost price per unit (₹): "))

    for item in inventory:
        if item['name'] == medicine_name:
            item['quantity'] += qty
            item['price'] = price
            item['cost_price'] = cost_price
            print(f"🔄 Updated {medicine_name.title()} with {qty} more units.")
            return

    inventory.append({
        'name': medicine_name,
        'quantity': qty,
        'price': price,
        'cost_price': cost_price
    })
    print(f"➕ Added new medicine: {medicine_name.title()}")

def view_sales_summary():
    total_sales = 0
    total_profit = 0
    try:
        with open('sales.csv', 'r') as file:
            reader = csv.DictReader(file)
            print("\n📊 All-Time Sales Summary:")
            for row in reader:
                profit = float(row.get('profit', 0))
                print(f"{row['timestamp']} | {row['buyer']}: {row['medicine']} x{row['quantity']} = ₹{row['total']} (Profit: ₹{profit})")
                total_sales += float(row['total'])
                total_profit += profit
        print(f"\n💰 Total Sales: ₹{total_sales}")
        print(f"📈 Total Profit: ₹{total_profit}")
    except FileNotFoundError:
        print("No sales data found.")

def view_today_report():
    today = datetime.now().strftime("%Y-%m-%d")
    total_sales = 0
    total_profit = 0
    print("\n📅 Today's Sales Report:")
    try:
        with open('sales.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['timestamp'].startswith(today):
                    profit = float(row.get('profit', 0))
                    print(f"{row['timestamp']} | {row['buyer']}: {row['medicine']} x{row['quantity']} = ₹{row['total']} (Profit: ₹{profit})")
                    total_sales += float(row['total'])
                    total_profit += profit
        print(f"\n📟 Total Sales Today: ₹{total_sales}")
        print(f"💸 Total Profit Today: ₹{total_profit}")
    except FileNotFoundError:
        print("No sales data available.")

# Main loop
while True:
    print("\n🧪 Zinc.inc Pharmacy Software")
    print("1. Sell Medicines")
    print("2. Restock Inventory")
    print("3. View All-Time Sales Summary")
    print("4. View Today's Report")
    print("5. View Inventory")
    print("0. Exit")

    choice = input("Choose an option: ")
    inventory = load_inventory()

    if choice == '1':
        sell_medicines(inventory)
        save_inventory(inventory)
    elif choice == '2':
        restock_inventory(inventory)
        save_inventory(inventory)
    elif choice == '3':
        view_sales_summary()
    elif choice == '4':
        view_today_report()
    elif choice == '5':
        view_inventory(inventory)
    elif choice == '0':
        print("👋 Exiting Zinc.inc. Goodbye!")
        break
    else:
        print("❌ Invalid option. Please choose again.")
