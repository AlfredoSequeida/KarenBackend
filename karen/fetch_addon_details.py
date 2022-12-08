import requests

# get addon details


def resource_exists(resource):
    exists = True

    request = requests.get(resource)

    if request.status_code == 404:
        exists = False

    return exists


def get_raw_url(upstream_url):
    # remove trailing slashes
    if upstream_url[-1] == "/":
        upstream_url = upstream_url[:-1]

    return upstream_url.replace("github", "raw.githubusercontent")


def get_icon_url(upstream_url, icon_path):
    # remove ./ from the begining of a path
    if icon_path[: -(len(icon_path) - 2)] == "./":
        icon_path = icon_path[2:]

    # remove . from the begining of a path
    elif icon_path[0] == ".":
        icon_path = icon_path[1:]

    return f"{get_raw_url(upstream_url)}/master/{icon_path}"


def get_config_url(upstream_url):
    return f"{get_raw_url(upstream_url)}/master/config.json"


def get_readme_url(upstream_url):
    readme_ulr = f"{get_raw_url(upstream_url)}/master/README.md"

    if not resource_exists(readme_ulr):
        readme_ulr = f"{get_raw_url(upstream_url)}/master/README"

    return readme_ulr


def fetch_config(upstream_url):
    config_url = f"{get_raw_url(upstream_url)}/master/config.json"
    return requests.get(config_url).json()


def fetch_readme(readme_url):
    return requests.get(readme_url).text