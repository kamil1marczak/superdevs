import os

from django.conf import settings
from django.db import models

from superdevs.common.models import BaseModel


class Dataset(BaseModel):
    is_deleted = models.BooleanField(default=False)
    path = models.FilePathField(
        path=os.path.join(settings.MEDIA_ROOT, "starwars"),
        match=r".*\.csv$",
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["path", "is_deleted"], name="unique_path_active"),
        ]

    def __str__(self):
        return os.path.basename(self.path)
