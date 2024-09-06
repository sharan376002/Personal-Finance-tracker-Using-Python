from datetime import datetime

Catogories = {"I":"Income","E":"Expense"}

# it iis a recurisive function 

def get_date(prompt, allow_default=False):
    date_format = "%d-%m-%y"
    date_str = input(prompt)
    
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Please Enter the valid date in the format...like dd-mm-yy")
        return get_date(prompt, allow_default)




def get_amount():
    try:
        amount = float(input("Enter the Amount : "))
        if amount<=0:
            raise ValueError("the amount must be non-negative value, please Enter the postive value")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()
    


def get_category():
    category = input("Enter the catogory ('I' as Income and 'E' as Expense) : ").upper()
    if category in Catogories:
        return(Catogories[category])
    

    print("Invalid Input.. please Enter the corret value Income is 'I' and Expense is 'E'")
    return get_category


def get_description():
    return input("Enter the anything description about your finance tracking (optional) :")
