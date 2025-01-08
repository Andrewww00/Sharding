from database import *
from getpass import getpass

class Login:
    def execute():
        isNotLogged = True
        while isNotLogged:
            username = str(input("Username: "))
            password = str(getpass("Password: "))
            userid = Database.login(username, password)

            if userid:
                print(f"\n>> Benvenuto {username}\n")
                isNotLogged = False
                return userid
            else:
                print("\n>> Login fallito\n")


    """
    def register():
        username = str(input("Username: "))
        password = str(getpass("Password: "))
        Database.register(username, password)
    """
