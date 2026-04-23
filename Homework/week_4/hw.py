# Task 1
class Person:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = None
        self.phone = None

    def set_birthdate(self, birthdate):
        self.birthdate = birthdate

    def set_phone(self, phone):
        self.phone = phone

    def __str__(self):
        return (f"Name: {self.firstname} {self.lastname}\n"
                f"Birthdate: {self.birthdate}\n"
                f"Phone: {self.phone}")
    

# Task 2
class Employee(Person):
    def __init__(self, firstname, lastname, company, salary):
        super().__init__(firstname, lastname)
        self.company = company
        self.salary = salary

    def __str__(self):
        return (super().__str__() +
                f"\nCompany: {self.company}\n"
                f"Salary: ${self.salary:.2f}")
    
# Task 3
p = Person("Maria", "Gonzales")
p.set_birthdate("1990-05-14")
p.set_phone("+1-555-1234")
print("--- Person ---")
print(p)

print()

e = Employee("John", "Smith", "Google", 85000)
e.set_birthdate("1985-03-22")
e.set_phone("+1-555-9876")
print("--- Employee ---")
print(e)
