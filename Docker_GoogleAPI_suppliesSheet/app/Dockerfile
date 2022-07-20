FROM python:latest

WORKDIR /usr/app/src

COPY sup_data_process.py ./
COPY cbr_rate_rub.py ./
COPY postgresql_connection.py ./
COPY credentials.json ./

RUN apt-get update -y && apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev libsnmp-dev

COPY requirements.txt ./

RUN pip install -r ./requirements.txt

CMD ["python", "./postgresql_connection.py"]
