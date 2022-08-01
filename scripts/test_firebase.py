from firebase_admin import firestore

fdb = firestore.Client()

def testing():
    snapshots = list(fdb.collection(u'forms').get())
    for snapshot in snapshots:
        print(snapshot.to_dict())