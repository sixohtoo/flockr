"""
    datetime: Gives access to datetime functions to compare with standup function returns
    pytest: Gives access to pytest command (for testing)
    channel(channel.py): Gives access to channel functions
    auth(auth.py): Gives access to register, login and logout functions
    channels(channels.py): Gives access to channel_create
    standup(standup.py): Gives access to standup_start, standup_active, standUp_send
    other(other.py): Gives access to other.clear command
    error(error.py): Gives access to error classes
"""

import time
import datetime
import pytest
import channel
import auth
import user
import channels
import standup
import other
from error import InputError, AccessError

# Successful
def test_start_valid():
    """
    Tests standup_start is returns the valid end time
    """
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_channel_id = channels.channels_create(user_channel_creater["token"], "test", True)
    currtime = datetime.datetime.now().replace().timestamp()
    standup_time = standup.standup_start(user_channel_creater["token"], test_channel_id["channel_id"], 1)
    # Asserts the time given is between 1 second ahead and less then 2 seconds ahead
    assert currtime + 1 <= standup_time["time_finish"]
    assert currtime + 2 > standup_time["time_finish"]
    other.clear()

def test_start_invalid_same_channel():
    """
    Tests two standups cannot be started at the same time in the same channel
    """
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    test_channel_id = channels.channels_create(user_channel_creater["token"], "test", True)
    channel.channel_join(test_user1["token"], test_channel_id["channel_id"])
    standup.standup_start(user_channel_creater["token"], test_channel_id["channel_id"], 1)
    with pytest.raises(InputError):
        standup.standup_start(test_user1["token"], test_channel_id["channel_id"], 1)
    other.clear()

def test_start_invalid_no_channel():
    """
    Tests an error is raised when an invalid channel is given
    """
    test_user1 = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    with pytest.raises(InputError):
        standup.standup_start(test_user1["token"], 4, 1)
    other.clear()

def test_start_diff_channel():
    """
    Tests if two standups can be started in two different channels
    """
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_channel_id1 = channels.channels_create(user_channel_creater["token"], "test1", True)
    test_channel_id2 = channels.channels_create(user_channel_creater["token"], "test2", True)
    standup.standup_start(user_channel_creater["token"], test_channel_id1["channel_id"], 1)
    standup.standup_start(user_channel_creater["token"], test_channel_id2["channel_id"], 1)
    other.clear()

def test_start_not_in_channel():
    """
    Tests a person not in the channel cannot start the standup
    """
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    test_channel_id1 = channels.channels_create(user_channel_creater["token"], "test1", True)
    with pytest.raises(AccessError):
        standup.standup_start(test_user1["token"], test_channel_id1["channel_id"], 1)
    other.clear()

def test_start_no_standup_sent():
    """
    Checks no message is printed if there were no standup_sends called
    """
    channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_channel_id1 = channels.channels_create(channel_creater["token"], "test1", True)
    standup.standup_start(channel_creater["token"], test_channel_id1["channel_id"], 1)
    time.sleep(2)
    message_from_channel = channel.channel_messages(channel_creater["token"],
                                                    test_channel_id1["channel_id"], 0)
    assert len(message_from_channel["messages"]) == 0
    other.clear()

def test_active_valid():
    """
    Tests if the standup_active can correctly determine when a standup is occuring
    """
    channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_channel_id1 = channels.channels_create(channel_creater["token"], "test1", True)
    before_start = standup.standup_active(channel_creater["token"], test_channel_id1["channel_id"])
    assert before_start["is_active"] is False
    assert before_start["time_finish"] is None
    stand_time = standup.standup_start(channel_creater["token"], test_channel_id1["channel_id"], 1)
    after_start = standup.standup_active(channel_creater["token"], test_channel_id1["channel_id"])
    assert after_start["is_active"] is True
    assert after_start["time_finish"] == stand_time["time_finish"]
    time.sleep(2)
    after_end = standup.standup_active(channel_creater["token"], test_channel_id1["channel_id"])
    assert after_end["is_active"] is False
    assert after_end["time_finish"] is None
    other.clear()

def test_active_not_in_channel():
    """
    Tests if standup_active returns an access error when called by a user not in the channel
    """
    channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    test_channel_id1 = channels.channels_create(channel_creater["token"], "test1", True)
    standup.standup_start(channel_creater["token"], test_channel_id1["channel_id"], 1)
    with pytest.raises(AccessError):
        standup.standup_active(test_user1["token"], test_channel_id1["channel_id"])
    other.clear()

