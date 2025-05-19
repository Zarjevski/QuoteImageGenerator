FROM python:3.11-slim

# Install dependencies for Pillow + libraqm
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libraqm-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install flask flask-cors pillow

RUN mkdir -p output

EXPOSE 5000

CMD ["python", "app.py"]
