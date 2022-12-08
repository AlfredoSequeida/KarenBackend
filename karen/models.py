from django.db import models
from django.core.validators import RegexValidator


class Addon(models.Model):
    # name = models.CharField(
    #     max_length=100,
    # )
    # developer = models.CharField(max_length=100)
    # icon_url = models.URLField(max_length=200, blank=True)
    config_url = models.URLField(max_length=200)
    upstream_url = models.URLField(
        max_length=200,
        validators=[
            RegexValidator(
                regex="^((http(s)?:\/\/)([\w\.]+)(\/|:))([\w,\-,\_]+)\/([\w,\-,\_]+)((\/){0,1})$",
                message="invalid github repo link",
                code="invalid_url",
            )
        ],
        unique=True,
    )
