"""
Tests for data.py functions
	pytest: Gives access to pytest command (for testing)
    auth(auth.py): Gives access to auth functions
    channel(channel.py): Gives access to channel functions
    channels(channels.py): Gives access to channel_create
    other(other.py): Gives access to other.clear command
    error(error.py): Gives access to error classes
    user(user.py): Gives access to user functions
    data(data.py): Gives access to global data variable
    message(message.py): Gives access to message functions (send, edit, remove)
    datetime: Gives access to the datetime functions
    threading: Gives access to threading functions
"""
from error import AccessError, InputError
import data
import auth
import channels
import other
import channel
import message
import user
import datetime
import pytest
import threading

@pytest.fixture
def user1():
    """
    Pytest fixture that automatically registers a user and returns their info
    """
    user = auth.auth_register("kevin@gmail.com", "kh12345", "Kevin", "Huang")
    user1 = data.get_user_info(user["u_id"])
    return user1

@pytest.fixture
def channel1():
    """
    Pytest fixture that automatically registers a user
    and creates a channel. It returns a channel dictionary
    """
    user = auth.auth_register("kevin@gmail.com", "kh12345", "Kevin", "Huang")
    channel = channels.channels_create(user["token"], "test_channel", True)
    return channel


def test_get_user_with(user1):
    """
    Returns user when given correct attribute, otherwise returns none
    """    
    assert data.get_user_with({"email":"kevin@gmail.com"})
    assert data.get_user_with({"email":"doesntexist@gmail.com"}) == None
    
    other.clear()

def test_get_user_info(user1):
    """
    Returns user's info when given correct u_id, otherwise returns none
    """ 
    assert data.get_user_info(user1["u_id"]) 
    assert data.get_user_info(2) == None
    
    other.clear()

def test_update_user(user1):
    """
    Updates attribute of user. Returns nothing
    """
    user_info = data.get_user_info(user1["u_id"])
    data.update_user(user_info,{"name_last":"Hang"})
    assert data.get_user_with({"name_last": "Hang"}) == user_info #data.users[1]
    
    other.clear()

def test_update_user_channel_list(user1):
    """
    Adds channel id to user's channel list. Returns nothing
    """
    user_info = data.get_user_info(user1["u_id"])
    data.update_user_channel_list(user_info, 52)
    assert data.users[user1["u_id"]]["channel_list"] == {52}
    
    other.clear()

def test_register_user(user1):
    """
    Checks if user has been adding to existing list of users
    """
    assert data.users[user1["u_id"]]["u_id"] == user1["u_id"]
    
    other.clear()

def test_login_user(user1):
    """
    Check if user has been logged in
    """
    data.logout_user(user1["u_id"])
    data.login_user(user1["u_id"])
    assert data.check_logged_in(user1["u_id"]) is True
    
    other.clear()

def test_check_logged_in(user1):
    """
    Check if checking user is logged in works
    """
    assert data.check_logged_in(user1["u_id"]) is True
    
    other.clear()

def test_logout_user(user1):
    """
    Check if user has been logged out
    """
    data.logout_user(user1["u_id"])
    assert data.check_logged_in(user1["u_id"]) is False
    
    other.clear()

def test_get_channel_info(channel1):
    """
    Returns channel info when given corresponding channel_id
    """
    channel_id = channel1["channel_id"]
    assert data.get_channel_info(channel_id) == data.channels[channel_id]
    assert data.get_channel_info(561) == None
    
    other.clear()

def test_channel_add_member(channel1):
    """
    Adds given member to the given channel
    """
    channel_id = channel1["channel_id"]
    user2 = auth.auth_register("Elliot@hotmail.com", "password123", "Elliot", "Rottenstein")
    data.channel_add_member(channel_id, user2["u_id"])
    assert data.check_user_in_channel(channel_id, user2["u_id"]) == True
    
    other.clear()

def test_check_user_in_channel(channel1):
    """
    Returns True if user is member of channel
    """
    channel_id = channel1["channel_id"]
    assert data.check_user_in_channel(channel_id, 1) == True
    assert data.check_user_in_channel(channel_id, 643) == False
    
    other.clear()
    
