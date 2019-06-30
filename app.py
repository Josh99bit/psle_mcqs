from flask import Flask, request, jsonify,render_template, session
# import session
from flask_session import Session
# data-object mapper
from mongoengine import *
# json library 
import json

# if production => mongodb+srv://voom:Tanw7knSIDT2IKpP@cluster0-aoahk.mongodb.net/test?retryWrites=true&w=majority
# if development => locahost
connect('psle_test')

# starts the application 
app = Flask(__name__)

# sets a few randomly given context
app.config.from_object(__name__)
app.secret_key = "ee08a4d7ab79568073415f1667a78ed1"

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
  credit=StringField(required=True)

class Attempt(Document):
  question=ReferenceField(Question,required=True)
  given_answer=IntField(required=True)
  user=ReferenceField(User,required=True,unique_with="question")

  def is_correct(self):
    return self.given_answer==self.question.answer

# homepage
@app.route("/")
def homepage():
  return render_template("homepage.html")

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

  # after the user is saved, set the session
  session["uid"] = str(u.id)

  # returns the user objecct in a json form
  return u.to_json()


@app.route("/login",methods=["POST"])
def post_login ():
  email = request.args["email"]
  password=request.args["password"]
  u = User.objects(email=email,password=password).first()
  if u==None :
    raise
  else:
    session["uid"]=str(u.id)
    return u.to_json()

@app.route("/login")
def get_login ():
    return render_template('login.html')

@app.route("/questions/<qid>",methods=["GET"])
def get_questions (qid):
  q=Question.objects(id=qid).first()
  if q==None:
    raise
  else:
    return  render_template("question.html" ,question=q)

@app.route("/get_new_question")
def get_new_question():
  attempts = Attempt.objects(user=current_user())
  qids = list(map(lambda a: a.question.id, attempts))
  question = Question.objects(id__nin=qids).first()
  return render_template("question.html",question=question)


@app.route("/add_question",methods=["POST"])
def add_question ():
  text = request.args["text"]
  options=request.args.getlist("options")
  answer=int(request.args["answer"])
  q=Question(text=text ,options=options,answer=answer)
  q.save()
  return q.to_json()


@app.route("/questions/<qid>/attempt",methods=["POST"])
def attempt (qid):
  given_answer=request.args["given_answer"]
  u=current_user()
  q=Question.objects(id=qid).first()
  a=Attempt(user=u,question=q,given_answer=given_answer)
  a.save()
  given_answer=a.given_answer
  answer=q.answer
  correct=given_answer==answer
  result={"answer":answer,"given_answer":given_answer,"correct":correct}
  return jsonify(result)

@app.route("/questions/attempted")
def get_attempted_questions ():
  u = current_user()
  if u == None:
    raise
  else:
    list_of_attempts=Attempt.objects(user=u)    
    return render_template("attempts.html",attempts=list_of_attempts) 


  
@app.route("/debug")
def debug():
  raise

@app.route("/check_logined_user")
def check_logined_user():
  return current_user().name




###### HELPER FUNCTIONS #######


# if user is logged in ,return user object otherwise ,return None
def current_user():
  uid=session.get("uid")
  if uid==None :
    return None
  else:
    a=User.objects(id=uid).first()
    return a



# converts the byte data into a dictionary 
def bytes_to_dict(byte_data):
  data_as_dict = json.loads(byte_data.decode('utf-8'))
  return data_as_dict

# helper function to test data
def log(data, message="TESTING"):
  app.logger.info(message)
  app.logger.info(data)
