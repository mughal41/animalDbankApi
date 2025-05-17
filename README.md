# animalDbankApi
AnimalDbank is a Django REST API that interacts with a Dockerized backend service to fetch, normalize, and post animal data. It utilizes multi-threading to enhance performance while retrieving large datasets and includes retry mechanisms for improved network resilience.

## Project Description
This project serves as a middleware layer between a frontend (or client) and a containerized backend API. It provides endpoints to:

- Fetch animal details - using multi-threading to fetch animal-id and using it to fetch animal details from an internal service
- Normalize data - (e.g., converting timestamps, splitting comma separated friend names into list)
- Bulk submit - cleaned data to a secondary POST API endpoint

## Workflow Overview

Data Retrieval:
   The API fetches paginated animal data from a Dockerized internal service.
   Multi-threading is used to fetch individual animal details concurrently.
   Gracefully retries in case of unexpected hangup or connection break.

Data Normalization:
   `friends` comma separated string is converted into a list.
   `born_at` timestamp is parsed and converted into UTC datetime.

Data Submission:
   Transformed data got from data retrieval endpoint is sent in batches (100 per request) to the targeted docker endpoint.

---
## Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/mughal41/animalDbankApi.git
cd animalDbankApi
```
### Step 2: Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate # if os is linux
```
OR
```bash
python -m venv .venv
.\.venv\Scripts\activate # if using windows
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```
### Step 4: Run the development server
```bash
python manage.py runserver
```

### Step 5: Download targetd docker image
```bash
wget https://storage.googleapis.com/lp-dev-hiring/images/lp-programming-challenge-1-1625758668.tar.gz
```

### Step 6: Load the container
```bash
docker load -i lp-programming-challenge-1-1625610904.tar.gz
```

### Step 7: Expose port 3123
```bash
docker run --rm -p 3123:3123 -ti lp-programming-challenge-1
```

### Step 8: Running Local Tests
```bash
python manage.py test
```
