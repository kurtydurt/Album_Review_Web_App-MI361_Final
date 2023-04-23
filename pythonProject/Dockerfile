FROM python:3.9-slim-buster

WORKDIR /pythonProject

COPY /pythonProject/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
