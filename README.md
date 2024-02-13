# Cam to Web
A web server that allows users to add live streams then embed the streams into a webpage

## Motivation
The project came from a need for a demo embeddable live stream for a rtsp protocol camera feed on eyesonic.com.

## Technologies used
- Python
- Flask
  - Flask-SQLAlchemy
  - Flask-Login
  - Flask-WTForms
  - Flask-Bcrypt
- OpenCV

## Checklist

### Checklist (initial functionality)
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
