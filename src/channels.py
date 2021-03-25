"""
data(data.py): Gives access to global data variable
error(error.py): Gives access to error classes
validation(validation.py): Gives access to validate functions
hangman(hangman.py): Gives access to hangman functions
"""
import data
from error import InputError, AccessError
import validation
import hangman

def channels_list(token):
    """
    Returns a list of all channels the user is a part of

    Parameters:
        token(string): A user authorisation hash

    Returns:
        List of channel dictionaries containing channel_id and name
    """
    # Check if token is valid
    u_id = validation.check_valid_token(token)

    return data.channels_list_user(u_id)

def channels_listall(token):
    """
    Returns a list of all channels after checking whether token is valid

    Parameters:
        token(string): A user authorisation hash

    Returns:
        List of channel dictionaries containing channel_id and name
    """
    # Check if token is valid
    validation.check_valid_token(token)

    return data.channels_list_all()

def channels_create(token, name, is_public):
    """
    Checks information given is valid, then creates a new channel

    Parameters:
        token(string): A user authorisation hash
        name(string): Name of channel
        is_public(boolean): True if channel should be public

    Returns:
        Dictionary with information about the created channel
    """
    # Check if token is valid
    u_id = validation.check_valid_token(token)

    # Returns InputError if channel name is more than 20 characters
    if len(name) > 20:
        raise InputError(description = "Name cannot be more than 20 characters long")

    # Creates a new channel and stores to "channels" in data.py
    new_channel = {
        "channel_id" : data.get_num_channels() + 1,
        "name" : name,
        "is_public" : is_public,
        "owners" : {u_id},
        "members" : {u_id},
        "messages" : {},
        "hangman" : hangman.init()
    }
    data.channel_create(new_channel)

    # Stores channel as part of the user"s channel list
    user = data.get_user_info(u_id)
    data.update_user_channel_list(user, new_channel["channel_id"])

    return {
        "channel_id": new_channel["channel_id"]
    }