def test_active_inavalid_channel_id():
    """
    Tests if standup_active returns an input error if a invalid channel_id is given
    """
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    with pytest.raises(InputError):
        standup.standup_active(test_user1["token"], 1)
    other.clear()

def test_send_valid():
    """
    Tests if standup_send will send a message after the alloted time
    """
    channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_channel_id1 = channels.channels_create(channel_creater["token"], "test1", True)
    standup.standup_start(channel_creater["token"], test_channel_id1["channel_id"], 1)
    creater_profile = user.user_profile(channel_creater["token"], channel_creater["u_id"])
    new_message = "Know the new message"
    standup.standup_send(channel_creater["token"], test_channel_id1["channel_id"], new_message)
    inserted_message = creater_profile["user"]["handle_str"] + ": " + new_message + "\n"
    time.sleep(2)
    message_from_channel = channel.channel_messages(channel_creater["token"],
                                                    test_channel_id1["channel_id"], 0)
    assert inserted_message == message_from_channel["messages"][0]["message"]
    assert channel_creater["u_id"] == message_from_channel["messages"][0]["u_id"]
    other.clear()

def test_send_multiple():
    """
    Test if the standup_send can combine multiple message from send message
    """
    channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    test_channel_id1 = channels.channels_create(channel_creater["token"], "test1", True)
    channel.channel_join(test_user1["token"], test_channel_id1["channel_id"])
    standup.standup_start(channel_creater["token"], test_channel_id1["channel_id"], 1)
    creater_profile = user.user_profile(channel_creater["token"], channel_creater["u_id"])
    test_user_profile = user.user_profile(test_user1["token"], test_user1["u_id"])
    new_message = "Know the new message"
    new_message2 = "Second message"
    standup.standup_send(channel_creater["token"], test_channel_id1["channel_id"], new_message)
    standup.standup_send(test_user1["token"], test_channel_id1["channel_id"], new_message2)
    inserted_message = creater_profile["user"]["handle_str"] + ": " + new_message + "\n"
    inserted_message += test_user_profile["user"]["handle_str"] + ": " + new_message2 + "\n"
    time.sleep(2)
    message_from_channel = channel.channel_messages(channel_creater["token"],
                                                    test_channel_id1["channel_id"], 0)
    assert inserted_message == message_from_channel["messages"][0]["message"]
    assert channel_creater["u_id"] == message_from_channel["messages"][0]["u_id"]
    other.clear()

def test_send_too_long():
    """
    Test if an error is raised if message is too long
    """
    channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_channel_id1 = channels.channels_create(channel_creater["token"], "test1", True)
    standup.standup_start(channel_creater["token"], test_channel_id1["channel_id"], 1)
    message_exp = (
        "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula "
        "eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient "
        "montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, "
        "pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, "
        "aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis "
        "vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras "
        "dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo "
        "ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus "
        "in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. "
        "Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper "
        "ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum "
        "rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum...12345"
    )
    with pytest.raises(InputError):
        standup.standup_send(channel_creater["token"], test_channel_id1["channel_id"], message_exp)
    other.clear()

def test_send_invalid_channel_id():
    """
    Test if an error is raised if the channel id is invalid
    """
    channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_channel_id1 = channels.channels_create(channel_creater["token"], "test1", True)
    standup.standup_start(channel_creater["token"], test_channel_id1["channel_id"], 1)
    message_exp = "known little message"

    with pytest.raises(InputError):
        standup.standup_send(channel_creater["token"], 10, message_exp)
    other.clear()

def test_send_no_active_standup():
    """
    Test if an error is raised if there is no running standup
    """
    channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_channel_id1 = channels.channels_create(channel_creater["token"], "test1", True)
    message_exp = "Not Large Message"
    with pytest.raises(InputError):
        standup.standup_send(channel_creater["token"], test_channel_id1["channel_id"], message_exp)
    other.clear()

def test_send_not_in_channel():
    """
    Test if an error is raised if the sender is not in the channel
    """
    channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    test_channel_id1 = channels.channels_create(channel_creater["token"], "test1", True)
    standup.standup_start(channel_creater["token"], test_channel_id1["channel_id"], 1)
    message_exp = "Not Large Message"
    with pytest.raises(AccessError):
        standup.standup_send(test_user1["token"], test_channel_id1["channel_id"], message_exp)
    other.clear()

if __name__ == "__main__":
    test_active_valid()
    print("pickl")
