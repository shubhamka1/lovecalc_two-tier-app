#base 

FROM python:3.10-slim

#workdir
WORKDIR /app
#copy code 

COPY . /app

#install 

RUN pip install flask 
RUN pip install mysql-connector-python

#env var 

ENV host=love_calc_database
ENV user=root
ENV password=root
ENV database=love_calculator

#run

CMD ["python","app.py"]