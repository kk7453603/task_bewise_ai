FROM python:3.11

WORKDIR /app

COPY . .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
