"""
Contains all functions to do with the global variables and dictionaries.
Only file that interacts with the data state.
The threading is stored here and is run here so all functions dealing with
the class will be stored here
Note: Many functions in this file assume that everything is valid.
eg message_remove assumes that the message is already in the channel.
The validation checks are generally done before these functions are called.
"""
from error import AccessError, InputError
from urllib.parse import urljoin
import validation
"""
Global variables containing the state of flockr
"""

# Users is a dictionary that contains information of every user
# and uses u_id as the key.
users = {
    # u_id = {
        #     "channel_list"  = set()
        #     "name_first" : "",
        #     "name_last" : "",
        #     "email": "",
        #     "u_id" : "",
        #     "password" : ""
        #     "handle_str" : ""
        #     "permission_id" : ""
        #     "num_logged_in : ""
        #     "profile_img_url: ""
        # }
}

# Logged_in is a set of all logged in users by u_id.
logged_in = set() 

# Channels is a dictionary that contains information of every channel
# and uses channel_id as the key.
channels = {
        # channel_id = {
        #     "name" : "",
        #     "is_public" : "", # public or private (True or False)
        #     "channel_id" : ""
        #     "owners" = set(),
        #     "members" : set(),
        #     "pinned" : ""
        #     "standup" : {
        #           running : "", # currently running (True or False)
        #           u_id : "",
        #           message : "",
        #           time_finish : "",
        #           timer_class : ""   # the class that was returned from the timer
        #                              # which is used to cancel the timer
        #      }
         #    "messages" = {
        #         message_id = {
            #         {
            #             "message" : "",
            #             "message_id" : "",
            #             "u_id" : "",
            #             "date" : ""
            #             "reacts" = [
            #               {
                    #           react_id : '',
                    #            users : []
                    #       }
                    #   ]
            #         }
            #    }
            #}
            # "hangman" : {
            #     is_active : False,
            #     u_id : '',
            #     word : None,
            #     guesses : set(),
            #     failures : 0,
            #     status_message : ''
            #}
            # "kahio" : {
            #     running : "", currently running (True or False)
            #     u_id : "",
            #     timer_class : "",
            #     time_start : "",
            #     scores : "",   a message that has users and their times
            #     answer : "",
            #     got_answer = []
            #}
    #}
}

# Stores the sendlater messages so that it can be cancelled if clear
# is called. Is a list of dictionaries containing the end time and
# timer class to cancel
sendlater_messages = [
        # {
        #   end_time : "",
        #   timer_class : ""
        # }
]

# Message_num is the total number of messages that have been sent.
# This number does not decrease when a message is removed.
message_num = 0

# jwt_secret is the secret string used in jwt encoding.
# It never changes.
jwt_secret = "Mango2Team"

# List of existing react_ids
react_ids = [1,2,3,4]



def clear_data():
    """
    Restarts the global variable to it"s default state (empty)
    """
    global users, channels, logged_in, message_num
    users = {}
    channels = {

    }
    logged_in = set()
    message_num = 0
    

def get_user_with(attributes):  
    """
    Given an attribute(dict), finds user(dict) with matching attribute and returns it
    """
    for user in users:
        if attributes.items() <= users[user].items():
            return users[user]
    return None
     

def get_user_info(u_id):
    """
    Returns user dictionary from u_id
    """
    try:
        return users[u_id]
    except:
        return None

def get_user_secret(u_id):
    """
    Returns the user's secret session code
    to validate tokens
    """
    user = get_user_info(u_id)
    return user["session_secret"]

def update_user(user, attributes):
    """
    Given a user(dict) and attribute(dict), updates that user with given new attributes
    """
    for item in attributes:
        user[item] = attributes[item]    

def update_user_channel_list(user, channel_id):
    """
    Given a user(dict) and channel_id(int), adds the channel id to the users channel list
    """
    user["channel_list"].add(channel_id)  

def register_user(user):
    """
    Given a user(dict), adds it to list of existing users
    """
    users[user["u_id"]] = user

