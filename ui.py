from db import AuthorizationRepo, TransferRepo
from exceptions import UnauthorizedException, BadRequestException, NotFoundException
from models import User
from service import AuthorizationService, TransferService

from utils import print_menu, print_error

session_user: User = None


def main_menu():
    global session_user
    if session_user is None:
        print_menu("Login ---------------------> 1")
        print_menu("Register ------------------> 2")
    else:
        print_menu("Show Balance --------------> 1")
        print_menu("Add Balance ---------------> 2")
        print_menu("Transfer Money ------------> 3")
        print_menu("Transfer History-----------> 4")
        print_menu("Delete Account--------------> 5")
        print_menu("Log Out  -------------------> 6")
    print_menu("Quit -----------------------> q")
    choice = input(">?")
    if choice == "q":
        return
    try:
        if session_user is None:
            auth_menu(choice)
        else:
            user_menu(choice)
    except (UnauthorizedException, BadRequestException, NotFoundException) as e:
        print_error(e.message)
    main_menu()


def user_menu(choice: str):
    global session_user
    match choice:
        case "1":
            transfer_service.show_balance(session_user)
        case "2":
            amount = float(input("Input amount: "))
            transfer_service.add_balance(session_user, amount)
        case "3":
            receiver_id = input("Input receiver id: ")
            amount = float(input("Input amount: "))
            transfer_service.transfer_money(session_user, receiver_id, amount)
        case "4":
            transfer_service.transfer_history(session_user)
        case "5":
            id = input("Input your id like:  XXXX-XXXX-XXXX-XXXX-XXXX\n")
            if session_user.id == id:
                auth_service.delete_account(id)
                session_user = None
            else:
                raise BadRequestException(f"You can not delete other account")
        case "6":
            session_user = None


def auth_menu(choice: str):
    global session_user
    match choice:
        case "1":
            username = input("Username: ")
            password = input("Password: ")
            session_user = auth_service.login(username=username, password=password)
        case "2":
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            username = input("Username: ")
            password = input("Password: ")
            auth_service.register(first_name=first_name, last_name=last_name, username=username, password=password)


if __name__ == '__main__':
    auth_repo = AuthorizationRepo("users.json")
    auth_service = AuthorizationService(auth_repo)
    transfer_repo = TransferRepo("transfers.json", auth_repo)
    transfer_service = TransferService(transfer_repo)
    main_menu()
