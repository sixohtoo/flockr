"""
datetime: Gives access to the datetime functions
error(error.py): Gives access to error classes
data(data.py): Gives access to global data variable
validation(validation.py): Gives access to the premade validations
hangman(hangman.py): Gives access to hangman functions
"""
import datetime
from error import AccessError, InputError
import data
import validation
import hangman
import weather
import kahio
import threading

def find_channel_with_message(message_id, u_id):
    """
    Will go through every channel and if message_in_channel returns a channel it
    will return it otherwise it raises an Input Error

    Parameters:
        message_id(string): The id of the message being searched for
        user_id(string): The id of the user searching for the message it will return
                         an access error if the user is not an owner of the channel
                         or creator of the message
    Returns:
        channel(channel dictionary): If the channel was found it will return the channel
                                     dictionary
    """
    channel_id = data.find_channel(message_id)
    message = data.get_message(channel_id, message_id)
    if message["u_id"] == u_id or data.check_channel_owner(channel_id, u_id):
        return channel_id
    raise AccessError(description="User is not creator or owner")



def message_send(token, channel_id, message):
    """
    Adds a new message to the messages in a channel

    Parameters:
        token(string): An authorisation hash
        channel_id(int): The channel_id of the channel the message is being added too
        message(string): The message of the message being added

    Returns:
        message_id(int): An identifier for the new message
    """
    # Check that the token is valid
    user_input_id = validation.check_valid_token(token)

    # Check that the message is valid.
    validation.valid_message(message)

    # Check that the channel_id is valid
    validation.check_valid_channel_id(channel_id)

    # Check that user is in channel
    validation.check_user_in_channel(user_input_id, channel_id)

    
    new_message_id = data.make_message_id()
    new_message = {}
    new_message["message"] = message
    new_message["u_id"] = user_input_id
    new_message["time_created"] = datetime.datetime.now().replace().timestamp()
    new_message["message_id"] = new_message_id
    new_message["is_pinned"] = False
    new_message["reacts"] = [
            {
        "react_id": 1,
        "u_ids": []
            },
            {
        "react_id": 2,
        "u_ids": []
            },
            {
        "react_id": 3,
        "u_ids": []
            },
            {
        "react_id": 4,
        "u_ids": []
            }
    ]
    
    # Check if message is calling weather API
    if validation.check_weather_call(message):
        new_message['message'] = weather.get_weather(message)

    # Check if message will start a hangman session
    if validation.check_start_hangman(channel_id, message):
        return hangman.start(user_input_id, channel_id, new_message, new_message_id)
        
    # Check if hangman is active and message is a guess
    if validation.check_if_hangman(channel_id, message):
        hangman.guess(user_input_id, channel_id, message)

    # Check if hangman should stop (/hangman stop)
    if validation.check_if_stop_message(message):
        return hangman.stop(user_input_id, channel_id)

    if message.startswith("/KAHIO/END"):
        new_message["message"] = kahio.kahio_end(user_input_id, channel_id)
    elif message.startswith("/KAHIO"):
        new_message["message"] = kahio.start_kahio(user_input_id, channel_id, message)
    elif data.check_kahio_running(channel_id):
        return kahio.kahio_guess(user_input_id, channel_id, new_message)

    data.add_message(new_message, channel_id)

    return {
        "message_id": new_message_id,
    }

def message_remove(token, message_id):
    """
    Removes an existing message from the channel it is in

    Parameters:
        token(string): An authorisation hash
        message_id(int): The id of the message being removed
        message(string): The message of the message being added

    Returns:
		Nothing
    """
    # Check valid token
    user_input_id = validation.check_valid_token(token)

    # Check valid message id
    validation.valid_message_id(message_id)

    # Check message is not the hangman status message
    validation.check_not_status_message(message_id)

    channel_id = find_channel_with_message(message_id, user_input_id)
    data.remove_message(message_id, channel_id)

    return {}

