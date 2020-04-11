from django.db import models
MAX_LENGTH = 100

class Site(models.Model):
    id = models.CharField(primary_key=True, max_length=MAX_LENGTH)

    def __str__(self):
        return self.id


class Campus(models.Model):
    id = models.CharField(primary_key=True,max_length=MAX_LENGTH)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class Floor(models.Model):
    floor_num = models.PositiveIntegerField(primary_key=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)

    def __str__(self):
        return self.floor_num


class Space(models.Model):
    id = models.UUIDField(primary_key=True)
    type = models.CharField(choices=(('lab', 'lab'), ('conference_room', 'conference_room')),max_length=MAX_LENGTH)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class Cubic(models.Model):
    id = models.UUIDField(primary_key=True)
    type = models.CharField(choices=(('shared', 'shared'), ('private', 'private')),max_length=MAX_LENGTH)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    # group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
