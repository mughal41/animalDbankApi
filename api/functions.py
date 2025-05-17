import requests
from django.conf import settings
import datetime
import time
import threading
import queue
import logging
from typing import Optional, List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def str2list(animal: Dict[str, Any]):
    try:
        friends_data = animal.get("friends")
        if friends_data:
            animal["friends"] = [f.strip() for f in friends_data.split(",")]
            return animal
        return None
    except Exception as e:
        logger.exception("Error in str2list")
        return None


def utc_format(animal: Dict[str, Any]):
    try:
        animal_born_at_time = animal.get("born_at")
        if animal_born_at_time is not None:
            animal["born_at"] = datetime.datetime.fromtimestamp(
                animal_born_at_time / 1000, tz=datetime.timezone.utc
            )
            return animal
        return None
    except Exception as e:
        logger.exception("Error in utc_format")
        return None


def normalize_response(data: Dict[str, Any]):
    try:
        animal_data = str2list(data)
        if animal_data:
            animal_data = utc_format(animal_data)
            if animal_data:
                return animal_data
            else:
                logger.warning(
                    f"Unable to convert to UTC time for animal_DetailID-{data.get('id')} with value {data.get('born_at')}"
                )
        else:
            logger.warning(
                f"Unable to convert string2list for animal detailID-{data.get('id')} with value {data.get('friends')}"
            )
        return None
    except Exception as e:
        logger.exception("Error in normalize_response")
        return None


def graceful_retry(url: str, retry_count: int = 5):
    for retry_count in range(retry_count + 1):
        logger.info(f"GET {url} attempt {retry_count}")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response
        except requests.RequestException as e:
            logger.warning(f"Request exception on {url}: {e}")
        time.sleep(1)
    logger.error(f"GET {url} failed after {retry_count + 1} attempts")
    return None


def fetch_animal_details_and_transform(animal_id: int, queue_object: queue.Queue):
    try:
        retry_count = 0
        while retry_count <= 5:
            logger.info(f"Trying to fetch ID {animal_id}, attempt {retry_count}")
            response = graceful_retry(f"{settings.BASE_URL}/animals/v1/animals/{animal_id}")
            if response.status_code == 200:
                transformed_data = normalize_response(response.json())
                if transformed_data:
                    queue_object.put(transformed_data)
                    return True
                return None
            retry_count += 1
            time.sleep(1)
        return None
    except Exception as e:
        logger.error(f"Failed to fetch ID {animal_id}", exc_info=True)
        return None


def fetch_all_animal_details_with_threads(page: int = 1):
    try:
        total_pages = 0
        response = graceful_retry(f"{settings.BASE_URL}/animals/v1/animals?page={page}")
        if response.status_code == 200:
            total_pages = response.json().get("total_pages", 0)
        if total_pages <= 0:
            return []

        all_ids: List[int] = []
        for p in range(page, total_pages + 1):
            page_response = graceful_retry(f"{settings.BASE_URL}/animals/v1/animals?page={p}")
            if page_response.status_code == 200:
                ids = [item.get("id") for item in page_response.json().get("items", [])]
                all_ids.extend(ids)

        result_queue = queue.Queue()
        threads: List[threading.Thread] = []

        for animal_id in all_ids:
            t = threading.Thread(
                target=fetch_animal_details_and_transform,
                args=(animal_id, result_queue)
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        response_list: List[Dict[str, Any]] = []
        while not result_queue.empty():
            item = result_queue.get()
            if item:
                response_list.append(item)

        return response_list
    except Exception as e:
        logger.exception("Error in fetch_all_animal_details_with_threads")
        return None


def bulk_parse_data(payload: List[Dict[str, Any]]) -> Optional[bool]:
    try:
        for i in range(0, len(payload), 100):
            chunk = payload[i:i + 100]
            response = requests.post(f"{settings.BASE_URL}/animals/v1/home", json=chunk)
            if response.status_code == 200:
                logger.info(f"Successfully sent batch {i // 100 + 1} ({len(chunk)} records)")
            else:
                logger.error(
                    f"Failed to send batch {i // 100 + 1}: {response.status_code} - {response.text}"
                )
                break
        return True
    except Exception as e:
        logger.exception("Error in bulk_parse_data")
        return None