def message_edit(token, message_id, message):
    """
    Removes an existing message from the channel it is in

    Parameters:
        token(string): An authorisation hash
        message_id(string): The id of the message being removed

    Returns:
        Nothing
    """
    # Check valid token
    user_input_id = validation.check_valid_token(token)

    # Check valid message
    validation.valid_message(message)

    # Check valid message id
    validation.valid_message_id(message_id)

    # Check message is not the hangman status message
    validation.check_not_status_message(message_id)

    # Editing a message to an empty string will delete the message.
    if message == "":
        return message_remove(token, message_id)


    channel_id = find_channel_with_message(message_id, user_input_id)
    data.edit_message(channel_id, message_id, message)
    return {}

def message_sendlater(token, channel_id, message, time_sent):
    """
    Adds a new message to the messages in a channel at a set date

    Parameters:
        token(string): An authorisation hash
        channel_id(int): The channel_id of the channel the message is being added too
        message(string): The message of the message being added
        time_sent(int): The Unix timestamp of the date the message is to be sent

    Returns:
        message_id(int): An identifier for the new message
    """

    # Check that the token is valid
    user_input_id = validation.check_valid_token(token)

    # Check that the message is valid.
    validation.valid_message(message)

    # Check that the channel_id is valid
    validation.check_valid_channel_id(channel_id)

    # Check that user is in channel
    validation.check_user_in_channel(user_input_id, channel_id)

    current_timestamp = round(datetime.datetime.now().timestamp())
    delta = time_sent - current_timestamp
    if round(delta) <= 0:
        raise InputError(description="Can't send to the past")


    t = threading.Timer(delta, message_send(token, channel_id, message))
    t.start()

    data.add_sendlater(t, time_sent)
    new_message_id = data.get_message_num()
    return {
        "message_id": new_message_id,
    }

def message_pin(token, message_id):
    """
    Given a message within a channel, mark it as "pinned" to 
    be given special display treatment by the frontend

    Parameters:
        token(string): An authorisation hash
        message_id(int): Identifier for message in channel
        
    Returns:
        Nothing
    """
    # Check that the token is valid
    u_id = validation.check_valid_token(token)

    # Check that the message exists
    channel_id = validation.check_message_exists(message_id)

    # Check that message is not already pinned
    validation.check_not_pinned(message_id)

    # Check that the user has permission
    validation.check_is_channel_owner(u_id, channel_id) # CHANGE TO ACCESSERROR

    data.pin_message(message_id, channel_id)

    return {}

def message_unpin(token, message_id):
    """
    Given a message within a channel, remove it's mark as unpinned

    Parameters:
        token(string): An authorisation hash
        message_id(int): Identifier for message in channel
        
    Returns:
        Nothing
    """
    # Check that the token is valid
    u_id = validation.check_valid_token(token)

    # Check that the message exists
    channel_id = validation.check_message_exists(message_id)

    # Check that message is already pinned
    validation.check_is_pinned(message_id)

    # Check that the user has permission
    validation.check_is_channel_owner(u_id, channel_id) # CHANGE TO ACCESSERROR

    data.unpin_message(message_id, channel_id)

    return {}

def message_react(token, message_id, react_id):
    """
    Given a message within a channel the authorised user is part of, 
    add a "react" to that particular message

    Parameters:
        token(string): An authorisation hash
        message_id(int): Identifier for message in channel
        react_id(int): identifier for react in list of reacts
        
    Returns:
        Nothing
    """
    # Check that the token is valid
    u_id = validation.check_valid_token(token)

    # Check that the message exists
    channel_id = validation.check_message_exists(message_id)

    # Check react id is valid
    validation.check_valid_react(react_id)

    # Check that message has already been reacted
    validation.check_is_reacted_already(channel_id, message_id, react_id, u_id)

    data.react_message(message_id, channel_id, react_id, u_id)

    return {}

def message_unreact(token, message_id, react_id):
    """
    Given a message within a channel the authorised user is part of, 
    remove a "react" to that particular message

    Parameters:
        token(string): An authorisation hash
        message_id(int): Identifier for message in channel
        react_id(int): identifier for react in list of reacts
        
    Returns:
        Nothing
    """ 
    # Check that the token is valid
    u_id = validation.check_valid_token(token)

    # Check that the message exists
    channel_id = validation.check_message_exists(message_id)

    # Check react id is valid
    validation.check_valid_react(react_id)

    # Check that message has already been reacted
    validation.check_has_not_reacted(channel_id, message_id, react_id, u_id)

    data.unreact_message(message_id, channel_id, react_id, u_id)

    return {}
