from flask import Flask, Response, render_template, url_for, redirect, request
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
  
from config import Config
from models import db, Users, Cameras
from forms import CameraForm, LoginForm, RegisterForm, SearchForm, ChangeSettingsForm, EditCameraForm

import threading
import argparse
import time
import numpy
import cv2

## --Flask App--
app = Flask(__name__)
app.config.from_object(Config)

## --Bcrypt--
bcrypt = Bcrypt(app)

## --Database--
db.init_app(app)


## --Flask Login--
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

## --Cameras' Frames--
# dictionary of frames: {alias: frames}
outputFrames = {}

## --Thread Lock--
lock = threading.Lock()

## --Stop Event--
# dictionary of stop events {alias: stop event}
stop_events = {}


## --Functions--

# stream(alias) gets the stream and frames of the aliased camera then lives on a daemon thread
def stream(alias, stop_event):
    global outputFrames, stop_events, lock
    with app.app_context():
        camera = Cameras.query.filter_by(alias=alias).first()
    outputFrames[alias] = None
    if camera:
        source = camera.uri
        cap = cv2.VideoCapture(source)
        time.sleep(2.0)
        if cap.isOpened():
            while not stop_event.is_set():
                if cap.isOpened():
                    ret_val, frame = cap.read()
                    if (not frame is None) and frame.shape:
                        frame = cv2.resize(frame, (camera.width, camera.height))
                        with lock:
                            outputFrames[alias] = frame.copy()
                    else:
                        cap = cv2.VideoCapture(source)
                        time.sleep(10)
                        continue
                else:
                    cap.release()
                    time.sleep(10)
                    continue
            cap.release()
        else:
            print('camera open failed')
    else:
        print('no camera found with alias')

# create_daemon(alias) creates a daemon thread for the aliased camera that the stream function lives on
# side effect: creates a daemon thread that has a stop event in stop_events dictionary with key alias
def create_daemon(alias):
    global stop_events
    if not (alias in stop_events):
        stop_events[alias] = threading.Event()
        stop_events[alias].clear()
        t = threading.Thread(target=stream, args=(alias, stop_events[alias]))
        t.daemon = True
        t.start()

# generate(alias) generates the feed from the frames of the aliased camera
def generate(alias):
    global outputFrames, stop_events, lock
    create_daemon(alias)
    while True:
        with lock:
            if not (alias in outputFrames) or outputFrames[alias] is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrames[alias])
            if not flag:
                continue

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

## --Routes--
# Home route
@app.route('/')
@app.route('/index')
@app.route('/home')
def home():
    return render_template('index.html')

# Add camera route
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    message = "Input new camera info.\nNote: does not check if uri is valid"
    form = CameraForm()
    if form.validate_on_submit():
        try:
            print("0")
            camera = Cameras(alias=form.alias.data.replace(" ", ""), uri=form.uri.data, width=int(form.width.data), height=int(form.height.data))
            print("1")
            db.session.add(camera)
            print("2")
            db.session.commit()
            message = "Success!\nInput new camera info.\nNote: does not check if uri is valid"
        except:
            message = "Something went wrong!\nInput new camera info.\nNote: does not check if uri is valid"
    else:
        print("NOT SUPPOSED TO BE HERE")
    return render_template('add_cam.html', form=form, message=message)

# Edit camera route
@app.route('/edit/<string:alias>', methods=['GET', 'POST'])
@login_required
def edit(alias):
    message = "Camera does not exist."
    form = EditCameraForm()
    if alias:
        camera = Cameras.query.filter_by(alias=alias).first()
        if camera:
            message = "Edit info:"
            if form.validate_on_submit() and (camera.alias == form.alias.data or not Cameras.query.filter_by(alias=form.alias.data).first()):
                camera.alias = form.alias.data
                camera.uri = form.uri.data
                camera.width = form.width.data
                camera.height = form.height.data
                db.session.commit()
                message = "Success!\nEdit info:"
            else:
                message = "Invalid input!\nEdit info:"
            form.alias.data = camera.alias
            form.uri.data = camera.uri
            form.width.data = camera.width
            form.height.data = camera.height

    return render_template('edit_cam.html', form=form, message=message, alias=alias)

# View camera route
@app.route('/view', methods=['GET', 'POST'])
@login_required
def view():
    message = ""
    cameras = Cameras.query.all()
    form = SearchForm()
    if form.validate_on_submit():
        camera = Cameras.query.filter_by(alias=form.search.data).first()
        if camera:
            return redirect(url_for('edit', alias=form.search.data))
        else:
            message = "Camera does not exist."
    return render_template('view.html', cameras=cameras, form=form, message=message)

# Delete Camera route
@app.route('/delete/<string:alias>', methods=['GET', 'POST'])
@login_required
def delete(alias):
    try:
        Cameras.query.filter_by(alias=alias).first().delete()
        stop_events[alias].set()
        stop_events.pop(alias)
        outputFrames.pop(alias)
        db.session.commit()
    except:
        print("Bad things happend")
    return redirect(url_for('view'))


""" # Register route
@ app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form) """

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = "Log in"
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('view')) 
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('view'))
        else:
            message = "Invalid username or password"
    return render_template('login.html', form=form, message=message)

# Remove User route
@app.route('/remove/<string:username>', methods=['GET', 'POST'])
@login_required
def remove(username):
    if Users.query.count() > 1:
        try:
            Users.query.filter_by(username=username).first().delete()
            db.session.commit()
        except:
            print("Bad things happend")
    return redirect(url_for('view'))

""" # View users route
@app.route('/users_list', methods=['GET', 'POST'])
@login_required
def users_list():
    users = Users.query.all()    
    return render_template('users_list.html', users=users) """

# View users route
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = ChangeSettingsForm()
    user = current_user
    message = "Edit info:"
    if form.validate_on_submit() and (user.username == form.username.data or not Users.query.filter_by(username=form.username.data).first()):
        user.username = form.username.data
        message = "Success\nEdit info:"
        if bcrypt.check_password_hash(user.password, form.old_password.data):
            user.password = bcrypt.generate_password_hash(form.new_password.data)
        elif form.old_password.data:
            message = "Incorrect Password\nEdit info:"
        db.session.commit()
    form.username.data = user.username
    return render_template('settings.html', form=form, message=message)

# Logout route
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Video source routes
# Shows video of aliased camera
@app.route("/video_feed/<string:alias>")
def video_feed(alias):
    camera = Cameras.query.filter_by(alias=alias).first()
    if camera:
        return Response(generate(alias),
            mimetype = "multipart/x-mixed-replace; boundary=frame")
    else:
        return 'alias not found!', 404 

## --Main--
if __name__ == '__main__':
    
    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=False, default='0.0.0.0',
        help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=False, default=8000, 
        help="ephemeral port number of the server (1024 to 65535)")
    args = vars(ap.parse_args())
    
    with app.app_context():
        db.create_all()
        if not Users.query.first():
            new_user = Users(username="username", password=bcrypt.generate_password_hash("password"))
            db.session.add(new_user)
            db.session.commit()
            print("Created default user")
        print("Welcome back")
    
    # start the flask app
    app.run(
	    host=args["ip"],
        threaded=True, 
        use_reloader=False,
	    debug=False,
	    port=args["port"]
    )