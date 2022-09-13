FROM python:3.9-slim-buster

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_APP=quiz
ENV FLASK_ENV=development
CMD ["flask","run","--host=0.0.0.0"]