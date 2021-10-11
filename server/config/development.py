"""
The settings we use for the development server
"""

from typing import List

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-$q)9zxy=@&c_i_(97tsp86hs)v#u8$j0jtiyn1zco9ov62am$0"

ALLOWED_HOSTS: List[str] = ["*"]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# In production, we would like to read the authentication
# information from environmental variables
DATABASES = {
    "default": {
        "HOST": "db",
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "antipoaching",
        "USER": "passerine",
        "PASSWORD": "development_password",
        "PORT": 5432,
    }
}
