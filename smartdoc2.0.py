# this project is birthed from the idea of a patient having a 10% savings
# from every transaction made to any diagnosis in a health center or hospital.

from models import User
import json
import os
from time import sleep

USERS_FILE = os.path.join(os.path.dirname(__file__), "use.json")

print(
'''
\t\t====================================
\t\t\tHI # WELCOME TO SMARTDOC 2.0 #
\t\t====================================
''')

# ----------------------------
# UTILITIES
# ----------------------------

def load_users():
    if not os.path.exists(USERS_FILE):
        return {"user": []}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def timecount():
    print("processing...")
    sleep(1)
    print("processing...")
    sleep(1)

SMART_LIMIT = 500_000

def check_smart_account(user):
    if user.smart_balance >= SMART_LIMIT:
        print("\n🚨 ALERT 🚨")
        print("Your SmartAccount has reached $500,000.")
        print("Please consider making a withdrawal.\n")

def sync_user_to_json(user, users_data):
    for u in users_data["user"]:
        if u["username"] == user.username:
            u["balance"] = user.balance
            u["smart_balance"] = user.smart_balance
            u["history"] = user.history
            break

# ----------------------------
# AUTHENTICATION
# ----------------------------

users_data = load_users()
sign_up = input("Already have an account (yes/no): ").lower()

try:
    if sign_up == "yes":
        attempt = 0
        current_user = None

        while attempt < 3:
            username = input("Enter username: ").lower().replace(" ", "")
            password = input("Enter password: ").replace(" ", "")

            for u in users_data["user"]:
                if u["username"] == username and u["password"] == password:
                    current_user = u
                    break

            if current_user:
                user = User(
                    current_user["username"],
                    current_user["password"],
                    current_user["pin"],
                    current_user["balance"],
                    current_user["smart_balance"]
                )
                timecount()
                print("Login successful ✔️\n")
                break
            else:
                attempt += 1
                print(f"❌ Invalid credentials. {3 - attempt} attempt(s) left.")

        if attempt == 3:
            print("🚫 Too many attempts. System locked 🔐")
            exit()

    elif sign_up == "no":
        username = input("Create username: ").lower()
        password = input("Create password: ")
        pin = input("Create 4-digit PIN: ")

        users_data["user"].append({
            "username": username,
            "password": password,
            "pin": pin,
            "balance": 0,
            "smart_balance": 0,
            "history": []
        })

        save_users(users_data)
        print("\n✅ Successfully signed up!") 
        print("➡ Please log in now.\n") 
        # ------------------------------- 
        # # AUTO LOGIN 
        # # ------------------------------- 
        attempt = 0 
        current_user = None 
        while attempt < 3: 
            login_username = input("Enter username: ").lower() 
            login_password = input("Enter password: ") 
            for u in users_data["user"]: 
                if u["username"] == login_username and u["password"] == login_password: 
                    current_user = u 
                    break 
                if current_user: 
                    user = User( 
                        current_user["username"], 
                        current_user["password"],
                        current_user["pin"], 
                        current_user["balance"], 
                        current_user["smart_balance"] 
                    ) 
                    timecount() 
                    print("Login successful ✔️\n") 
                    break 
                else: 
                    attempt += 1 
                    timecount() 
                    print(f"❌ Invalid login. {3 - attempt} attempt(s) left.") 

                    if attempt == 3:
                        print("Too many attempts. System locked") 
                        exit()
    else:
        print("Invalid input.")
        exit()

except Exception as e:
    print("Error:", e)
    exit()

# ----------------------------
# HOSPITAL DATA
# ----------------------------

Radiology_examinations = {
    "MRI": 2000,
    "ULTRASOUND": 600,
    "X-RAY": 700,
    "FLUOROSCOPY": 800,
    "SPECIALS": 450
}

Histopathology_examinations = {
    "AUTOPSY": 1300,
    "TISSUE PROCESSING": 450,
    "MORBID": 5000
}

