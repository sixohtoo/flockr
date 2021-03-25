"""
data(data.py): Gives access to global data variable
validation(validation.py): Gives access to validate functions
error(error.py): Gives access to error classes
"""
import data
import validation
from error import InputError, AccessError

def channel_invite(token, channel_id, u_id):
    """
    Invites a user (with user id u_id) to join a channel with ID channel_id.
    Once invited the user is added to the  channel immediately

    Parameters:
        token(string): an authorisation hash
        channel_id(int): identifier for channel
        u_id(int): Identifier for user

    Returns:
        Nothing
    """
    # Check if token is valid
    inviter_uid = validation.check_valid_token(token)

    # Check if given valid channel_id
    validation.check_valid_channel_id(channel_id)

    # Check if is authorised(member of channel)
    validation.check_user_in_channel(inviter_uid, channel_id)
        
    # Check if given valid u_id
    validation.check_valid_u_id(u_id)
    
    # Check if invitee is already part of channel. If so,raise input error
    validation.check_is_not_existing_channel_member(u_id, channel_id)
      
    # Everything valid, Proceed with adding to channel
    data.channel_add_member(channel_id, u_id) 
    return {
    }

def channel_details(token, channel_id):
    """
    Checks that given information (token, channel_id, u_id) is valid then 
    given a Channel with ID channel_id that the authorised user is part of,
    provide basic details about the channel

    Parameters:
        token(string): an authorisation hash
        channel_id(int): identifier for channel

    Returns:
        (dict): { name, owner_members, all_members }
    """
    # Check if token is valid
    u_id = validation.check_valid_token(token)

    # Check if given valid channel_id
    validation.check_valid_channel_id(channel_id)
      
    # Check if user is authorised(member of channel)
    validation.check_user_in_channel(u_id, channel_id)

    # Everything valid, Proceed with getting details
    channel_info = {
        "name" : "",
        "owner_members" : [],
        "all_members" : []
    }
    # Find channel and copy infomation into channel_details
    channel = data.get_channel_info(channel_id)
    channel_info["name"] = channel["name"]
    for u_id in channel["members"]:
        user = data.get_user_info(u_id)
        member = {}
        member["u_id"] = user["u_id"]
        member["name_first"] = user["name_first"]
        member["name_last"] = user["name_last"]
        member["name_last"] = user["name_last"]
        member["profile_img_url"] = user["profile_img_url"]
        channel_info["all_members"].append(member)

    for u_id in channel["owners"]:
        user = data.get_user_info(u_id)
        owner = {}
        owner["u_id"] = user["u_id"]
        owner["name_first"] = user["name_first"]
        owner["name_last"] = user["name_last"]
        owner["profile_img_url"] = user["profile_img_url"]
        channel_info["owner_members"].append(owner)
    return channel_info

def channel_messages(token, channel_id, start):
    """
    Checks that given information (token, channel_id, u_id) is valid then 
    given a Channel with ID channel_id that the authorised user is part of,
    return up to 50 messages between index "start" and "start + 50". Message
    with index 0 is the most recent message in the channel. This function
    returns a new index "end" which is the value of "start + 50", or, if this
    function has returned the least recent messages in the channel, returns -1
    in "end" to indicate there are no more messages to load after this return.

    Parameters:
        token(string): an authorisation hash
        channel_id(int): identifier for channel
        start(int): index of starting message

    Returns:
        (dict): {messages, start, end}
    """
    # Check if valid token
    u_id = validation.check_valid_token(token)

    # Check if given valid channel_id
    validation.check_valid_channel_id(channel_id)

    # Check if user is authorised(member of channel)
    validation.check_user_in_channel(u_id, channel_id)

    # Proceed to getting messages
    messages_list = {
        "messages" : [],
        "start" : start,
        "end": start + 50
    }

    channel = data.get_channel_info(channel_id)
    # Checking if start value is greater than number of total messages 
    # and if so, raise Input Error
    if len(channel["messages"]) < start:
        raise InputError(description = "Start value is too high")
    for message in reversed(list(channel["messages"].keys())[start:start + 50]):   
        
        for react in channel["messages"][message]["reacts"]:
            if u_id in react['u_ids']:
                react['is_this_user_reacted'] = True
            else:
                react['is_this_user_reacted'] = False

        messages_list["messages"].append(channel["messages"][message])
    # Returns -1 when "end" is less than start + 50 and no more messages
    # to load
    if len(channel["messages"]) < start + 50:
        messages_list["end"] = -1
    return messages_list

def channel_leave(token, channel_id):
    """
    Checks if user is in channel, then removes the user from the channel

    Parameters:
        token(string): An authorisation hash
        channel_id(int): Identifier for channels

    Returns:
        Empty dictionary
    """
    # Check valid token
    u_id = validation.check_valid_token(token)

    # Check if given valid channel_id
    validation.check_valid_channel_id(channel_id)

    # Check if token is valid and user is authorised(member of channel)
    validation.check_user_in_channel(u_id, channel_id)

    # Everything valid, Proceed with leaving channel
    data.channel_remove_member(channel_id, u_id)
    return {}

def channel_join(token, channel_id):
    """
    Given a channel_id of a channel that the authorised user can join,
    adds them to that channel

    Parameters:
        token(string): an authorisation hash
        channel_id(int): identifier for channel

    Returns:
        Nothing
    """
    # Check valid token
    user_id = validation.check_valid_token(token)

    # Checks channel exists
    validation.check_valid_channel_id(channel_id)

    #Checks the person wasn"t already in the channel
    validation.check_is_not_existing_channel_member(user_id, channel_id)
       
    validation.check_channel_is_public(channel_id)
    #Checks the channel is public and adds the user to the members
    data.channel_add_member(channel_id, user_id)
    return {}

def channel_addowner(token, channel_id, u_id):
    """
    Make user with user id u_id an owner of this channel

    Parameters:
        token(string): an authorisation hash. (Current owner)
        channel_id(int): identifier for channel
        u_id(int): Identifier for user. (New owner)

    Returns:
        Nothing
    """
    #owner_id = token_to_id(token)
    # Check if token is valid
    owner_id = validation.check_valid_token(token)

    #checks the owner is an owner of the channel
    validation.check_is_channel_owner(owner_id, channel_id)

    #checks the member is a member of the channel
    validation.check_user_in_channel(u_id, channel_id)

    #checks the member is not already an owner
    validation.check_isnot_channel_owner(u_id, channel_id)

    #Will change the u_id from member to owner
    data.channel_add_owner(channel_id, u_id)
    return {}

def channel_removeowner(token, channel_id, u_id):
    """
    Remove user with user id u_id an owner of this channel

    Parameters:
        token(string): an authorisation hash. (Remains owner)
        channel_id(int): identifier for channel
        u_id(int): Identifier for user. (Will no longer be owner)

    Returns:
        Nothing
    """
    # Check if token is valid
    owner_id = validation.check_valid_token(token)

    #checks the owner is an owner of the channel
    validation.check_is_channel_owner(owner_id, channel_id)

    #checks the u_id is an owner of the channel
    validation.check_is_channel_owner(u_id, channel_id)

    #Will change the u_id from member to owner
    data.channel_remove_owner(channel_id, u_id)
    return {}
