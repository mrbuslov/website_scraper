FROM python:3.8-slim-buster
# # весь output в терминал
# ENV PYTHONBUFFERED=1
WORKDIR /django
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt    

COPY . .
# нужно в cmd использовать только "", а не ''
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"] 

