# animalDbankApi

## Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/mughal41/animalDbankApi.git
cd animalDbankApi
````
### Step 2: Create a virtual environment

python3 -m venv .venv
source .venv/bin/activate # if os is linux

OR

python -m venv .venv
.\.venv\Scripts\activate # if using windows


### Step 3: Install dependencies
pip install -r requirements.txt

### Step 4: Run the development server
python manage.py runserver

### Step 5: Download targetd docker image
https://storage.googleapis.com/lp-dev-hiring/images/lp-programming-challenge-1-1625758668.tar.gz

### Step 6: Load the container
docker load -i lp-programming-challenge-1-1625610904.tar.gz

### Step 7: Expose port 3123
docker run --rm -p 3123:3123 -ti lp-programming-challenge-1

### Step 8: Running Local Tests
python manage.py test