def login_user(u_id):
    """
    Given a u_id(int), adds u_id to list of logged in users
    """
    logged_in.add(u_id) 

def check_logged_in(u_id):
    """
    Given a u_id(int) checks and returns true if user is logged in
    """
    return u_id in logged_in 

def logout_user(u_id):
    """
    Given a u_id(int), removes u_id from logged in list
    """
    logged_in.remove(u_id)

def get_channel_info(channel_id):
    """
    Given a channel_id(int), returns infomation on channel(dict)
    """
    try:
        return channels[channel_id]
    except:
        return None
    
def get_hangman_info(channel_id):
    """
    Given a channel_id(int), returns infomation on channel's hangman session(dict).
    Assumes channel_id exists.
    """
    channel = get_channel_info(channel_id)
    return channel['hangman']

def get_hangman_status_message(channel_id):
    """
    Given a channel_id, gives the status of hangman in a message
    """
    info = get_hangman_info(channel_id)
    return get_message(channel_id, info['status_message'])

def channel_add_member(channel_id, u_id):
    """
    Given a channel_id(int) and u_id(int), add the u_id to channel
    """
    channel = channels[channel_id]   
    if u_id == 1:
        channel["owners"].add(u_id)
    channel["members"].add(u_id)
    user = get_user_info(u_id)
    user["channel_list"].add(channel_id)

def check_user_in_channel(channel_id, u_id):
    """
    Given a channel_id(int) and u_id(int), returns true if user is a member of channel
    """
    channel = get_channel_info(channel_id)
    return u_id in channel["members"]

def check_channel_owner(channel_id, u_id):
    """
    Given a channel_id(int) and u_id(int), returns true if user is an owner of channel
    """
    channel_info = get_channel_info(channel_id)
    return u_id in channel_info["owners"]

def channel_add_owner(channel_id, u_id):
    """
    Given a channel_id(int) and u_id(int), adds user to list of owners of channel
    """
    channel = channels[channel_id]   
    channel["owners"].add(u_id)

def channel_remove_member(channel_id, u_id):
    """
    Given a channel_id(int) and u_id(int), removes that member from the channel
    """
    channel = channels[channel_id]
    user = get_user_info(u_id)
    if u_id in channel["owners"]:
        channel["owners"].remove(u_id)
    channel["members"].remove(u_id)
    user['channel_list'].remove(channel_id)

def channel_remove_owner(channel_id,u_id):
    """
    Given a channel_id(int) and u_id(int), removes that member as an owner of the channel
    """
    channel = channels[channel_id]   
    channel["owners"].remove(u_id)

def get_message_num():
    """
    Return the value of message_num (the total number of messages).
    This function is used to generate a message_id, so it also includes
    all deleted messages as part of the count.
    """
    return message_num

def get_num_users():
    """
    Returns the number of total users
    """
    return len(users)

def get_jwt_secret():
    """
    Returns the jwt_secret
    """
    return jwt_secret
    
def make_message_id():
    """
    Creates a unique message_id for a new message
    """
    global message_num
    message_num += 1

    return message_num

def channels_list_user(u_id):
    """
    Given a u_id(int), generates a list of all channels user is a part of and returns it
    """
    user = get_user_info(u_id)
    channels_info = []
    for channel in user["channel_list"]:
        chan_info = get_channel_info(channel)
        channel_copy = {
            "channel_id" : chan_info["channel_id"],
            "name" : chan_info["name"]
        }
        channels_info.append(channel_copy)
    return {"channels" : channels_info}    

def channels_list_all():
    """
    Generates a list of all existing channels and returns it
    """
    channels_info = []
    for channel in channels:
        channel_copy = {
            "channel_id" : channel,
            "name" : channels[channel]["name"]
        }
        channels_info.append(channel_copy)
    return {"channels" : channels_info}

def get_num_channels():
    """
    Returns the total number of channels
    """
    return len(channels)

