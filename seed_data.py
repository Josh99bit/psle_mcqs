from mongoengine import *
from app import User, Question, Attempt

connect('psle_test')

# remove ALL the users in the database
User.drop_collection()
Question.drop_collection()
Attempt.drop_collection()

# create users
u1 = User(name="Joshua",email="joshua@gmail.com" ,password="cowhead")
u1.save()
u2 = User(name="Isaac",email="isaac@gmail.com" ,password="cow")
u2.save()
u3 = User(name="Cow",email="cow@gmail.com" ,password="milk")
u3.save()
u4 = User(name="moo",email="moo@gmail.com" ,password="head")
u4.save()
# # create questions
q1 = Question(text="Joshua went the the market to buy ___head biscuits",options=["went","arrow","sheep","cow"],answer=4,credit="oxcow university")
q1.save()
q2 = Question(text="Joshua and Isaac were eating ___head biscuits ",options=["cow","arrow","went","sheep"],answer=1,credit="cowbridge university")
q2.save()
q3 = Question(text="Isaac exclamed that ___head biscuits were his favourite",options=["went","arrow","cow","sheep"],answer=3,credit="cowbridge university")
q3.save()
q4 = Question(text="Cows are the key to ___head biscuits ",options=["went","arrow","cow","sheep"],answer=3,credit="cowvord university")
q4.save()
#create attempts
a1=Attempt(user=u4,question=q4 , given_answer=3)
a1.save()
a2=Attempt(user=u1,question=q1 , given_answer=4)
a2.save()
a3=Attempt(user=u3,question=q3 , given_answer=2)
a3.save()
a4=Attempt(user=u2,question=q3 , given_answer=3)
a4.save()
a5=Attempt(user=u1,question=q2 , given_answer=3)
a5.save()