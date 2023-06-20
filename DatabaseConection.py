from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
import datetime


# venv\Scripts\activate
load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://pau_mateu:{password}@cluster0.wo7p07a.mongodb.net/?retryWrites=true&w=majority"                
printer = pprint.PrettyPrinter()

# Database class to conect MongoClient
class Database():
    def __init__(self):
        self.client = MongoClient(connection_string)
        self.Db = self.client.MiniSocialMedia

##########################################################################################
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
    
    # Return a list of user names
    def showUserNames(self) -> list():
        users = self.user_collection.find({})
        return [user['Username'] for user in users]

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
    def readUserPosts(self, user_id):
        posts = self.post_collection.find({'ID_USER': str(user_id)}).sort('Date', -1)
        user_posts = [post for post in posts]
        
        return user_posts

class ListsConnection(Database):
    def __init__(self):
        super().__init__()
        self.List_collection = self.Db.Lists

    # Create a new list
    def create_list(self, Name, Description, user_id):
        new_list = {
            "owner_id": str(user_id),
            "Name": Name,
            "Description": Description,
            "participants": []
        }

        result = self.List_collection.insert_one(new_list)

        return result.inserted_id

    # Add a new user on the list
    def addNewUser(self, list_id,user_id):
        from bson.objectid import ObjectId
        _id = ObjectId(list_id)

        # Update the document with the new item in the array
        self.List_collection.update_one(
            {'_id':_id},
            {"$push": {"participants":str(user_id)}}
        )


    # Read all IDs from the list
    def read_IDs_from_post(self, post_id):
        from bson.objectid import ObjectId
        _id = ObjectId(post_id)

        posts = self.List_collection.find({'_id':_id})
        post_ids = [post.get('IDs', []) for post in posts]

        return post_ids
    
    # Read list with owner_id
    def readListsFromID(self, user_id):
        lists = self.List_collection.find({'owner_id':user_id})
        list_data = [list for list in lists]

        return list_data

    # Get ID of List name
    def getListID(self, name):
        lists = self.List_collection.find_one({'Name': name})

        return lists['_id']

    def getDataFromID(self, list_id):
        from bson.objectid import ObjectId
        _id = ObjectId(list_id)

        list_data = self.List_collection.find_one({'_id':_id})
        return list_data


if __name__ == '__main__':
    os.system('cls')
    MyUserConection = UserConnection()
    MyPostConection = PostsConnection()
    # MyUserConection.addNewUser("Pepino","1234567","pepino@gmail.com",18,"640523319")

    print(MyUserConection.showUserNames())

    
