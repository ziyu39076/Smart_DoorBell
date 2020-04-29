import os
import requests
from bs4 import BeautifulSoup

# This url links to the web app
url_root_path="http://ec2-3-86-230-21.compute-1.amazonaws.com/"
login_url=url_root_path+'login'
identify_url=url_root_path+'identify'

def login(login_info):
    with requests.Session() as sess:
        login_res = sess.get(login_url)
        signin = BeautifulSoup(login_res._content, 'html.parser')
        login_info['csrf_token'] = signin.find('input', id='csrf_token')['value']
        # login
        sess.post(login_url, data=login_info)

        return sess

def identify(sess,image_path):
    # key point: the key need to be the same as id in form
    files = {'photo': open(image_path, 'rb')}
    identify_res = sess.post(identify_url,files=files)

    return "granted" in identify_res.text # boolean return type

def activate_door(signal):
    if signal:
        # activate the door, could be represented by lighting an LED on pi board
        # green: permitted, red: denied
        pass

def main():
    # this login info is valid
    login_info={
        'email':"test@test.com",
        'password':"test"
    }

    # remember to change img file path
    img_path="t2.jpg"

    sess=login(login_info)
    res=identify(sess,img_path)
    print(res)
    activate_door(res)

if __name__=="__main__":
    main()