from django.contrib.auth.models import User
from django.db import models


class TaskList(models.Model):
    # models.CASCADE > If you delete a user, all the tasks associated with this user will be deleted
    manager = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    task = models.CharField(max_length=300)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.task
