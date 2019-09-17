from flask import Flask,render_template,request

site     = Flask(__name__)
response = "" 

# Landing page for the site
@site.route('/')
def home():
    return render_template('index.html')  

# Implementing the ussd functionality
@site.route('/app/ussd',methods=['POST','GET'])
def ussd_callback():
    global response
    # getting operation data for the app
    sessionId = request.values.get("sessionId", None)
    serviceCode = request.values.get("serviceCode", None)
    phoneNumber = request.values.get("phoneNumber", None)
    userResp = request.values.get("text", "default")

    if userResp == "":
        response = "CON Enter your email:\n"
    return response

if __name__ == "__main__":
    site.run(host='0.0.0.0')