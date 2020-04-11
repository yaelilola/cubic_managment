from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser,BaseUserManager
from facilities.models import Cubic
MAX_LENGTH = 100


class Unit(models.Model):
    id = models.CharField(primary_key=True, max_length=MAX_LENGTH)

    def __str__(self):
        return self.id

#
# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None):
#         """
#         Creates and saves a User with the given email and password.
#         """
#         if not email:
#             raise ValueError('Users must have an email address')
#
#         user = self.model(
#             email=self.normalize_email(email),
#         )
#
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_staffuser(self, email, password):
#         """
#         Creates and saves a staff user with the given email and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#         )
#         user.staff = True
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, password):
#         """
#         Creates and saves a superuser with the given email and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#         )
#         user.staff = True
#         user.admin = True
#         user.save(using=self._db)
#         return user
#
#
# class CustomUser(AbstractBaseUser):
#     employee_number = models.CharField(primary_key=True,max_length=MAX_LENGTH)
#     type = models.CharField(choices=(('regular','regular'),('space_planner','space_planner'),('focal_point','focal_point')), max_length=MAX_LENGTH)
#     start_date = models.DateField(null=True, blank=True)
#     end_date = models.DateField(null=True, blank=True)
#     percentage = models.CharField(choices=(('full_time','full_time'),('part_time','part_time')),max_length=MAX_LENGTH)
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     USERNAME_FIELD = 'employee_number'
#     objects = UserManager()
#
#     def __str__(self):
#         return self.username

class UserManager(BaseUserManager):
    def create_user(self, email, employee_number, type, percentage , unit, start_date=None, end_date=None, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            employee_number=employee_number,
            type=type,
            start_date=start_date,
            end_date=end_date,
            percentage=percentage,
            unit=unit,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, employee_number, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            employee_number=employee_number,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        unit = Unit(email)#TODO: for trial
        unit.save()
        user = self.create_user(
            email,
            password=password,
            employee_number="0",
            type='regular',
            percentage='full_time',
            unit=unit,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that is built in.
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    employee_number = models.CharField(max_length=MAX_LENGTH,default="1") #TODO: unique? think about admins( now they are always 0)
    type = models.CharField(
        choices=(('regular', 'regular'), ('space_planner', 'space_planner'), ('focal_point', 'focal_point')),
        max_length=MAX_LENGTH, default='regular')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    percentage = models.CharField(choices=(('full_time','full_time'),('part_time','part_time')),max_length=MAX_LENGTH,
                                  default="full_time")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)


    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active
