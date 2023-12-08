import logging

from django.contrib.auth.models import Group

from core.users.models import User


def add_users():
    try:
        administrator_user = User.objects.create(
            username="administrator",
            email="sajjad.eb@gmail.com",
            first_name="Sajjad",
            last_name="Ebrahimi",
            is_staff=True,
            is_superuser=True,
        )
        administrator_user.set_password("123")
        administrator_user.save()
        logging.info("Created administrator user")

        admin_user = User.objects.create(
            username="admin", email="sina@webneshin.com", first_name="Siba", last_name="Kalan", is_staff=True
        )
        admin_user.set_password("123")
        admin_user.save()
        logging.info("Created admin user")
        admin_user.groups.add(Group.objects.get(name="Admin"))
        logging.info("add Admin Group")

        user_user = User.objects.create(
            username="user", email="nima@webneshin.com", first_name="Nima", last_name="Kabo", is_staff=True
        )
        user_user.set_password("123")
        user_user.save()
        logging.info("Created user user")
        user_user.groups.add(Group.objects.get(name="User"))
        logging.info("add User Group")
    except Exception as e:
        print(e)


add_users()
