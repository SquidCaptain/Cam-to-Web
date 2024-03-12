FROM python:3.12.1

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install flask flask_sqlalchemy flask_wtf flask_bcrypt flask_login opencv-python numpy

ADD . /usr/src/app

WORKDIR /usr/src/app

EXPOSE 8000

CMD [ "python", "server.py" ]
