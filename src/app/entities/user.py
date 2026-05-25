from typing import Tuple
import re


class User:

    name: str
    agency: str
    account: str
    current_balance: float

    def __init__(
        self,
        name: str = None,
        agency: str = None,
        account: str = None,
        current_balance: float = 0.0
    ):
        from ..errors.entity_errors import ParamNotValidated

        validation_name = self.validate_name(name)
        if not validation_name[0]:
            raise ParamNotValidated("name", validation_name[1])
        self.name = name

        validation_agency = self.validate_agency(agency)
        if not validation_agency[0]:
            raise ParamNotValidated("agency", validation_agency[1])
        self.agency = agency

        validation_account = self.validate_account(account)
        if not validation_account[0]:
            raise ParamNotValidated("account", validation_account[1])
        self.account = account

        validation_balance = self.validate_current_balance(current_balance)
        if not validation_balance[0]:
            raise ParamNotValidated("current_balance", validation_balance[1])
        self.current_balance = current_balance

    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        if name is None:
            return (False, "Name is required")
        if type(name) != str:
            return (False, "Name must be a string")
        if len(name) < 3:
            return (False, "Name must be at least 3 characters long")
        return (True, "")

    @staticmethod
    def validate_agency(agency: str) -> Tuple[bool, str]:
        if agency is None:
            return (False, "Agency is required")
        if type(agency) != str:
            return (False, "Agency must be a string")
        if not re.fullmatch(r'\d{4}', agency):
            return (False, "Agency must be exactly 4 digits")
        return (True, "")

    @staticmethod
    def validate_account(account: str) -> Tuple[bool, str]:
        if account is None:
            return (False, "Account is required")
        if type(account) != str:
            return (False, "Account must be a string")
        if not re.fullmatch(r'\d{5}-\d', account):
            return (False, "Account must follow the format XXXXX-X")
        return (True, "")

    @staticmethod
    def validate_current_balance(current_balance: float) -> Tuple[bool, str]:
        if current_balance is None:
            return (False, "Current balance is required")
        if type(current_balance) not in [float, int]:
            return (False, "Current balance must be a number")
        if current_balance < 0:
            return (False, "Current balance cannot be negative")
        return (True, "")

    def to_dict(self):
        return {
            "name": self.name,
            "agency": self.agency,
            "account": self.account,
            "current_balance": float(self.current_balance)
        }

    def __repr__(self):
        return f"User(name={self.name}, agency={self.agency}, account={self.account}, current_balance={self.current_balance})"