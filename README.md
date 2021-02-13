# How To Run

i made **requirements.txt** to list packages and dependencies .

you have to make a venv and install dependencies(requirements.txt).



also you need to run redis in port 6379 .

after set celery configurations you need to run it with command :

```
celery -A  Schular beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

```
u also need to run :

```
celery -A Schedular worker -l info 
```
u also need to config email settings in django app's settings.py

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

first of all i created my custom user model using Foreign key(profile method) model and  add some fields to it and used signals to connect to original user model

i made a new user panel beside django admin panel.
normal users can login to their panel and add , edit , delete their own tasks they can also filter,order or search them with paginator and export their tasks as csv file
admin user can also do that job beside that they can add,edit and delete users tasks and even they can add ,delete users with their permissions
also create login and registration form
user cant see other user's task and they cant see or even acess admin perimissions thorugh urls
  
```
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250, blank=True)
    PERMISSION_STATUS = (
        ("Normal", "normal"),
        ("Admin", "admin"),
    )
    permissions = models.CharField(max_length=8, choices=PERMISSION_STATUS, default="N")

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
```


# celery 

for manage schedule tasks we have to use celery . i installed celery and cofigure it in Schedular/celery.py file.

i used redis as Broker .
i used celery beat schedular that checks tasks if  current time  reachs the send time it will send a email to user
you can change celery beat settings in django admin .



we have to get exact time for celery task execution. i wrote a method in send_emails function to get time difference between current time 
```
current_time = datetime.now().strftime("%H:%M")
    tasks = Task.objects.all()

    for i in tasks:

        if i.time_to_send == current_time:

            send_mail(
                "Django Schedular",
                "Your task's time has come ",
                "Your Email",
                [i.owner.email],
            )



```


## Api 

at the end i installed DRF(Django Rest framework) to manage APIes.

i used AuthToken to secure them.

we have 5 endpoints :

- register(POST)
- get token(POST)
- LOgin(POST)
- AllTasks(GET)
- UserTasks(GET)

after login or register through api user gets their token.they can always get token form api token ,too.

i write a custom permission for all tasks api to limit access for only admin users.


i made **serializers.py** to create input or output for APIes


## Tests 

finally i wrote some tests in api/tests.py** file.

i tested login and register endpoints in such senarios :

- Valid_data
- invalid_data
-register with username that already signup
-IncorrentCredentials



email : alireza.sh076@gmail.com
phone_number : 09351974608

Alireza Shirmohammadi

