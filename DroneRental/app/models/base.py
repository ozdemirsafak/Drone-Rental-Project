from django.db import models

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)

    created_on = models.DateTimeField(
        auto_now_add=True,
        help_text='Oluşturulma'
    )

    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        abstract = True