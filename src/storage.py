import uuid
from typing import Optional
from src.models import Expense, ExpenseCreate


class ExpenseStorage:
    """In-memory expense storage with helper filter/aggregation methods."""

    def __init__(self):
        self._expenses: dict[str, Expense] = {}

    def add_expense(self, data: ExpenseCreate) -> Expense:
        expense_id = str(uuid.uuid4())
        expense = Expense(
            id=expense_id,
            title=data.title,
            amount=data.amount,
            category=data.category.strip().title(),
            date=data.expense_date,
        )
        self._expenses[expense_id] = expense
        return expense

    def get_all(self, category: Optional[str] = None) -> list[Expense]:
        if category:
            formatted_cat = category.strip().lower()
            return [
                e
                for e in self._expenses.values()
                if e.category.lower() == formatted_cat
            ]
        return list(self._expenses.values())

    def delete(self, expense_id: str) -> bool:
        if expense_id in self._expenses:
            del self._expenses[expense_id]
            return True
        return False

    def calculate_totals(self) -> dict:
        overall_total = sum(e.amount for e in self._expenses.values())
        category_totals: dict[str, float] = {}

        for e in self._expenses.values():
            category_totals[e.category] = (
                category_totals.get(e.category, 0.0) + e.amount
            )

        return {
            "total_expenses": round(overall_total, 2),
            "category_totals": {
                k: round(v, 2) for k, v in category_totals.items()
            },
        }

    def clear(self):
        """Helper to clear state between unit tests."""
        self._expenses.clear()


storage = ExpenseStorage()
