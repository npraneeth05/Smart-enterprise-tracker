from typing import Optional
from fastapi import FastAPI, HTTPException, Query, status
from src.models import Expense, ExpenseCreate, TotalSummary
from src.storage import storage

app = FastAPI(
    title="Smart Expense Tracker API",
    description="REST API to manage personal expenses with categorization and summary calculations.",
    version="1.0.0",
)


@app.post(
    "/expenses", response_model=Expense, status_code=status.HTTP_201_CREATED
)
def create_expense(expense_in: ExpenseCreate):
    """Add a new expense entry."""
    return storage.add_expense(expense_in)


@app.get("/expenses", response_model=list[Expense])
def get_expenses(category: Optional[str] = Query(None, description="Filter by category")):
    """View all expenses, optionally filtered by category."""
    return storage.get_all(category=category)


@app.get("/expenses/summary", response_model=TotalSummary)
def get_expense_summary():
    """Calculate overall total expenses and breakdown by category."""
    return storage.calculate_totals()


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: str):
    """Delete an expense by ID."""
    success = storage.delete(expense_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with ID '{expense_id}' not found.",
        )
    return None
