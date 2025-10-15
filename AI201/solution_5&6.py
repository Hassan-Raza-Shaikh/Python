transaction_id_counter = 0

class Account:
    def __init__(self, account_no, holder_name, pin, balance):
        self.account_no = account_no
        self.holder_name = holder_name
        self.pin = pin
        self.balance = balance
        self.daily_withdrawn = 0
        self.transaction_log = []

    def add_transaction(self, trans_type, amount, meta=""):
        global transaction_id_counter
        transaction_id_counter += 1
        
        transaction_record = {
            "id": transaction_id_counter,
            "type": trans_type,
            "amount": amount,
            "balance_after": self.balance,
            "meta": meta
        }
        
        self.transaction_log.append(transaction_record)
        
        if len(self.transaction_log) > 10:
            self.transaction_log.pop(0)

class Bank:
    def __init__(self):
        self.accounts = {}

        self.cash_cassette = {
            5000: 10,
            1000: 25,
            500: 30,
            100: 50
        }

    def add_account(self, account):
        self.accounts[account.account_no] = account

    def get_account(self, account_no):
        if account_no in self.accounts:
            return self.accounts[account_no]
        else:
            return None

class ATM:
    def __init__(self, bank_system):
        self.bank = bank_system
        self.state = "IDLE"
        self.current_account = None
        self.current_account_no = None
        self.pin_tries = 0

    def process_command(self, command):
        parts = command.split()
        if not parts:
            return

        cmd = parts[0]
        
        if self.state == "IDLE":
            if cmd == "CARD":
                if len(parts) == 2:
                    self.card_insert(parts[1])
                else:
                    print("ERROR FORMAT")
            else:
                print("ERROR INVALID_STATE")
        
        elif self.state == "CARD_INSERTED":
            if cmd == "PIN":
                if len(parts) == 2:
                    self.enter_pin(parts[1])
                else:
                    print("ERROR FORMAT")
            else:
                print("ERROR INVALID_STATE")
        
        elif self.state == "AUTHENTICATED":
            if cmd == "BALANCE":
                self.check_balance()
            elif cmd == "WITHDRAW":
                if len(parts) == 2:
                    self.withdraw_cash(int(parts[1]))
                else:
                    print("ERROR FORMAT")
            elif cmd == "DEPOSIT":
                if len(parts) == 2:
                    self.deposit_cash(int(parts[1]))
                else:
                    print("ERROR FORMAT")
            elif cmd == "TRANSFER":
                 if len(parts) == 3:
                    self.transfer_funds(parts[1], int(parts[2]))
                 else:
                    print("ERROR FORMAT")
            elif cmd == "MINI":
                self.get_mini_statement()
            elif cmd == "EJECT":
                self.eject_card()
            else:
                print("ERROR INVALID_STATE")
                
    def card_insert(self, account_no):
        account = self.bank.get_account(account_no)
        if account:
            self.current_account_no = account_no
            self.state = "CARD_INSERTED"
            self.pin_tries = 0
            print("CARD_OK " + account_no)
        else:
            print("ERROR UNKNOWN_ACCOUNT")

    def enter_pin(self, pin):
        account = self.bank.get_account(self.current_account_no)
        if account.pin == pin:
            self.state = "AUTHENTICATED"
            self.current_account = account
            self.current_account.add_transaction("PIN", 0)
            print("PIN_OK")
        else:
            self.pin_tries += 1
            if self.pin_tries >= 3:
                print("ERROR PIN_TRIES_EXCEEDED")
                self.eject_card()
            else:
                remaining = 3 - self.pin_tries
                print("PIN_INVALID " + str(remaining))

    def check_balance(self):
        balance = self.current_account.balance
        self.current_account.add_transaction("BALANCE", 0)
        print("BALANCE " + str(balance))

    def withdraw_cash(self, amount):
        if amount % 100 != 0 or amount < 100 or amount > 50000:
            print("ERROR AMOUNT_INVALID")
            return
        if self.current_account.balance < amount:
            print("ERROR INSUFFICIENT_FUNDS")
            return
        if self.current_account.daily_withdrawn + amount > 100000:
            print("ERROR DAILY_LIMIT_EXCEEDED")
            return

        notes_to_dispense = {}
        remaining_amount = amount
        denominations = [5000, 1000, 500, 100]
        temp_cassette = self.bank.cash_cassette.copy()

        for d in denominations:
            notes_needed = remaining_amount // d
            notes_available = temp_cassette[d]
            notes_to_give = min(notes_needed, notes_available)
            if notes_to_give > 0:
                notes_to_dispense[d] = notes_to_give
                remaining_amount -= notes_to_give * d
                temp_cassette[d] -= notes_to_give

        if remaining_amount == 0:
            self.bank.cash_cassette = temp_cassette
            self.current_account.balance -= amount
            self.current_account.daily_withdrawn += amount
            mix_parts = []
            for d in sorted(notes_to_dispense.keys(), reverse=True):
                mix_parts.append(str(d) + "x" + str(notes_to_dispense[d]))
            mix_str = " ".join(mix_parts)
            meta_str = "MIX=" + ",".join(mix_parts).replace(" ", "")
            self.current_account.add_transaction("WITHDRAW", amount, meta_str)
            print("WITHDRAW_OK " + str(amount) + " " + mix_str)
        else:
            print("ERROR DENOMINATION_UNAVAILABLE")

    def deposit_cash(self, amount):
        if amount <= 0 or amount % 100 != 0:
            print("ERROR AMOUNT_INVALID")
            return
        self.current_account.balance += amount
        self.current_account.add_transaction("DEPOSIT", amount)
        print("DEPOSIT_OK " + str(amount))

    def transfer_funds(self, target_account_no, amount):
        if target_account_no == self.current_account_no:
            print("ERROR TARGET_SAME_AS_SOURCE")
            return
        target_account = self.bank.get_account(target_account_no)
        if not target_account:
            print("ERROR TARGET_UNKNOWN")
            return
        if amount <= 0:
            print("ERROR AMOUNT_INVALID")
            return
        if self.current_account.balance < amount:
            print("ERROR INSUFFICIENT_FUNDS")
            return
        self.current_account.balance -= amount
        target_account.balance += amount
        self.current_account.add_transaction("TRANSFER_OUT", amount, "TO=" + target_account_no)
        target_account.add_transaction("TRANSFER_IN", amount, "FROM=" + self.current_account_no)
        print("TRANSFER_OK " + str(amount) + " to:" + target_account_no)
        
    def get_mini_statement(self):
        log = self.current_account.transaction_log
        if not log:
            print("TX NONE")
            return
        last_5_transactions = log[-5:]
        last_5_transactions.reverse()
        for tx in last_5_transactions:
            line = "TX " + str(tx["id"]) + " " + tx["type"] + " " + str(tx["amount"])
            line += " BAL " + str(tx["balance_after"])
            if tx["meta"]:
                line += " " + tx["meta"]
            print(line)
            
    def eject_card(self):
        print("CARD_EJECTED")
        self.state = "IDLE"
        self.current_account = None
        self.current_account_no = None
        self.pin_tries = 0

my_bank = Bank()
my_bank.add_account(Account("1001", "HASSAN RAZA", "1234", 50000))
my_bank.add_account(Account("1002", "ABDUL RAFAY", "2468", 20000))
my_bank.add_account(Account("1003", "HAMZA ARIF", "1357", 150000))

atm_machine = ATM(my_bank)

print("start")
print("Welcome! Please insert your card to begin.")
print("Example: CARD 1001")
print("Available accounts for testing: 1001, 1002, 1003")
print("Type 'EXIT' to end the session.")
print("---------------------------------")

while True:
    try:
        command_line = input("> ")
        if command_line.upper() == 'EXIT':
            print("\nend")
            break
        atm_machine.process_command(command_line)
    except EOFError:
        print("\nend")
        break

