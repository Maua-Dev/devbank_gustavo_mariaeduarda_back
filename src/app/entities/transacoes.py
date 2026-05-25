from typing import Tuple
import uuid
from ..enums.transaction_type_enum import TransactionTypeEnum


class Transaction:

    transaction_id: str
    value: float
    transaction_type: TransactionTypeEnum

    def __init__(
        self,
        value: float = None,
        transaction_type: TransactionTypeEnum = None,
        transaction_id: str = None
    ):
        from ..errors.entity_errors import ParamNotValidated

        # gera um id automatico se nao for passado
        if transaction_id is None:
            transaction_id = str(uuid.uuid4())
        self.transaction_id = transaction_id

        validation_value = self.validate_value(value)
        if not validation_value[0]:
            raise ParamNotValidated("value", validation_value[1])
        self.value = value

        validation_type = self.validate_transaction_type(transaction_type)
        if not validation_type[0]:
            raise ParamNotValidated("transaction_type", validation_type[1])
        self.transaction_type = transaction_type

    @staticmethod
    def validate_value(value: float) -> Tuple[bool, str]:
        if value is None:
            return (False, "Value is required")
        if type(value) not in [float, int]:
            return (False, "Value must be a number")
        if value <= 0:
            return (False, "Value must be greater than 0")
        return (True, "")

    @staticmethod
    def validate_transaction_type(transaction_type) -> Tuple[bool, str]:
        if transaction_type is None:
            return (False, "Transaction type is required")
        if not isinstance(transaction_type, TransactionTypeEnum):
            return (False, "Transaction type must be a TransactionTypeEnum")
        return (True, "")

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "value": float(self.value),
            "transaction_type": self.transaction_type.value
        }

    def __repr__(self):
        return f"Transaction(transaction_id={self.transaction_id}, value={self.value}, transaction_type={self.transaction_type})"