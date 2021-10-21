FROM python:3.8-alpine
WORKDIR /photoblocks
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY ./photoblocks ./photoblocks
CMD ["python3", "photoblocks/main.py"]