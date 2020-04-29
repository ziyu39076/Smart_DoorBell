from flaskapp import db
from os import path,sep,remove

def main():
    if path.exists('flaskapp'+sep+'data.db'):
        remove('flaskapp'+sep+'data.db')
    db.create_all()

if __name__=="__main__":
    main()