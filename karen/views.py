from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

from karen.models import Addon
from karen.forms import AddonForm

from karen import fetch_addon_details


def index(request):

    addons_from_db = Addon.objects.all()
    addons = []

    for addon in addons_from_db:
        try:
            config = fetch_addon_details.fetch_config(addon.upstream_url)
            icon_url = ""

            if config.get("icon"):
                icon_url = fetch_addon_details.get_icon_url(
                    addon.upstream_url, config.get("icon")
                )

            addons.append(
                {
                    "name": config.get("name"),
                    "upstream_url": addon.upstream_url,
                    "icon_url": icon_url,
                }
            )
        except:
            pass

    form = AddonForm()

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = AddonForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            addon_form = form.save(commit=False)

            upstream_url = form.cleaned_data["upstream_url"]
            addon_form.config_url = fetch_addon_details.get_config_url(
                upstream_url
            )

            # addon_form.name = config["name"]
            # addon_form.developer = config["developer"]

            # --------------- icon ---------------
            # if config.get("icon"):
            #     icon_url = fetch_addon_details.get_icon_url(
            #         upstream_url, config["icon"]
            #     )

            #     if fetch_addon_details.resource_exists(icon_url):
            #         addon_form.icon_url = icon_url

            # --------------- readme ---------------
            readme_url = fetch_addon_details.get_readme_url(upstream_url)

            if fetch_addon_details.resource_exists(readme_url):
                print(readme_url)
                addon_form.readme_url = readme_url

            addon_form.save()

            messages.add_message(request, messages.SUCCESS, "Addon Submitted!")

            # redirect to a new URL:
            return HttpResponseRedirect("")

    return render(
        request,
        "karen/index.html",
        {
            "addons": addons,
            "form": form,
        },
    )


def docs(request, version):
    return render(request, f"karen/docs-{version}.html")