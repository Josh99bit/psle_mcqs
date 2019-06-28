from flask import Flask, request, jsonify,render_template
# data-object mapper
from mongoengine import *
# json library 
import json

# connects to psle_test database on mongoengine
connect('psle_test')

# starts the application 
app = Flask(__name__)

# defines the user class
class User(Document):
  email = StringField(required=True, unique=True)
  name = StringField(max_length=50)
  password = StringField(max_length=50)

  # converts object to json
  def to_json(self):
    user_dict={
      'email':self.email,
      'id':str(self.id),
      'name':self.name
    }
    return str(user_dict)
  
class Question(Document):
  text = StringField(required=True,unique=True)
  answer=IntField(required=True)
  options=ListField(StringField(),required=True)

class Attempt(Document):
  question=ReferenceField(Question,required=True)
  given_answer=IntField(required=True)
  user=ReferenceField(User,required=True)

# homepage
@app.route("/")
def homepage():
  return 'This is the homepage'

# handles the register page
@app.route("/register",methods=["GET"])
def get_register_page():
  return render_template('register.html')

# handles the register POST request
@app.route("/register",methods=["POST"])
def post_register ():

  # gets the data from the request context
  email = request.args["email"]
  password=request.args["password"]
  name=request.args["name"]
  
  # creates and saves the user
  u=User(name=name,email=email,password=password)
  u.save()

  # returns the user objecct in a json form
  return u.to_json()


@app.route("/login",methods=["POST"])
def post_login ():
  email = request.args["email"]
  password=request.args["password"]
  # 1: can you change this to get the specific user from the database?
  u = User.objects(email=email,password=password).first()
  if u==None :
    return "user not found"
  else:
    return u.to_json()

@app.route("/login")
def get_login ():
    return render_template('login.html')

# get a question
@app.route("/questions/<qid>",methods=["GET"])
def get_questions (qid):
  q=Question.objects(id=qid).first()
  if q==None:
    # JOSH: This should throw an error
    return"question not found"
  else:
    # return the full page
    return  render_template("question.html" ,question=q)

@app.route("/add_question",methods=["POST"])
def add_question ():
  text = request.args["text"]
  options=request.args.getlist("options")
  answer=int(request.args["answer"])
  q=Question(text=text ,options=options,answer=answer)
  q.save()
  return q.to_json()


@app.route("/questions/<qid>/attempt",methods=["GET"])
def attempt (qid):
  uid=request.args['uid']
  given_answer=request.args["given_answer"]
  u=User.objects(id=uid).first()
  q=Question.objects(id=qid).first()
  a=Attempt(user=u,question=q,given_answer=given_answer)
  a.save()

  return "this should return if the answer is correct or not"

@app.route("/attempt/<uid>/questions")
def get_attempted_questions (uid):
  u=User.objects(id=uid).first()
  return u.name
  
  # if u==None :
  #   return "user not found"
  # else: 
  #   list_of_attempts=Attempt.objects(user=u.id)
  #   for h in list_of_attempts:
      


  #   return a.question

@app.route("/debug")
def debug():
  raise

###### HELPER FUNCTIONS #######

def current_user():
  # pretending to be the user
  return User.objects().first


# converts the byte data into a dictionary 
def bytes_to_dict(byte_data):
  data_as_dict = json.loads(byte_data.decode('utf-8'))
  return data_as_dict

# helper function to test data
def log(data, message="TESTING"):
  app.logger.info(message)
  app.logger.info(data)
