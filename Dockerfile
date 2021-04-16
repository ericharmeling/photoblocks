FROM python:3.8-alpine
WORKDIR /photoblocks
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./photoblocks ./photoblocks
CMD ["main.py"]