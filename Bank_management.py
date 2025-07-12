class Bankaccount:
    account_counter = 1000
    def __init__(self , balance=0.0):
        self.account_number=Bankaccount.account_counter
        Bankaccount.account_counter += 1
        self.balance = balance

    def deposit(self , amount):
        if amount > 0:
            self.balance += amount 
            print(f"Deposited Rs.{amount:.2f}. New balance: Rs.{self.balance:.2f}")
        else:
            print("Enter valid amount")  

    def withdraw(self , amount):
        if 0 < amount <= self.balance :
            self.balance -= amount
            print(f"Withdrew Rs.{amount:.2f}. Remaining: RS.{self.balance:.2f}")
        else:
            print("Insufficient funds or invalid amount")

    def get_balance(self):
        return self.balance                  

class Saving_account(Bankaccount):
    def __init__(self , balance = 0.0 , interest_rate = 0.04):
        super().__init__(balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        print(f"Interest Rs.{interest:.2f} applied; New balance: Rs.{self.balance:.2f}")   

class User:
    user_counter = 1
    def __init__(self , name):
        self.id = User.user_counter
        User.user_counter += 1
        self.name = name
        self.accounts = []

    def add_account(self , account):
        self.accounts.append(account)
        print(f"Added {type(account).__name__} #{account.account_number} for {self.name}")

    def list_account(self):
        for acc in self.accounts:
            typ = "Savings" if isinstance(acc, Saving_account) else "Checking"
            print(f"{typ} #{acc.account_number}: Rs.{acc.balance:.2f}")  

class Bank:
    def __init__(self):
        self.users = {}

    def add_user(self , user):
        self.users[user.id] = user                  
        print(f"User '{user.name}' added with ID {user.id}")

    def find_user(self, uid):
        return self.users.get(uid, None)

    def transfer(self , from_acc , to_acc , amount):
        if from_acc.balance >= amount:
            from_acc.withdraw(amount)
            to_acc.deposit(amount)
            print(f"Rs.{amount:.2f} transferred from #{from_acc.account_number} to #{to_acc.account_number}")    
        else:
            print("Transfer failed: Insufficient funds")

def main():
    bank = Bank()
    print("=== Welcome to Python Bank ===")

    while True:
        print("""
                1. Add new user
                2. Open account for user
                3. Deposit / Withdraw / Balance check
                4. Apply interest (Savings)
                5. Transfer between accounts
                6. List user accounts
                7. Exit
                """) 
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Enter user name: ")
            bank.add_user(User(name))  

        elif choice == "2":
            uid = int(input("User ID: "))
            user = bank.find_user(uid)
            if not user :
                print("User not found.")
                continue
            typ = input("Type (c=Checking, s=Savings): ").lower()
            if typ == 'c':
                user.add_account(Bankaccount())          
            elif typ == 's':
                rate = float(input("Interest rate (e.g. 0.04): ") or 0.04)
                user.add_account(Saving_account(interest_rate=rate))
            else:
                print("Invalid type.")  

        elif choice == "3":
            uid = int(input("User ID: "))
            user = bank.find_user(uid)
            if not user:
                print("Unknown user")
                continue
            user.list_account()

            aid = int(input("Account number: "))
            acc = next((a for a in user.accounts if a.account_number == aid), None)
            if not acc:
                print("Account not found.")
                continue

            action = input("(d)eposit, (w)ithdraw, (b)alance: ").lower()
            if action == 'd':
                acc.deposite(float(input("Amount: ")))
            elif action == 'w':
                acc.withdraw(float(input("Amount: ")))
            elif action == 'b':
                print(f"Balance: Rs.{acc.get_balance():.2f}")
            else:
                print("Invalid.")

        elif choice == "4":
            uid = int(input("User ID: "))
            user = bank.find_user(uid)
            if not user:
                print("User not found.")
                continue
            for acc in user.accounts:
                if isinstance(acc, Saving_account):
                    acc.apply_interest()

        elif choice == "5":
            a1 = int(input("From account #: "))
            a2 = int(input("To account #: "))
            amt = float(input("Amount: "))
            src = dst = None
            for u in bank.users.values():
                for acc in u.accounts:
                    if acc.account_number == a1: src = acc
                    if acc.account_number == a2: dst = acc
            if src and dst:
                bank.transfer(src, dst, amt)
            else:
                print("One or both accounts not found.")

        elif choice == "6":
            uid = int(input("User ID: "))
            user = bank.find_user(uid)
            if user:
                user.list_account()
            else:
                print("User not found.")

        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")  

if __name__ == "__main__":
    main()            
                          