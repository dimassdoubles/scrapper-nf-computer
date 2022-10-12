import firebase_admin
from firebase_admin import credentials, firestore_async
import asyncio

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