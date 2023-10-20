from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
        def create_user(self, email, first_name, last_name, role ,password=None,):
            """
            Creates and saves a User with the given email and password.
            """
            if not email:
                raise ValueError("Users must have an email address")

            user = self.model(
                email=self.normalize_email(email),
                first_name=first_name,
                last_name=last_name,
                user_type=role
            )

            user.set_password(password)
            user.save(using=self._db)
            return user

        def create_superuser(self, email,first_name, last_name, role, password=None):
            user = self.create_user(
                email,
                first_name,
                last_name,
                password=password,
            )
            return user




class User(AbstractBaseUser):
    CUSTOMER = "customer"
    PROVIDER = "provider"

    USER_TYPE_CHOICES = (
        (1, CUSTOMER),
        (2, PROVIDER),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=CUSTOMER)
    first_name = models.CharField("first name", max_length=150)
    last_name = models.CharField("last name", max_length=150)
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["name", "surname"]
    objects = CustomUserManager()



