import firebase_admin
from firebase_admin import credentials, firestore_async
import asyncio
import json

COLLECTION = "tasks"

def pushData(tasks):
    cred = credentials.Certificate("firebaseCredential.json")
    app = firebase_admin.initialize_app(cred)

    db = firestore_async.client(app=app)
    nf_tasks_ref = db.collection(COLLECTION)
    asyncio.set_event_loop(asyncio.new_event_loop())
    for task in tasks:
        asyncio.get_event_loop().run_until_complete(nf_tasks_ref.document(document_id=task["id"]).set(document_data=task))
    
    asyncio.get_event_loop().close()

class FirebaseController:
    def __init__(self, collection):
        self.__cred = credentials.Certificate("firebaseCredential.json")
        self.__app = firebase_admin.initialize_app(self.__cred)
        self.__collection = firestore_async.client(app=self.__app).collection(collection)
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.__loop = asyncio.get_event_loop()
    
    def get_tasks(self):
        docs = self.__loop.run_until_complete(self.__collection.get())
        data = []
        for doc in docs:
            data.append(doc.to_dict())
        
        tasks = {"data": data}

        json_object =json.dumps(tasks, indent=4)
        with open("tasks.json", "w") as file:
            file.write(json_object)

    def push_tasks(self, tasks):
        for task in tasks:
            self.__loop.run_until_complete(self.__collection.document(document_id=task["id"]).set(document_data=task))
    
    def close(self):
        self.__loop.close()

