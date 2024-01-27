## RESTful API using DRF

### User Class has extended

<br>

# Features
1. using JWT for authenticaton
2. all endpoints protected by defaul(need to authenticate first)
3. using celery to handle email sending(when ever user send a get request to task_status endpoint, he can check his done tasks)

## Sample
### Get Task List:
if user is a superuse (admin), he can check all tasks here
if he/she is just a normal user with limited permissions, he just can check his own tasks.

<div align="left" >
<img loading="lazy" style="width:1000px; height:1000px" src="images/admin_taskList.png">
</div>

<br>

### Get Task for an authenticated normal user:
<div align="left" >
<img loading="lazy" style="width:400px; height:600px" src="images/task_list_for_user.png">
</div>
<br>

### POST a task:
<div align="left" >
<img loading="lazy" style="width:400px; height:600px" src="images/create_task.png">
</div>
<br>

### Check Task Status:
if you visit this endpoint and any of your task is done, this will show you those tasks and sending those tasks to your email aswell.
<div align="left" >
<img loading="lazy" style="width:400px; height:600px" src="images/check_task_status.png">
</div>
<br>


### Register User:
#### fields to fill:
1. username
2. password
3. email
4. firstname
5. lastname
<div align="left" >
<img loading="lazy" style="width:400px; height:600px" src="images/creating_user.png">
</div>
<br>

### Delete a user:
auth/users/2
Admin users can delete users, Normal users can delete own's profile aswell.
<div align="left" >
<img loading="lazy" style="width:400px; height:600px" src="images/deleting_user.png">
</div>
<br>

### Create a Jason-Web-Token (access & refresh tokens):
auth/jwt/create
First You need to create a user, then you just kinda log in in this endpoint and get your tokens
<div align="left" >
<img loading="lazy" style="width:400px; height:600px" src="images/create_jwt.png">
</div>
<br>

### Delete a protected task:
if you want to delete a task that associated with another task as pretasks of that task, then you can't delete that task
<div align="left" >
<img loading="lazy" style="width:400px; height:600px" src="images/delete_a_protected_task.png">
</div>
<br>

### Delete a unprotected task:
it means there is no dependeny on this task
<div align="left" >
<img loading="lazy" style="width:400px; height:600px" src="images/delete_unprotected_task.png">
</div>
<br>

### Searching tasks by title:
tasks/?title=SOMETHING
<div align="left" >
<img loading="lazy" style="width:400px; height:600px" src="images/search_by_title.png">
</div>
<br>

### Searching tasks by id:
tasks/?id=1
<div align="left" >
<img loading="lazy" style="width:400px; height:600px" src="images/search_by_id.png">
</div>
<br>


### Updating task:
tasks/2
<div align="left" >
<img loading="lazy" style="width:400px; height:600px" src="images/updating_task.png">
</div>
<br>


### Users List:
If you are an admin, you can see all users data here
if you are a normal user, you just see your account details here
<div align="left" >
<img loading="lazy" style="width:400px; height:600px" src="images/admin_users_list.png">
</div>
<br>

### User Endpoint:
To check your profile data and edit that
auth/users/me
<br>
<br>


## Definiton

We just have a single model.Task class
owner is a foreignkey to User model(User model Extended and customized and refrenced from core app)
pre_task field is also a foreignkey to itself(Task --> 'self')

API view used to decorate function-based views
we didnt use router for limited time(firsly code written in function-based)

we just have a Single Serializer to handle serializion and deserialization of Task Object

### urls are also like this:

127.0.0.1:8000/tasks
127.0.0.1:8000/tasks/{task_id}
127.0.0.1:8000/tasks/task_status
127.0.0.1:8000/auth/users
127.0.0.1:8000/auth/users/me
127.0.0.1:8000/auth/users/{user_id}/me
127.0.0.1:8000/auth/jwt/create
127.0.0.1:8000/auth/jwt/refresh