def test_check_channel_owner(channel1):
    """
    Returns True if user is owner of channel
    """
    channel_id = channel1["channel_id"]
    assert data.check_channel_owner(channel_id, 1) == True
    assert data.check_channel_owner(channel_id, 643) == False
    
    other.clear()

def test_channel_add_owner(channel1):
    """
    Adds user to list of owners in channel, returns nothing
    """
    channel_id = channel1["channel_id"]
    user2 = auth.auth_register("Elliot@hotmail.com", "password123", "Elliot", "Rottenstein")
    data.channel_add_owner(channel_id,user2["u_id"])
    assert data.check_channel_owner(channel_id, user2["u_id"]) == True
    
    other.clear()

def test_channel_remove_member(channel1):
    """
    Removes member from channel, returns nothing
    """
    channel_id = channel1["channel_id"]
    user = data.get_user_info(1)
    data.channel_remove_member(channel_id, user["u_id"])
    
    assert data.check_user_in_channel(channel_id, user["u_id"]) == False
    user2 = auth.auth_register("gmail@gmail.com", "google", "Alphabet", "Gamma")
    channel.channel_join(user2["token"], channel_id)
    data.channel_remove_member(channel_id, user2["u_id"])
    assert data.check_user_in_channel(channel_id, user2["u_id"]) == False
    
    other.clear()


def test_channel_remove_owner(channel1):
    """
    Removes member as an owner, returns nothing
    """
    channel_id = channel1["channel_id"]
    user = data.get_user_info(1)
    data.channel_remove_owner(channel_id, user["u_id"])
    assert data.check_channel_owner(channel_id, user["u_id"]) == False
    
    other.clear()

def test_get_message_num(channel1):
    """
    Return the value of message_num
    """
    channel_id = channel1["channel_id"]
    user2 = auth.auth_register("elliot@balgara.com", "Dipdop", "Elliot", "REDACTED")
    channel.channel_join(user2["token"], channel_id)
    assert data.get_message_num() == 0
    message.message_send(user2["token"], channel_id, "Welcome to the HHGTTG by Doug")
    assert data.get_message_num() == 1
    
    other.clear()

def test_get_num_users(user1):
    """
    Return the number of total users
    """
    assert data.get_num_users () == 1
    auth.auth_register("Awhole@new.wor","ldsomething", "abouta", "flyingcarpet")
    assert data.get_num_users() == 2
    
    other.clear()

def test_make_message_id():
    """
    Returns a unique message_id for a new message
    """
    assert data.make_message_id() == 1
    assert data.make_message_id() == 2
    assert data.make_message_id() == 3
    
    other.clear()

def test_get_num_channels(channel1):  
    """
    Returns the total number of channels
    """
    user2 = auth.auth_register("Elliot@hotmail.com", "password123", "Elliot", "Rottenstein")
    assert data.get_num_channels() == 1
    channels.channels_create(user2["token"], "nicecenew", True)
    assert data.get_num_channels() == 2
    
    other.clear()


def test_find_channel(channel1):
    """
    Returns channel_id of channel that contains the message_id
    """
    user2 = auth.auth_register("elliot@coldmail.com", "123password", "Elliot", "Rotensttein")
    channel.channel_join(user2["token"], channel1["channel_id"])
    message1 = message.message_send(user2["token"], channel1["channel_id"], "G\'day")
    assert data.find_channel(message1["message_id"]) == channel1["channel_id"]
    
    other.clear()


def test_get_message(channel1):
    """
    Given channel containing message and message_id,
    returns dictionary containing message info
    """
    channel_id = channel1["channel_id"]
    message_text = "G\'day"
    user2 = auth.auth_register("elliot@coldmail.com", "123password", "Elliot", "Rotensttein")
    channel.channel_join(user2["token"], channel_id)
    sent_message = message.message_send(user2["token"], channel_id, message_text)
    message_info =  data.get_message(channel_id, sent_message["message_id"])
    
    assert message_info["message_id"] == sent_message["message_id"]
    assert message_info["message"] == message_text
    assert message_info["u_id"] == user2["u_id"]
    
    other.clear()

