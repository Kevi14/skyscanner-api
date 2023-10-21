from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
# from sky_scanner.models import Address,DocumentType

class CustomUserManager(BaseUserManager):
        def create_user(self, email, first_name, last_name ,password,date_of_birth):
            """
            Creates and saves a User with the given email and password.
            """
            if not email:
                raise ValueError("Users must have an email address")

            user = self.model(
                email=self.normalize_email(email),
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth
            )

            user.set_password(password)
            user.save(using=self._db)
            return user

        def create_superuser(self, email,first_name, last_name, password,date_of_birth):
            user = self.create_user(
                email,
                first_name,
                last_name,
                password,
                date_of_birth,
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
    phone = models.CharField(max_length=15, blank=True, null=True)
    # address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    frequent_flyer_number = models.CharField(max_length=20, blank=True, null=True)
    # document = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField()



    USERNAME_FIELD = 'email'
    objects = CustomUserManager()



