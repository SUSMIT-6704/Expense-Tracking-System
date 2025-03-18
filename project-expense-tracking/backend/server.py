from fastapi import FastAPI, HTTPException
from datetime import date
from typing import List
from pydantic import BaseModel
import db_helper  # Ensure this module is properly implemented and available

app = FastAPI()


class Expense(BaseModel):
    amount: float
    category: str
    notes: str


class DateRange(BaseModel):
    start_date: date
    end_date: date


@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=404, detail="No expenses found for the given date.")

    return expenses


@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date, expenses: List[Expense]):
    try:
        db_helper.delete_expenses_for_date(expense_date)
        for expense in expenses:
            db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)
        return {"message": "Expenses updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update expenses: {str(e)}")


@app.post("/analytics/")
def get_analytics(date_range: DateRange):
    try:
        data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
        if not data:
            return {"breakdown": {}, "total": 0}

        total = sum(row['total'] for row in data)
        breakdown = {
            row['category']: {
                "total": row['total'],
                "percentage": (row['total'] / total) * 100 if total != 0 else 0,
            }
            for row in data
        }
        return {"breakdown": breakdown, "total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve analytics: {str(e)}")


@app.get("/monthly_summary/")
def get_monthly_summary():
    try:
        monthly_summary = db_helper.fetch_monthly_expense_summary()
        if not monthly_summary:
            return []

        return monthly_summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve monthly summary: {str(e)}")
