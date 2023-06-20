import re
import datetime
import random
import time
import os 
from datetime import datetime as dt
#venv\Scripts\activate

# Import database conection
from DatabaseConection import  *

admin_user = "Palolo"
admin_password = "12345"
MyUserConection = UserConnection()
MyPostConection = PostsConnection()
MyListConection = ListsConnection()

os.system('cls')

#################################################################
# Main things and important methods
def extract_date_time(string):
    date, time = string.split(' ')
    date = date.split('-')
    formatted_date = '{}/{}/{}'.format(date[2], date[1], date[0])
    time = time.split(':')
    formatted_time = '{}:{}'.format(time[0], time[1])
    return formatted_date, formatted_time


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
    print("6- Modify user post")
    print("7- Exit")

# This function is for login. In case the user doenen't work, will be redirect in main panel.
def user_login():
    print("Type your user name:")
    user_name = input(": ")
    try:
        if MyUserConection.readUserInfo(username=user_name)['Username'] == user_name:
            print("Type your password:")
            user_pass = input(": ")
            try:
                if MyUserConection.readUserInfo(username=user_name)['Password'] == user_pass:
                    return user_name, MyUserConection.readUserInfo(username=user_name)['_id']
            except TypeError:
                print("The password is not correct!")
                return False, False
    except TypeError:
        print("User not correct!")
        return False, False

# Read 10 last post 
def seeLast10Posts():
    posts = MyPostConection.read_10_posts()
    
    for post in posts[::-1]:
        date,time = extract_date_time(str(post['Date']))
        print(f"--------------------------{MyUserConection.getDataFromID(post['ID_USER'])['Username']}:")
        print(f"Title: {post['Header']}")
        print(f"Content: {post['Content']}")
        print(f"-----------------{date} at {time}------------\n")

# Read user posts
def readUserPosts(user_id):
    posts = MyPostConection.readUserPosts(user_id)
   
    if posts is not None:
        for post in posts[::-1]:
            date,time = extract_date_time(str(post['Date']))
            print(f"--------------------------{MyUserConection.getDataFromID(post['ID_USER'])['Username']}:")
            print(f"Title: {post['Header']}")
            print(f"Content: {post['Content']}")
            print(f"-----------------{date} at {time}------------\n")
    else:
        print("You have not created any post!\n")
        
# Create new post
def createNewPost(user, user_id):
    print("\n-------------------------------------")
    print("Create new post!\n")
    
    title = input(f"First, {user}, introduce the title: ")
    content = input("Type the content: ")
   
    MyPostConection.public_post(str(user_id), title, content)
    
    print("Post published!")

# Create a new post, the user can select users, and see them
def createNewList(user_id):
    print(f"Ok {MyUserConection.getDataFromID(user_id)['Username']}, you have to introduce the post name, a description and select the users")
    print("Type post name")
    Name = input(": ")

    # Prompt for the description
    print("Type a description:")
    Description = input(": ")

    # Create a new list with the provided name and description
    post_id = MyListConection.create_list(Name, Description, user_id)

    # Retrieve a list of user names
    Users = MyUserConection.showUserNames()
    try:
        for user in Users:
            print(user, end=" - ")

        # Prompt the user to enter a user name
        user_selected_id = MyUserConection.getIdFromUser(input("\nText user name: "))
        MyListConection.addNewUser(post_id,user_selected_id)
        while True:    
            # Ask the user if they want to add another user to the list
            if not input("Would you like add another user in the list?(Y/N)").lower() == "y":
                break  
            
            for user in Users:
                print(user, end=" - ")        

            user_selected_id = MyUserConection.getIdFromUser(input("\nText user name: "))
            MyListConection.addNewUser(post_id,user_selected_id)
            
          
    except TypeError:
        print("Selet a correct user!")

# See users in the potcasts
def seeListUser(user_id):
    members = []
    print("Select your Post:")
    MyLists = MyListConection.readListsFromID(user_id)

    for i in MyLists:
        print(f"- {i['Name']}")
    try:
        # I identificate the id and then i try to get the data.
        list_selected_id = MyListConection.getListID(input("\nIntroduce the name of the List: "))
        data_selected = MyListConection.getDataFromID(list_selected_id)

        # Print the Name, descriptions and its members
        print("--------------------------------------------------")
        print(f"{data_selected['Name']}")
        print(f"{data_selected['Description']}")
        print("\nList members:")
        for member_id in data_selected['participants']:
            print(f"- {MyUserConection.getDataFromID(member_id)['Username']}")
            members.append(MyUserConection.getDataFromID(member_id)['Username'])
        time.sleep(1)

        # I ask if he wants to see the members posts
        print(f"\nWould you like to see {', '.join(members)}'s posts? (y/n)")
        if input("> ").lower() == 'y':
            while True:
                for user_id in data_selected['participants']:
                    print(f"{MyUserConection.getDataFromID(user_id)['Username'].title()}'s posts:")
                    readUserPosts(user_id)
                break
        else:
            print("OK")

        print("--------------------------------------------------")

    except TypeError:
        print("Select a correct post!")



# Main while user mode and inculde its metohds
def userMode():
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

        # See posts from list
        elif option == '5':
            seeListUser(str(user_id))

        # Modify the members of a group
        elif option == '6':
            pass

        elif option == '7':
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

