# Task 1 
import random

list1 = [random.randint(1,100) for _ in range(20)]
print("List 1:", list1)

evens = [n for n in list1 if n % 2 == 0]
print("Even numbers:", evens)
print("Total of even numbers:", sum(evens))

# Task 2 
list2 = [random.randint(1,100) for _ in range(20)]
print("List 2:", list2)

common = [n for n in list2 if n in list1]
print("Elements in list2 that also appear in list1:", common)

# Task 3 
sales_data = [
    [2020, 2.3, 2.2, 1.8, 3.1],
    [2021, 2.4, 2.0, 1.7, 3.0],
    [2022, 1.7, 1.2, 1.0, 1.8],
    [2023, 1.9, 1.0, 0.7, 2.0],
    [2024, 2.0, 2.4, 2.0, 3.2],
]

# a. Total sales per year
for row in sales_data:
    year, *quarters = row
    print(f"{year}: total = ${sum(quarters):.1f}M")

# b. Average per quarter per year
for row in sales_data:
    year, *quarters = row
    print(f"{year}: avg = ${sum(quarters)/len(quarters):.2f}M")

# c. Max and Min (yar + quarter)
max_val, min_val = float('-inf'), float('inf')
max_info, min_info = None, None

for row in sales_data:
    year, *quarters = row
    for i, q in enumerate(quarters, 1):
        if q > max_val:
            max_val, max_info = q, (year, i)
        if q < min_val:
            min_val, min_info = q, (year, i)

print(f"Max: {max_info[0]} Q{max_info[1]} = ${max_val}M")
print(f"Min: {min_info[0]} Q{min_info[1]} = ${min_val}M")



