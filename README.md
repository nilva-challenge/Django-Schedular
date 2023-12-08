# In name of Allah

## Introduction
We want a simple app to schedule & validate tasks for users. It should be possible to use django admin as interface for this application.

There are two kind of users:
- normal users
- admin users

**note** that each user must have below fields:
- email
- username
- password
- first name
- last name
- permissions (admin & normal)

You should extend AbstractUser for implementing user model.

normal users can only see, filter & add to their own tasks. These tasks will have a title, description, owner, time to send and precondition tasks field. the task should be scheduled to send an email to its owner at the specified time (use celery for this purpose) **Note** that every task has a set of precondition tasks (which are tasks as well) meaning for a task to be done, first, the set of tasks defined for it should have been done by the time it needs to be sent, otherwise the task will not be considered done. Also definition of done for a task is if it was sent at the specified time.

admin users have the permission to manage users, add to them and delete them. Also they can manage all tasks of users, add task for them and edit their tasks. When created or edited, scheduled tasks should be added or edited.

### Note
Write an API for validating a set of tasks (validation means if the set of tasks is possible to be done or not). If there is a precondition task which is not in the specified set of tasks, you do not need to consider it.

### Example

#### example 1
- Task
  - id: 1
  - title: task 1
  - description: desc 1
  - owner: nilva.man
  - time to send: 2020-05-10 10:30
  - pre-tasks:
- Task
  - id: 2
  - title: task 2
  - description: desc 2
  - owner: nilva.man
  - time to send: 2020-05-06 10:30
  - pre-tasks:
    - 1
    - 3
- Task
  - id: 3
  - title: task 3
  - description: desc 3
  - owner: nilva.man
  - time to send: 2020-02-10 9:30
  - pre-tasks:

result: **No**, task 1 happens after task 2, but is a precondition of task 2, which makes it impossible to happen

#### example 2
- Task
  - id: 1
  - title: task 1
  - description: desc 1
  - owner: nilva.man
  - time to send: 2020-05-10 10:30
  - pre-tasks:
- Task
  - id: 2
  - title: task 2
  - description: desc 2
  - owner: nilva.man
  - time to send: 2020-06-10 12:30
  - pre-tasks:
    - 1
    - 3
- Task
  - id: 3
  - title: task 3
  - description: desc 3
  - owner: nilva.man
  - time to send: 2020-06-01 12:30
  - pre-tasks:
    - 1

result: **Yes**, First task 1 will happen, then task 3, then task 2


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


## Descriptions
Hello
I prefer to send additional details by email.

Thanks for your trust.
