import datetime

from utils import generate_id


class User:
    id: str
    first_name: str
    last_name: str
    username: str
    password: str
    balance: int = 0

    def __init__(self, first_name: str,
                 last_name: str,
                 username: str,
                 password: str,
                 balance=0,
                 id=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.balance = balance
        self.id = id or generate_id()


class Transfer:
    sender_id: str
    receiver_id: str
    amount: float

    def __init__(self, sender_id: str, receiver_id: str, amount: float):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.date = datetime.datetime.now()
