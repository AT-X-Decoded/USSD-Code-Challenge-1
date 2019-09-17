from flask import Flask,render_template,request
import africastalking
import os
import re
site     = Flask(__name__)
response = "" 
userEmail = ""
userName  = ""
isEmail    = False #checking if email was provided
isUserName = False #checking if username was provided
isStarted  = False #checking if the app is just starting

def sendSMS(phoneNumber):
    userName = "sandbox"
    apiKey = os.environ['API_KEY']
    africastalking.initialize(userName,apiKey)
    sms = africastalking.SMS

    response = sms.send(f"Welcome to the platform!\nRegistration details: Username:{userName} Email:{userEmail}",[phoneNumber])

# Landing page for the site
@site.route('/')
def home():
    return render_template('index.html')  

# Implementing the ussd functionality
@site.route('/app/ussd',methods=['POST','GET'])
def ussdCallback():
    global isStarted
    global response
    global userEmail
    global userName
    global isEmail
    global isUserName
    #regex corner
    userNameRegex = '^[a-zA-Z]+[a-zA-Z0-9._-]{3,8}$'
    emailRegex = '^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$'
    emailCheck = re.compile(emailRegex)
    userNameCheck = re.compile(userNameRegex)
    # getting operation data for the app
    sessionId = request.values.get("sessionId", None)
    serviceCode = request.values.get("serviceCode", None)
    phoneNumber = request.values.get("phoneNumber", None)
    userResp = request.values.get("text", "default")
    #split the user input using * to get the last input from the user
    userResp = userResp.split('*')[-1]
    if userResp == "":
        if isStarted:
            #if the user sent an empty string when the app is up and running
            response = "END ERROR\nYou provided no input\n"
            isStarted = False  
        elif isStarted==False:   
            #if the user is starting the app    
            response = "CON What would you like us to call you:\n"
            response += "Guideline (4-8) characters\n"
            isStarted = True
            isUserName = True #time of obtaining the username
    elif isUserName:
        #check if the user's input was valid username
        if userNameCheck.match(userResp) is None:
            response = "END The username was not according to guidelines.\n"
            isStarted = False
            isUserName = False
        else:
        #if the user provided a valid username
            userName = userResp #save the username
            response = f"CON Hello {userResp} :-),\n"
            response += "Please enter your email:\n"
            isEmail = True #time to obtain the email
            isUserName = False #time to obtain username is over
    elif isEmail:
        #check if the user's input was a valid email
        if emailCheck.match(userResp) is None:
            response = f"END Oh snap! It seems you did not provide a valid email address.\n{userResp}"
            isStarted = False
            isEmail =False
        else:
            userEmail = userResp #save the email
            response = "END Wow! You have successfully registered on our platform!\n"
            response += "You will receive an SMS confirming your registration.\n"
            isEmail =False #time to obtain email is over
            isStarted = False #app ends
            sendSMS(phoneNumber)

    return response

if __name__ == "__main__":
    site.run(host='0.0.0.0')