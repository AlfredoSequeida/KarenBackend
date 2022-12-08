from rest_framework.response import Response
from rest_framework.views import APIView

from karen.models import Addon
from karen import fetch_addon_details


class KarenView(APIView):
    def get(self, request, format=None):

        addons_from_db = Addon.objects.all()
        addons = []

        for addon in addons_from_db:
            try:
                config = fetch_addon_details.fetch_config(addon.upstream_url)
                icon_url = ""
                readme = ""

                if config.get("icon"):
                    icon_url = fetch_addon_details.get_icon_url(
                        addon.upstream_url, config.get("icon")
                    )

                readme = fetch_addon_details.fetch_readme(
                    fetch_addon_details.get_readme_url(addon.upstream_url)
                )

                addons.append(
                    {
                        "name": config.get("name"),
                        "developer": config.get("developer"),
                        "upstream_url": addon.upstream_url,
                        "icon_url": icon_url,
                        "readme": readme,
                    }
                )
            except:
                pass

        return Response(addons)
