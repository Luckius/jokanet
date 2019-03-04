#!/usr/bin/env python3
import datetime
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from hashlib import md5
from peewee import *




DATABASE = SqliteDatabase('social.db')

class User(UserMixin, Model):
    username = CharField(unique = True)
    email = CharField(unique = True)
    password = CharField(max_length = 100)
    joined_at = DateTimeField(default= datetime.datetime.now)
    is_admin = BooleanField(default = False)



    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)



    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)




    def get_posts(self):
        return Post.select().where(Post.user == self)

    def get_messages(self):
        #messages = Message.select(Message, User).join(User).order_by(Message.create_date.desc())
        return Message.select().where(Message.user == self)


    def get_images_stream(self):
        return Images.select().where(Images.user == self)


    def get_drphoto_stream(self):
        return Drphoto.select().where(Drphoto.user == self)


    def get_ourgamesimage_stream(self):
        return Gamesimage.select().where(Gamesimage.user == self)


    def get_ourgamesmsg_stream(self):
        return Gamesmsg.select().where(Gamesmsg.user == self)



    def get_oursportsimage_stream(self):
        return Sportsimage.select().where(Sportsimage.user == self)


    def get_oursportsmsg_stream(self):
        return Sportsmsg.select().where(Sportsmsg.user == self)


    def get_ourbussnesimage_stream(self):
        return Bussnesimage.select().where(Bussnesimage.user == self)

    def get_ourbussnesmsg_stream(self):
        return Bussnesmsg.select().where(Bussnesmsg.user == self)


    def get_ourpolitcsimage_stream(self):
        return Politcsimages.select().where(Politcsimages.user == self)


    def get_ourpolitcsmsg_stream(self):
        return Politcsmsg.select().where(Politcsmsg.user == self)





    def get_stream(self):
        return Post.select().where(
            (Post.user << self.following())&
            (Post.user == self)
        )



    def get_message_stream(self):
        return Message.select().where(
            (Message.user << self.following())|
            (Message.user == self)
        )

    def get_comment_stream(self):
        return Comment.select().where(
            (Comment.user << self.following()) |
            (Comment.user == self)
        )

    def get_photomessage_stream(self):
        return Photomessage.select().where(
            (Photomessage.user << self.following()) |
            (Photomessage.user == self)
        )






    def following(self):
        """the user that we are following"""
        return(
            User.select().join(
                Relationship, on=Relationship.to_user
            ).where(
                Relationship.from_user == self
            )
        )
    def followers(self):
        """get users following the current user"""
        return(
            User.select().join(
                Relationship, on=Relationship.from_user
            ).where(
                Relationship.to_user == self
            )
        )


    @classmethod
    def create_user(cls, username,email,password, admin = False):
        try:
            with DATABASE.transaction():
                cls.create(
                    username =username,
                    email = email,
                    password =generate_password_hash(password),
                    is_admin =admin,
                )
        except IntegrityError:
            raise ValueError("User aready exists")



class Post(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User,
        rel_model=User,
        related_name='posts'
    )
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)




class Message(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User,
        rel_model=User,
        related_name='messages'
    )
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)



class Images(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User,
        rel_model=User,
        related_name='images'
    )
    filename=TextField()
    fp = TextField()
    #data = BlobField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)




class Drphoto(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User,
        rel_model=User,
        related_name='drphotos'
    )
    filename=TextField()
    fp = TextField()
    #data = BlobField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)




class Gamesimage(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User,
        rel_model=User,
        related_name='ourgamesimages'
    )
    filename=TextField()
    fp = TextField()
    #data = BlobField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)



class Sportsimage(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User,
        rel_model=User,
        related_name='oursportsimages'
    )
    filename=TextField()
    fp = TextField()
    #data = BlobField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)




class Bussnesimage(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User,
        rel_model=User,
        related_name='ourbussnesimages'
    )
    filename=TextField()
    fp = TextField()
    #data = BlobField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)



class Politcsimages(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User,
        rel_model=User,
        related_name='ourpolitsimages'
    )
    filename=TextField()
    fp = TextField()
    #data = BlobField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)




class Comment(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User,
        rel_model=User,
        related_name='commented'
    )
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)




class Gamescmtd(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User,
        rel_model=User,
        related_name='gamescmtd'
    )
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)


class Sportscmtd(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User,
        rel_model=User,
        related_name='sportscmtd'
    )
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)



class Bussnescmtd(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User,
        rel_model=User,
        related_name='bussnescmtd'
    )
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)



class Politcscmtd(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User,
        rel_model=User,
        related_name='politcscmtd'
    )
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)





class Photomessage(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User,
        rel_model=User,
        related_name='photomessages'
    )
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)



class Gamesmsg(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User,
        rel_model=User,
        related_name='ourgamesmsgs'
    )
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)



class Sportsmsg(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User,
        rel_model=User,
        related_name='oursportsmsgs'
    )
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)



class Bussnesmsg(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User,
        rel_model=User,
        related_name='ourbussnesmsgs'
    )
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)



class Politcsmsg(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User,
        rel_model=User,
        related_name='ourpolitcsmsgs'
    )
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)



class Msgchat(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)

    user = ForeignKeyField(
        User,
        rel_model=User,
        related_name='messages',
    )
    content = TextField()


    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)




class Relationship(Model):
    from_user = ForeignKeyField(User, related_name='relationships')
    to_user = ForeignKeyField(User, related_name='related_to')


    class Meta:
        database = DATABASE
        indexes = (
            (('from_user', 'to_user'),True),
        )


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User ,Comment, Politcscmtd ,Bussnesmsg ,Drphoto , Photomessage,
                            Sportsimage,Bussnescmtd,Politcsimages , Gamescmtd ,Gamesimage ,Gamesmsg ,Images
                             ,Msgchat,Sportscmtd, Politcsmsg,Bussnesimage , Sportsmsg,
                              Post, Message, Relationship],safe=True)
    DATABASE.close()
