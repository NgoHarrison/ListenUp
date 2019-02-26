from firebase_orm import models

# An argument with no subargument will contain the Thread id for its parent id
class Argument(models.Models):
	parent_id = models.TextField()
        id = models.TextField()
	contents = models.TextField()
	authorship = models.TextField()
	vote_score = models.TextField()

class User(models.Models):
	username = models.TextField()
	id = models.TextField()
	hashed_pass = models.TextField()
	vote_record = models.TextField()

# A thread holds arguments
class Thread(models.Models):
	id = models.TextField()
	question = models.TextField()
	author = models.TextField()
