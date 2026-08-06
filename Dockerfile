FROM python:3.14-slim
WORKDIR /app
COPY ./app .

RUN apt update -y && apt install awscli -y
# 1. Use a lightweight Python base image (adjust version if needed)
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy ONLY requirements.txt first
# This is a Docker trick: it caches this layer so you don't reinstall 
# packages every time you change a single line of your app code.
COPY requirements.txt .

# 4. Install dependencies
# --no-cache-dir is crucial here! It prevents pip from saving downloaded 
# .whl files, saving hundreds of megabytes (and preventing disk space errors).
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code into the container
COPY . .

# 6. Expose the port Gunicorn will listen on
EXPOSE 8000

# 7. Start the application
# Note: Change 'app:app' if your main file or Flask instance is named differently
# (e.g., 'application:application' or 'main:app')
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
RUN pip install -r requirements.txt

CMD ["python3", "application.py"]