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


# How To Run

i made **requirements.txt** to list packages and dependencies .

you have to make a venv and install dependencies(requirements.txt).

you have to make a .env file and set Email configuration in that file. i made a envsample to show you how to set email configuration.

also you need to run rabbitmq in port 5672 or change settings and make your own configurations.

after set celery configurations you need to run it with command :

```
celery -A nilva_project worker -l info 
```

you have to create your own database . i didnt push it.

you can create your own database(sqlite) with command :
```
python manage.py migrate
```
also you need to create superuser :

```
python manage.py createsuperuser
```

and finnaly you need to run your app :

```
python manage.py runserver
```

# Development RoadMap

# users 

first of all i created my custom user model using AbstractUser model and some fields to it.

also we need to allow users to access admin panel in order to manage their tasks(Todo) . i used signals to do that for us.
```
class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

def access_users_to_admin_panel(sender,instance,*args,**kwargs):
    if not instance.is_staff:
        instance.is_staff = True

pre_save.connect(access_users_to_admin_panel , User)
```

also for implement clean architecture and dont implement business logic in views i made UserInterface and UserService for manage business logic.  

# celery 

for manage schedule tasks we have to use celery . i installed celery and cofigure it in **nilva_project/celeryapp.py** file.

i used rabbitmq as Broker and rpc as Backend.

# Todos 

i made a class(Todo) to manage tasks .
```
class Todo(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(default=1)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField()
    async_task_id = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.title
```

we have to get exact time for celery task execution. i wrote a method in Todo class to get time difference between current time and Todo date and calculate total_second to set as countdown for celery task :
```
def get_time_difference(self):
    now = datetime.now(timezone.utc)
    todo_time = self.date
    difference = todo_time - now
    return difference.total_seconds()
```

due to  we cant change celery tasks time , we have to remove them and make a new task when user edit Todo's date(time to send email). for this we have to save celery task id in Todo class : **async_task_id**

i used signals to set a celery task when user make a Todo or delete a task when user delete it.
```

def set_todo_reminder(sender,instance,*args,**kwargs):
    if instance.async_task_id is None:
        task_id = set_new_task(instance.get_time_difference(),instance.owner.email)
        instance.async_task_id = task_id
    else:
        remove_current_task(instance.async_task_id)
        task_id = set_new_task(instance.get_time_difference(),instance.owner.email)
        instance.async_task_id = task_id


def delete_reminder(sender,instance,*args,**kwargs):
    remove_current_task(instance.async_task_id)


pre_save.connect(set_todo_reminder,Todo)
pre_delete.connect(delete_reminder,Todo)
```

we allowed users to access to admin panel . but users cant manage their tasks yet . i made some changes in Todo ModelAdmin to allow users manage their tasks :

```
def has_add_permission(self,request):
        return True

    def has_change_permission(self,request,obj=None):
        return True

    def has_view_permission(self,request,obj=None):
        return True

    def has_module_permission(self,request,obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
```


there is still a problem that users can see or edit other users tasks . to prevent this i change some bultin methods in Todo ModelAdmin :

```
def get_queryset(self, request):
        qs = super(TodoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
```

there is still a problem . in create Todo page users can make a Todo and assign it to another user . to prevent this  i removed owner field in that page and override save_model method to assign Owner automatically :
```
exclude = ('owner',)
def save_model( self, request, obj, form, change ):
    obj.owner = request.user
    obj.save()
```

## Api 

at the end i installed DRF(Django Rest framework) to make some apis.

i installed simplejwt to secure apis too.

we have 5 endpoints :

- register(POST)
- get token(POST)
- refresh token(POST)
- AllTasks(GET)
- UserTasks(GET)


i made **serializers.py** to create input or output Schema for apis.

also i made **premissions.py** to create some custom permissions for apis.


## Tests 

finally i wrote some tests in **nilva_apis/tests.py** file.

i tested authentication endpoints in two senarios :

- Valid_data
- invalid_data


# Done

please contact me for result

phone_number : 09372232486

email : erfanmorsalidev@gmail.com


Thx.