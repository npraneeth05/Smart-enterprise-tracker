---

### `AI_NOTES.md`
```markdown
# AI Collaboration Notes

This document details how AI assistance was leveraged during the design, development, and testing of the Smart Expense Tracker API.

---

## 1. Code Generation vs. Manual Implementation

### AI-Generated Components:
* **Initial Boilerplate Setup:** Drafted the basic FastAPI route skeletons (`src/main.py`) and initial `pytest` mock structures.
* **OpenAPI & Pydantic Schema Annotations:** Generated initial field definitions (`amount: float`, `category: str`, etc.) and Pydantic validation rules.

### Written / Authored manually:
* **In-Memory Storage Abstraction (`src/storage.py`):** Designed the `ExpenseStorage` class to encapsulate dictionary operations, string normalization (category case-insensitivity), and rounding logic for currency totals.
* **Pytest Fixture State Isolation:** Implemented `storage.clear()` and the `autouse` pytest fixture to prevent persistent state pollution between integration test cases.

---

## 2. Validation, Testing, and Modifications to AI Outputs

* **Category Normalization:**
  * *Original AI Draft:* Stored categories exactly as received, making filtered queries case-sensitive (`/expenses?category=food` missed `"Food"`).
  * *Refactored Change:* Added `.strip().title()` when storing expenses and `.strip().lower()` during evaluation in `storage.py` to ensure case-insensitive category filtering and uniform grouping in summaries.
* **Float Precision rounding:**
  * *Original AI Draft:* Simple floating-point additions, which resulted in Python binary float representation artifacts like `40.000000000000006`.
  * *Refactored Change:* Wrapped total sum operations with `round(val, 2)` before returning final API responses.

---

## 3. AI Suggestions Rejected & Why

* **SQLite / SQLAlchemy Integration:**
  * *Suggestion:* The AI recommended setting up a SQLite database using SQLAlchemy ORM to persist data.
  * *Decision:* **Rejected.** The assignment spec explicitly allowed in-memory storage and prioritized simplicity and zero-dependency database setup for automated evaluation environments.
* **Complex JWT Authentication Middleware:**
  * *Suggestion:* The AI proposed an endpoint authorization system.
  * *Decision:* **Rejected.** It added unnecessary operational complexity outside the exact scope of the evaluation criteria.
