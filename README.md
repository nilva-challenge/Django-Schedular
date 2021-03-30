# In name of Allah

## Trello Tasks
![alt text](https://github.com/sadrakhamoshi/Django-Schedular/blob/feature_custom_task_admin/ch_nilva/pic/SharedScreenshot.jpg)

![alt text](https://github.com/sadrakhamoshi/Django-Schedular/blob/feature_custom_task_admin/ch_nilva/pic/SharedScreenshot2.jpg)

![alt text](https://github.com/sadrakhamoshi/Django-Schedular/blob/feature_custom_task_admin/ch_nilva/pic/SharedScreenshot3.jpg)

## Introduction
We want a simple app to schedule tasks for users. It should be possible to use django admin as interface for this application.

There are two kind of users:
- normal users:
- admin users

normal users can only see, filter & add to their own tasks. These tasks will have a title, description, owner and time to send field. When user creates new task, it should be scheduled to send an email to its owner at the specified time (use celery for this purpose).

admin users have the permission to manage users, add to them and delete them. Also they can manage all tasks of users, add task for them and edit their tasks. When created or edited, scheduled tasks should be added or edited.

**note** totaly we have 3 type of users in the whole of the project:
- superuser
- admin
- normal
each type of this users can log in into the admin interface of Django with different policies.

account & authentication
------------------------
superusers have all permissions. they can change, create and etc the other users.
admin can create normal user and admin user and change some parts of their information ( e.g admin can not change the user's role into the superuser)
normal users can only see their information and can not edit it.

Tasks
----------------
superusers again have all permissions. they can create, edit tasks for theirselves or others.
admins can do same but for normal users or admin users. they can not edit or create new task for superusers.
normals can only see or edit or create tasks for normal users.

Road Map
===================

Authenticationt & Account-admin
---------------
First of all i started with creating login/ signup APIs for users. For that i used JWT from rest-framework. For users i inherited AbstractUser from django.
i Created 3 kind of API for : 
- login
- signup
- refresh token

After that i tryed to customize the admin pannel for the different users. For that i used admin.ModelAdmin class from django and override some of methods.

Tasks
---------------
Next i went for Tasks in schedule app. i built Task model and created Api for geting the list of the Tasks base on the users permission (as it mentioned)

Celery
---------------
After task i went into the celery lib and read about and did some resarch. we need that to do some tasks  asynchronous. If you want to use celery you need 
broker, which i used redis.\

celery doc : (https://docs.celeryproject.org/en/stable/index.html)

Tasks Admin
--------------
finally i created a customized admin interface for users base on their permissions

-------------------------------------------------

Run
==================
1.clone the porject : 

````
git clone https://github.com/sadrakhamoshi/Django-Schedular.git
````
----------------------------

2.Install pip and python3.7 and virtualenv if you don't have them.\
pip install link : https://pip.pypa.io/en/stable/installing/

````
pip install virtualenv
````
------------------------------
3.create virtual environment for python3.7 base on you os (UNIX/Mac or windows)\

venv link : https://docs.python.org/3/library/venv.html

-----------------------------

4.install postgres\

Download Link: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
- Create a Database (Check ch_nilva/ch_nilva/settings.py for database name)
- create a Login/Group Roles (Check ch_nilva/ch_nilva/settings.py for user and password)

--------------------------------
5.Install requirements\
> $ pip install -r requirements.txt

-------------------
6.Migrate your project
> $ python manage.py migrate

**note** that each user must have below fields:
- email
- username
- password
- first name
- last name
- permissions (admin & normal)

You should extend AbstractUser for implementing user model.

In addition to these (all should be implemented in django admin) write an API for authentication (login & signup) and an API for getting list of tasks (according to permission of user).

### Note
Use django rest framework and JWT for authentication.

Also do not forget to write unit test for authentication API.

## Expectations

So What does matter to us?
- a clean structure of codebase & components
- clean code practices
- well written unit tests
- finally, ability to learn

## Tasks

1. Fork this repository
2. Break and specify your tasks in project management tool (append the image of your tasks to readme file of your project)
3. Learn & Develop
4. Push your code to your repository
5. Explain the roadmap of your development in readme of repository (also append the image of your specified tasks on part 2 to file)
6. Send us a pull request, we will review and get back to you
7. Enjoy

**Finally** don't be afraid to ask anything from us.
