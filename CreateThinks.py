from dotenv import load_dotenv
import os
import pprint
import datetime
from pymongo import MongoClient
from DatabaseConection import *

# venv\Scripts\activate
load_dotenv()
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://pau_mateu:{password}@cluster0.wo7p07a.mongodb.net/?retryWrites=true&w=majority"                
client = MongoClient(connection_string)
printer = pprint.PrettyPrinter()

# Select collections
Db = client.MiniSocialMedia
userCollection = Db.Users
postCollection = Db.Posts
ListCollection = Db.Lists
print(ListCollection)

# Validations -->
user_validator = {
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["Username", "Password", "email", "others"],
    "properties": {
      "Username": {
        "bsonType": "string",
        "maxLength": 25,
        "description": "Must be a string with a maximum length of 25 characters"
      },
      "Password": {
        "bsonType": "string",
        "minLength": 1,
        "description": "Must be a non-empty string"
      },
      "email": {
        "bsonType": "string",
        "minLength": 1,
        "description": "Must be a non-empty string"
      },
      "others": {
        "bsonType": "object",
        "required": ["age", "phone"],
        "properties": {
          "age": {
            "bsonType": "int",
            "maximum": 100,
            "description": "Must be an integer with a maximum value of 100"
          },
          "phone": {
            "bsonType": "string",
            "minLength": 9,
            "maxLength": 9,
            "description": "Must be a string with a length of 9 characters"
          }
        }
      }
    }
  }
}

post_validator = {
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["ID_USER", "Header", "Content","Date", "Category"],
    "properties": {
      "ID_USER": {
        "bsonType": "int",
        "description": "ID of the user who created the post"
      },
      "Header": {
        "bsonType": "string",
        "description": "Title or header of the post"
      },
      "Content": {
        "bsonType": "string",
        "description": "Content of the post"
      },
      "Date": {
          "bsonType": "date",
          "description":"Must be a date and is required"
      },
      "Category": {
        "bsonType": "array",
        "description": "Categories associated with the post",
        "items": {
          "bsonType": "string"
        }
      }
    }
  }
}




def createUserValidation():
    # Create User Validation
  try:
      Db.create_collection("Users")
  except Exception as e:
      print(e)

  Db.command("collMod", "Users", validator=user_validator)



def createPostValidation():
    # Create Posts Validation
  try:
      Db.create_collection("Lists")
  except Exception as e:
      print(e)

  Db.command("collMod", "Lists", validator=post_validator)
   

def createListValidation():
      # Create List Validation
  list_validator = {
      "$jsonSchema": {
        "bsonType": "object",
        "required": ["Name", "Description", "participants"],
        "properties": {
          "Name": {
            "bsonType": "string",
            "description": "Name of the list"
          },
          "Description": {
            "bsonType": "string",
            "description": "Description of the list"
          },
          "participants": {
            "bsonType": "array",
            "description": "Participants associated with the list",
            "items": {
              "bsonType": "int32"
            }
          }
        }
      }
  }


  try:
      Db.create_collection("Lists")
  except Exception as e:
      print(e)

  Db.command("collMod", "Lists", validator=list_validator)
if __name__ == '__main__':
    #createListValidation()
    #createPostValidation()
    #createUserValidation()

  # MyPostConection = PostsConnection()
  # MyPostConection.public_post("6485e150edc5338001d2b67c", "Hey guys, big gay","Hello guys this is just a test to try my program and seee if it works!" )
  MyUserConection = UserConnection()
  MyUserConection.addNewUser("aSteve_","123qweasd", "paumat17@gmail.com",22,"629620022")
  MyUserConection.addNewUser("raul123","123qweasd", "aldeloya121@gmail.com",25,"687368372")
  MyUserConection.addNewUser("ivan321_","123qweasd", "ivanero3221@gmail.com",19,"629021029")
  MyUserConection.addNewUser("Susanero023","123qweasd", "susanerista@gmail.com",17,"635329382")
  MyUserConection.addNewUser("carlassx26","123qweasd", "holacarla@gmail.com",22,"629620022")

