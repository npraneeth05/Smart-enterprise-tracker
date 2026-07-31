# AI Collaboration & Engineering Notes

This document details how AI assistance was integrated into the workflow to design, implement, test, and refine the **Smart Expense Tracker API**.

---

## 1. Code Generation vs. Manual Implementation

### AI-Generated Skeletons
* **Boilerplate & OpenAPI Schema:** Generated the initial FastAPI route definitions, Pydantic request models (`ExpenseCreate`), and response models (`TotalSummary`).
* **Test Case Boilerplate:** Drafted basic `pytest` HTTP route assertions using FastAPI's `TestClient`.

### Written / Authored Manually
* **In-Memory Storage Architecture (`src/storage.py`):** Encapsulated all storage, querying, and aggregation logic inside a clean `ExpenseStorage` class to decouple state management from the HTTP routing layer.
* **Test State Isolation (Pytest Fixture):** Added an explicit `storage.clear()` reset method paired with an `autouse` pytest fixture. This prevents state leakages between test runs—a common issue with in-memory stores during automated grading.
* **Input Normalization Pipeline:** Implemented string sanitization (`.strip().title()` for storage and `.strip().lower()` for comparisons) to handle inconsistent user inputs gracefully.

---

## 2. Validation, Testing, and Refactoring of AI Output

During code review and testing of the AI's initial suggestions, I identified and fixed three crucial edge cases:

* **Issue 1: Floating-Point Binary Precision Errors**
  * *AI Output:* Standard `sum()` over floats produced floating-point inaccuracies in responses (e.g., `$45.050000000000004`).
  * *Fix & Reason:* Refactored `storage.calculate_totals()` to round both individual category sums and overall totals to 2 decimal places (`round(val, 2)`), preserving proper financial currency representations.

* **Issue 2: Case-Sensitive Filtering Behavior**
  * *AI Output:* Category filtering matched exact strings only. An expense added under `"Food"` was omitted when queried via `GET /expenses?category=food`.
  * *Fix & Reason:* Normalized categories to Title Case upon creation and lowercased query params before filtering to ensure flexible, case-insensitive searching.

* **Issue 3: Silent Failures on Resource Deletion**
  * *AI Output:* The initial `DELETE /expenses/{id}` endpoint returned `204 No Content` even if the ID did not exist.
  * *Fix & Reason:* Updated `storage.delete()` to return a boolean result and raised an explicit `404 Not Found` exception with a descriptive error payload when an invalid ID is provided.

---

## 3. Rejected AI Suggestions & Technical Justifications

* **Rejected: SQLite + SQLAlchemy Database Layer**
  * *Why:* The AI recommended setting up a persistent SQLite database with an ORM. I rejected this because the assignment spec explicitly allowed in-memory storage. Avoiding external file I/O and DB dependencies ensures fast, zero-side-effect execution in automated grading environments.
* **Rejected: Multi-Level Subcategories (e.g., `Food -> Groceries`)**
  * *Why:* The AI suggested a hierarchical category schema. I rejected this to maintain an intuitive flat-category API contract aligned strictly with the assignment requirements.
* **Rejected: JWT Authentication Middleware**
  * *Why:* The AI proposed adding user authentication and login routes. I omitted this to avoid unnecessary scope creep and focus entirely on core business logic, schema validation, and test coverage.
