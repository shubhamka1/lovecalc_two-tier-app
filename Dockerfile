#base 
# stage 1
FROM python:3.10-slim as builder

#workdir
WORKDIR /app
#copy code 

COPY . /app

#install 

RUN pip install flask 
RUN pip install mysql-connector-python

# base 2 

FROM python:3.10-slim

COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /app /app
#env var 

ENV host=love_calc_database
ENV user=root
ENV password=root
ENV database=love_calculator

#run

CMD ["python","app.py"]