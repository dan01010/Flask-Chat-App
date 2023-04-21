from flask import Flask, render_template, request,redirect,url_for
from flask_socketio import SocketIO, join_room,leave_room
from flask_login import current_user,login_user,login_required,logout_user, LoginManager
import pymongo

from db import get_user,save_user


login_manager=LoginManager()
app=Flask(__name__)
app.secret_key='meir'
socketio= SocketIO(app)
login_manager.init_app(app)
login_manager.login_view='login'

@app.route('/')
def home():
      return render_template("1.html")

@app.route('/signup',methods=["GET","POST"])
def signup():
            if current_user.is_authenticated:
                  return redirect(url_for('home'))
            message=" "
            if request.method =="POST":
                  username=request.form.get('username')
                  password=request.form.get('password')
                  email=request.form.get('email')
                  save_user(username,email,password)
                  try:
                        save_user(username,email,password)
                        return redirect(url_for('login'))
                  except pymongo.errors.DuplicateKeyError:
                        message='user already exists'
            return render_template('signup.html',message=message)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/login",methods=["GET","POST"])
def login():
      if current_user.is_authenticated:
            return redirect(url_for('home'))
      message=" "
      if request.method =="POST":
            username=request.form.get('username')
            password=request.form.get('password')
            user=get_user(username)

            if user and user.check_password(password):
                  login_user(user)
                  return redirect(url_for('home'))
            else:
                  message='failed to login'            
      return render_template('login.html',message=message)

@app.route('/chat')
@login_required
def chat():
      username=request.args.get('username')
      room_no=request.args.get("room_no")
      
      if username and room_no:
            return render_template("chat.html",username=username,room_no=room_no)
      else:
            return redirect(url_for('home'))
      
@socketio.on("join_room")
def handle_join_room(data):
        app.logger.info("{} has joined the room {}" .format(data['username'],data['room']))
        join_room(data['room'])
        socketio.emit("join_room_announcement",data,room=data['room'])

@socketio.on("send_message") 
def handle_send_message(data):
      app.logger.info("{} has sent message to the room {}:{}".format(data['username'],data['room'],data['message']))
      socketio.emit('receive_message',data, room=data['room'])


@login_manager.user_loader
def load_user(username):
      return get_user(username)




if __name__=='__main__':
      socketio.run(app,debug=True)




