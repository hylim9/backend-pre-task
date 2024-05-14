from django.db import models


class CommonModel(models.Model):
    """공통 모델"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
    updated_by = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
