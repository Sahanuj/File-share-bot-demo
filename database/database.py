#(©)CodeXBotz

import pymongo, os
from config import DB_URI, DB_NAME

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]
user_data = database['users']
join_request_data = database['join_requests']

async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return

def _join_request_doc_id(chat_ref, user_id: int) -> str:
    return f"{str(chat_ref).lower()}:{user_id}"


async def add_join_request(chat_ref, user_id: int):
    join_request_data.update_one(
        {'_id': _join_request_doc_id(chat_ref, user_id)},
        {'$set': {'chat_ref': str(chat_ref).lower(), 'user_id': user_id}},
        upsert=True
    )
    return


async def has_join_request(chat_ref, user_id: int):
    return bool(join_request_data.find_one({'_id': _join_request_doc_id(chat_ref, user_id)}))
