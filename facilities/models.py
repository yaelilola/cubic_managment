from django.db import models
from custom_user.models import CustomUser
from focal_point.models import FocalPoint
MAX_LENGTH = 100


class Campus(models.Model):
    id = models.CharField(primary_key=True, max_length=MAX_LENGTH)

    def __str__(self):
        return self.id

    def get_campuses(self):
        pass

    def get_capacity(self):
        pass

    def get_available_campuses(self):
        pass

    def get_amount_of_free_cubics(self):
        pass

    def get_id(self):
        return self.id


class Building(models.Model):
    id = models.CharField(primary_key=True, max_length=MAX_LENGTH)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)

    def __str__(self):
        return self.id

    def get_floors(self):
        pass

    def get_capacity(self):
        pass

    def get_available_floors(self):
        pass

    def get_amount_of_free_cubics(self):
        pass

    def get_campus(self):
        return self.campus

    def get_id(self):
        return self.id

class Floor(models.Model):
    floor_num = models.PositiveIntegerField(primary_key=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def __str__(self):
        return self.floor_num

    def get_amount_of_free_cubics_of_space(self, space):
        pass

    def get_available_spaces(self):
        pass

    def get_capacity(self):
        pass

    def get_spaces(self):
        pass

    def get_campus(self):
        return self.campus

    def get_floor_num(self):
        return self.floor_num


class Space(models.Model):
    id = models.CharField(primary_key=True, max_length=MAX_LENGTH)
    type = models.CharField(choices=(('lab', 'lab'), ('conference_room', 'conference_room')),max_length=MAX_LENGTH)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)

    def __str__(self):
        return self.id

    def get_capacity(self):
        pass

    def get_free_cubics(self):
        pass

    def get_cubics(self):
        pass

    def get_floor(self):
        return self.floor

    def get_type(self):
        return self.type

    def get_id(self):
        return self.id


class Cubic(models.Model):
    id = models.CharField(primary_key=True, max_length=MAX_LENGTH)
    type = models.CharField(choices=(('shared', 'shared'), ('private', 'private')), max_length=MAX_LENGTH)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    # group = models.ForeignKey(Group, on_delete=models.CASCADE)
    focal_point = models.ForeignKey(FocalPoint, on_delete=models.CASCADE)#Todo: think how to enforce only focal point users
    area = models.DecimalField()

    def __str__(self):
        return self.id

    def get_availability(self):
        pass

    def get_employees_assigned_to_cubic(self):
        pass

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def get_focal_point(self):
        return self.focal_point

    def set_focal_point(self, focal_point):
        self.focal_point = focal_point
