from fastapi import FastAPI, HTTPException
from mangum import Mangum

from .repo.user_repository_mock import UserRepositoryMock
from .entities.user import User
from .entities.transaction import Transaction
from .enums.transaction_type_enum import TransactionTypeEnum
from .errors.entity_errors import ParamNotValidated

app = FastAPI()

repo = UserRepositoryMock()

# GET / - retorna os dados do usuário
@app.get("/")
def get_user():
    user = repo.get_user()
    return user.to_dict()


# POST /deposit - realiza um depósito
@app.post("/deposit")
def deposit(request: dict):
    value = request.get("value")

    if value is None:
        raise HTTPException(status_code=400, detail="Value is required")
    if type(value) not in [float, int]:
        raise HTTPException(status_code=400, detail="Value must be a number")
    if value <= 0:
        raise HTTPException(status_code=400, detail="Value must be greater than 0")

    transaction = repo.deposit(float(value))

    return {
        "message": "Deposit successful",
        "transaction": transaction.to_dict(),
        "current_balance": repo.get_user().current_balance
    }


# POST /withdraw - realiza um saque
@app.post("/withdraw")
def withdraw(request: dict):
    value = request.get("value")

    if value is None:
        raise HTTPException(status_code=400, detail="Value is required")
    if type(value) not in [float, int]:
        raise HTTPException(status_code=400, detail="Value must be a number")
    if value <= 0:
        raise HTTPException(status_code=400, detail="Value must be greater than 0")

    transaction = repo.withdraw(float(value))

    if transaction is None:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    return {
        "message": "Withdraw successful",
        "transaction": transaction.to_dict(),
        "current_balance": repo.get_user().current_balance
    }


# POST /transfer - realiza uma transferência
@app.post("/transfer")
def transfer(request: dict):
    value = request.get("value")
    target_account = request.get("target_account")

    if value is None:
        raise HTTPException(status_code=400, detail="Value is required")
    if type(value) not in [float, int]:
        raise HTTPException(status_code=400, detail="Value must be a number")
    if value <= 0:
        raise HTTPException(status_code=400, detail="Value must be greater than 0")
    if target_account is None:
        raise HTTPException(status_code=400, detail="Target account is required")
    if type(target_account) != str:
        raise HTTPException(status_code=400, detail="Target account must be a string")

    transaction = repo.transfer(float(value), target_account)

    if transaction is None:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    return {
        "message": "Transfer successful",
        "transaction": transaction.to_dict(),
        "current_balance": repo.get_user().current_balance
    }


# GET /transactions - retorna todas as transações
@app.get("/transactions")
def get_transactions():
    transactions = repo.get_transactions()
    return {
        "transactions": [t.to_dict() for t in transactions]
    }


handler = Mangum(app, lifespan="off")