FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY model.pkl .
COPY inference.py .

RUN mkdir -p /input/logs /output

CMD ["python", "inference.py"]
