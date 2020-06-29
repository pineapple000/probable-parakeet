from decouple import config


# MongoDB
# https://api.mongodb.com/python/current/api/pymongo/mongo_client.html
MONGODB = {
    'NAME': config('MONGODB_NAME'),
    'USER': config('MONGODB_USER'),
    'PASSWORD': config('MONGODB_PASSWORD'),
    'HOST': config('MONGODB_HOST', default='localhost'),
    'PORT': config('MONGODB_PORT', default=27017, cast=int)
}

