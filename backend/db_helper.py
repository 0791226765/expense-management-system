import mysql.connector
from contextlib import contextmanager
from . logging_setup import setup_logger

logger = setup_logger('db_helper')
@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
        # host = "sql7.freesqldatabase.com",
        # user = "sql7769328",
        # password = "Y5y8BR6rb8",
        # database = "sql7769328"
    )
    if connection.is_connected():
        print("Connection successful")
    else:
        print("Failed in connecting to a database")
    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    connection.commit()
    cursor.close()
    connection.close()
def fetch_all_records():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT*FROM sql7769328.expenses")
        expenses = cursor.fetchall()
        for expense in expenses:
            print(expense)

def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT*FROM sql7769328.expenses WHERE expense_date=%s",(expense_date,))
        expenses = cursor.fetchall()
        return expenses

def insert_expense(expense_date,amount,category,notes):
    logger.info(f"insert_expenses called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("INSERT INTO sql7769328.expenses(expense_date,amount,category,notes)VALUES(%s,%s,%s,%s)",
                       (expense_date,amount,category,notes))

def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM sql7769328.expenses WHERE expense_date = %s",(expense_date,))

def fetch_expense_summary(start_date,end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute('''SELECT category,SUM(amount) as total
                       FROM sql7769328.expenses WHERE expense_date
                        BETWEEN %s and %s
                        GROUP BY category''', (start_date,end_date)
                       )
        data = cursor.fetchall()
        return data

def fetch_monthly_summary(year):
    logger.info(f"fetch_monthly_summary called with year {year}")
    with get_db_cursor() as cursor:
        cursor.execute(''' SELECT 
    DATE_FORMAT(expense_date, '%M') AS month,SUM(amount) AS total
    FROM sql7769328.expenses
    WHERE YEAR(expense_date) = %s
    GROUP BY month
    ORDER BY STR_TO_DATE(month, '%M')''', (year,)
                       )
        data = cursor.fetchall()
        return data
def fetch_daily_expenditure(month,year):
    logger.info(f"fetch_daily_summary called with year month: {month}, year: {year}")
    with get_db_cursor() as cursor:
        cursor.execute(''' SELECT Day(expense_date) AS expense_day,
    SUM(amount) AS total
    FROM sql7769328.expenses
    WHERE MONTHNAME(expense_date) = %s
    AND YEAR(expense_date) = %s 
    GROUP BY expense_day
    ORDER BY expense_day''', (month,year)
                       )
        data = cursor.fetchall()
        return data
if __name__ == "__main__":
    expenses = fetch_daily_expenditure("March","2025")
    for i in expenses:
        print(i)
    # expenses = fetch_monthly_summary("2025")
    # print(expenses)
    # print("***expenses for 8/20******")
#     summary = fetch_expense_summary("2024-08-01","2024-08-05")
#     for record in summary:
#         print(record)