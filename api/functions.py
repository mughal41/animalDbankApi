import requests
from django.conf import settings
import datetime
from django.utils import timezone


def str2list(animal):
    try:
        friends_data = animal.get("friends", None)
        if friends_data:
            animal["friends"] = [f.strip() for f in friends_data.split(",")]

            return animal
        else:
            return None
    except Exception as e:
        print(str(e))
        return None


def utcFormat(animal):
    try:
        animal_born_at_time = animal.get("born_at", None)
        if animal_born_at_time and animal_born_at_time is not None:
            animal["born_at"] = timezone.make_aware(datetime.datetime.fromtimestamp(animal_born_at_time/1000, timezone.utc)).isoformat()

            return animal
        else:
            return None

    except Exception as e:
        print(str(e))
        return None


