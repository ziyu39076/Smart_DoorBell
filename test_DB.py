from flaskapp import db
from os import path,sep,remove
from flaskapp.models import User,Visitor,VisitRecord

def main():
    users=User.query.all()
    visitors=Visitor.query.all()
    records=VisitRecord.query.all()
    for u in users:
        print(u.username)
    for v in visitors:
        print(v.name,v.photo,v.user_id)
    for r in records:
        print(r.photo,r.date_visited,r.user_id)

if __name__=="__main__":
    main()