FROM python:3.6.5

LABEL maintener="John Slankas <jbslanka@ncsu.edu."
RUN pip install --upgrade pip
RUN pip install flask pandas sklearn flasgger
RUN pip install scipy
RUN mkdir /myapp
COPY app.py /myapp/app.py
COPY classify.py /myapp/classify.py
COPY spam.csv /myapp/spam.csv

WORKDIR /myapp
ENTRYPOINT python app.py

EXPOSE 5000