def channel_create(new_channel):
    """
    Given a new_channel(dict), adds it to list of existing channels
    """
    channels[new_channel["channel_id"]] = new_channel
    standup = {"running" : False}
    kahio = {"running" : False}
    channels[new_channel["channel_id"]]["standup"] = standup
    channels[new_channel["channel_id"]]["kahio"] = kahio

def find_channel(message_id):
    """
    Given a message_id, returns channel_id of channel with that message
    """
    for channel in channels:
        if message_id in channels[channel]["messages"]:
            return channel
    raise InputError(description = "Message not in any channel")

def get_message(channel_id, message_id):
    """
    Given channel containing message and message_id,
    returns dictionary containing message info
    """
    return channels[channel_id]['messages'][message_id]

def add_message(message, channel_id):
    """
    Adds given message to channel with given channel_id
    """
    channel = channels[channel_id]
    message_id = message["message_id"]
    channel["messages"][message_id] = message

def remove_message(message_id, channel_id):
    """
    Removes message with given message_id from 
    channel with given channel_id.
    """
    channel = channels[channel_id]
    del channel["messages"][message_id]

def edit_message(channel_id, message_id, message):
    """
    Edits the target message and changes
    target_message["message"] to message
    """
    channels[channel_id]["messages"][message_id]["message"] = message

def user_list():
    """
    Returns a list of every user in the system
    """
    list_users = []
    for user in users.values():
        user_info = {
            "u_id" : user["u_id"],
            "email" : user["email"],
            "name_last" : user["name_last"],
            "name_first" : user["name_first"],
            "handle_str" : user["handle_str"],
            "profile_img_url": user["profile_img_url"]
        }
        list_users.append(user_info)
    return list_users

def change_permission(u_id, permission):
    """
    Changes user's serverwide permissions
    to whatever was specified
    """
    user = get_user_info(u_id)
    user["permission_id"] = permission

def update_user_img(host_url,token):
    u_id = validation.check_valid_token(token)
    user = get_user_info(u_id)
    user["profile_img_url"] = host_url + f"static/{u_id}.jpg"
    
def create_standup(channel_id, u_id, timer_class, time_finish):
    """
    Will add a new standup to a channel
    """
    channels[channel_id]["standup"]["running"] = True
    channels[channel_id]["standup"]["u_id"] = u_id
    channels[channel_id]["standup"]["message"] = ''
    channels[channel_id]["standup"]["time_finish"] = time_finish
    channels[channel_id]["standup"]["timer_class"] = timer_class

def add_message_standup(u_id, message, channel_id):
    """
    Will add the message to the end of the standup message string
    """
    handle = users[u_id]["handle_str"]
    channels[channel_id]["standup"]["message"] += handle + ": " + message + "\n"

def check_standup_running(channel_id):
    """
    Checks if the standup is running
    """
    return channels[channel_id]["standup"]["running"]

def return_standup_message(channel_id):
    """
    Will change the standup to false, and return the message
    """
    channels[channel_id]["standup"]["running"] = False
    return channels[channel_id]["standup"]["message"]

def get_timer_class(channel_id):
    """
    Will return the timer class so the timer can be terminated
    """
    return channels[channel_id]["standup"]["timer_class"]

def get_standup_timer_finish(channel_id):
    """
    Will return the time the standup finishes at
    """
    return channels[channel_id]["standup"]["time_finish"]

def get_channel_from_message(message_id):
    """
    Returns channel_id of channel that contains message_id
    """
    for channel in channels:
        if message_id in channels[channel]['messages']:
            return channel

def pin_message(message_id, channel_id):
    """
    Pins message in channel
    """
    message = get_message(channel_id, message_id)
    message['is_pinned'] = True

def unpin_message(message_id, channel_id):
    """
    Unpins message in channel
    """
    message = get_message(channel_id, message_id)
    message['is_pinned'] = False

def check_valid_react(react_id):
    """
    Checks if react id is valid (exists)
    """
    if react_id in react_ids:
        return True
    return False
        
def check_user_already_reacted(channel_id, message_id, react_id, u_id):
    """
    Check if user has existing react to message, if so return False
    """
    messages = channels[channel_id]["messages"]
    for react_id in messages[message_id]["reacts"]:
        if u_id in react_id["u_ids"]:
            return True
    return False

