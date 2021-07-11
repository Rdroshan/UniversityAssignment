import pymongo
import certifi
# To reference the installed certificate authority
ca = certifi.where()

client = pymongo.MongoClient('mongodb+srv://prodigal_be_test_01:prodigaltech@test-01-ateon.mongodb.net/sample_training', tlsCAFile=ca)