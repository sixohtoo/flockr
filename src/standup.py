"""
time: Gives access to function sleep
threading: Gives access to multi threading
datetime: Gives access to the datetime functions
error(error.py): Gives access to error classes
data(data.py): Gives access to global data variable
validation(validation.py): Gives access to the premade validations
"""
import time
import threading
import datetime
from error import AccessError, InputError
import data
import validation

def get_time_finish(length):
    """
    Gets the datetime of the time standup finishes

    Parameters:
        length(int) : The time the standup will take

    Returns:
        finish_time(int(unix timestamo)) : the time the standup will finish
    """
    return datetime.datetime.now().replace().timestamp() + length

def send_standup(*args):
    """
    Sends the standup message from the given u_id

    Parameters:
        args[0] (u_id(int)) : The u_id that standup will be sent from
        args[1] (channel_id(int)) : The channel that the message will be sent to
    """
    new_message_id = data.make_message_id()
    new_message = {}
    new_message["message"] = data.return_standup_message(args[1])
    if new_message["message"] == "":
        #If no message was added to the standup it will not print standup
        return
    new_message["u_id"] = args[0]
    new_message["time_created"] = datetime.datetime.now().replace().timestamp()
    new_message["message_id"] = new_message_id
    new_message["is_pinned"] = False
    new_message["reacts"] = [
            {
        "react_id": 1,
        "u_ids": []
            }  
    ]
    data.add_message(new_message, args[1])

def standup_start(token, channel_id, length):
    """
    Starts the standup for the given channel

    Parameters:
        token(string): An authorisation hash
        channel_id(int): The channel_id of the channel the standup is being started for
        length(int): The delay before the standup should be posted

    Returns:
        time_finish(int(unix timestamp)): When the standup will be posted
    """

    # Check that the token is valid
    user_input_id = validation.check_valid_token(token)

    # Check that the channel_id is valid
    validation.check_valid_channel_id(channel_id)

    # Check that user is in channel
    validation.check_user_in_channel(user_input_id, channel_id)

    # Check that the length is greater then 0
    validation.check_length_valid(length)

    #Checks a standup isn't already running on this channel, raises error if it is
    validation.check_standup_not_running(channel_id)

    # Will begin the timer which will wait the length amount of time before calling the
    # function
    timer_class = threading.Timer(length, send_standup, [user_input_id, channel_id])

    # Calculates when the standup will finish
    time_finish = get_time_finish(length)

    # Inserts the standup into the channel
    data.create_standup(channel_id, user_input_id, timer_class, time_finish)
    timer_class.start()
    return {
        "time_finish": time_finish
    }

def standup_active(token, channel_id):
    """
    Checks if there is a standup active on the channel

    Parameters:
        token(string): An authorisation hash
        channel_id(int): The channel_id of the channel that the standup is being checked

    Returns:
        is_active(boolean): If there is a standup active on the given channel
        time_finish(int(unix timestamp)): When the standup will be posted
    """
    # Check that the token is valid
    user_input_id = validation.check_valid_token(token)

    # Check that the channel_id is valid
    validation.check_valid_channel_id(channel_id)

    # Check that user is in channel
    validation.check_user_in_channel(user_input_id, channel_id)

    # checks if the standup is running for the channel
    running = data.check_standup_running(channel_id)

    # Creates time_finish and if the standup is running puts the finish_time in it
    time_finish = None
    if running:
        time_finish = data.get_standup_timer_finish(channel_id)
    
    return {
        "is_active": running,
        "time_finish": time_finish
    }

def standup_send(token, channel_id, message):
    """
    Adds a new message to the standup in a channel

    Parameters:
        token(string): An authorisation hash
        channel_id(int): The channel_id of the channel standup the message is being added too
        message(string): The message of the message being added

    Returns:
        Nothing
    """

    # Check that the token is valid
    user_input_id = validation.check_valid_token(token)

    # Check that the channel_id is valid
    validation.check_valid_channel_id(channel_id)

    # Check that user is in channel
    validation.check_user_in_channel(user_input_id, channel_id)

    #Checks a standup is already running on this channel, raises error if it isn't
    validation.check_standup_running(channel_id)

    # Check that the message is valid
    validation.valid_message(message)

    # Will insert the message to the running standup
    data.add_message_standup(user_input_id, message, channel_id)
    return {
    }
