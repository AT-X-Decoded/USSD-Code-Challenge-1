from flask import Flask,render_template,request

site     = Flask(__name__)
response = "" 
userEmail = ""
userName  = ""
isEmail    = False #checking if email was provided
isUserName = False #checking if username was provided
isStarted  = False

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
    # getting operation data for the app
    sessionId = request.values.get("sessionId", None)
    serviceCode = request.values.get("serviceCode", None)
    phoneNumber = request.values.get("phoneNumber", None)
    userResp = request.values.get("text", "default")

    if userResp == "":
        if isStarted:
            response = "END ERROR\nYou provided no input\n"  
        elif isStarted==False:          
            response = "CON What would you like us to call you:\n"
            isStarted = True
            isEmail = True
    elif isEmail:
        response = f"END welcome {userResp}\n"
    return response

if __name__ == "__main__":
    site.run(host='0.0.0.0')