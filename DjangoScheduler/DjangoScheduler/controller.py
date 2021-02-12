from scheduler.models import Task as schedulerTask
from main.models import *
from scheduler.tasks import send_email_task

from celery.result import AsyncResult


class Controller():

    def scheduleTask(self, task):
        # scheduling & adding task to db & Queue
        result = send_email_task.apply_async(
            args=[task.title,
                  task.description,
                  task.owner.email],
            eta=task.timeToSend)

        id = result.task_id
        schedulerTask.objects.create(uuid=id, data=task)

    def updateTask(self, task):

        # revoking & deleting old task
        old_task = schedulerTask.objects.get(data__pk=task.pk)
        AsyncResult(old_task.uuid).revoke()
        old_task.delete()

        # reScheduling task
        self.scheduleTask(task)
