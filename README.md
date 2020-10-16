# Smart Doorbell
Activate the door for permitted visitors automatically with the help of flask web app and Raspberry Pi development board
## Prerequisites
1. AWS account
2. Raspberry Pi Model B
## How to deploy the web app to AWS EC2 instance
1. clone the repo to your home directory
```
git clone https://github.com/ziyu39076/Smart_DoorBell
```
2. install python3-pip, python3-venv, then activate the venv and install all packages with 
```
pip install -r requirements.txt
```
3. setup AWS face-recognition API according to the official documentation
https://docs.aws.amazon.com/rekognition/latest/dg/getting-started.html, if only trying to run the app on local host, after setting up env and AWS API, just need to run `python run.py`in terminal, then go to http://localhost:5000/
4. install nginx and supervisor with `sudo apt install`
5. remove nginx default file
```
sudo rm /etc/nginx/sites-enabled/default
```
6. create our config app
```
sudo nano /etc/nginx/sites-enabled/flaskblog
```
7. configure supervisor.conf and create folders as well as files in this .conf file
```
sudo nano /etc/supervisor/conf.d/supervisor.conf
```

8. edit ngnix configuration file
```
sudo nano /etc/nginx/nginx.conf
```
9. restart nginx and supervisor
```
sudo systemctl restart nginx
sudo supervisorctl reload
```
(.conf files are in the repo)


