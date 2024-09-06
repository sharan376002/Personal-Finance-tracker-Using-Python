import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_category, get_amount, get_description
import matplotlib.pyplot as plt

class CSVFile:
    csv_file = "finance_data.csv"
    COLUMNS = ["date", "category", "amount", "description"]
    Format = "%d-%m-%y"

    @classmethod
    def creating_csv(cls):
        try:
            pd.read_csv(cls.csv_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.csv_file, index=False)
            print(f"Created file {cls.csv_file}")

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "category": category,
            "amount": amount,
            "description": description,
        }
        with open(cls.csv_file, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry successfully added")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.csv_file)
        df["date"] = pd.to_datetime(df["date"], format=CSVFile.Format)
        
        # Parse the start and end dates
        start_date = datetime.strptime(start_date, CSVFile.Format)
        end_date = datetime.strptime(end_date, CSVFile.Format)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions are recorded in the given date range.")
        else:
            print(f"Transactions from {start_date.strftime(CSVFile.Format)} to {end_date.strftime(CSVFile.Format)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSVFile.Format)}))

            total_income = pd.to_numeric(filtered_df[filtered_df["category"] == "Income"]["amount"], errors='coerce').sum()
            total_expense = pd.to_numeric(filtered_df[filtered_df["category"] == "Expense"]["amount"], errors='coerce').sum()

            print("\nSummary")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${total_income - total_expense:.2f}")

        return filtered_df

    @staticmethod
    def plot_transaction(df):
        df.set_index("date", inplace=True)
        df.index = pd.to_datetime(df.index, format=CSVFile.Format)  # Ensure the index is in datetime format

        income_df = (df[df["category"] == "Income"]
                    .resample("D")
                    .sum()
                    .reindex(df.index, fill_value=0))

        expense_df = (df[df["category"] == "Expense"]
                    .resample("D")
                    .sum()
                    .reindex(df.index, fill_value=0))

        plt.figure(figsize=(10, 5))  
        plt.plot(income_df.index, income_df["amount"], label="Income", color="g")  
        plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")  
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.title("Income and Expense Over Time")
        plt.legend()
        plt.grid(True)
        plt.show()

    @staticmethod
    def pie_transaction(df):
        df.set_index("date", inplace=True)
        df.index = pd.to_datetime(df.index, format=CSVFile.Format)  

        income_df = (df[df["category"] == "Income"]
                    .resample("D")
                    .sum()
                    .reindex(df.index, fill_value=0))

        expense_df = (df[df["category"] == "Expense"]
                    .resample("D")
                    .sum()
                    .reindex(df.index, fill_value=0))    
        
        
        plt.figure(figsize=(10, 5))

        # Plot pie charts
        plt.subplot(1, 2, 1)  # First subplot
        plt.pie(income_df["amount"], labels=income_df.index.strftime(CSVFile.Format), 
                colors='g', autopct='%1.1f%%')
        plt.title("Income")

        plt.subplot(1, 2, 2)  # Second subplot
        plt.pie(expense_df["amount"], labels=expense_df.index.strftime(CSVFile.Format), 
                colors='r', autopct='%1.1f%%')
        plt.title("Expense")

        plt.suptitle("Income vs Expense")

        # Show the plot
        plt.show()



def add():
    CSVFile.creating_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yy) or enter today's date: ", allow_default=True)
    category = get_category()
    amount = get_amount()
    description = get_description()
    CSVFile.add_entry(date, amount, category, description) 

def main():
    print("=====================================")
    print(".....The Personal Finance Tracker....")
    print("=====================================")
    print("\n1. Add Transactions.")
    print("2. View the transactions and summary within date range:")
    print("3. Quit")

    choices = int(input("Enter the choice (1-3): "))
    if choices == 1:
        add()
    elif choices == 2:
        start_date = get_date("Enter the starting date of the transaction (dd-mm-yy): ")
        end_date = get_date("Enter the ending date of the transaction (dd-mm-yy): ")

        df = CSVFile.get_transactions(start_date, end_date)
        if input("Do you want to plot (y/n): ").strip().lower() == "y":
            CSVFile.plot_transaction(df)
        elif input("do you want to see the pie chat for the transaction(y/n) : ").strip().lower() == "y":
            CSVFile.pie_transaction(df)    
        else:
            print("Invalid input.")
    elif choices == 3:
        print("Thank you...")
        quit()
    else:
        print("Invalid input. Please enter 1, 2, or 3...")

if __name__ == "__main__":
    main()

