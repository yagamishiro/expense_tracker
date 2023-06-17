import calendar
from expense import Expense
import datetime
import colorama


def main():
    print("Running Expense Tracker!")
    expense_file_name = "expenses.csv"
    budget = 15000

    # Get user expense
    expense = get_user_expense()

    # Save expense to file
    save_expense_to_file(expense, expense_file_name)

    # Summarize the expenses
    summarize_expense(expense_file_name, budget)

def get_user_expense():
    print(f"🎯 Getting user expense")
    expense_name = input("Please enter the expense name: ")
    expense_amount = float(input("Please enter the expense amount: "))
    expense_categories = [
        "Food",
        "Home",
        "Work",
        "Fun",
        "Misc"
    ]
    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"{i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        try:
            selected_index = int(input(f"Please enter a category number {value_range}: ")) - 1

            if selected_index in range(len(expense_categories)):
                selected_category = expense_categories[selected_index]
                new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)

                return new_expense
            else:
                print("Invalid category. Please try again.")
        except:
            print("Invalid category. Please try again.")

def save_expense_to_file(expense: Expense, expense_file_name):
    print(f"🎯 Saving user expense: {expense} to {expense_file_name}")
    with open(expense_file_name, "a") as f:
        f.write(f"{expense.name}, {expense.amount:.2f}, {expense.category}\n")

def summarize_expense(expense_file_name, budget):
    print(f"🎯 Summarizing user expense")
    expenses: list[Expense] = []
    with open(expense_file_name, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expense = Expense(name=expense_name, amount=float(expense_amount), category=expense_category)
            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses by category 📈:")
    for key, amount in amount_by_category.items():
        print(f"{key}: ₱{amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f"💸 You have spent ₱{total_spent:.2f} this month.")

    remaining_budget = budget - total_spent
    print(f"✅ You have ₱{remaining_budget:.2f} left.")

    # Get the current date
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    colorama.init()
    print(green(f"👉 Approximate budget per day to survive for the rest of the month is ₱{daily_budget:.2f}."))
    colorama.deinit()

def green(text):
    return colorama.Fore.GREEN + text + colorama.Style.RESET_ALL

if __name__ == "__main__":
    main()
