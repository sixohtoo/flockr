"""
Contains all the functions used in story_test.py.
I copied them to here to save space for extra tests (without hitting 1000 line limit)
"""
import requests
import datetime

def assert_different_people(user1, user2):
    """
    Takes 2 user dictionaries and asserts they are
    2 different people with unique attributes
    """
    assert user1 != user2
    assert user1["u_id"] != user2["u_id"]
    assert user1["token"] != user2["token"]
    assert user1["token"] is not None
    assert user2["token"] is not None
    assert user1["u_id"] is not None
    assert user2["u_id"] is not None
    assert len(user1) == 2
    assert len(user2) == 2

def time_from_now(seconds):
    """
    returns a unix timestamp for x seconds in the future
    """
    now = datetime.datetime.now()
    future = now + datetime.timedelta(seconds=seconds)
    return future.timestamp()

def register_user(name_first, name_second, email, password, url):
    """
    Takes information about a user and registers them
    """
    user_reg = {
        "name_first" : name_first,
        "name_last" : name_second,
        "email" : email,
        "password" : password
        }
    resp = requests.post(url + "/auth/register", json = user_reg)
    return resp.json()

def logout_user(token, url):
    """
    Takes information about a user and logs them out
    """
    logout_info = {
        "token" : token
    }
    resp = requests.post(url + "/auth/logout", json = logout_info)
    return resp.json()

def login_user(email, password, url):
    """
    Takes information about a user and logs them in
    """
    login_info = {
        "email" : email,
        "password" : password
    }
    resp = requests.post(url + "/auth/login", json = login_info)
    return resp.json()

def create_channel(token, name, is_public, url):
    """
    Takes information about a channel and creates it
    """
    channel_info = {
        "token" : token,
        "name" : name,
        "is_public" : is_public
    }
    resp = requests.post(url + "/channels/create", json = channel_info)
    chan_dict = resp.json()
    return chan_dict['channel_id']

def channel_list(token, url):
    list_info = {
        'token' : token
    }
    resp = requests.get(url + "/channels/list", params = list_info)
    list_dict = resp.json()
    return list_dict['channels']

def channel_listall(token, url):
    list_info = {
        'token' : token
    }
    resp = requests.get(url + "/channels/listall", params = list_info)
    listall_dict = resp.json()
    return listall_dict['channels']

def join_channel(token, channel_id, url):
    """
    Takes information about user and channel and adds them
    """
    join_info = {
        "token" : token,
        "channel_id" : channel_id,
    }
    resp = requests.post(url + "/channel/join", json = join_info)
    return resp.json()

def invite_channel(token, channel_id, u_id, url):
    invite_info = {
        "token" : token,
        "channel_id" : channel_id,
        "u_id" : u_id
    }
    resp = requests.post(url + "/channel/invite", json = invite_info)
    return resp.json()

def leave_channel(token, channel_id, url):
    leave_info = {
        'token' : token,
        'channel_id' : channel_id
    }
    resp = requests.post(url + "/channel/leave", json = leave_info)
    return resp.json()

def check_messages(token, channel_id, start, url):
    """
    Takes information about channel and returns a list of messages
    """
    chan_info = {
        "token" : token,
        "channel_id" : channel_id,
        "start" : start
    }
    resp = requests.get(url + "/channel/messages", params = chan_info)
    return resp.json()

def channel_info(token, channel_id, url):
    chan_info = {
        "token" : token,
        "channel_id" : channel_id
    }
    resp = requests.get(url + "/channel/details", params = chan_info)
    return resp.json()

def add_owner(token, channel_id, u_id, url):
    add_info = {
        "token" : token,
        "channel_id" : channel_id,
        "u_id" : u_id
    }
    resp = requests.post(url + "/channel/addowner", json = add_info)
    return resp.json()

def remove_owner(token, channel_id, u_id, url):
    remove_info = {
        "token" : token,
        "channel_id" : channel_id,
        "u_id" : u_id
    }
    resp = requests.post(url + "/channel/removeowner", json = remove_info)
    return resp.json()

