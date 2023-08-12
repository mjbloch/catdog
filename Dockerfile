# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install dependencies for opencv-python (cv2)
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Install pip requirements
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app into the container
WORKDIR /application
COPY . /application

# Set the environment variable for Flask
ENV FLASK_APP=main.py

EXPOSE 8080

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

# Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "360", "main:app"]
