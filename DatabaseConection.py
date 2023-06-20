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
        """
        
        """
        self._client = MongoClient(connection_string)
        self._Db = self._client.MiniSocialMedia

##########################################################################################
# User collection conection class
class UserConnection(Database):
    def __init__(self):
        super().__init__()
        self._user_collection = self._Db.Users

    def readUserInfo(self, ID_user=None, username=None, withoutID = False):
        """Read user collection depending of ID or username"""
        from bson.objectid import ObjectId
        if username is None:
            _id = ObjectId(ID_user)
        else:
            _id = ObjectId(self.getIdFromUser(username))

        if withoutID == False:
            return self._user_collection.find_one({"_id": _id})
        else:
            return self._user_collection.find_one({"_id": _id},{'_id':0})

    def addNewUser(self, username, password, email, age, phone):
        """Add a new user collection in _user_collection"""
        user_data = {
            "Username": username,
            "Password": password,
            "email": email,
            "others": {
                "age": age,
                "phone": phone
            }
        }

        self._user_collection.insert_one(user_data)

    def deleteUser(self, user_id):
        """Delete user collection with their ID"""
        from bson.objectid import ObjectId
        _id = ObjectId(user_id)

        self._user_collection.delete_one({'_id':_id})
    
    def showUserNames(self) -> list():
        """Return a list of usernames of _user_collection"""
        users = self._user_collection.find({})
        return [user['Username'] for user in users]

    @property
    def getIdFromUser(self, username):
        """Get username id with their name"""
        MyUser =  self._user_collection.find_one({'Username':username})
        return MyUser['_id']

    @property
    def getDataFromID(self, user_id):
        """Get user collection data from user_id"""
        from bson.objectid import ObjectId
        _id = ObjectId(user_id)

        return self._user_collection.find_one({'_id':_id}, {'_id':False})

# Posts collection conection class
class PostsConnection(Database):
    def __init__(self):
        super().__init__()
        self._post_collection = self._Db.Posts

    def read_10_posts(self):
        """Read last 10 posts"""
        cursor = self._post_collection.find().sort('Date', -1).limit(10)
        Last_10_posts = [post for post in cursor]

        return Last_10_posts

    def public_post(self,User_id,Name, Description, Category = []):
        """Create a new collection about posts"""
        post = {
        "ID_USER": User_id,
        "Header": Name,
        "Content": Description,
        "Date": datetime.datetime.now(),
        "Category": []
        }
        
        self._post_collection.insert_one(post)

    def readUserPosts(self, user_id):
        """Return a list of user posts in a list"""
        posts = self._post_collection.find({'ID_USER': str(user_id)}).sort('Date', -1)
        user_posts = [post for post in posts]
        
        return user_posts

# Lists collection conection class
class ListsConnection(Database):
    def __init__(self):
        super().__init__()
        self._List_collection = self._Db.Lists

    def create_list(self, Name, Description, user_id):
        """Create a new list in the Lists collection"""
        new_list = {
            "owner_id": str(user_id),
            "Name": Name,
            "Description": Description,
            "participants": []
        }

        result = self._List_collection.insert_one(new_list)

        return result.inserted_id

    def addNewUser(self, list_id,user_id):
        """Add a new user to the list"""
        from bson.objectid import ObjectId
        _id = ObjectId(list_id)

        self._List_collection.update_one(
            {'_id':_id},
            {"$push": {"participants":str(user_id)}}
        )

    def read_IDs_from_post(self, post_id):
        """Read all ID from post"""
        from bson.objectid import ObjectId
        _id = ObjectId(post_id)

        posts = self.__List_collection.find({'_id':_id})
        post_ids = [post.get('IDs', []) for post in posts]

        return post_ids
    
    def readListsFromID(self, user_id):
        """Read list with owner_id"""
        lists = self._List_collection.find({'owner_id':user_id})
        list_data = [list for list in lists]

        return list_data

    @property
    def getListID(self, name):
        """Get ID from List ID"""
        lists = self._List_collection.find_one({'Name': name})

        return lists['_id']
    
    @property
    def getDataFromID(self, list_id):
        """Get all list data from ID"""
        from bson.objectid import ObjectId
        _id = ObjectId(list_id)

        list_data = self.__List_collection.find_one({'_id':_id})
        return list_data


if __name__ == '__main__':
    os.system('cls')
    MyUserConection = UserConnection()
    MyPostConection = PostsConnection()
    # MyUserConection.addNewUser("Pepino","1234567","pepino@gmail.com",18,"640523319")

    print(MyUserConection.showUserNames())

    
