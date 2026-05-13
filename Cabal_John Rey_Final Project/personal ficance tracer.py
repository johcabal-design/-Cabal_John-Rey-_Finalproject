#Dependencies: 
 #   - csv: For data persistence and file handling.
  #  - time: For performance analysis and execution timing.
   # - os: For file path and existence checks.
    #- typing: For static type hints and code clarity.
import csv
import time
import os
from typing import List, Set

class Transaction:
    #Represents a single financial record.
    def __init__(self, amount: float, category: str, desc: str):
        self.amount: float = amount
        self.category: str = category
        self.desc: str = desc

    def __repr__(self) -> str:
        return f"[{self.category}] ${self.amount:.2f} - {self.desc}"

class FinanceTracker:
    #Manages transactions, file I/O, and data processing algorithms.
    
    FILE_NAME = "finance_data.csv"

    def __init__(self):
        self.transactions: List[Transaction] = []
        self.categories: Set[str] = {"Transportation", "Food", "Bills", "Salary"}
        self._load_from_file()

    def _load_from_file(self) -> None:
        """Implements File Handling to persist data across sessions."""
        if not os.path.exists(self.FILE_NAME):
            return
        try:
            with open(self.FILE_NAME, mode='r', newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        amt, cat, dsc = float(row[0]), row[1], row[2]
                        self.transactions.append(Transaction(amt, cat, dsc))
                        self.categories.add(cat)
        except (IOError, ValueError):
            print("Error loading existing data file.")

    def save_to_file(self) -> None:
        #Writes current transaction list to a CSV file using a Context Manager.
        # The 'with' statement is the Context Manager
        with open(self.FILE_NAME, mode='w', newline='') as f:
            writer = csv.writer(f)
            for tx in self.transactions:
                writer.writerow([tx.amount, tx.category, tx.desc])

    def add_entry(self, amount: float, category: str, desc: str) -> None:
        #Adds a new transaction and updates the category set.
        self.transactions.append(Transaction(amount, category, desc))
        self.categories.add(category)
        self.save_to_file()

    def recursive_sum(self, data: List[Transaction]) -> float:
        """
        Algorithm: Calculates total spend recursively.
        Base Case: An empty list has a sum of 0.0.
        """
        if not data:
            return 0.0
        return data[0].amount + self.recursive_sum(data[1:])

    def get_summary(self) -> None:
        """Demonstrates Performance Analysis and Data Processing."""
        if not self.transactions:
            print("\nNo data to process.")
            return

        start = time.perf_counter()
        total = self.recursive_sum(self.transactions)
        end = time.perf_counter()

        print(f"\n--- Performance Analysis ---")
        print(f"Items Processed: {len(self.transactions)}")
        print(f"Execution Time: {end - start:.6f} seconds")
        print(f"Calculated Total: \u20b1{total:.2f}")

def get_valid_float(prompt: str) -> float:
    """Ensures user input is a valid number (Input Validation)."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a numeric value.")

def main():
    """Main CLI Menu with proper error handling."""
    tracker = FinanceTracker()
    
    while True:
        print("   INTERMEDIATE FINANCE TRACKER   ")
        print("1. Record Expense/Income")
        print("2. View Unique Categories (Set)")
        print("3. Generate Performance Report")
        print("4. Exit")
        
        choice = input("\nSelect Option: ")

        if choice == "1":
            amount = get_valid_float("Enter Amount (use negative for expenses): ")
            category = input("Enter Category: ").strip().title()
            desc = input("Description: ").strip()
            tracker.add_entry(amount, category, desc)
            print("Entry saved successfully!")

        elif choice == "2":
            print(f"\nStored Categories: {', '.join(tracker.categories)}")

        elif choice == "3":
            tracker.get_summary()

        elif choice == "4":
            print("Exiting. Data saved to CSV.")
            break
        else:
            print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()