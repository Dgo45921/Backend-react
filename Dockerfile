FROM python:3.10


WORKDIR /app


ENV FLASK_APP=main.py

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]