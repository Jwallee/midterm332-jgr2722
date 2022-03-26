FROM python:3

RUN apt-get update

WORKDIR /app

RUN pip install pytest==7.0.0

RUN pip install xmltodict==0.12.0

RUN pip install Flask==2.0.3

RUN pip install flask

ADD app.py /app

ADD test_app.py /app

ADD ISS.OEM_J2K_EPH.xml /app

ADD XMLsightingData_citiesUSA02.xml /app

CMD python3 app.py