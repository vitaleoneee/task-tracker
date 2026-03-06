FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /tasktracker

RUN apt-get update && apt-get install -y netcat-openbsd\
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "tasktracker.wsgi:application", "--bind", "0.0.0.0:8000"]