def test_add_message():
    """
    Add_message always returns None, but we can test it
    by checking if the number of messages changes after add_message is run.
    """
    # Need user token so can't use user1 pytest fixture
    user = auth.auth_register("test@gmail.com", "testing", "anew", "user")
    chan1 = channels.channels_create(user["token"], "green", True)
    assert data.get_message_num() == 0
    fake_message = {
        "message" : "Pretend this is legit", 
        "u_id" : user["u_id"],
        "time_created" : datetime.datetime.now(),
        "message_id" : data.make_message_id()
    }
    
    assert data.add_message(fake_message, chan1["channel_id"]) == None
    assert data.get_message_num() == 1
    
    other.clear()

def test_remove_message():
    """
    Remove_message always returns None, but we can test it
    by checking if the number of messages changes after remove_message is run.
    """
    # Need user token so can't use user1 pytest fixture
    user = auth.auth_register("test@gmail.com", "testing", "anew", "user")
    chan1 = channels.channels_create(user["token"], "green", True)
    mess1 = message.message_send(user["token"], chan1["channel_id"], "Greetings from earth...")
    assert data.get_message_num() == 1
    assert data.remove_message(mess1["message_id"], chan1["channel_id"]) == None
    assert data.get_message_num() == 1 # get_message_num returns total amount of created messages
    
    other.clear()

def test_edit_message():
    """
    Remove_message always returns None, but we can test it
    by checking if the number of messages changes after remove_message is run.
    """
    # Need user token so can't use user1 pytest fixture
    user = auth.auth_register("bananas@gmail.com", "in pajamas", "are", "coming")
    chan1 = channels.channels_create(user["token"], "down", True)
    mess1 = message.message_send(user["token"], chan1["channel_id"], "the stairs")
    assert data.get_message_num() == 1
    new_message = "through the door"
    assert data.edit_message(chan1["channel_id"], mess1["message_id"],new_message) == None
    message_info = data.get_message(chan1["channel_id"], mess1["message_id"])
    assert message_info["message"] == new_message
    assert data.get_message_num() == 1
    
    other.clear()

def test_user_list():
    """
    Returns a list of all registered users
    """
    user1 = auth.auth_register("gmail@gmail.com", "google", "Alphabet", "Gamma")
    list1 = data.user_list()
    user_info = user.user_profile(user1["token"], user1["u_id"])["user"]
    assert list1 == [user_info]
    user2 = auth.auth_register("bikini@bottom.com","squidward", "patrick", "star")
    user2_info = user.user_profile(user2["token"], user2["u_id"])["user"]
    list2 = data.user_list()
    assert list2 == [user_info, user2_info]
    
    other.clear()

def test_change_permission(user1):
    """
    Changes user"s serverwide permissions
    to whatever was specified
    """
    user2 = auth.auth_register("Mike@MU.us", "Sullivan", "Mike", "Wazowski")
    # User2 is not owner, so can't remove owner
    with pytest.raises(AccessError):
        assert other.admin_userpermission_change(user2["token"], user1["u_id"], 2)
    # User1 is owner, so can add owner
    data.change_permission(user2["u_id"], 1)
    # User2 is owner so can remove owner (Would raise AccessError if 
    # change_permission didn't work as intended)
    assert other.admin_userpermission_change(user2["token"], user1["u_id"], 2) == {}

    other.clear()

def test_sendlater_functions():
    """
    Will test that the sendlater functions are run
    """
    timer_class = threading.Timer(60, timed_function)
    time = datetime.datetime.now().replace().timestamp()
    data.add_sendlater(timer_class, time)
    assert data.sendlater_not_empty() is True
    time_con = data.remove_sendlater()
    time_con["timer_class"].cancel()

def timed_function():
    """
    This function is run the test has failed
    """
    assert False is True
