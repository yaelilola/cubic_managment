from django.db import models
from custom_user.models import BusinessGroup
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
    id = models.CharField(primary_key=True, max_length=MAX_LENGTH)
    floor_num = models.CharField(max_length=MAX_LENGTH)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("floor_num", "building"),)

    def __str__(self):
        return str(self.id)

    def get_amount_of_free_cubics_of_space(self, space):
        pass

    def get_available_spaces(self):
        pass

    def get_capacity(self):
        pass

    def get_spaces(self):
        pass

    def get_campus(self):
        return self.building

    def get_floor_num(self):
        return self.floor_num


class Space(models.Model):
    id = models.CharField(primary_key=True, max_length=MAX_LENGTH)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True, blank=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, null=True, blank=True)
    area = models.DecimalField(decimal_places=5, max_digits=10, default=0)

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
    capacity = models.PositiveIntegerField(default=1)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    business_group = models.ForeignKey(BusinessGroup, on_delete=models.CASCADE, null=True, blank=True)
    area = models.DecimalField(decimal_places=5, max_digits=10)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, null=True, blank=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True, blank=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(default="Cubic", max_length=MAX_LENGTH, null=True, blank=True)

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

    def get_business_group(self):
        return self.business_group

    def set_business_group(self, business_group):
        self.business_group = business_group




class Lab(models.Model):
    id = models.CharField(primary_key=True, max_length=MAX_LENGTH)
    type = models.CharField(choices=(('Low Density Lab', 'Low Density Lab'),
                                     ('High Density Lab', 'High Density Lab')), max_length=MAX_LENGTH)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    business_group = models.ForeignKey(BusinessGroup, on_delete=models.CASCADE, null=True, blank=True)
    area = models.DecimalField(decimal_places=5, max_digits=10)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, null=True, blank=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True, blank=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(default="Lab", max_length=MAX_LENGTH)

    def __str__(self):
        return self.id


