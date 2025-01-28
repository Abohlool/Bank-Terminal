import re
from random import randint
from date import convert
import exceptions as e

names = list()
bdays = list()
acc_types = list()
pins = list()
nums = list()
balances = list()


class Bank:
    # ==========================================================Info=======================================================
    current_account: int = None

    def getter(name: str = None, bday: str = None, acc_type: str = None, pin: int = None):
        names.append(Bank.get_name(name))
        bdays.append(Bank.get_bday(bday))
        acc_types.append(Bank.get_type(acc_type))
        pins.append(Bank.get_pin(pin))
        nums.append(Bank.gen_acc_num())

    def gen_acc_num():
        return f"{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}"

    def get_name(name: str = None) -> str:
        if name:
            return name.title()

        try:
            name = input("Enter your full name: ").strip().title()
            if not re.search(r"^([A-Z][a-z]+) ([A-Z][a-z]+)( [A-Z][a-z]+)?( [A-Z][a-z]+)?$", name):
                raise e.InputError("Name Error")

            return name.title()

        except e.InputError:
            return Bank.get_name()

    def get_bday(bday: str = None) -> str:
        if bday:
            return convert(bday)

        try:
            return convert(input("Enter your birthday (MM/DD/YYYY): ").lower())

        except ValueError:
            return Bank.get_bday()

    def get_pin(pin: int = None) -> int:
        if pin:
            return int(pin)

        try:
            pin = input("Choose a PIN number: ").strip()
            if not re.search(r"[0-9]+", pin) or len(pin) < 4 or len(pin) > 8:
                raise e.InputError("PIN Error")

            return int(pin)

        except e.InputError:
            return Bank.get_pin()

    def confirm_pin(pin: int, _pin: int = None):
        if not _pin:
            _pin = int(input("Comfirm your PIN number: "))

        try:
            if _pin != pin:
                raise e.InputError("PIN Error")

        except e.InputError:
            return Bank.confirm_pin(pin)

    def get_type(type: str = None) -> str:
        if type:
            return type

        try:
            acc_type = input("Checking or Savings: ").lower()
            if match := re.search(r"((savings)|(checking))", acc_type):
                return match.group(1).title()

            else:
                raise e.InputError("Type Error")

        except e.InputError:
            return Bank.get_type()

    def rename():
        new_name = Bank.get_name()
        names[Bank.current_account] = new_name
        return "Name successfuly changed!"

    def change_pin():
        if Bank.check_pin():
            pins[Bank.current_account] = input("Enter your new PIN number: ")
            return "PIN number successfuly changed"

    # ==============================================================Tech=========================================================

    def check_pin(name: str = None, pin: int = None):
        if not name:
            name = input("Enter your name: ")

        if not pin:
            pin = int(input("Enter your pin number: "))

        try:
            if pin == pins[names.index(name)]:
                return True

            else:
                print("INCORRECT PIN NUMBER")
                Bank.check_pin()

        except ValueError:
            Bank.check_pin(name)

    def sign_up(name: str = None, bday: str = None, acc_type: str = None, pin: int = None, _pin: int = None):
        Bank.getter(name, bday, acc_type, pin)
        Bank.confirm_pin(pins[-1], _pin)
        balances.append(0)
        Bank.current_account = -1

    def sign_in(name: str = None, pin: int = None):
        if not name:
            name = Bank.get_name()

        if not pin:
            pin = int(input("Enter your PIN number: "))

        try:
            if name in names:
                if Bank.check_pin(name, pin):
                    raise e.CorrectInput

                else:
                    raise e.InputError("Wrong PIN")

        except e.InputError:
            print("Incorrect PIN number")
            Bank.sign_in(name)

        except e.CorrectInput:
            Bank.current_account = names.index(name)

    def sign_out(confirm: str) -> str | None:
        acceptable = ["yes", "y", "1", "no", "n", "0"]
        if confirm in acceptable:
            if confirm in acceptable[0:2]:
                Bank.current_account = None
                return "SIGNED OUT!"

            elif confirm in acceptable[2:-1]:
                return None

        else:
            return None
    # ===============================================================Transactions=================================================================

    def deposit(amount: int | str = None) -> str:
        """
        deposits ${amount} to the account balance witch the function was called with
        """
        if not amount:
            amount = int(get_amount("deposit"))

        try:
            if amount < 0 and amount != -1:
                raise e.InputError("Deposit Error")

            elif amount == -1:
                return None

            balances[Bank.current_account] += amount
            return f"Balance: ${balances[Bank.current_account]}"

        except e.InputError:
            Bank.deposit()

    def withdraw(amount: int | str = None) -> str:
        """
        withdraws ${amount} from the account balance witch the function was called with
        """
        if not amount:
            amount = get_amount("withdraw")

        try:
            if amount > balances[Bank.current_account] or amount < 0 and amount != -1:
                raise e.InputError("Withdraw Error")

            elif amount == -1:
                raise e.Back

            balances[Bank.current_account] -= amount
            return f"Balance: ${balances[Bank.current_account]}"

        except e.InputError:
            Bank.withdraw()

    def transfer(amount: int | str = None, acc_num: str = None):
        """
        transfers the amount $n from the account withch the function was called with, to the account specified after the amount
        """
        if not amount:
            amount = get_amount("transfer")

        if not acc_num:
            acc_num = get_num()

        try:
            if amount < 0 and amount != -1:
                raise e.TransactionError("Transfer Error")

        except e.TransactionError:
            return "Transfer Failed!"

        balances[Bank.current_account] -= amount
        balances[nums.index(acc_num)] += amount
        return f"Balance: ${balances[Bank.current_account]}"


# =======================================================================================================================
def get_amount(transaction: str) -> int:
    amount = input(f"Enter the amount you want to {transaction}: ")
    if amount.isnumeric():
        if transaction in ["withdraw", "transfer"]:
            check_balance(amount)
        return int(amount)

    else:
        raise e.Back


def check_balance(amount: int):
    if int(amount) > balances[Bank.current_account]:
        raise e.TransactionError("Insufficient Funds")


def get_num():
    try:
        acc_num = input("Enter the account number: ").strip()
        if acc_num.strip()[0].isnumeric():
            if re.search(r"[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}", acc_num):
                pass

            elif re.search(r"[0-9]{4} [0-9]{4} [0-9]{4} [0-9]{4}", acc_num):
                acc_num = "-".join(acc_num.split())

            elif re.search(r"[0-9]{16}", acc_num):
                for i in [3, 7, 11, 15]:
                    acc_num = "".join(acc_num.split("").insert(i, "-"))

            if acc_num not in nums:
                raise e.InputError("Incorrect Account Number")

            return acc_num

        else:
            raise e.Back

    except e.InputError:
        get_num()


def main():
    acc1 = Bank()
    acc2 = Bank()
    acc3 = Bank()
    print(acc1)
    print(acc2)
    print(acc3)
    Bank.deposit(20)
    print(acc1)
    print(Bank.acc_dict)
    # acc1.transfer(5, "1300-9851-8499-6484")
    # print(acc1)
    # print(acc2)


if __name__ == "__main__":
    main()
