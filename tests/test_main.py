import pytest
from src.app.repo.user_repository_mock import UserRepositoryMock
from src.app.entities.user import User
from src.app.entities.transaction import Transaction
from src.app.enums.transaction_type_enum import TransactionTypeEnum


class TestUser:

    def test_create_user(self):
        user = User(
            name="Vitor Soller",
            agency="0000",
            account="00000-0",
            current_balance=1000.0
        )
        assert user.name == "Vitor Soller"
        assert user.agency == "0000"
        assert user.account == "00000-0"
        assert user.current_balance == 1000.0

    def test_user_name_too_short(self):
        with pytest.raises(Exception):
            User(name="AB", agency="0000", account="00000-0", current_balance=0.0)

    def test_user_invalid_agency(self):
        with pytest.raises(Exception):
            User(name="Vitor Soller", agency="00", account="00000-0", current_balance=0.0)

    def test_user_invalid_account(self):
        with pytest.raises(Exception):
            User(name="Vitor Soller", agency="0000", account="123", current_balance=0.0)

    def test_user_negative_balance(self):
        with pytest.raises(Exception):
            User(name="Vitor Soller", agency="0000", account="00000-0", current_balance=-1.0)

    def test_user_to_dict(self):
        user = User(
            name="Vitor Soller",
            agency="0000",
            account="00000-0",
            current_balance=1000.0
        )
        d = user.to_dict()
        assert d["name"] == "Vitor Soller"
        assert d["agency"] == "0000"
        assert d["account"] == "00000-0"
        assert d["current_balance"] == 1000.0


class TestTransaction:

    def test_create_deposit(self):
        tx = Transaction(value=500.0, transaction_type=TransactionTypeEnum.DEPOSIT)
        assert tx.value == 500.0
        assert tx.transaction_type == TransactionTypeEnum.DEPOSIT

    def test_create_withdraw(self):
        tx = Transaction(value=200.0, transaction_type=TransactionTypeEnum.WITHDRAW)
        assert tx.value == 200.0
        assert tx.transaction_type == TransactionTypeEnum.WITHDRAW

    def test_transaction_invalid_value(self):
        with pytest.raises(Exception):
            Transaction(value=-100.0, transaction_type=TransactionTypeEnum.DEPOSIT)

    def test_transaction_zero_value(self):
        with pytest.raises(Exception):
            Transaction(value=0.0, transaction_type=TransactionTypeEnum.DEPOSIT)

    def test_transaction_to_dict(self):
        tx = Transaction(value=100.0, transaction_type=TransactionTypeEnum.DEPOSIT)
        d = tx.to_dict()
        assert d["value"] == 100.0
        assert d["transaction_type"] == "DEPOSIT"


class TestRepository:

    def test_get_user(self):
        repo = UserRepositoryMock()
        user = repo.get_user()
        assert user is not None
        assert user.name == "Vitor Soller"

    def test_deposit(self):
        repo = UserRepositoryMock()
        repo.deposit(500.0)
        assert repo.get_user().current_balance == 1500.0

    def test_withdraw(self):
        repo = UserRepositoryMock()
        repo.withdraw(200.0)
        assert repo.get_user().current_balance == 800.0

    def test_withdraw_insufficient_balance(self):
        repo = UserRepositoryMock()
        result = repo.withdraw(9999.0)
        assert result is None

    def test_transfer(self):
        repo = UserRepositoryMock()
        repo.transfer(300.0, "12345-6")
        assert repo.get_user().current_balance == 700.0

    def test_transfer_insufficient_balance(self):
        repo = UserRepositoryMock()
        result = repo.transfer(9999.0, "12345-6")
        assert result is None

    def test_get_transactions(self):
        repo = UserRepositoryMock()
        repo.deposit(100.0)
        repo.withdraw(50.0)
        transactions = repo.get_transactions()
        assert len(transactions) == 2