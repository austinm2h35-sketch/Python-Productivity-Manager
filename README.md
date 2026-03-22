# Productivity Management Application

---

# Overview

This program is a multi-faceted productivity manager, allowing you to add tasks to a weekly to-do list, manage upcoming
events (in this case, exam dates), and receive daily emails which print this information in addition to motivational
sayings and a daily quote taken from a web API. 

---

## Components

The components used for this program are outlined as follows. When the program has
been used already, there will be five files relating to this application:

1) To-Do.py
2) To-Do.bat
3) To-Do.csv
4) Exam-Scheduler.py
5) Exam-Scheduler.csv

All components except the csv files are clarified here, since the csv files will
be automatically generated once the program is run. Note that this is geared towards
Windows with the .bat file; for Linux users, it should be a .sh file.

### To-Do.py

This is the main python file which sets everything up. Its responsibilities include:

- Setting up the To-Do.csv file
- Editing the to-do list for any day of the week:
	~ Add a task
	~ Print the list
	~ Change a task
	~ Move a task to a different day
	~ Delete a task
- Fetching a daily quote from an API
- Composing and sending a daily email

To distinguish the program's mission between editing the list and sending the email,
the bat file (see below) should include a keyword so that, when the program is
opened by Task Scheduler, the email will send. If the program is opened manually
by the user, it will display a CLI to edit the list as described above.

### Exam-Scheduler.py

An optional extension of the program for students, this file sets up a CLI program
to edit a csv file to store upcoming exams. It offers a space for the class name,
exam type (i.e., quiz, test, final), and exam date. This connects to the To-Do.py
file so that the upcoming exams and their dates print in the daily email so that
no exams sneak up on you. The CLI offers manipulation of the list to:

- Add an exam
- Edit an existing exam
- Print the list of upcoming exams
- Remove an exam

Note that this can be easily edited so that, instead of exams, it prints things
like upcoming meetings, due dates, or any other revolving event you need to keep
track of.


### To-Do.bat

In order to send emails, you'll need to set up a .bat file (Microsoft) titled 'To-Do.bat'. This should be its contents:

@echo off
set "EMAIL_ADDRESS=[your email address]"
set "EMAIL_PASSWORD=[email key]"
cd /d "[file path]"
pythonw To-Do_List.py send

For the password, do NOT use your email password! Instead, you can set up a generated key through the email provider. I
used Gmail, which was a very straight-forward process. Be sure to keep this private, since it can now directly access
your email account. 
The last line specifies that the email will send, as opposed to simply editing the task list as you would be able to do by
opening the .py file through IDLE.

---

## Set-Up

You can set this up to automatically send the daily email at a specific time by setting up a new task on your device's Task
Scheduler. To do this, go to Task Scheduler and click 'Create Basic Task'. Set up the trigger as frequently as you'd like
(daily makes the most sense for this, but of course the script is editable to suit your needs), select 'Start a program'
under Actions, and then paste your To-Do.bat file path in the Program/script. When you have it set up, you can test it
by right-clicking the task in task scheduler and selecting 'run', which will push it to run outside of the scheduled time.
Note that this will ONLY run when your device is on and awake, so if you have your laptop sleeping or shut down when the
scheduled time comes, the program will only run once you turn your computer on.

---

# Conclusion

This program provides everything you need to keep better track of what you have
going on in life. Specifically geared towards students, it can be easily edited
to suit your scheduling needs. Ideas for other components to add to it for a more
complete daily email include adding information about the daily weather forecast,
news headlines, or stock/currency exchange information through other API extensions.