Hematology_examinations = {
    "M.P": 50,
    "WIDAL": 60,
    "PCV": 80,
    "WBC COUNT": 50,
    "HEMOGLOBIN": 50
}

Fertility_examinations = {
    "IVF": 10000,
    "SEMEN ANALYSIS": 2000,
    "HORMONE SCREENING": 2500,
    "TESTICULAR BIOPSY": 4500
}

Pharmaceuticals = {
    "ANALGESIC": 350,
    "OPIODS": 250,
    "MALARIA THERAPY": 500
}

hospital_units = {
    1: ("RADIOLOGY", Radiology_examinations),
    2: ("HISTOPATHOLOGY", Histopathology_examinations),
    3: ("HEMATOLOGY", Hematology_examinations),
    4: ("FERTILITY", Fertility_examinations),
    5: ("PHARMACEUTICALS", Pharmaceuticals)
}

# ----------------------------
# MAIN MENU
# ----------------------------

while True:
    print("""
1. Deposit
2. Make Payment
3. Check Balances
4. Exit
""")

    choice = input("Choose option: ")

    # ----------------------------
    # DEPOSIT
    # ----------------------------
    if choice == "1":
        try:
            amount = int(input("Deposit amount: "))
            if amount <= 0:
                print("❌ Invalid amount")
                continue

            user.deposit(amount)
            timecount()
            print(f"✅ Deposited ${amount}")

            sync_user_to_json(user, users_data)
            save_users(users_data)

        except ValueError:
            print("❌ Enter a valid number")

    # ----------------------------
    # MAKE PAYMENT
    # ----------------------------
    elif choice == "2":
        print("""
1. RADIOLOGY
2. HISTOPATHOLOGY
3. HEMATOLOGY
4. FERTILITY
5. PHARMACEUTICALS
""")

        try:
            unit_choice = int(input("Select unit (1-5): "))
        except ValueError:
            print("❌ Invalid input")
            continue

        unit = hospital_units.get(unit_choice)
        if not unit:
            print("❌ Invalid unit selection")
            continue

        unit_name, unit_data = unit
        print(f"\n===== {unit_name} EXAMINATIONS =====")

        exam_map = {}
        for idx, (exam, price) in enumerate(unit_data.items(), start=1):
            exam_map[idx] = exam
            print(f"{idx}. {exam} - ${price}")

        try:
            exam_choice = int(input("\nSelect examination number: "))
        except ValueError:
            print("❌ Enter a number")
            continue

        if exam_choice not in exam_map:
            print("❌ Invalid examination selection")
            continue

        selected_exam = exam_map[exam_choice]
        exam_cost = unit_data[selected_exam]

        print(f"\n🧾 Examination: {selected_exam}")
        print(f"💰 Amount to pay: ${exam_cost}")

        try:
            amount_pay = int(input("Payment amount: "))
        except ValueError:
            print("❌ Invalid amount")
            continue

        pin_pay = input("Enter your 4-digit PIN: ")

        if pin_pay != user.pin:
            print("❌ Incorrect PIN.")
            continue

        if amount_pay > user.balance:
            print("❌ Insufficient balance.")
            continue

        success, saved = user.make_payment(amount_pay)

        if success:
            print(f"✅ Payment successful. ${saved} saved.")
            check_smart_account(user)

            sync_user_to_json(user, users_data)
            save_users(users_data)

    # ----------------------------
    # CHECK BALANCES
    # ----------------------------
    elif choice == "3":
        print(f"\n Main Balance: ${user.balance}")
        print(f" SmartAccount Balance: ${user.smart_balance}")

    # ----------------------------
    # EXIT
    # ----------------------------
    elif choice == "4":
        sync_user_to_json(user, users_data)
        save_users(users_data)
        print("\nThank you for using SMARTDOC PAY")
        break

    else:
        print("❌ Invalid menu choice")

print("\nThank you for using SMARTDOC PAY")
