from datetime import datetime

class LeaveRequest:
    def __init__(self, leave_type, start_date, end_date, status):
        self.leave_type = leave_type
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def __str__(self):
        return f"{self.leave_type} from {self.start_date} to {self.end_date} [{self.status}]"


class Employee:
    def __init__(self, name, leave_balances, leave_history):
        """
        leave_balances: dict -> {"Sick Leave": 5, "Annual Leave": 10}
        leave_history: list[LeaveRequest]
        """
        self.name = name
        self.leave_balances = leave_balances
        self.leave_history = leave_history

    def get_balance(self, leave_type):
        return self.leave_balances.get(leave_type, 0)

    def update_balance(self, leave_type, delta):
        self.leave_balances[leave_type] = self.leave_balances.get(leave_type, 0) + delta

    def add_leave_request(self, leave_request: LeaveRequest):
        self.leave_history.append(leave_request)

    def __str__(self):
        balance_info = ", ".join([f"{k}: {v}" for k, v in self.leave_balances.items()])
        return f"Employee: {self.name}\nBalances: {balance_info}"
    
# if __name__ == "__main__":
#     history = [
#         LeaveRequest("Sick Leave", "2025-05-10", "2025-05-12", "Approved"),
#         LeaveRequest("Annual Leave", "2025-04-01", "2025-04-03", "Cancelled")
#     ]
#     balances = {"Sick Leave": 3, "Annual Leave": 8, "Maternity Leave": 0}
#     emp = Employee("Alice", balances, history)

#     print(emp)
#     for req in emp.leave_history:
#         print(" -", req)
