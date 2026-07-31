# Smart Expense Tracker API

A lightweight REST API to manage personal expenses, filter by category, and calculate spending summaries. Built with Python and FastAPI.

## Features Included
- **Add Expense:** `POST /expenses`
- **View & Filter Expenses:** `GET /expenses` or `GET /expenses?category={category}`
- **Calculate Totals:** `GET /expenses/summary`
- **Delete Expense:** `DELETE /expenses/{expense_id}`
- **OpenAPI Documentation:** Interactive Swagger docs at `/docs` (Bonus)

---

## Installation Commands

Ensure you have Python 3.9+ installed.

```bash
# Clone repository
git clone <your-repository-url>
cd smart-expense-tracker

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
