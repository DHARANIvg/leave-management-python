from database import *
from employee import Employee, LeaveRequest
from ai import process_user_input
from utils import validate_dates
import datetime



def load_employee(name):
    emp_id = get_employee_by_name(name)
    if not emp_id:
        print("Employee not found. Exiting.")
        return None, None

    balances = get_leave_balance(emp_id)
    raw_history = get_leave_requests(emp_id)
    history = [LeaveRequest(*row) for row in raw_history]
    return emp_id, Employee(name, balances, history)

def handle_check_balance(employee, leave_type):
    balance = employee.get_balance(leave_type)
    print(f"You have {balance} {leave_type} remaining.")

def handle_request_leave(emp_id, employee, leave_type, start_date, num_days):
    if employee.get_balance(leave_type) < num_days:
        print(f"Sorry, you only have {employee.get_balance(leave_type)} {leave_type}.")
        return

    end_date = (datetime.datetime.strptime(start_date, "%Y-%m-%d") + datetime.timedelta(days=num_days - 1)).strftime("%Y-%m-%d")

    if not validate_dates(start_date, end_date):
        print("Invalid date range.")
        return

    update_leave_balance(emp_id, leave_type, -num_days)
    add_leave_request(emp_id, leave_type, start_date, end_date, status="Approved")
    employee.update_balance(leave_type, -num_days)
    employee.add_leave_request(LeaveRequest(leave_type, start_date, end_date, "Approved"))
    print(f"Your {leave_type} from {start_date} to {end_date} has been approved.")

def handle_cancel_leave(emp_id, employee, leave_type, start_date):
    cancel_leave(emp_id, leave_type, start_date)
    print(f"Your {leave_type} on {start_date} has been cancelled.")

def handle_view_history(employee):
    print("\nYour Leave History:")
    for req in employee.leave_history:
        print("-", req)

def main():
    init_db()
    print("=== Leave Management System ===")
    name = input("Enter your name: ").strip()
    emp_id, employee = load_employee(name)

    if not emp_id:
        return

    print(f"\nHello {name}! How can I help you today?")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\n> ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break


        result = process_user_input(user_input)
        print("Model output:", result)  # ADD THIS LINE

        if not result:
            print("Sorry, I didn’t understand that. Try again.")
            continue

        intent = result.get("intent", "").lower()

        leave_type = result.get('leave_type')
        start_date = result.get('start_date')
        num_days = result.get('num_days')

        if "check" in intent or "balance" in intent:
            handle_check_balance(employee, leave_type)
        elif "request" in intent or "apply" in intent:
            handle_request_leave(emp_id, employee, leave_type, start_date, num_days)
        elif "cancel" in intent:
            handle_cancel_leave(emp_id, employee, leave_type, start_date)
        elif "history" in intent:
            handle_view_history(employee)
        else:
            print("Unknown intent. Try again.")


if __name__ == "__main__":
    main()

