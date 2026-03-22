import pandas as pd



def add_exam(df):
    # Add an ID to each exam for easy manipulation
    id_field = df['ID'].max() + 1 if not df.empty else 1
    # Collect exam information
    class_name = input("Enter class name: ")
    exam_type = input("Is this a test or a quiz? ")
    exam_date = input("Enter the date of the exam (dd/mm): ")
    new_entry = {col: '' for col in df.columns}
    new_entry['ID'] = id_field
    new_entry['Class'] = class_name
    new_entry['Exam Type'] = exam_type
    new_entry['Date'] = exam_date
    df.loc[len(df)] = new_entry # Add exam to spreadsheet
    print(f"Exam added with ID {id_field}")
    return df

def print_exams(df):
    if df.empty:
        print("No upcoming exams!")
    else:
        print(df.to_string(index=False))
    return df

def change_exam(df):
    try:
        id_field = int(input("Enter ID of exam to change: "))
        updated_field = input("Enter field to update: ")
        #Check if field is in columns
        updates = input("Enter changes: ")
        if id_field in df['ID'].values:
            df.loc[df['ID'] == id_field, updated_field] = updates
            print("Exam updated")
        else:
            print("No exam with that ID")
    except ValueError:
        print("Invalid format; please enter a number")
    return df

def remove_exam(df, file_path):
    print("Another one down!")
    try:
        id_field = int(input("Enter ID of exam to change: "))
        if id_field in df['ID'].values:
            df = df[df['ID'] != id_field] # Remove exam with given ID
            print("Exam removed")
        else:
            print("No exam with that ID")
    except ValueError:
        print("Invalid format; please enter a number")
    return df

def save_and_exit(df, file_path):
    df.to_csv(file_path, index=False)
    return True

def exam_menu():
    print()
    print("Select from the following: ")
    print("1 - Add an exam")
    print("2 - Edit an existing exam")
    print("3 - View upcoming exams")
    print("4 - Remove an exam")
    print("9 - Save and exit")
    print()
    return

def exam_menu_handler(selection, df, file_path):
    if selection == '1':
        df = add_exam(df)
    elif selection == '2':
        df = change_exam(df)
    elif selection == '3':
        df = print_exams(df)
    elif selection == '4':
        df = remove_exam(df, file_path)
    elif selection == '9':
        saved = save_and_exit(df, file_path)
        if saved == True:
            print("Changes saved successfully")
        else:
            print("Warning! Changes not saved!")
    else:
        print("Invalid selection; please try again")
    return df

def main():
    file_path = 'Exam_Schedule.csv'
    df = pd.read_csv(file_path)
    print("Welcome to your exam scheduler!")
    print("Here are your current upcoming tests: ")
    print()
    print_exams(df)
    print()
    rerun = 'y'
    while rerun.lower() == 'y':
        exam_menu()
        selection = input()
        df = exam_menu_handler(selection, df, file_path)
        rerun = input("Would you like to run again? (y/n): ")
    # Safeguard to make sure info saves
    just_in_case = save_and_exit(df, file_path)
    if just_in_case == True:
        print("Changes saved successfully")
    else:
        print("Warning! Changes not saved!")

main()
        
        


        
    
