import json
from pymongo import MongoClient
from pymongo.errors import ExecutionTimeout
import sys
import time

def setup(port_number):
    client = MongoClient('localhost', port_number) # 27017
    db = client['MP2Norm'] # Create MP2Norm database
    return db

def create_indices(db):
    db.messages.create_index("sender")
    db.messages.create_index([("text", "text")])
    db.senders.create_index("sender_id")


#Q1: Return the number of messages that have “ant” in their text. Not case insensitive
def q1(db):
    start_time = time.time()
    try:
        #match all messages with "ant" and count them
        result = db.messages.count_documents({"text": {"$regex": "ant"}}, maxTimeMS=120000) 
        end_time = time.time()
        duration_seconds = end_time - start_time
        duration_milliseconds = duration_seconds * 1000
        print(f"Q1: Number of messages containing 'ant': {result}\nTime taken: {duration_seconds:.2f} seconds ({duration_milliseconds:.2f} milliseconds)")
    except ExecutionTimeout:
        print("Q1: Query took more than 2 minutes")

#Q2: Find the nick name/phone number of the sender who has sent the greatest number of messages. Return the nick name/phone number and the number of messages sent by that sender. You do not need to return the senders name or credit.
def q2(db):
    start_time = time.time()
    #group messages by sender and then count the number of messages
    try:
        pipeline = [
            {"$group": {"_id": "$sender", "total": {"$sum": 1}}},
            {"$sort": {"total": -1}},
            {"$limit": 1}
        ]
        result = list(db.messages.aggregate(pipeline, maxTimeMS=120000))
        end_time = time.time()
        duration_seconds = end_time - start_time
        duration_milliseconds = duration_seconds * 1000
        if result:
            top_sender = result[0]
            print(f"Q2: Sender with the most messages: {top_sender['_id']}, Number of messages: {top_sender['total']}\nTime taken: {duration_seconds:.2f} seconds ({duration_milliseconds:.2f} milliseconds)")
        else:
            print("Q2: No messages found!\nTime taken: {duration_seconds:.2f} seconds ({duration_milliseconds:.2f} milliseconds)")
    except ExecutionTimeout:
        print("Q2: Query took more than 2 minutes")

#Q3: Return the number of messages where the sender’s credit is 0.
def q3(db):
    start_time = time.time()
    #match messages where the sender as zero credit and then count them
    try:
        result = db.messages.count_documents({"sender_info.credit": 0}, maxTimeMS=120000)
        end_time = time.time()
        duration_seconds = end_time - start_time
        duration_milliseconds = duration_seconds * 1000
        print(f"Q3: Number of messages with sender's credit as 0: {result}\nTime taken: {duration_seconds:.2f} seconds ({duration_milliseconds:.2f} milliseconds)")
    except ExecutionTimeout:
        print("Q3: Query took more than 2 minutes")

#Q4: Double the credit of all senders whose credit is less than 100.
def q4(db):
    start_time = time.time()
    try:
        #Find all senders with credit less than 100
        senders_to_update = db.senders.find({"credit": {"$lt": 100}})
        #Get a list of sender IDs to update
        sender_ids = [sender["_id"] for sender in senders_to_update]
        result = db.senders.update_many({"_id": {"$in": sender_ids}}, {"$mul": {"credit": 2}})
        end_time = time.time()
        duration_seconds = end_time - start_time
        duration_milliseconds = duration_seconds * 1000
        print(f"Q4: Number of senders with credit less than 100 updated: {result.modified_count}\nTime taken: {duration_seconds:.2f} seconds ({duration_milliseconds:.2f} milliseconds)")
    except ExecutionTimeout:
        print("Q4: Query took more than 2 minutes")

def main():
    port_number = int(sys.argv[1])
    db = setup(port_number)
    q1(db)
    q2(db)
    q3(db)
    q4(db)
    create_indices(db)

    print('**************************')

    q1(db)
    q2(db)
    q3(db)

if __name__ == "__main__":
    main()
