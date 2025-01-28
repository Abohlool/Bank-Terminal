from Bank import *
from pyfiglet import Figlet
import re
import exceptions as e
import sys


def main():
    title()
    while True:
        signin(input("Sign up or sign in: ").lower())
        acc = Bank.current_account
        running: bool = False
        op: int = None
        if acc != None:
            running = True

        while running:
            try:
                if op not in [0, 1, 2]:
                    op = menu()

                if op == 0:
                    print(transaction())
                    print("==================================================================================================================")


                elif op == 1:
                    print(print_info())
                    print("==================================================================================================================")
                    op = None

                elif op == 2:
                    print(settings())
                    print("==================================================================================================================")

            except e.InputError:
                pass

            except e.Back:
                op = None

            except e.Exit:
                print(Bank.sign_out(input("Confirm weather you would like to log out: ").lower().strip()))
                running = False


def title():
    f = Figlet()
    print(f.renderText("                                   - BANK -"))
    print("==================================================================================================================")


def signin(option: str):
    try:
        if match := re.search(r"sign ?(in)|(up)", option):
            if match.group(1) == "in":
                Bank.sign_in()

            else:
                return Bank.sign_up()

        else:
            raise e.InputError("Sign in Error")

    except e.InputError:
        signin(input("Sign up or sign in: ").lower())


def menu(option: str = None) -> int | None:
    print("1. Transaction\n2. info\n3. Setting\n4. logout")
    try:
        if not option:
            option = input("what would you like to do: ")

        options = ["transaction", "t", "1", "info", "i", "2", "setting", "s", "3", "logout", "l", "4"]
        if option.lower() in options:
            if option.lower() in options[0:3]:
                return 0

            elif option.lower() in options[3:6]:
                return 1

            elif option.lower() in options[6:9]:
                return 2

            elif option.lower() in options[9:12]:
                raise e.Exit

        else:
            raise e.InputError("Wrong Option")

    except e.InputError:
        return menu(option)

    except e.TransactionError:
        return menu(option)


def settings(option: str = None):
    options = ["rename", "r", "1", "change pin", "c", "2", "quit", "q", "3", "back", "b", "4"]
    print("1. rename\n2. change pin\n3. quit\n4. back")
    try:
        if not option:
            option = input("What would you like to do: ")

        if option.lower() in options:
            if option.lower() in options[0:3]:
                Bank.rename()

            elif option.lower() in options[3:6]:
                Bank.change_pin()

            elif option.lower() in options[6:9]:
                if (input("Confirm weather you would like to quit: ").lower().strip() in [1, "y", "yes"]):
                    sys.exit()

            else:
                raise e.Back

        else:
            raise e.InputError("Wrong Option")

    except e.InputError:
        settings()


def transaction(trans: str = None, amount: int = None, num: int = None):
    options = ["transfer", "t", "1", "deposit", "d", "2", "withdraw", "w", "3", "back", "b", "4"]
    print("1. transfer\n2. deposit\n3. withdraw\n4. back")
    if not trans:
        trans = input("What would you like to do: ")
        if trans.lower() in options[9:-1]:
            raise e.Back

    try:
        if trans.lower() in options:
            if trans.lower() in options[0:3]:
                print(print_accounts())
                return Bank.transfer(amount)

            elif trans.lower() in options[3:6]:
                return Bank.deposit(amount)

            elif trans.lower() in options[6:9]:
                return Bank.withdraw(amount)

        else:
            raise e.InputError("Transaction Error")

    except e.InputError:
        return transaction()

    except e.TransactionError:
        print("Insufficient Funds")
        return transaction()

    except e.Back:
        return transaction()


def print_accounts() -> str:
    l = list()
    for i in range(len(names)):
        l.append(f"Name: {names[i]}\nAccount Number: {nums[i]}")

    return "\n".join(l)


def print_info():
    print("==================================================================================================================")
    acc = Bank.current_account
    return f"Name: {names[acc]}         Birthday: {bdays[acc]}\nAccount Number: {nums[acc]}\nAccount Type: {acc_types[acc]}         Balance: ${balances[acc]}"


def testing():
    Bank.sign_up("abcde fghi", "1/1/1900", "savings", 12345, 12345)
    Bank.deposit(20)
    Bank.withdraw(5)
    Bank.sign_up("ihgf edcba", "1/1/2000", "checkings", 54321, 54321)
    Bank.deposit(30)
    Bank.withdraw(2)
    print(print_accounts())
    Bank.transfer(amount=5, acc_num=nums[0])
    Bank.sign_in("Abcde Fghi", 12345)
    print(print_info())


def test_accs():
    Bank.sign_up("abcde fghi", "1/1/1900", "savings", 54321, 54321)
    # Bank.sign_up("ihgf edcba", "1/1/2000", "checkings", 12345, 12345)
    Bank.sign_out("yes")


if __name__ == "__main__":
    test_accs()
    main()
    # testing()
