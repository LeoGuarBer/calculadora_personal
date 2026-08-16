import pandas as pd
import os 
import re

#User class 
class User:
    def __init__(self,username,email,__password):
        self.username = username
        self._email = email
        self.__password =__password
       
    @property 
    def password (self):
        return self.__password
    
    @password.setter
    def password (self,password):
        self.__password = password
    
#User manager class
class UserManager:
    def __init__(self,file):
        self.file = file
        self.data_base = pd.read_csv(file)
        
    def add_user(self,user):
        new_user = pd.DataFrame([{
            "usernames": user.username,
            "emails": user._email,
            "passwords": user.password
        }])
        
        self.data_base = pd.concat([self.data_base,new_user], ignore_index=True)
        
        self.data_base.to_csv(self.file,index=False)

#Sign up manager class
class SignUpManager:
    def __init__(self,user,file):
        self.user = user
        self.data_base = pd.read_csv(file)
    
    def username_verification(self):
        return re.fullmatch(r"[a-zA-Z]+(?: [a-zA-Z]+)*",self.user.username)
    
    def email_verification(self):
        return re.fullmatch(r"[0-9a-zA-Z._%+-]+@[a-zA-Z.-]+\.[a-zA-Z]{2,}",self.user._email)
    
    def avoid_duplicate_accounts(self):
        for email in self.data_base['emails']:
            if self.user._email == email:
                return False
        else:
            return True
    
    def password_verification(self):
        return re.fullmatch (r"[0-9a-zA-Z!¡¿?#$%&/=+.-]{8,}",self.user.password)
    
class LogInManager:
    def __init__(self,user,file):
        self.user = user
        self.data_base = pd.read_csv(file)
        
    def search_email(self):
        for i,email in enumerate(self.data_base['emails']):
            if email == self.user._email:
                return i
        else:
            return None
    
    def search_password(self,i):
        if self.user.password == self.data_base.loc[i,'passwords']:
            return True
        else:
            return False
        
    def search_username(self,i):
        return self.data_base.loc[i,'usernames']
  
      
#Sign up function
def sign_up():
    while True:
        os.system('clear')
        
        print ("Personal Calculator")
        print ("="*36)
        
        username = input("\n\nPut your name:  ")
        email = input ("Put your email:  ")
        password = input ("Put your password:  ")
        user = User(username,email,password)
        manager = SignUpManager(user,"data_base/accounts.csv")
        
        username_verification = manager.username_verification()
        email_verification = manager.email_verification()
        avoid_duplicate_accounts = manager.avoid_duplicate_accounts()
        password_verification = manager.password_verification()
        
        if not username_verification:
            print ("User name isn't valid, try again")   
            os.system('read')
        elif not email_verification:
            print ("The emial isn't valid, try again")
            os.system('read')
        elif not avoid_duplicate_accounts:
            print ("This email already has an account")
            os.system('read')
        elif not password_verification:
            print ("The password isn't valid, try again")
            os.system('read')
        else:
            manager = UserManager("data_base/accounts.csv")
            manager.add_user(user)
            print ("Your account has been created succesfully, try logging in")
            os.system('read')
            break   
                  
def log_in():
    while True:
        os.system('clear')      
        print ("Personal Calculator")
        print ("="*36)
        
        email = input ("\n\nPut your email:  ")
        password = input ("Put your password:  ")
         
        user = User(" ",email,password)
        manager = LogInManager(user,"data_base/accounts.csv")
        
        email_found = manager.search_email()
        if type(email_found) != int :
            print ("The email what you wrote doesn't have a registered account")
            os.system('read')
            continue
        else: 
            password_found = manager.search_password(email_found)
        
        if password_found:
            username = manager.search_username(email_found)
            user = User (username,email,password)
            print (f"Hi, {username}")
            os.system('read')
            break
        else:
            print ("The password isn't correct, try again")
            os.system('read')
