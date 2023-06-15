import re
import datetime
import random
import pprint
from datetime import datetime as dt
#venv\Scripts\activate

# Import database conection
from DatabaseConection import  *

admin_user = "Palolo"
admin_password = "12345"
MyUserConection = UserConnection()
MyPostConection = PostsConnection()

#################################################################
# Main things and important methods

# Select user or admin
def select_acount():
    while True:
        print("------------------------------------------------")
        print("What would you like to do? (Admin/User):")
        print("If you want to close the aplication text 's'")
        option = input(": ").lower()
        if option == 'admin' or option == 'a':
            return 'admin'
        elif option == 'user' or option == 'u':
            return 'user'
        elif option == 's':
            return 'exit'
        else:
            print("Choose a correct option!")

def type_program():
    account = select_acount()
    if account == 'admin':
        if adminLog() == True:
            return 'admin'
    elif account == 'user':
            return 'user'
    elif account == 'exit':
            return 's'
    else:
        print("You haven't selected a correct option!")



#################################################################
# Admin mode and its methods

def adminLog():
    print("Type username:")
    AUsername = input(": ")
    if AUsername == admin_user:
        print("Type password:")
        APasowrd = input(": ")
        if APasowrd == admin_password:
            print("You've logged in as an admin!")
            return True
    print("Something worng!")
    return False

def printAdminModeOption():
    print("1- ")
    print("2- ")
    print("3- ")
    print("4- ")
    print("5- ")


def adminMode():
    print("-----------------------------------------")
    print("You are in admin mode!")

    while True:
        pass

#################################################################
# User mode and its methods

def printUserModeOption(user):
    print(f"\nHello {user} select a correct option:")
    print("1- See last 10 posts published")
    print("2- Publish a new post")
    print("3- See all my posts")
    print("4- Create a new list")
    print("5- See all posts from specific list")
    print("6- Exit")

# This function is for login. In case the user doenen't work, will be redirect in main panel.
def user_login():
    print("Type your user name:")
    user_name = input(": ")
    try:
        if MyUserConection.readUserInfo(username=user_name)['Username'] == user_name:
            print("Type your password:")
            user_pass = input(": ")
            if MyUserConection.readUserInfo(username=user_name)['Password'] == user_pass:
                return user_name, MyUserConection.readUserInfo(username=user_name)['_id']
    except TypeError:
        print("Something worng!")
        return False, False

# Read 10 last post 
def seeLast10Posts():
    posts = MyPostConection.read_10_posts()
    
    for post in posts[::-1]:
        print(f"-------------------{MyUserConection.getDataFromID(post['ID_USER'])['Username']}:")
        print(f"Title:{post['Header']}")
        print(f"Content:{post['Content']}")
        print("--------------------------\n")

# Read user posts
def readUserPosts(user_id):
    posts = MyPostConection.readUserPosts(user_id)
    for post in posts:
        print(f"-------------------{MyUserConection.getDataFromID(post['ID_USER'])['Username']}:")
        print(f"Title:{post['Header']}")
        print(f"Content:{post['Content']}")
        print("--------------------------\n")

# Create new post
def createNewPost(user, user_id):
    print("\n-------------------------------------")
    print("Create new post!\n")
    
    title = input(f"First, {user}, introduce the title: ")
    content = input("Type the content: ")
   
    MyPostConection.public_post(str(user_id), title, content)
    
    print("Post published!")

# Create a new post, the user can select users, and see them
def createNewList():
    print("Type post's name")
    Name = input(": ")

    print("Type a description")
    Description = input(": ")

    




# Main while user mode and inculde its metohds
def userMode():
    insideLoop = True
    print("-----------------------------------------")
    print("You are in user mode!")    

    user,user_id = user_login()
    # MyPostConection.setUSerId(user_id) # Set the user id in the class

    while user:
        printUserModeOption(user)
        option = input(": ")

        # See last 10 posts
        if option == '1':
            seeLast10Posts()

        # Createa new post
        elif option == '2':
            createNewPost(user,str(user_id))

        # See user posts
        elif option == '3':
            readUserPosts(user_id)

        # Create new list
        elif option == '4':
            createNewList(user_id)

        elif option == '5':
            pass
        elif option == '6':
            break
        else:
            print("Choose a correct option!")









if __name__ == '__main__':
    while True:
        type_program_ = type_program()
        if type_program_ == 's':
            break
        elif type_program_ == 'user':
            userMode()
        elif type_program_ == 'admin':
            adminMode()

