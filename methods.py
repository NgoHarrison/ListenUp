from models import User, Thread, Article
import hashlib, uuid
import ast

# Here we implement some backend methods

# to-do: add salts, id values
login_worked = lambda user, pwd: hashlib.sha512(User.objects(username=user).password)==hashlib.sha512(pwd)
create_thread = lambda user, title: Thread(author=user, question=title).save()
add_argument = lambda user, text:  Argument(author=user, content=text).save()
create_user = lambda user, pwd, email: User(username=user, password=hashlib.sha512(pwd), address=email).save() 


def vote(user, arg_id, up_down):
	 n = ast.literal_eval(Argument.objects(id=arg_id).voting_record)[arg_id]=up_down
	 Argument.objects(arg_id).voting_record= str(n)

         # For each user, their voting record is represented as a dictionary, with each argument id
         # as a key and {-1, 0, 1} as a value

