FROM python:3.8.10-buster
RUN apt-get update && apt-get -y install sqlite3
ENV HOST '0.0.0.0'
ENV PORT 5000
ENV SQLITE3_PATH cocktail.db
COPY app.py /usr/app/
COPY requirements.txt /usr/app/
COPY cocktail.sql /usr/app
WORKDIR /usr/app
RUN pip install -r requirements.txt
RUN sqlite3 cocktail.db < cocktail.sql
CMD python app.py