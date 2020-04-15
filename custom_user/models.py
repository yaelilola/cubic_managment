from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
MAX_LENGTH = 100


class BusinessGroup(models.Model):
    id = models.CharField(primary_key=True, max_length=MAX_LENGTH)

    def __str__(self):
        return self.id

    def get_users(self):
        pass


class UserManager(BaseUserManager):
    def create_user(self, email, employee_number, percentage, business_group, focal_point=False, space_planner=False,
                    start_date=None, end_date=None, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            employee_number=employee_number,
            start_date=start_date,
            end_date=end_date,
            percentage=percentage,
            business_group=business_group,
            focal_point=focal_point,
            space_planner=space_planner
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, employee_number, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        business_group = BusinessGroup(email)  # TODO: for trial
        business_group.save()
        user = self.create_user(
            email,
            password=password,
            employee_number=employee_number,
            percentage='full_time',
            business_group=business_group,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        business_group = BusinessGroup(email)#TODO: for trial
        business_group.save()
        user = self.create_user(
            email,
            password=password,
            employee_number="0",
            percentage='full_time',
            business_group=business_group,
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
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    # notice the absence of a "Password field", that is built in.
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    employee_number = models.CharField(max_length=MAX_LENGTH, default="1")  #TODO: unique? think about admins( now they are always 0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    percentage = models.CharField(choices=(('full_time', 'full_time'), ('part_time', 'part_time')), max_length=MAX_LENGTH,
                                  default="full_time")
    business_group = models.ForeignKey(BusinessGroup, on_delete=models.CASCADE)
    focal_point = models.BooleanField(default=False)
    space_planner = models.BooleanField(default=False)
    #TODO: does user have name?

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.staff

    @property
    def is_admin(self):
        """Is the user a admin member?"""
        return self.admin

    @property
    def is_active(self):
        """Is the user active?"""
        return self.active

    def get_employee_number(self):
        return self.employee_number

    def get_email(self):
        return self.email


    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_percentage(self):
        return self.percentage

    def get_business_group(self):
        return self.business_group

    def is_focal_point(self):
        return self.is_focal_point

    def is_space_planner(self):
        return self.is_space_planner

    def set_start_date(self, start_date):
        self.start_date = start_date

    def set_end_date(self, end_date):
        self.end_date = end_date

    def set_focal_point_status(self, status):
        self.is_focal_point = status

    def set_space_planner_status(self, status):
        self.is_space_planner = status

    def set_business_group(self, business_group):
        self.business_group = business_group


