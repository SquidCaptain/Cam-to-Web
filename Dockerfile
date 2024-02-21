FROM python:3.12.1

RUN pip install flask flask_sqlalchemy flask_wtf flask_bcrypt flask_login opencv-python numpy

ADD . .

EXPOSE 8000

CMD [ "python", "./server.py" ]
