from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
import datetime


# venv\Scripts\activate
load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://pau_mateu:{password}@cluster0.wo7p07a.mongodb.net/?retryWrites=true&w=majority"                
client = MongoClient(connection_string)
printer = pprint.PrettyPrinter()

# DB selector
class Database():
    def __init__(self):
        self.Db = client.MiniSocialMedia
        



class UserConnection(Database):
    def __init__(self):
        super().__init__()
        self.user_collection = self.Db.Users

    # Read a user field
    def readUserInfo(self, ID_user=None, username=None, withoutID = False):
        from bson.objectid import ObjectId
        if username is None:
            _id = ObjectId(ID_user)
        else:
            _id = ObjectId(self.getIdFromUser(username))

        if withoutID == False:
            return self.user_collection.find_one({"_id": _id})
        else:
            return self.user_collection.find_one({"_id": _id},{'_id':0})

    # Add new user into User collection
    def addNewUser(self, username, password, email, age, phone):
        user_data = {
            "Username": username,
            "Password": password,
            "email": email,
            "others": {
                "age": age,
                "phone": phone
            }
        }

        self.user_collection.insert_one(user_data)

    # Delete a user field
    def deleteUser(self, user_id):
        from bson.objectid import ObjectId
        _id = ObjectId(user_id)

        self.user_collection.delete_one({'_id':_id})

    

    # Get ID from a username
    def getIdFromUser(self, username):
        id = None
        MyUser =  self.user_collection.find_one({'Username':username})
        id = MyUser['_id']

        return id

    # Get all data from
    def getDataFromID(self, user_id):
        from bson.objectid import ObjectId
        _id = ObjectId(user_id)

        return self.user_collection.find_one({'_id':_id}, {'_id':False})


class PostsConnection(Database):
    def __init__(self):
        super().__init__()
        self.post_collection = self.Db.Posts

    def read_10_posts(self):
        cursor = self.post_collection.find().sort('Date', -1).limit(10)
        Last_10_posts = [post for post in cursor]

        return Last_10_posts

    # Create a new post
    def public_post(self,User_id,Name, Description, Category = []):
        post = {
        "ID_USER": User_id,
        "Header": Name,
        "Content": Description,
        "Date": datetime.datetime.now(),
        "Category": []
        }
        
        self.post_collection.insert_one(post)

    # Read user posts
    def readUserPosts(self,user_id):
        user_posts = []
        from bson.objectid import ObjectId
        _id = ObjectId(user_id)

        posts = self.post_collection.find({'_id':_id})
        user_posts = [post for post in reversed(posts)]
        
        return user_posts

class ListsConnection(Database):
    def __init__(self):
        super().__init__()
        self.List_collection = self.Db.Lists

    # Create a new list
    def create_list(self, Name, Description):
        new_list = {
            "Name": Name,
            "Description": Description,
            "participants": []
        }

        self.List_collection.insert_one(new_list)

    # Add a new user on the list
    def addNewUser(self, list_id,user_id):
        from bson.objectid import ObjectId
        _id = ObjectId(list_id)

        # Update the document with the new item in the array
        self.List_collection.insert_one(
            {'_id':_id},
            {'$push':{'description':user_id}}
        )


    # Read all IDs from the list
    def read_IDs_from_post(self, post_id):
        from bson.objectid import ObjectId
        _id = ObjectId(post_id)

        posts = self.List_collection.find({'_id':_id})
        post_ids = [post.get('IDs', []) for post in posts]

        return post_ids

    

if __name__ == '__main__':
    MyUserConection = UserConnection()
    # MyUserConection.addNewUser("Pepino","1234567","pepino@gmail.com",18,"640523319")

    pprint.pprint(MyUserConection.getDataFromID('6489bed5de667e2705ba19c9'))

    
