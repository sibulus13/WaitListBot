"# WaitListBot" 
Discord bot for handling weekly sign up and waitlist of SFU and non-SFU students for SSBC

# Stack Used
## Python (Discord.py)[https://discordpy.readthedocs.io/en/stable/] (Firebase Admin)[https://firebase.google.com/docs/reference/admin/python]
The Python script utilizes the bot instance as well as command and task decorators to create functional implementation of responses and actions for the bot. Currently the functionalities signup, unsignup, info (show possible commands), and show (shows sign up and waitlist statuses) have been implemented.

Future implementation can look into:
- Adding a check in command and scheduled weekly check in times to automate sign up confirmation on play day
- Adding a command or task to export weekly sign up results to a CSV file or something similar for documentation of weekly sign up rates, flaking players, etc.
- Adding an auto role assign/de-assigner bot that classifies flakey players as low priority sign up based on condition

## Firebase realtime database (If you want the acc info, ask me.)
The waitlist backend database is super simple: two lists:(signedup, waitlist) which are maintained through the Python script. The lists are cleared weekly after play day, and priority queue is filled with waitlisted players a day before play day.

## Google Compute Engine (If you want the acc info, ask me.)
Currently running on lowest spec f1-micro machine which is estimated at 5$/month, lets see how it goes.

Can look into AWS and other hosting services to optimize cost.