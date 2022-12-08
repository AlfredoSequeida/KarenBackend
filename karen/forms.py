from django.forms import ModelForm
from karen.models import Addon
from karen.fetch_addon_details import resource_exists, get_config_url

from django.forms import ValidationError
import re


class AddonForm(ModelForm):
    class Meta:
        model = Addon
        fields = ["upstream_url"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["upstream_url"].widget.attrs.update(
            {"class": "form-control round", "placeholder": "Github repo url"}
        )
        self.fields["upstream_url"].label = False

    def clean_upstream_url(self):
        data = self.cleaned_data["upstream_url"]

        # remove trailing slash
        if data[-1] == "/":
            data = data[:-1]

        if not resource_exists(get_config_url(data)):
            raise ValidationError("Repo is missing config.json")

        if not resource_exists(data):
            raise ValidationError(
                "This URL can't be accessed",
            )

        match = re.search(
            "^((http(s)?:\/\/)([\w\.]+)(\/|:))([\w,\-,\_]+)\/([\w,\-,\_]+)((\/){0,1})$",
            data,
        )

        if not match:
            raise ValidationError(
                "Invalid Github Repo URL",
            )

        if Addon.objects.filter(upstream_url=data).exists():
            raise ValidationError(
                "This addon has already been submitted",
            )

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data