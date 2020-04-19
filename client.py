import os
import requests

def is_permitted(url_root_path,user_name,img_path):
    # img_path is the absoulte path of input image
    img=open(img_path,'rb')
    files={
        'img':(
            os.path.basename(img_path),
            img,
            'multipart/form-data'
        )
    }
    post_url="%susers/%s/identify/" % (url_root_path,user_name)
    response=requests.post(post_url,files=files)
    return "Permitted" in response.text

def activate_door(signal):
    if signal:
        # activate the door
        pass

def main():
    url_root_path="http://localhost:5000/"
    user_name="bob"
    """ img_name="musk2.jpg"
    img_path=os.getcwd()+os.sep+"imgs"+os.sep+img_name """
    img_path="xxxxxxxxxxx"
    print(is_permitted(url_root_path,user_name,img_path))

if __name__=="__main__":
    main()