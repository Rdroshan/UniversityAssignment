import pymongo
from django.conf import settings
import certifi
# To reference the installed certificate authority
ca = certifi.where()

client = pymongo.MongoClient(settings.MONGODB['HOST'], tlsCAFile=ca)