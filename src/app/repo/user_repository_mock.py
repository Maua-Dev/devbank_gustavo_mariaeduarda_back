from typing import List
from .user_repository_interface import UserRepositoryInterface
from ..entities.user import User
from ..entities.transaction import Transaction
from ..enums.transaction_type_enum import TransactionTypeEnum


class UserRepositoryMock(UserRepositoryInterface):

    def __init__(self):
        self.user = User(
            name="Vitor Soller",
            agency="0000",
            account="00000-0",
            current_balance=1000.0
        )
        self.transactions: List[Transaction] = []

    def get_user(self) -> User:
        return self.user

    def deposit(self, value: float) -> Transaction:
        self.user.current_balance += value
        transaction = Transaction(
            value=value,
            transaction_type=TransactionTypeEnum.DEPOSIT
        )
        self.transactions.append(transaction)
        return transaction

    def withdraw(self, value: float) -> Transaction:
        if value > self.user.current_balance:
            return None
        self.user.current_balance -= value
        transaction = Transaction(
            value=value,
            transaction_type=TransactionTypeEnum.WITHDRAW
        )
        self.transactions.append(transaction)
        return transaction

    def transfer(self, value: float, target_account: str) -> Transaction:
        if value > self.user.current_balance:
            return None
        self.user.current_balance -= value
        transaction = Transaction(
            value=value,
            transaction_type=TransactionTypeEnum.TRANSFER
        )
        self.transactions.append(transaction)
        return transaction

    def get_transactions(self) -> List[Transaction]:
        return self.transactions