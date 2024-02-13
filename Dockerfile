FROM python:3.12.1

ADD *.py .

ADD templates ./templates

ADD static ./static

RUN pip install flask flask_sqlalchemy flask_wtf flask_bcrypt flask_login opencv-python

