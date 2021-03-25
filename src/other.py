"""
data(data.py): Gives access to global variable
validation(validation.py): Gives access to the premade validations
error(error.py): Gives access to error classes
channels(channels.py): Gives access to channel_list
"""
import data
import validation
from error import InputError, AccessError
import channels
import datetime

def clear():
    """
    Clears global data variable and terminates any running timers
    """

    # Keeping everything related to the
    # global variable in the same file.
    channels_list = data.channels_list_all()
    for channel in channels_list["channels"]:
        if data.check_standup_running(channel["channel_id"]):
            timer_class = data.get_timer_class(channel["channel_id"])
            timer_class.cancel()
        if data.check_kahio_running(channel["channel_id"]):
            timer_class = data.get_kahio_timer_class(channel["channel_id"])
            timer_class.cancel()
    while (data.sendlater_not_empty()):
        current_time = datetime.datetime.now().replace().timestamp()
        sendlater_con = data.remove_sendlater()
        if (sendlater_con["end_time"] > current_time): # pragma: no cover
            sendlater_con["timer_class"].cancel()

    data.clear_data()

def users_all(token):
    """
    Returns a dictionary containing a list of all users in Flockr

    Parameters:
        token(string): A user authorisation hash

    Returns:
        users: A dictionary containing a list of all users in Flockr with their user details
    """
    # Check that token is valid
    validation.check_valid_token(token)


    # Accesses data.py and appends user info of each user to users
    return {"users" : data.user_list()}
    
def admin_userpermission_change(token, u_id, permission_id):
    """
    Sets a user's permissions described by permission_id

    Parameters:
        token(string): A user authorisation hash
        u_id(int): Indentifier for User
        permission_id(int): A value describing a user"s permissions
                            - permission_id for owners: 1
                            - permission_id for members: 2

    Returns:
        Nothing
    """
    # Check that token is valid
    auth_u_id = validation.check_valid_token(token)

    # Dictionary of all valid permission values:
    valid_permission_id = {1, 2}

    # Checks if authorised user is an owner of Flockr
    # Returns AccessError if not an owner of Flockr
    
    if data.get_user_info(auth_u_id)["permission_id"] != 1:
        raise AccessError(description = "User is not owner of Flockr")
    
    # Finds target user and sets "permission_id" value to permission_id
    target_user = data.get_user_info(u_id)
    if target_user is None:
        raise InputError("Target user does not exist")
    if permission_id in valid_permission_id:
        data.change_permission(u_id, permission_id)
        return {}

    raise InputError(description = "Permission id is not a valid value")

def search(token, query_str):
    """
    Returns a dictionary containing a list of all users in Flockr

    Parameters:
        token(string): A user authorisation hash

    Returns:
        messages: A dictionary containing a list of all messages that the user has sent 
                  with the corresponding query string
    """
    # Check that token is valid
    validation.check_valid_token(token)

    # Initialises messages to return to user
    messages = []

    # Finds all messages that the user has sent containing the query string

    user_channels = channels.channels_list(token)["channels"]
    print(user_channels)
    for channel in user_channels:
        channel_info = data.get_channel_info(channel["channel_id"])
        for message in channel_info["messages"].values():
            print(message['message'])
            if query_str in message["message"]:
                messages.append(message)

    return {'messages' : messages}