def react_message(message_id, channel_id, react_id, u_id):
    """
    Adds user to list of users who have reacted to message
    """
    messages = channels[channel_id]["messages"]
    for react in messages[message_id]['reacts']:
        if react['react_id'] == react_id:
            react['u_ids'].append(u_id)

def unreact_message(message_id, channel_id, react_id, u_id):
    """
    Removes user from list of users who have reacted to message
    """
    messages = channels[channel_id]["messages"]
    for react in messages[message_id]['reacts']:
        if react['react_id'] == react_id:
            react['u_ids'].remove(u_id)

def add_sendlater(timer_class, end_time):
    """
    Will add the new sendlater timer_class and unix end_time so
    They can be cancelled by other.clear
    """
    sendlater = {
        "end_time" : end_time,
        "timer_class" : timer_class
    }
    sendlater_messages.append(sendlater)

def remove_sendlater():
    """
    Will remove and return an element form the list
    """

    return sendlater_messages.pop()

def sendlater_not_empty():
    """
    Will return true if the list sendlater_messages is not empty
    """
    if sendlater_messages == []:
        return False
    return True

def check_kahio_running(channel_id):
    """
    Checks if the kahio game is running on this channel
    """
    return channels[channel_id]["kahio"]["running"]

def create_kahio(channel_id, u_id, time_start, answer):
    """
    Will add a new kahio to a channel
    """
    channels[channel_id]["kahio"]["running"] = True
    channels[channel_id]["kahio"]["u_id"] = u_id
    channels[channel_id]["kahio"]["score"] = ''
    channels[channel_id]["kahio"]["time_start"] = time_start
    channels[channel_id]["kahio"]["answer"] = answer
    channels[channel_id]["kahio"]["got_answer"] = [u_id]

def end_kahio_game(channel_id):
    """
    Will end a kahio game by setting running to false
    """
    channels[channel_id]["kahio"]["running"] = False

def kahio_update_timer_class(channel_id, timer_class):
    """
    Will update the timer class when a new multithreading is running
    """
    channels[channel_id]["kahio"]["timer_class"] = timer_class

def return_kahio_num_correct_answers(channel_id):
    """
    Will return the number of users that have guessed the correct answers
    in a game of kahio
    """
    return len(channels[channel_id]["kahio"]["got_answer"]) - 1

def return_kahio_score(channel_id):
    """
    Will return the score message from the kahio game
    """
    return channels[channel_id]["kahio"]["score"]

def return_kahio_answer(channel_id):
    """
    Will return the answer from the kahio game
    """
    return channels[channel_id]["kahio"]["answer"]

def return_kahio_starter(channel_id):
    """
    Will return the user id from the user that started the kahio game
    """
    return channels[channel_id]["kahio"]["u_id"]

def correct_kahio_guess(u_id, channel_id, current_time):
    """
    Will update the kahio dictionary to say that user got the question correct
    And will return the message to be printed
    """

    handle = users[u_id]["handle_str"]
    time_since_game_started = current_time - channels[channel_id]["kahio"]["time_start"]
    time_since_game_started = round(time_since_game_started, 1)
    channels[channel_id]["kahio"]["score"] += "\n" + str(len(channels[channel_id]["kahio"]["got_answer"]) -1) + ": "
    channels[channel_id]["kahio"]["score"] += handle + " got the correct answer at "
    channels[channel_id]["kahio"]["score"] += str(time_since_game_started) + " seconds"
    channels[channel_id]["kahio"]["got_answer"].append(u_id)
    return handle + " guessed the correct answer"

def get_kahio_timer_class(channel_id):
    """
    Will return the timer class so the timer can be terminated
    """
    return channels[channel_id]["kahio"]["timer_class"]

def user_already_got_answer(channel_id, u_id):
    """
    Checks if the user in the list of users that have already have the answer
    """
    return u_id in channels[channel_id]["kahio"]["got_answer"]
