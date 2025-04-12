FROM python:3.12

LABEL maintainer="Jesus Levano <jlevanotasayco@gmail.com>"

COPY ./app /app
WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
   pip install -r requirements.txt

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "80"]