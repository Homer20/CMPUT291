from pymongo import MongoClient
from pymongo.errors import ExecutionTimeout
import sys
import time

# This function establishes a connection to the MongoDB database
def setup(port_number):
    client = MongoClient('localhost', port_number) # 27017
    db = client['MP2Norm'] # Create MP2Norm database
    return db

def q1(db, collection_name, keyword):
    start_time = time.time()
    try:
        collection = db[collection_name]
        
        # Finding messages containing the keyword
        query = {"text": {"$regex": keyword, "$options": "x"}}
        
        # Counting the matching documents in the collection
        count = collection.count_documents(query, maxTimeMS=120000)
        
        end_time = time.time()

        # Calculating the time taken for the query execution
        time_taken = end_time - start_time
        time_ms = time_taken * 1000

        print(f"Number of messages containing '{keyword}': {count}")
        print(f"Time taken: {time_taken:.0f} seconds and {time_ms:.0f} milliseconds")

    except ExecutionTimeout:
        print("Query takes more than 2 minutes!")

    except Exception as e:
        print(f"Error executing query: {e}")
        

def q2(db, messages_collection, senders_collection):
    start_time = time.time()
    try:
        messages = db[messages_collection]
        senders = db[senders_collection]

        # This pipeline groups messages by sender and finds the top sender
        pipeline = [
            {
                "$group": {
                    "_id": "$sender",
                    "message_count": {"$sum": 1}
                }
            },
            {
                "$sort": {"message_count": -1}
            },
            {
                "$limit": 1
            }
        ]

        # Finding the top sender by executing the aggregation pipeline
        result = list(messages.aggregate(pipeline, allowDiskUse=True, maxTimeMS=120000))
        end_time = time.time()

        time_taken = end_time - start_time
        time_ms = time_taken * 1000

        # Getting the top sender info from the result
        if result:
            top_sender = result[0]
            sender_id = top_sender["_id"]
            message_count = top_sender["message_count"]
            print(f"Sender with the most messages: {sender_id}")
            print(f"Number of messages sent by {sender_id}: {message_count}")
        else:
            print("No messages found!")
        
        print(f"Time taken: {time_taken:.0f} seconds and {time_ms:.0f} milliseconds")

    except ExecutionTimeout:
        print("Query takes more than 2 minutes!")

    except Exception as e:
        print(f"Error executing query: {e}")


def q3(db, messages_collection, senders_collection):
    start_time = time.time()
    try:
        messages = db[messages_collection]
        senders = db[senders_collection]

        # This aggregation pipeline looks up sender info and matches messages with credit = 0
        pipeline = [
            {
                "$lookup": {
                    "from": senders_collection,
                    "localField": "sender",
                    "foreignField": "sender_id",
                    "as": "sender_info"
                }
            },
            {
                "$match": {
                    "sender_info.credit": 0
                }
            },
            {
                "$count": "message_count"
            }
        ]

        # Counting messages with 0 credit by executing the aggregation pipeline
        result = list(messages.aggregate(pipeline, allowDiskUse=True, maxTimeMS=120000))
        end_time = time.time()

        time_taken = end_time - start_time
        time_ms = time_taken * 1000

        # Getting the message count from the result
        if result:
            message_count = result[0]["message_count"]
            print(f"Number of messages with sender's credit as 0: {message_count}")
        else:
            print("No messages found with sender's credit as 0!")

        print(f"Time taken: {time_taken:.0f} seconds and {time_ms:.0f} milliseconds")
    
    except ExecutionTimeout:
        print("Query takes more than 2 minutes!")

    except Exception as e:
        print(f"Error executing query: {e}")
        

def q4(db, senders_collection):
    start_time = time.time()
    try:
        senders = db[senders_collection]

        # Updating senders with credit less than 100 by doubling their credit
        result = senders.update_many({"credit": {"$lt": 100}}, {"$mul": {"credit": 2}})
        end_time = time.time()

        print(f"Number of senders with credit less than 100 updated: {result.modified_count}")
        
        time_taken = end_time - start_time
        time_ms = time_taken * 1000
        print(f"Time taken: {time_taken:.0f} seconds and {time_ms:.0f} milliseconds")

    except ExecutionTimeout:
        print("Query takes more than 2 minutes!")

    except Exception as e:
        print(f"Error executing query: {e}")

# Creating the indices
def create_indices(db):
    db.messages.create_index("sender")

    db.messages.create_index([("text", "text")])

    db.senders.create_index("sender_id")


def main():
    port_number = sys.argv[1]
    db = setup(int(port_number))

    # Running the queries normally
    q1(db, 'messages', 'ant')
    q2(db, 'messages', 'senders')
    q3(db, 'messages', 'senders')
    q4(db, "senders")

    # Creating the indices
    create_indices(db)

    print('**************************')

    # Running the queries after the indices have ben created
    q1(db, 'messages', 'ant')
    q2(db, 'messages', 'senders')
    q3(db, 'messages', 'senders')

if __name__ == "__main__":
    main()
