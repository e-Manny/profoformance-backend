from dotenv import load_dotenv
import os
import redis

load_dotenv()

class ApplicationConfig():
    os.environ["SECRET_KEY"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///./db.sqlite"

    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_SE_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")