class User:
    def __init__(self, username, password, pin, balance=0, smart_balance=0, history=None):
        self.username = username
        self.password = password
        self.pin = pin
        self.balance = balance
        self.smart_balance = smart_balance
        self.history = history or []

    def deposit(self, amount):
        self.balance += amount
        self.history.append({
            "type": "deposit",
            "amount": amount
        })

    def make_payment(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            saved = amount * 0.10
            self.smart_balance += saved
            self.history.append({
                "type": "payment",
                "amount": amount,
                "saved": saved
            })
            return True, saved
        return False, 0


 