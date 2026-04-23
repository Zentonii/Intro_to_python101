# Task 1
expenses = []

while True:
    category = input("Enter category (or 'done' to stop): ")
    if category.lower() == 'done':
        break
    amount = float(input("Enter amount: "))
    expenses.append((category, amount))

with open("expenses.csv" , "w") as f:
    for category, amount in expenses:
        f.write(f"{category},{amount}\n")

print("Expenses saved!")

# Task 2
expenses = []

while True:
    category = input("Enter category (or 'done' to stop): ")
    if category.lower() == 'done':
        break
    amount = float(input("Enter amount: "))
    expenses.append((category, amount))

with open("expenses.csv" , "a") as f:
    for category, amount in expenses:
        f.write(f"{category},{amount}\n")

print("Expenses saved!")

# Task 3
totals = {}

with open("expenses.csv" "r") as f:
    for line in f:
        line = line.strip()
        if line:
            category, amount = line.split(",")
            amount = float(amount)
            if category in totals:
                totals[category] += amount
            else:
                totals[category] = amount

for category, total in totals.items():
    print(f"{category}: ${total:.2f}")

# Task 4
totals = {}

with open("expenses.csv", "r") as f:
    for line in f:
        line = line.strip()
        if line:
            category, amount = line.split(",")
            amount = float(amount)
            if category in totals:
                totals[category] += amount
            else:
                totals[category] = amount

sorted_totals = sorted(totals.items(), key=lambda x: x[1], reverse=True)

for category, total in sorted_totals:
    print(f"{category}: ${total:.2f}")
    