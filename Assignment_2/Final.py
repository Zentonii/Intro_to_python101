import csv
import os
from datetime import datetime

CSV_FILE = "orders.csv"
FIELDNAMES = ["id", "customer_name", "address", "description", "date", "total_amount", "delivered"]

def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

def read_orders():
    with open(CSV_FILE, "r", newline="") as f:
        return list(csv.DictReader(f))

def write_orders(orders):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(orders)

def get_next_id(orders):
    if not orders:
        return 1
    return max(int(o["id"]) for o in orders) + 1

def add_order():
    print("\n--- Add New Order ---")
    name = input("Customer name: ").strip()
    if not name:
        print("Error: Customer name cannot be empty.")
        return

    address = input("Address: ").strip()
    if not address:
        print("Error: Address cannot be empty.")
        return

    description = input("Description: ").strip()
    if not description:
        print("Error: Description cannot be empty.")
        return

    while True:
        date_str = input("Date (YYYY/MM/DD): ").strip()
        try:
            datetime.strptime(date_str, "%Y/%m/%d")
            break
        except ValueError:
            print("Invalid date format. Please use YYYY/MM/DD.")

    while True:
        amount_str = input("Total amount: ").strip()
        try:
            total = float(amount_str)
            if total < 0:
                print("Amount cannot be negative.")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a number.")

    orders = read_orders()
    new_order = {
        "id": get_next_id(orders),
        "customer_name": name,
        "address": address,
        "description": description,
        "date": date_str,
        "total_amount": f"{total:.2f}",
        "delivered": "False"
    }
    orders.append(new_order)
    write_orders(orders)
    print(f"\nOrder added successfully! Assigned Order ID: {new_order['id']}")

def mark_delivered():
    print("\n--- Mark Order as Delivered ---")
    order_id = input("Enter Order ID: ").strip()

    orders = read_orders()
    for order in orders:
        if order["id"] == order_id:
            if order["delivered"] == "True":
                print(f"Order #{order_id} is already marked as delivered.")
                return
            order["delivered"] = "True"
            write_orders(orders)
            print(f"Order #{order_id} for '{order['customer_name']}' marked as delivered.")
            return

    print(f"No order found with ID {order_id}.")

def orders_by_customer():
    print("\n--- Orders by Customer ---")
    name = input("Enter customer name: ").strip().lower()
    if not name:
        print("Error: Name cannot be empty.")
        return

    orders = read_orders()
    matches = [o for o in orders if o["customer_name"].lower() == name]

    if not matches:
        print(f"No orders found for '{name}'.")
    else:
        print(f"\nTotal orders for '{matches[0]['customer_name']}': {len(matches)}")
        for o in matches:
            status = "Delivered" if o["delivered"] == "True" else "Pending"
            print(f"  ID: {o['id']} | Date: {o['date']} | Amount: ${o['total_amount']} | Status: {status}")

def pending_orders():
    print("\n--- Pending Orders ---")
    orders = read_orders()
    pending = [o for o in orders if o["delivered"] == "False"]

    if not pending:
        print("No pending orders.")
    else:
        print(f"Total pending orders: {len(pending)}\n")
        print(f"{'ID':<5} {'Customer':<20} {'Address':<25} {'Date':<12} {'Amount':>10} {'Description'}")
        print("-" * 85)
        for o in pending:
            print(f"{o['id']:<5} {o['customer_name']:<20} {o['address']:<25} {o['date']:<12} ${float(o['total_amount']):>9.2f} {o['description']}")

def main():
    initialize_csv()
    menu = """
=============================
   Coffee Shop Order System
=============================
1. Add new order
2. Mark order as delivered
3. Orders count by customer
4. View pending orders
5. Exit
-----------------------------
Choice: """

    while True:
        choice = input(menu).strip()
        if choice == "1":
            add_order()
        elif choice == "2":
            mark_delivered()
        elif choice == "3":
            orders_by_customer()
        elif choice == "4":
            pending_orders()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1–5.")

if __name__ == "__main__":
    main()