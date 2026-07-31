from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    title: str = Field(..., min_length=1, example="Groceries")
    amount: float = Field(..., gt=0, example=45.50)
    category: str = Field(..., min_length=1, example="Food")
    expense_date: date = Field(default_factory=date.today, alias="date")

    class Config:
        populate_by_name = True


class Expense(ExpenseCreate):
    id: str


class TotalSummary(BaseModel):
    total_expenses: float
    category_totals: dict[str, float]
