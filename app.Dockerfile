FROM python:3.8.2-alpine3.11
WORKDIR /app

RUN pip install requests==2.22.0
RUN pip install Flask==1.1.1
RUN pip install elasticsearch==7.0.4
 
