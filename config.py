import os

DJANGO_SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-ub+iz-a_q6t4_)v34set35$9)1!ya)h(hh-t-vffo&0#_)_m3",
)

API_MOUNT_PATH = os.environ.get(
    "API_MOUNT_PATH",
    "v1",
)


API_LIST_DEFAULT_PAGE_SIZE = int(
    os.environ.get(
        "API_LIST_DEFAULT_PAGE_SIZE",
        25,
    )
)
API_LIST_MAX_PAGE_SIZE = int(
    os.environ.get(
        "API_LIST_MAX_PAGE_SIZE",
        50,
    )
)

LOCATION_API_KEY = "d6d6b7d25a24498d8025068b20c818f4"
LOCATION_API = "https://api.geoapify.com/v1/geocode/search?text={}&format=json&apiKey=" + LOCATION_API_KEY
