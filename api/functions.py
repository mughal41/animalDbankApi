import requests
from django.conf import settings
import datetime
import time
import threading
import queue


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
            animal["born_at"] = datetime.datetime.fromtimestamp(animal_born_at_time / 1000, tz=datetime.timezone.utc)

            return animal
        else:
            return None

    except Exception as e:
        print(str(e))
        return None

def normalize_repsonse(data):
    try:
        animal_data = str2list(data)
        if animal_data:
            animal_data = utcFormat(animal_data)
            if animal_data:
                return animal_data
            else:
                print('Unable to convert to UTC time for animal_DetailID-{} having value {}'.format(data.get('id'), data.get('born_at')))
                return None
        else:
            print('Unable to convert string2list for animal detailID-{} having value {}'.format(data.get('id'), data.get('friends')))
            return None
    except Exception as e:
        print(str(e))
        return None


def fetch_animal_details_and_transform(animal_id, queue_object):
    try:
        rs = False
        retry_count = 0
        while not rs and retry_count <= 5:
            print('TRYING FOR THE {}th time'.format(retry_count))
            response = requests.get(f"{settings.BASE_URL}/animals/v1/animals/{animal_id}")
            if response.status_code == 200:
                transformed_data = normalize_repsonse(response.json())
                if transformed_data:
                    queue_object.put(transformed_data)
                    return True
                else:
                    return None
            else:
                retry_count += 1
                time.sleep(1)

        return None
    except Exception as e:
        print(f"Failed to fetch ID {animal_id}: {e}")
        return None


def fetch_all_animal_details_with_threads(page=1):
    try:
        rs = False
        retry_count = 0
        while not rs and retry_count <= 5:
            print('TRYING FOR THE {}th time'.format(retry_count))
            first_page_response = requests.get(f"{settings.BASE_URL}/animals/v1/animals", params={"page": page})
            if first_page_response.status_code == 200:
                first_page_data = first_page_response.json()
                total_pages = first_page_data["total_pages"]
                retry_count = 0
                break
            else:
                retry_count += 1
                time.sleep(1)


        all_ids = []
        if total_pages > 0:
            for p in range(int(page), total_pages + 1):
                while not rs and retry_count <= 5:
                    page_data_response = requests.get(f"{settings.BASE_URL}/animals/v1/animals", params={"page": p})
                    if page_data_response.status_code == 200:
                        ids = [item.get('id') for item in page_data_response.json().get('items', [])]
                        all_ids.extend(ids)
                        retry_count = 0
                        break
                    else:
                        retry_count += 1
                        time.sleep(1)

        result_queue = queue.Queue()
        threads = []
        for animal_id in all_ids:
            t = threading.Thread(target=fetch_animal_details_and_transform, args=(animal_id,result_queue,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        response_list = []
        while not result_queue.empty():
            item = result_queue.get()
            if item:
                response_list.append(item)

        return response_list
    except Exception as e:
        return None


def bulk_parse_data(payload):
    try:
        for i in range(0, len(payload), 100):
            chunk = payload[i:i + 100]
            response = requests.post(f"{settings.BASE_URL}/animals/v1/home", json=chunk)

            if response.status_code == 200:
                print(f"Successfully sent batch {i // 100 + 1} ({len(chunk)} records)")
            else:
                print(f"Failed to send batch {i // 100 + 1}: {response.status_code} - {response.text}")
                break
        return True
    except Exception as e:
        print(str(e))
        return None