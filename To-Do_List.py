###Title: To-Do List
###Date: 2 November 2025
###Author: Austin Heitzman
###Notes: This app allows for easy updating and documenting of daily activities
###       using a csv file to keep track of tasks that need to be completed. It
###       then allows for scheduled daily emails to send yourself the day's
###       task list as well as other organization tools and morning pep.

#Import libraries
import pandas as pd
import os
import smtplib
import ssl 
import sys
import requests
import csv
from email.message import EmailMessage
from datetime import datetime

#Read and set up file for tasks
file_path = 'To_Do_List.csv'

if not os.path.exists(file_path):
    header = ['ID', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df = pd.DataFrame(columns=header)
    df.to_csv(file_path, index=False)

df = pd.read_csv(file_path)



#Retrieve and validate column
def get_column(df):
    weekday = input("Enter day (start with capital letter): ")
    while weekday not in df.columns:
        print("Invalid weekday; try again")
        weekday = input("Enter day (start with capital letter): ")
    return weekday


#Use API to generate a quote of the day
def get_daily_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        #If API works (code == 200), print quote
        if response.status_code == 200:
            data = response.json()
            return f'"{data[0]["q"]}" — {data[0]["a"]}'
        else:
            #Default quote in case API fails
            return f"Perform all work carefully, guided by compassion\n\n"
    except Exception:
        #Another default quote in case API fails
        return f"Stay strong, stay bold, stay curious\n\n"

#Exam schedule tracker
def get_exam_schedule():
    exam_path = "Exam_Schedule.csv"
    columns = ["Class", "Exam Type", "Date"]
    df2 = pd.read_csv(exam_path)
    exams = df2[columns]
    return exams

#Send email
def send_email(file_path, auto_day=False):
    SMTP_SERVER = "smtp.gmail.com"
    PORT = 587
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    df = pd.read_csv(file_path)
    weekday = datetime.today().strftime('%A') if auto_day else get_column(df)
    tasks = df[['ID', weekday]]
    tasks = tasks[tasks[weekday].notna() & (tasks[weekday] != '')]

    quote = get_daily_quote()

    #Personalized comments to head the emails based on the day of the week
    day_flair = {
    "Monday": "A new week is a new you! You got this!",
    "Tuesday": "You're doing great, keep it up!",
    "Wednesday": "Halfway through, let's keep the strong energy!",
    "Thursday": "Almost there, enjoy the rest of the week!",
    "Friday": "Happy Friday! Let's finish strong!",
    "Saturday": "Put the work down and enjoy yourself, you've earned it!",
    "Sunday": "Self-Care Sunday, let's start the new week right!"
    }

    # Build the email message
    msg = EmailMessage()
    msg['Subject'] = f"Daily Tasks and Updates - {weekday}"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    #Start email off with greeting and 'daily flair'
    body = f"Good morning!"
    body += f"\n\n {day_flair.get(weekday, '')}\n\n"
    body += f"~Here's your daily report~\n\n"

    #Print daily to-do list in email
    body += f"TO-DO TODAY:\n\n"
    if tasks.empty:
        body += f"No tasks scheduled for today.\n\n"
    else:
        body += f"Here are your tasks for today:\n\n"
        for _, row in tasks.iterrows():
            body += f"• ID {row['ID']}: {row[weekday]}\n"

    #Exam schedule
    schedule = get_exam_schedule()
    body += f"\n\nUPCOMING EXAMS:\n\n"
    for _, row in schedule.iterrows():
        body += f"• {row['Class']} {row['Exam Type']}: {row['Date']}\n"
    body += f"You got this!!\n\n"

    #Add quote to email using quote API
    body += f"\n\nDAILY QUOTE: \n\n"
    body += quote 

    #Closing quote for consistency
    body += f"\n\nHave a great day today! And remember:\n\n"
    body += "Give life your best, and life will give you its best"

    msg.set_content(body)

    # Send the email, catching any errors
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print("Email failed:", e)

#Add task
def add_task(df, weekday):
    task = input("Enter task: ")
    id_field = df['ID'].max() + 1 if not df.empty else 1
    new_entry = {col: '' for col in df.columns}
    new_entry['ID'] = id_field
    new_entry[weekday] = task
    df.loc[len(df)] = new_entry
    print(f"Task added with ID {id_field}")
    return df 

#Print tasks
def read_list(df, weekday):
    tasks = df[['ID', weekday]]
    tasks = tasks[(tasks[weekday].notna()) & (tasks[weekday] != '')]
    if tasks.empty:
        print(f"No tasks listed for {weekday}.")
    else:
        print(tasks.to_string(index=False))
    return tasks
    

#Update task
def change_task(df, weekday):
    try:
        id_field = int(input("Enter ID of task to change: "))
        updated_task = input("Enter updates: ")
        if id_field in df['ID'].values:
            df.loc[df['ID'] == id_field, weekday] = updated_task
            print("Task updated")
        else:
            print("No task with that ID")
    except ValueError:
        print("Invalid format; please enter a number")
    return df

#Move task to a different day
def move_task(df, weekday):
    id_field = int(input("Enter ID of task to change: "))
    new_day = input("Enter the day you want this task assigned to: ")
    row = df[df["ID"] == int(id_field)].iloc[0]
    current_day = None
    current_task_text = None
    for col in df.columns:
        if col == "ID":
            continue
        if pd.notna(row[col]) and row[col] != "":
            current_day = col
            current_task_text = row[col]
            break

    if current_day is None:
        print(f"Task {id_field} not found for any day")
        return df

    df.loc[df["ID"] == int(id_field), current_day] = ""
    df.loc[df["ID"] == int(id_field), new_day] = current_task_text

    print(f"Task {id_field} moved from {current_day} to {new_day}")
    return df

#Delete task
def delete_task(df, weekday):
    print("Woo-hoo! You finished a task!")
    try:
        id_field = int(input("Enter ID of task to change: "))
        if id_field in df['ID'].values:
            df.loc[df['ID'] == id_field, weekday] = ""
            print("Task deleted")
        else:
            print("No task with that ID")
    except ValueError:
        print("Invalid format; please enter a number")

    df = df[df.apply(lambda row: not all(cell == "" for cell in row[1:]), axis=1)]

    return df

#Save file and exit program
def save_and_exit(df, filename):
    df.to_csv(filename, index=False)
    return True
    
#Task editor menu
def task_menu():
    print()
    print("Select from the following:")
    print("1 - Add a task")
    print("2 - Change a task")
    print("3 - Print all day's tasks")
    print("4 - Remove a task")
    print("5 - Move a task's day")
    print("9 - Stop editing day's tasks")
    option = input("Enter your selection: ")
    print()
    return option
    
   

#Daily task editor handling
def task_menu_handler(weekday):
    #Allow for continuous editing of one day's tasks
    print()
    initial_read = read_list(df, weekday)
    print()
    menu_option = task_menu()
    while menu_option != '9':
        match menu_option:
            case '1':
                add_task(df, weekday)
            case '2':
                change_task(df, weekday)
            case '3':
                read_list(df, weekday)
            case '4':
                delete_task(df, weekday)
            case '5':
                move_task(df, weekday)
            case _:
                print("Error: invalid option, try again")
                menu_option = task_menu()
        menu_option = task_menu()
    return
    
#Main menu
def main():
    print("Welcome to the Daily Do - your all-in-one to-do list!")
    run_again = 'y'
    while run_again.lower() == 'y':
        weekday = get_column(df)
        task_menu_handler(weekday)
        run_again = input("Would you like to edit a different day?")
    save = save_and_exit(df, file_path)
    if save == True:
        print()
        print("Changes saved successfully")
        print("Exiting program")
        print()
    input("Press Enter to exit...")
    return

#If program call is coming from Task Scheduler/.bat file, send email
#If program call is coming from the .py file, run to-do list editor
if __name__ == "__main__":
    if "send" in sys.argv:
        send_email("To_Do_List.csv", auto_day=True)
    else:
        main()
    

