FROM tensorflow/tensorflow
WORKDIR /photoblocks
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
EXPOSE 5000
COPY ./photoblocks ./photoblocks
CMD ["python3", "photoblocks/main.py"]