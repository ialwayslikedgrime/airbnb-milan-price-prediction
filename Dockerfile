# 1. Start from a lightweight Python base image
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /code

# 3. Copy the requirements file first (for caching speed)
COPY ./requirements.txt /code/requirements.txt

# 4. Install dependencies
# --no-cache-dir keeps the image small
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. Copy your actual application code and models
COPY ./app /code/app
COPY ./models /code/models

# 6. Tell the container how to run the API
# We use port 8000, just like on your laptop
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]