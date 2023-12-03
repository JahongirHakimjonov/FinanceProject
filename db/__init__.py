import datetime
import json

from exceptions import NotFoundException
from models import User
from utils import print_info


class AuthorizationRepo:
    """
        crud -> create read update delete
    """

    def __init__(self, file):
        self.file = file
        self.__get_data()

    def __get_data(self):
        try:
            with open(self.file, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            with open(self.file, "w") as f:
                data = []
                json.dump(data, f, indent=3)
        self.users = data

    def _commit(self):
        with open(self.file, "w") as f:
            json.dump(self.users, f, indent=3)

    def create_user(self, user: dict):
        self.users.append(user)
        self._commit()

    def delete_user(self, id: str):
        for user in self.users:
            if user["id"] == id:
                self.users.remove(user)
                self._commit()
                return
        raise NotFoundException(message=f" Not found such  {id} user ")

    def find_user_by_id(self, user_id: str) -> User:
        for user in self.users:
            if user["id"] == user_id:
                return User(**user)
        raise NotFoundException(message=f"Non Exist such user with ID {user_id} in the database")


class TransferRepo:
    def __init__(self, file, authorization_repo):
        self.file = file
        self.authorization_repo = authorization_repo
        self.__get_data()
        self.date = datetime.datetime.now()

    def __get_data(self):
        try:
            with open(self.file, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            with open(self.file, "w") as f:
                data = []
                json.dump(data, f, indent=3)
        self.transfers = data

    def __commit(self):
        with open(self.file, "w") as f:
            json.dump(self.transfers, f, indent=3)

    def add_balance(self, user: User, amount: float):
        for u in self.authorization_repo.users:
            if u["id"] == user.id:
                u["balance"] += amount
                self.authorization_repo._commit()
                break
        else:
            raise NotFoundException(message="Non Exist such user in db")

    def transfer_money(self, sender_id: str, receiver_id: str, amount: float):
        authorization_repo = self.authorization_repo

        for u in authorization_repo.users:
            if u["id"] == sender_id:
                u["balance"] -= amount
                authorization_repo._commit()
                break
        else:
            raise NotFoundException(message="Non Exist such user in db")

        for u in authorization_repo.users:
            if u["id"] == receiver_id:
                u["balance"] += amount
                authorization_repo._commit()
                break
        else:
            raise NotFoundException(message="Non Exist such user in db")

        self.transfers.append({
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "amount": amount,
            "date": f"{self.date.day}.{self.date.month}.{self.date.year}"
        })
        self.__commit()

    def transfer_history(self, user: User):
        for transfer in self.transfers:
            if transfer["sender_id"] == user.id or transfer["receiver_id"] == user.id:
                print_info(
                    f"{transfer['sender_id']} -> {transfer['receiver_id']} : {transfer['amount']}, {transfer['date']}")
        else:
            print_info("You have not any transfer history")

    def find_user_by_id(self, user_id: str) -> User:
        return self.authorization_repo.find_user_by_id(user_id)


__all__ = ["AuthorizationRepo", "TransferRepo"]
