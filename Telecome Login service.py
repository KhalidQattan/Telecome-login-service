import time
import sys
import os
import getpass
import pandas as pd
import hashlib
import hmac


def Clear_OutPut():
    os.system("cls" if os.name == "nt" else "clear") 

def hash_password(password):
    salt = os.urandom(16).hex()
    mixed = salt + password
    hashed = hashlib.sha3_256(mixed.encode()).hexdigest()
    return salt + ":" + hashed

def verify_password(password , stored):
    salt, old_hash = stored.split(":")
    mixed = salt + password
    new_hashed = hashlib.sha3_256(mixed.encode()).hexdigest()
    return hmac.compare_digest( new_hashed , old_hash )



if os.path.exists("Accounts_DataFrame.csv"): 
    Accounts_Frame = pd.read_csv("Accounts_DataFrame.csv" , dtype = str)
else:
    Accounts_Frame = pd.DataFrame(columns = [ "phone_numbers" , "password_accounts" ])


Clear_OutPut()

attempt = 0

print("================ Welcome To  MTN Services ================\n")


while True:

    print("\n                Please select a sign-in method. \n \n")
    print("               1-  Login / Start \n")
    print("                2-  Register / Create an account. \n ")

    answer_account = input("\n")

    if answer_account == "2":

        Clear_OutPut()

        while True:

            print("\n Please Enter Your Phone Number: 09xxxxxxxx  ")

            New_PhoneNumber = input("\n")

            if (
                len(New_PhoneNumber) == 10
                and New_PhoneNumber.isdigit() 
                and New_PhoneNumber.startswith("09")
            ):
                if New_PhoneNumber in Accounts_Frame["phone_numbers"].values:
                    print("\n This number is already registered.\n")
                    time.sleep(2)
                    Clear_OutPut()
                    continue
                break
            else:
                print("\n Please Enter Valid number after 3 sec..\n")
                time.sleep(3)
                Clear_OutPut() 

        
        while True:

            print("\n Please Enter Your Password.. [ For Your Security We Hid the password !! ] \n ")
            New_Password = getpass.getpass("\n")

            if ( len(New_Password) >= 7
                and New_Password.isalnum()
                and not New_Password.isalpha()
                and not New_Password.isdigit() ):
                pass

            else:
                print("\n Make Your Password Stronger.. [ Password must be at least 7 characters long and contain both letters and numbers. ] \n")
                time.sleep(3)
                Clear_OutPut()
                continue
            
             
            print("\n Please rewrite The Password again to make sure.. \n")
            
            ToMakeSure = getpass.getpass("\n")

            if ToMakeSure == New_Password:
                break

            print("\n password are not match !")
            time.sleep(2.5)
            Clear_OutPut()

        new_account_row = pd.DataFrame([{
            "phone_numbers": New_PhoneNumber,
            "password_accounts": hash_password(New_Password)}]) 

        Accounts_Frame = pd.concat([Accounts_Frame , new_account_row] , ignore_index = True)
        Accounts_Frame.to_csv("Accounts_DataFrame.csv" , index = False)

        print("\n The account is being created..\n ", end="")
        for x in range(4):
            time.sleep(1.5)
            sys.stdout.write(".")
            sys.stdout.flush()

        print("\n\n Account created and saved.\n")
        time.sleep(2)
        Clear_OutPut()

    elif answer_account == "1": 

        Clear_OutPut()

        login_phone = input("\n Please Enter Your Phone Number: 09xxxxxxxx  \n")
        time.sleep(1)
        login_password = getpass.getpass("\n Please Enter Your Password.. [ For Your Security We Hid the password !! ] \n")

        login_ok = False

        found = Accounts_Frame[Accounts_Frame["phone_numbers"] == login_phone]

        if not found.empty:
            stored = found.iloc[0]["password_accounts"]
            login_ok = verify_password(login_password , stored)
        
        if login_ok:
            for x in range(5):
                time.sleep(1.5)
                sys.stdout.write(".")
                sys.stdout.flush()
            print(" \n Authentication Successful.. \n") 
            time.sleep(3)
            break
        else:
            attempt += 1
            if attempt == 3:
                print("\n You Exceed Your limit You have to wait 15 sec..\n")
                for x in range(15):
                    time.sleep(1)
                    sys.stdout.write("=")
                    sys.stdout.flush()
                attempt = 0
                Clear_OutPut()
            else:
                print(f"\n invalid phone number or password {3 - attempt} attempts left !! ")
                time.sleep(3)
                Clear_OutPut()
        
    else:
        Clear_OutPut()
        print("Please Choose One of the Options... ")
        time.sleep(2)
        Clear_OutPut()



while True: # -------------------------------------------------------------- starting the main program after the user has logged in successfully coming soon
    break
