from pymongo import MongoClient
import json
import sys
import time
# https://stackoverflow.com/questions/68554829/python-sorting-with-lambda-key-confusion

def setup(port_number):
    client = MongoClient('localhost', port_number) # 27017
    db = client['MP2Embd'] # Create MP2Embd database
    return db

def find_sender_info(element, sender_list): # Match sender_info using binary search strategy
    start = 0
    end = len(sender_list) - 1
    while start <= end:
        mid = (start+end)//2 # initalize mid
        if sender_list[mid]['sender_id'] < element: # if current sender_list[mid] < element, ignore left half
            start = mid + 1
        elif sender_list[mid]['sender_id'] > element:  # if current sender_list[mid] > element, ignore right half
            end = mid - 1
        else:
            return sender_list[mid] # return sender_info
    return None


def create_collection(name, db, json_filename): # create collection and insert into
    start_time = time.time()
    new_collection = db[name] # add collection named (name) into db
    new_collection.drop() # drop existing if exists

    sender_start = time.time() # initalize start time to read senders.json
    with open("senders.json", 'r', encoding='utf-8') as f: # open senders.json
        sender_list = json.load(f) # load senders.json file into program
        sender_list.sort(key=lambda x: x['sender_id']) # Sort sender_list into alphabetical order
    sender_end = time.time() # finish time to read senders.json
    sender_total = sender_end - sender_start
    print("Time taken to read senders.json: {}".format(sender_total))

    batch = [] # initialize empty batch
    messages_start = time.time() # initalize start time to read messages.json
    with open(json_filename, 'r', encoding='utf-8') as f: # open messages.json 
        for line in f: # for message in messages
            line = line.strip() # remove white spaces
            if line not in ['[',']']: # first or last line
                if line.endswith(','): # if line ends with comma
                    line = line[:-1] # remove comma
                    messages = json.loads(line) # load messages
                    sender = messages['sender'] # obtain sender name/phone number from message
                    sender_info = find_sender_info(sender, sender_list) # find sender_info
                    if sender_info is not None: # if sender info exists in senders
                        messages['sender_info'] = sender_info # create new attribute in data, and add corresponding sender from sender_list
                        batch.append(messages) 


            if len(batch) == 5000:
                new_collection.insert_many(batch) # insert batch once length == 5000
                batch = [] # reset batch
        messages_end = time.time() # finish time to read messages.json
        messages_total = messages_end - messages_start
        print("Time taken to read messages.json: {}".format(messages_total))

        if batch is not None: # if there any leftover entries
            new_collection.insert_many(batch) # append rest to batch
    
    end_time = time.time()
    total_time = end_time - start_time
    print("{} collection created. Time taken: {} seconds.".format(name, total_time))


def main():
    port_number = sys.argv[1]
    db = setup(int(port_number))
    create_collection("messages", db, "messages.json")

if __name__ == "__main__":
    main()