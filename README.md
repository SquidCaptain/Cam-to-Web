# Cam to Web
A web server that allows users to add live streams then embed the streams into a webpage

## Motivation
The project came from a need for a demo embeddable live stream for a rtsp protocol camera feed on eyesonic.com.

## Setup Guide
install docker and docker-compose
pull docker image using
```
docker pull squidcaptain/cam_to_web:0.1
```
(Note: check latest version on docker hub and change 0.1 to latest version if possible)
create docker-compose.yml copy and paste
```
version: "3"
services:
  web:
    image: squidcaptain/cam_to_web:0.1
    ports:
      - 8000:8000
    volumes:
        - ./cam-to-web-db:/usr/src/app/cam-to-web-db
```
into docker-compose.yml, cd to where docker-compose.yml is, and run
```
docker-compose up
```
the server should start running on port 8000

## Technologies used
- Python
- Flask
  - Flask-SQLAlchemy
  - Flask-Login
  - Flask-WTForms
  - Flask-Bcrypt
- OpenCV

## Checklist

### Checklist (Alpha)
- [x] Database models
- [x] Form models
- [x] Routes finished
  - [x] Home
    - [x] Guide
  - [x] Login
    - [x] Database implemented
    - [x] Flask-Login implemented
  - [x] User settings
    - [x] Allows users to change username and password
  - [x] Stream
    - [x] Stream connection rubustness (ie timeout handling)
    - [x] Multiple stream handling
    - [x] Stream close handling
- [x] Basic Frontend
  - [x] Template html
  - [x] Bootstrap
  - [x] Custom CSS

### Checklist (Beta)
- [x] Docker
  - [x] Docker Files
  - [x] Docker Hub
- [ ] Beta test
  - [ ] Collect test results
  - [ ] More features?

### Checklist (Full Release)

