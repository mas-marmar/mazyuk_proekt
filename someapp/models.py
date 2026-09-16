from django.db import models

class Task(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.CharField("Описание", max_length=255)
    date = models.DateTimeField("Дата создания")
    deadline = models.DateTimeField("Срок выполнения") 

    def __str__(self):
        return f"{self.name}"

class Tag(models.Model):
    name = models.CharField("Название", max_length=255)

    def __str__(self):
        return f"{self.name}"

class TaskTag(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_tags")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="task_tags")

    def __str__(self):
        return f"{self.task.name} - {self.tag.name}"

    class Meta:
        db_table = "task_tags"
        unique_together = ("task", "tag")
