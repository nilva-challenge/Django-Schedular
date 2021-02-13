# In name of Allah

## Introduction
We want a simple app to schedule tasks for users. It should be possible to use django admin as interface for this application.

There are two kind of users:
- normal users:
- admin users

normal users can only see, filter & add to their own tasks. These tasks will have a title, description, owner and time to send field. When user creates new task, it should be scheduled to send an email to its owner at the specified time (use celery for this purpose).

admin users have the permission to manage users, add to them and delete them. Also they can manage all tasks of users, add task for them and edit their tasks. When created or edited, scheduled tasks should be added or edited.

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
_____________________________________________________________________________________________________________________

My descriptions:
I configured the django admin panel and developed the authentication api with DRF and in this days i learned some things that i didnt know them so i developed this app but unfortunately i couldn't complete this challenge because i did not know any things about celery and i watch some videos in youtube about celery but i couldn't do this task completely .

![Alt text](https://github.com/AliEjlalzadeh/Django-Schedular/blob/main/TasksImage.PNG)
