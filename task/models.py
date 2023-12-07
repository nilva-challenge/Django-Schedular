from django.db import models

from config.settings.base import MAX_SECONDS_TO_DONE_TASK
from core.models import BaseModel, nb
from core.users.models import OwnedModel


class Task(BaseModel, OwnedModel):
    title = models.CharField(
        max_length=256,
    )
    description = models.TextField(
        **nb,
    )
    send_time_schedule = models.DateField()
    send_time_done = models.DateField(**nb)
    parent = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        related_name="preconditions",
        **nb,
    )

    @property
    def is_self_done(self):
        if self.send_time_done:
            delta = (self.send_time_done - self.send_time_schedule).total_seconds()
            if abs(delta) <= MAX_SECONDS_TO_DONE_TASK:
                return True

    @property
    def is_preconditions_done(self):
        for task in self.preconditions.all():
            if not task.is_self_done:
                return False
        return True

    @property
    def is_done(self):
        if self.is_self_done and self.is_preconditions_done:
            return True

    def __str__(self):
        return f"{self.title} ({self.owner.username})"

    class Meta:
        ordering = ["-created"]
