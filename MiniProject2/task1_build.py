# Reference: https://www.freecodecamp.org/news/loading-a-json-file-in-python-how-to-read-and-parse-json/
# https://www.geeksforgeeks.org/python-mongodb-insert_many-query/
# https://stackoverflow.com/questions/35051867/json-load-function-give-strange-unicodedecodeerror-ascii-codec-cant-decod
# https://www.programiz.com/python-programming/time
# https://www.w3schools.com/python/ref_string_endswith.asp



from pymongo import MongoClient
import json
import sys
import time


def setup(port_number):
    client = MongoClient('localhost', port_number) # 27017
    db = client['MP2Norm'] # Create MP2Norm database
    return db # return newly created database

def create_collection(name, db, json_filename): # create collection and insert into
    start_time = time.time() # initialize start time counter
    new_collection = db[name] # add collection named (name) into db
    new_collection.drop() # drop existing if exists

    if name == "messages": # LARGE file
        batch = []

        messages_start = time.time() # initalize start time for messages
        with open(json_filename, 'r', encoding='utf-8') as f: # open messages.json
            for line in f: # for line in messages.json
                line = line.strip() # remove white spaces
                if line != '[' or ']': # first or last line
                        if line.endswith(','): # if line ends with comma
                            line = line[:-1] # remove comma
                            data = json.loads(line) # load in data
                            batch.append(data) # append to batach
                if len(batch) == 5000:
                     new_collection.insert_many(batch) # insert batch into collection
                     batch = [] # reset batch
            messages_end = time.time() # finish time to read messages.json
            messages_total = messages_end-messages_start
            if batch is not None: # if there are any remaining entries in the batch, and the batch is < 5000
                new_collection.insert_many(batch) # insert remaining
        print("Time taken to read messages.json: {}".format(messages_total))

    else: 
        senders_start = time.time() # initialize start time for senders
        with open(json_filename, 'r', encoding="utf-8") as f: # open senders.json
            batch = [] # initalize batch
            data = json.load(f) # load entire file at once since it is a smaller file
            senders_end = time.time() # finish time to read senders.json
            for line in data: # for entry in senders
                batch.append(line) # append to batch
            new_collection.insert_many(batch) # once finished appending, insert into collection
        senders_total = senders_end-senders_start
        print("Time taken to read senders.json: {}".format(senders_total))

    
    end_time = time.time()
    total_time = end_time - start_time
    print("{} collection created. Time taken: {} seconds.".format(name, total_time))

def main():
    port_number = sys.argv[1]
    db = setup(int(port_number))
    create_collection("messages", db, "messages.json")
    create_collection("senders", db, "senders.json")


if __name__ == "__main__":
    main()