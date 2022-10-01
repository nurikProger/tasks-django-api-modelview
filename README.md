# tasks-django-api-modelview
Drf Task manager API

How to use:

Run /todolist/manage.py and add "runserver" in the end to run the server
Copy the url address of the local server and paste it to your browser's searchbar
Add one of these to the url: api/tasks/ api/tasks/?start_date=&end_date= (use "%20" for a space between the date and the time. For example, "2022-12-23%2012:30:23" = "2022-12-23 12:30:23") api/tasks/:id/ api/tasks/to-do/ api/tasks/expired/ api/tasks/in_progress/ api/tasks/done/
Use "YY-mm-dd HH:MM:SS" format for datetime inputs. Note! The input must contain digits for every value shown (month, day, seconds..)
