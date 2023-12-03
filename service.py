from db import AuthorizationRepo, TransferRepo
from exceptions import BadRequestException, NotFoundException
from models import User
from utils import matchpassword, hashpassword, print_succes, print_info
from validators import check_username_unique, check_user_exists


class AuthorizationService:
    def __init__(self, repo: AuthorizationRepo):
        self.repository = repo

    def login(self, username: str, password: str) -> User:
        users = self.repository.users
        for user_data in users:
            if user_data["username"] == username:
                user = User(**user_data)
                if matchpassword(password, user.password):
                    return user

        raise BadRequestException("Your password or login is wrong ")

    def register(self, *args, **kwargs):
        username = kwargs.get("username")
        password = kwargs.get("password")
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        check_username_unique(self.repository.users, username)
        user = User(username=username, password=hashpassword(password), first_name=first_name, last_name=last_name)
        self.repository.create_user(user.__dict__)

    def delete_account(self, id: str):
        code = check_user_exists(self.repository.users, id)
        if code == 200:
            self.repository.delete_user(id)
            print_succes("user successfully deleted")
        else:
            raise NotFoundException(f"{id} id user Not Found")


class TransferService:
    def __init__(self, repo: TransferRepo):
        self.repository = repo

    def show_balance(self, session_user: User):
        print_info(f"Your balance is {session_user.balance}")

    def add_balance(self, session_user: User, amount: float):
        session_user.balance += amount
        print_succes(f"Your balance is now {session_user.balance}")
        self.repository.add_balance(session_user, amount)

    def transfer_money(self, session_user: User, receiver_id: str, amount: float):
        if session_user.balance < amount:
            raise BadRequestException("You don't have enough money")
        self.repository.transfer_money(session_user.id, receiver_id, amount)
        print_succes(f"You successfully transfer {amount} to {receiver_id}")
        session_user.balance -= amount
        self.repository.add_balance(session_user, -amount)

    def transfer_history(self, session_user: User):
        self.repository.transfer_history(session_user)


__all__ = ["AuthorizationService", "TransferService"]
