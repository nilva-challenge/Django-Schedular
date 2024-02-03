# Django Schedular

## Introduction

Django Schedular is a web-based task scheduling and validation application built using the Django framework. It is designed to streamline task management for users, allowing them to schedule tasks, set dependencies, and receive timely notifications. The application is tailored to meet the needs of both individual users and administrators overseeing multiple users and tasks.


## Key Features

- Task Scheduling: Users can easily schedule tasks with specific details such as title description, owner, and time to send.

- Dependency Management: Tasks can have preconditions, ensuring that specific tasks are completed before others can be scheduled.

- Email Notifications: The application leverages Celery for task scheduling, including sending email notifications to task owners at the specified time.
## Table of Contents
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Usage](#usage)
4. [API Reference](#api-reference)

---
## project managment Board
i used trello for managing tasks

[board](https://trello.com/invite/b/2qjTiUPw/ATTI1ef0b3968c6c6932a821f871a4112a4514888892/nilva)

## Installation


#### Clone the repository

clone the repository with git clone 


#### Install dependencies
```sh
pip install -r requirements.txt
```

## Configuration

Explain any configuration settings that users may need to modify, including environment variables, configuration files, etc.

#### Set environment variables
```sh
...
SECRET_KEY=
DEBUG=
EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
CELERY_BROKER_URL=
SENDER_EMAIL=
...
``` 

## Usage

#### Perform migrations

```sh
python manage.py makemigrations
python manage.py migrate
```

#### Create SuperUser
```sh
python manage.py createsuperuser
```


#### Run the development server 
```sh
python manage.py runserver
```

#### Run the celery 
```sh
celery -A TaskScheduler worker --loglevel=info
```

----

visit the app in  [127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)


## API Reference

This project has only one endpoint that shows the list of tasks

Endpoint 1

    URL: /tasks/validate
    Method: GET
    Parameters:
        -
    Response:

      json

      [
         {
            "id": 1,
            "title": "task title",
            "description": "task description",
            "owner": 1, <user_id>
            "time_to_send": "2024-02-02T20:46:42Z",
            "precondition_tasks": [], <task_id>
            "is_valid": "yes" / "no"
         },
         {
            "id": 2,
            "title": "task title",
            "description": "task description",
            "owner": 1, <user_id>
            "time_to_send": "2024-02-02T20:46:42Z",
            "precondition_tasks": [], <task_id>
            "is_valid": "yes" / "no"
         },
      ]
