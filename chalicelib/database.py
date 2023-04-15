import os
from pymongo import MongoClient
from bson import ObjectId


class Database:

    def __init__(self) -> None:
        self.client = MongoClient(os.getenv('MONGO_URL')).apresentacao

    def create_user(self, user: dict):
        return self.client.user.insert_one(user)

    def get_user(self, query: dict = {}):
        return self.client.user.find_one(query)

    def get_notification(self, query: dict = {}):
        return list( self.client.notification.find(query))

    def create_notification(self, product: dict, many: bool = False):
        if many:
            return self.client.notification.insert_many(product)
        return self.client.notification.insert_one(product)

    def delete_notification(self, _id: ObjectId):
        return self.client.notification.delete_one({'_id': _id})

    def update_notification(self, notification: list, proximo: list):
        return self.client.notification.update_one({'_id': notification}, {'$set': {'proximo': proximo}})

    def get_notificacoes_agora(self, hora: str):
        return list(self.client.notification.aggregate(
            [{'$match': {'proximo': hora}}, 
             {'$lookup': {'from': 'user', 'localField': 'usuario', 'foreignField': '_id', 'as': 'users'}}]
        ))
