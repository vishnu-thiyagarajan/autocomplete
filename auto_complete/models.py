from django.db import models

# Create your models here.


class AutoComplete(models.Model):
    text = models.CharField(max_length=120, null=False, blank=False)
    count = models.PositiveIntegerField()
    text_len = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.text_len = len(self.text)
        return super(AutoComplete, self).save(*args, **kwargs)

    def __str__(self):  # def __str__(self):
        return self.text
