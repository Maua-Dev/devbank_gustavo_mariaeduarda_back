from abc import ABC, abstractmethod
from typing import List
from ..entities.user import User
from ..entities.transaction import Transaction


class UserRepositoryInterface(ABC):

    @abstractmethod
    def get_user(self) -> User:
        pass

    @abstractmethod
    def deposit(self, value: float) -> Transaction:
        pass

    @abstractmethod
    def withdraw(self, value: float) -> Transaction:
        pass

    @abstractmethod
    def transfer(self, value: float, target_account: str) -> Transaction:
        pass

    @abstractmethod
    def get_transactions(self) -> List[Transaction]:
        pass