def send_message(token, channel_id, message, url):
    """
    Takes information about a messag and sends it to the channel
    """
    mess_info = {
        "token" : token,
        "channel_id" : channel_id,
        "message" : message
    }
    resp = requests.post(url + "/message/send", json = mess_info)
    message_dict = resp.json()
    if len(message_dict) == 1:
        return message_dict['message_id']
    return message_dict

def remove_message(token, message_id, url):
    remove_info = {
        "token" : token,
        "message_id" : message_id
    }
    resp = requests.delete(url + "/message/remove", json = remove_info)
    return resp.json()

def edit_message(token, message_id, message, url):
    edit_info = {
        "token" : token,
        "message_id" : message_id,
        "message" : message
    }
    resp = requests.put(url + "/message/edit", json = edit_info)
    return resp.json()

def react_message(token, message_id, react_id, url):
    react_info = {
        "token" : token,
        "message_id" : message_id,
        "react_id" : react_id
    }
    resp = requests.post(url + '/message/react', json = react_info)
    return resp.json()

def unreact_message(token, message_id, react_id, url):
    unreact_info = {
        "token" : token,
        "message_id" : message_id,
        "react_id" : react_id
    }
    resp = requests.post(url + '/message/unreact', json = unreact_info)
    return resp.json()

def pin_message(token, message_id, url):
    pin_info = {
        "token" : token,
        "message_id" : message_id
    }
    resp = requests.post(url + "/message/pin", json = pin_info)
    return resp.json()

def unpin_message(token, message_id, url):
    unpin_info = {
        "token" : token,
        "message_id" : message_id
    }
    resp = requests.post(url + "/message/unpin", json = unpin_info)
    return resp.json()

def send_later(token, channel_id, message, time_sent, url):
    later_info = {
        "token" : token,
        "channel_id" : channel_id,
        "message" : message,
        "time_sent" : time_sent
    }
    resp = requests.post(url + "/message/sendlater", json = later_info)
    later_dict = resp.json()
    return later_dict['message_id']

def check_profile(token, u_id, url):
    profile_info = {
        "token" : token,
        "u_id" : u_id
    }
    resp = requests.get(url + "/user/profile", params = profile_info)
    profile_dict = resp.json()
    return profile_dict['user']

def change_name(token, first, last, url):
    name_info = {
        "token" : token,
        "name_first" : first,
        "name_last" : last
    }
    resp = requests.put(url + "/user/profile/setname", json = name_info)
    return resp.json()

def change_handle(token, handle, url):
    handle_info = {
        "token" : token,
        "handle_str" : handle
    }
    resp = requests.put(url + "/user/profile/sethandle", json = handle_info)
    return resp.json()

def change_email(token, email, url):
    email_info = {
        "token" : token, 
        "email" : email
    }
    resp = requests.put(url + "/user/profile/setemail", json = email_info)
    return resp.json()

def search_message(token, query, url):
    search_info = {
        "token" : token, 
        "query_str" : query
    }
    resp = requests.get(url + "/search", params = search_info)
    search_dict = resp.json()
    return search_dict['messages']

def change_permission(token, u_id, perm_id, url):
    perm_info = {
        "token" : token,
        "u_id" : u_id,
        "permission_id" : perm_id
    }
    resp = requests.post(url + "/admin/userpermission/change", json = perm_info)
    return resp.json()

def user_list(token, url):
    list_info = {
        "token" : token
    }
    resp = requests.get(url + "/users/all", params = list_info)
    user_dict = resp.json()
    return user_dict['users']

def start_standup(token, channel_id, length, url):
    start_info = {
        "token" : token,
        "channel_id" : channel_id,
        "length" : length
    }
    resp = requests.post(url + "/standup/start", json = start_info)
    stan_info = resp.json()
    return stan_info['time_finish']

def get_standup(token, channel_id, url):
    get_info = {
        "token" : token, 
        "channel_id" : channel_id
    }
    resp = requests.get(url + "/standup/active", params = get_info)
    return resp.json()

def send_standup(token, channel_id, message, url):
    send_info = {
        "token" : token,
        "channel_id" : channel_id,
        "message" : message
    }
    resp = requests.post(url + "/standup/send", json = send_info)
    return resp.json()