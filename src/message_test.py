"""
    pytest: Gives access to pytest command (for testing)
    message(message.py): Gives access to message_send, message_remove, message_edit
    channel(channel.py): Gives access to channel functions
    auth(auth.py): Gives access to register, login and logout functions
    channels(channels.py): Gives access to channel_create
    other(other.py): Gives access to other.clear command
    error(error.py): Gives access to error classes
"""
import pytest
import message
import channel
import auth
import channels
import other
import datetime
import time
from error import InputError, AccessError

@pytest.fixture
def users():
    """
    Pytest fixture that automatically registers a user and returns their info
    """
    user1 = auth.auth_register("kevin@gmail.com", "kh12345", "Kevin", "Huang")
    user2 = auth.auth_register("weogweg@hotmail.com", "egwegewg", "Kevin", "Huang")
    chan = channels.channels_create(user1["token"], "test_channel", True)
    channel.channel_join(user2["token"], chan["channel_id"])
    users_and_channel = (user1, user2, chan)
    return users_and_channel

@pytest.fixture
def user1():
    """
    Pytest fixture that automatically registers a user and returns their info
    """
    user1 = auth.auth_register("kevin@gmail.com", "kh12345", "Kevin", "Huang")
    chan = channels.channels_create(user1["token"], "test_channel", True)
    user_and_channel = (user1, chan)
    return user_and_channel

def time_from_now(seconds):
    """
    returns a unix timestamp for x seconds in the future
    """
    now = datetime.datetime.now()
    future = now + datetime.timedelta(seconds=seconds)
    return future.timestamp()

#Successful
def test_send_valid(user1):
    """
    Testing if a single message can be sent and be stored
    """
    user1, chan = user1
    message_exp = "Test 1 test 2 swiggity Swagg"
    message_id = message.message_send(user1["token"], chan['channel_id'], message_exp)
    message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)

    assert message_exp == message_from_channel["messages"][0]["message"]
    assert user1["u_id"] == message_from_channel["messages"][0]["u_id"]
    assert message_id["message_id"] == message_from_channel["messages"][0]["message_id"]
    other.clear()

def test_send_valid_multiple(users):
    """
    Testing if multiple messages can be sent and stored in correct order
    """
    user1, user2, chan = users
    message_exp1 = "Test 1 bleep blop bloop"
    message_exp2 = "/weather Sydney"
    message_exp3 = "Test 3 FLip Flop Slop"
    message_exp4 = "Test 4 Gling glong glip"
    message_id1 = message.message_send(user1["token"], chan['channel_id'], message_exp1)
    message_id2 = message.message_send(user2["token"], chan['channel_id'], message_exp2)
    message_id3 = message.message_send(user2["token"], chan['channel_id'], message_exp3)
    message_id4 = message.message_send(user1["token"], chan['channel_id'], message_exp4)
    message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)

    assert message_exp1 == message_from_channel["messages"][3]["message"]
    assert user1["u_id"] == message_from_channel["messages"][3]["u_id"]
    assert message_id1["message_id"] == message_from_channel["messages"][3]["message_id"]
    assert user2["u_id"] == message_from_channel["messages"][2]["u_id"]
    assert message_id2["message_id"] == message_from_channel["messages"][2]["message_id"]
    assert message_exp3 == message_from_channel["messages"][1]["message"]
    assert user2["u_id"] == message_from_channel["messages"][1]["u_id"]
    assert message_id3["message_id"] == message_from_channel["messages"][1]["message_id"]
    assert message_exp4 == message_from_channel["messages"][0]["message"]
    assert user1["u_id"] == message_from_channel["messages"][0]["u_id"]
    assert message_id4["message_id"] == message_from_channel["messages"][0]["message_id"]
    other.clear()

def test_send_valid_long_message(users):
    """
    Testing if a 1000 character length message can be sent and be stored
    """
    user1, user2, chan = users
    #1000 character length string
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
        "rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum..."
    )
    message_id1 = message.message_send(user2["token"], chan['channel_id'], message_exp)
    message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)

    assert message_exp == message_from_channel["messages"][0]["message"]
    assert user2["u_id"] == message_from_channel["messages"][0]["u_id"]
    assert message_id1["message_id"] == message_from_channel["messages"][0]["message_id"]
    other.clear()

def test_send_invalid_long_message(users):
    """
    Testing if a message over 1000 characters can be sent and be stored
    """
    user1, user2, chan = users
    #1005 character length string
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
        "rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum... Long"
    )
    with pytest.raises(InputError):
        assert message.message_send(user2["token"], chan["channel_id"], message_exp)
    message_from_channel = channel.channel_messages(user1["token"], chan["channel_id"], 0)
    assert message_exp != message_from_channel["messages"]
    other.clear()

def test_send_not_in_channel(users):
    """
    Testing if a single message can be sent by someone not in the channel
    """
    user1, user2, chan = users
    channel.channel_leave(user2['token'], chan['channel_id'])
    #The user has not joined the channel
    message_exp = "I'm not in the channel sad boi "

    with pytest.raises(AccessError):
        assert message.message_send(user2["token"], chan["channel_id"], message_exp)
    message_from_channel = channel.channel_messages(user1["token"], chan["channel_id"], 0)
    assert message_exp != message_from_channel["messages"]
    other.clear()

def test_remove_valid_sender(users):
    """
    Testing if a single message can be sent, be stored and removed by sender
    """
    user1, user2, chan = users
    message_exp = "Test 1 test 2 swiggity Swagg"
    message_exp2 = "This is to stop there being no message in the channel"
    message_id = message.message_send(user2["token"], chan['channel_id'], message_exp)
    message.message_send(user1["token"], chan['channel_id'], message_exp2)
    message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)

    #Checks that the message was added
    assert message_exp == message_from_channel["messages"][1]["message"]
    assert user2["u_id"] == message_from_channel["messages"][1]["u_id"]
    assert message_id["message_id"] == message_from_channel["messages"][1]["message_id"]
    message.message_remove(user2["token"], message_id["message_id"])
    new_message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)

    #Checks that the message was removed
    assert message_exp != new_message_from_channel["messages"][0]["message"]
    assert user2["u_id"] != new_message_from_channel["messages"][0]["u_id"]
    assert message_id["message_id"] != new_message_from_channel["messages"][0]["message_id"]
    other.clear()

def test_remove_valid_owner(users):
    """
    Testing if a single message can be sent, be stored and removed by owner
    """
    user1, user2, chan = users
    message_exp2 = "Test this is different from message_exp"
    message.message_send(user1["token"], chan['channel_id'], message_exp2)
    message_exp = "Test 1 test 2 swiggity Swagg"
    message_id = message.message_send(user2["token"], chan['channel_id'], message_exp)
    message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)

    #Checks that the message was added
    assert message_exp == message_from_channel["messages"][0]["message"]
    assert user2["u_id"] == message_from_channel["messages"][0]["u_id"]
    assert message_id["message_id"] == message_from_channel["messages"][0]["message_id"]
    message.message_remove(user1["token"], message_id["message_id"])
    new_message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)

    #Checks that the message was removed
    assert message_exp != new_message_from_channel["messages"][0]["message"]
    assert user2["u_id"] != new_message_from_channel["messages"][0]["u_id"]
    assert message_id["message_id"] != new_message_from_channel["messages"][0]["message_id"]
    other.clear()

def test_remove_already_removed_message(users):
    """
    Testing if a message that has already been removed is removed again an input error appears
    """
    user1, user2, chan = users
    message_exp = "Test 1 test 2 swiggity Swagg"
    message_id = message.message_send(user2["token"], chan['channel_id'], message_exp)
    #Pre-removes the messages
    message.message_remove(user1["token"], message_id["message_id"])

    with pytest.raises(InputError):
        message.message_remove(user2["token"], message_id["message_id"])
    other.clear()

def test_remove_multiple_messages_valid(users):
    """
    Testing if a message can be removed then a new message added then the new message removed
    """
    user1, user2, chan = users
    message_exp = "Test 1 test 2 swiggity Swagg"
    message_id1 = message.message_send(user2["token"], chan['channel_id'], message_exp)

    #Pre-removes the message
    message.message_remove(user1["token"], message_id1["message_id"])
    message_exp10 = "Spagetti and memeballs"
    message_id2 = message.message_send(user2["token"], chan['channel_id'], message_exp10)
    message_exp2 = "Test this is different from message_exp"
    message.message_send(user1["token"], chan['channel_id'], message_exp2)
    message.message_remove(user2["token"], message_id2["message_id"])
    new_message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)

    assert message_exp != new_message_from_channel["messages"][0]["message"]
    assert user2["u_id"] != new_message_from_channel["messages"][0]["u_id"]
    assert message_id2["message_id"] != new_message_from_channel["messages"][0]["message_id"]
    other.clear()

def test_remove_same_message_multiple_message(users):
    """
    Testing is a message can be removed then a new messaged is added and try remove
    the old message again, this tests if the new id is not the same as the old id
    """
    user1, user2, chan = users
    message_exp = "Test 1 test 2 swiggity Swagg"
    message_id1 = message.message_send(user2["token"], chan['channel_id'], message_exp)

    #Pre-removes the message
    message.message_remove(user1["token"], message_id1["message_id"])
    message.message_send(user2["token"], chan['channel_id'], message_exp)

    with pytest.raises(InputError):
        message.message_remove(user2["token"], message_id1["message_id"])
    other.clear()

def test_remove_not_owner_not_sender(user1):
    """
    Tests that an error is raised when a person who is not the sender or owner is tries to
    remove a message
    """
    user2, chan = user1
    test_user2 = auth.auth_register("thebumble@hotmail.com", "password", "Bumble", "Bee")
    channel.channel_join(test_user2["token"], chan['channel_id'])
    message_exp = "Test 1 test 2 swiggity Swagg"
    message_id1 = message.message_send(user2["token"], chan['channel_id'], message_exp)

    with pytest.raises(AccessError):
        message.message_remove(test_user2["token"], message_id1["message_id"])
    other.clear()

# Successful
def test_edit_valid_sender(users):
    """
    Testing if a single message can be sent, be stored and editted by sender
    """
    user1, user2, chan = users
    message_exp = 'Test 1 test 2 swiggity Swagg'
    message_exp2 = 'This is to stop there being no message in the channel'
    message.message_send(user1['token'], chan['channel_id'], message_exp2)
    message_id = message.message_send(user2['token'], chan['channel_id'], message_exp)
    message_from_channel = channel.channel_messages(user1['token'], chan['channel_id'], 0)

    #Checks that the message was added
    assert message_exp == message_from_channel['messages'][0]['message']
    assert user2['u_id'] == message_from_channel['messages'][0]['u_id']
    assert message_id['message_id'] == message_from_channel['messages'][0]['message_id']
    new_message = "This is the new message"
    message.message_edit(user2['token'], message_id['message_id'], new_message)
    new_message_from_channel = channel.channel_messages(user1['token'], chan['channel_id'], 0)

    #Checks that the message was changed
    assert new_message == new_message_from_channel['messages'][0]['message']
    assert user2['u_id'] == new_message_from_channel['messages'][0]['u_id']
    assert message_id['message_id'] == new_message_from_channel['messages'][0]['message_id']
    other.clear()

def test_edit_valid_owner(users):
    """
    Testing if a single message can be sent, be stored and editted by owner
    """
    user1, user2, chan = users
    message_exp = 'Test 1 test 2 swiggity Swagg'
    message_exp2 = 'This is to stop there being no message in the channel'
    message.message_send(user1['token'], chan['channel_id'], message_exp2)
    message_id = message.message_send(user2['token'], chan['channel_id'], message_exp)
    message_from_channel = channel.channel_messages(user1['token'], chan['channel_id'], 0)

    #Checks that the message was added
    assert message_exp == message_from_channel['messages'][0]['message']
    assert user2['u_id'] == message_from_channel['messages'][0]['u_id']
    assert message_id['message_id'] == message_from_channel['messages'][0]['message_id']
    new_message = "This is the new message"
    message.message_edit(user1['token'], message_id['message_id'], new_message)
    new_message_from_channel = channel.channel_messages(user1['token'], chan['channel_id'], 0)

    #Checks that the message was changed
    assert new_message == new_message_from_channel['messages'][0]['message']
    assert user2['u_id'] == new_message_from_channel['messages'][0]['u_id']
    assert message_id['message_id'] == new_message_from_channel['messages'][0]['message_id']
    other.clear()

def test_edit_long_message_valid(users):
    """
    Testing if a 1000 character length message can be sent as an edit and be stored
    """
    user1, user2, chan = users
    #1000 character length string
    message_exp = ("This is the original message and will be changed")
    new_message = (
        'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula '
        'eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient '
        'montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, '
        'pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, '
        'aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis '
        'vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras '
        'dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo '
        'ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus '
        'in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. '
        'Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper '
        'ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum '
        'rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum...'
    )
    message_id1 = message.message_send(user2['token'], chan['channel_id'], message_exp)
    message_from_channel = channel.channel_messages(user1['token'], chan['channel_id'], 0)

    assert message_exp == message_from_channel['messages'][0]['message']
    assert user2['u_id'] == message_from_channel['messages'][0]['u_id']
    assert message_id1['message_id'] == message_from_channel['messages'][0]['message_id']
    message.message_edit(user1['token'], message_id1['message_id'], new_message)
    new_message_from_channel = channel.channel_messages(user1['token'], chan['channel_id'], 0)

    assert new_message == new_message_from_channel['messages'][0]['message']
    assert user2['u_id'] == new_message_from_channel['messages'][0]['u_id']
    assert message_id1['message_id'] == new_message_from_channel['messages'][0]['message_id']
    other.clear()

# Unsuccessful
def test_edit_long_message_invalid(users):
    """
    Testing if a message over 1000 characters cannot be sent used to edit
    """
    user1, user2, chan = users
    # greater then 1000 character length string
    message_exp = ("This is the original message and will be changed")
    new_message = (
        'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula '
        'eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient '
        'montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, '
        'pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, '
        'aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis '
        'vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras '
        'dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo '
        'ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus '
        'in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. '
        'Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper '
        'ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum '
        'rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum...too long'
    )
    message_id1 = message.message_send(user2['token'], chan['channel_id'], message_exp)
    message_from_channel = channel.channel_messages(user1['token'], chan['channel_id'], 0)
    assert message_exp == message_from_channel['messages'][0]['message']
    assert user2['u_id'] == message_from_channel['messages'][0]['u_id']
    assert message_id1['message_id'] == message_from_channel['messages'][0]['message_id']
    with pytest.raises(InputError):
        message.message_edit(user1['token'], message_id1['message_id'], new_message)
    other.clear()

def test_edit_no_message(users):
    """
    Tests that a message edit with no message acts as a delete
    """
    user1, user2, chan = users
    message_exp = 'Test 1 test 2 swiggity Swagg'
    message_exp2 = 'This is to stop there being no message in the channel'
    message.message_send(user1['token'], chan['channel_id'], message_exp2)
    message_id = message.message_send(user2['token'], chan['channel_id'], message_exp)
    message_from_channel = channel.channel_messages(user1['token'], chan['channel_id'], 0)

    #Checks that the message was added
    assert message_exp == message_from_channel['messages'][0]['message']
    assert user2['u_id'] == message_from_channel['messages'][0]['u_id']
    assert message_id['message_id'] == message_from_channel['messages'][0]['message_id']

    #Uses the function message edit but has the message editted to an empty string
    message.message_edit(user2['token'], message_id['message_id'], '')
    new_message_from_channel = channel.channel_messages(user1['token'], chan['channel_id'], 0)

    #Checks that the message was removed
    assert message_exp != new_message_from_channel['messages'][0]['message']
    assert user2['u_id'] != new_message_from_channel['messages'][0]['u_id']
    assert message_id['message_id'] != new_message_from_channel['messages'][0]['message_id']
    other.clear()

def test_edit_not_owner_or_creator(users):
    """
    Testing if an access error is raised if a user without authority tries to edit a message
    """
    user1, user2, chan = users
    test_user2 = auth.auth_register('anothertransformer@hotmail.com', 'password', 'New', 'Guy')
    message_exp = 'Test 1 test 2 swiggity Swagg'
    message_exp2 = 'This is to stop there being no message in the channel'
    new_message = 'This is the edit message and changes'
    message.message_send(user1['token'], chan['channel_id'], message_exp2)
    message_id = message.message_send(user2['token'], chan['channel_id'], message_exp)
    message_from_channel = channel.channel_messages(user1['token'], chan['channel_id'], 0)

    #Checks that the message was added
    assert message_exp == message_from_channel['messages'][0]['message']
    assert user2['u_id'] == message_from_channel['messages'][0]['u_id']
    assert message_id['message_id'] == message_from_channel['messages'][0]['message_id']
    new_message = "This is the new message"
    with pytest.raises(AccessError):
        message.message_edit(test_user2['token'], message_id['message_id'], new_message)
    other.clear()


###################################################################################################
# Tests for message_react
# Successful    

def test_message_react_valid(user1):
    """
    Testing if messages can be reacted
    """
    user1, chan = user1
    test_message1 = "Hello Luke!"
    message_id1 = message.message_send(user1["token"], chan['channel_id'], test_message1)
    message.message_react(user1["token"], message_id1["message_id"], 1)    
    message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)

    reacts = message_from_channel["messages"][0]["reacts"]
    assert reacts[0]['react_id'] == 1
    assert reacts[0]['u_ids'] == [1]
    assert reacts[0]['is_this_user_reacted'] == True
    other.clear()

def test_message_react_same_message(users):
    """
    Testing if same message can be reacted by different users
    """
    user1, user2, chan = users 
    test_message1 = "Hello Luke!"
    message_id1 = message.message_send(user1["token"], chan['channel_id'], test_message1)
    message.message_react(user1["token"], message_id1["message_id"], 1)   
    message.message_react(user2["token"], message_id1["message_id"], 1)   
    message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)

    reacts = message_from_channel["messages"][0]["reacts"]
    assert reacts[0]['react_id'] == 1
    assert reacts[0]['u_ids'] == [1,2]
    assert reacts[0]['is_this_user_reacted'] == True  
    other.clear()

# Unsuccessful    
def test_message_react_invalid_message_id(user1):
    """
    Testing that Input Error is raised when the message_id is an invalid message 
    that authorised use is member of
    """
    user1, _chan = user1
    with pytest.raises(InputError):
        assert message.message_react(user1["token"], 123415, 1)

    other.clear()
    
def test_message_react_invalid_react_id(user1):
    """
    Testing that Input Error is raised when the react_id is an invalid React ID 
    """
    user1, chan = user1
    test_message1 = "Hello"
    message_id1 = message.message_send(user1["token"], chan['channel_id'], test_message1)
    
    with pytest.raises(InputError):
        assert message.message_react(user1["token"], message_id1["message_id"], 602)

    other.clear()
	
	
def test_message_react_already_reacted(user1):
    """
    Testing that Input Error is raised when a user attempts to react same message twice
    """
    user1, chan = user1
    test_message1 = "Hello"
    message_id1 = message.message_send(user1["token"], chan['channel_id'], test_message1)
    message.message_react(user1["token"], message_id1["message_id"], 1)  
    
    with pytest.raises(InputError):
        assert message.message_react(user1["token"], message_id1["message_id"], 1)
        
    other.clear()
    
    
###################################################################################################
# Tests for message_unreact 
# Successful

def test_message_unreact_valid(users):
    """
    Testing if message can be unreacted 
    """
    user1, user2, chan = users
    test_message1 = "Hello Luke!"
    message_id1 = message.message_send(user1["token"], chan['channel_id'], test_message1)
    message.message_react(user1["token"], message_id1["message_id"], 1)
    message.message_react(user2["token"], message_id1["message_id"], 1)
    message.message_unreact(user1["token"], message_id1["message_id"], 1)
    message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)
      
    reacts = message_from_channel["messages"][0]["reacts"]
    assert reacts[0]['react_id'] == 1
    assert reacts[0]['u_ids'] == [2]
    assert reacts[0]['is_this_user_reacted'] == False 
    other.clear()

def test_message_unreact_invalid_message_id(user1):
    """
    Testing that Input Error is raised when the message_id is an invalid message 
    that authorised use is member of
    """
    user1, _chan = user1
     
    with pytest.raises(InputError):
        assert message.message_unreact(user1["token"], 123415, 1)

    other.clear()    

def test_message_unreact_invalid_react_id(user1):
    """
    Testing that Input Error is raised when the react_id is an invalid React ID 
    """
    user1, chan = user1
    test_message1 = "Hello"
    message_id1 = message.message_send(user1["token"], chan['channel_id'], test_message1)
    message.message_react(user1["token"], message_id1["message_id"], 1)
    
    with pytest.raises(InputError):
        assert message.message_react(user1["token"], message_id1["message_id"], 602)

    other.clear()

def test_message_unreact_already_reacted(user1):
    """
    Testing that Input Error is raised when a user attempts to unreact same message twice
    """
    user1, chan = user1
    test_message1 = "Hello"
    message_id1 = message.message_send(user1["token"], chan['channel_id'], test_message1)
    
    with pytest.raises(InputError):
        assert message.message_unreact(user1["token"], message_id1["message_id"], 1)
        
    other.clear()
###################################################################################################   
# Tests for message_pin
# Successful
                          
def test_message_pin_valid(users):
    """
    Testing if multiple messages can be successfully pinned
    """
    user1, user2, chan = users
    m1 = "Hi Luke!"
    m2 = "Hello John! Nice to meet you!"
    m_id1 = message.message_send(user1["token"], chan['channel_id'], m1)['message_id']
    m_id2 = message.message_send(user2["token"], chan['channel_id'], m2)['message_id']

    assert message.message_pin(user1["token"], m_id1) == {}
    assert message.message_pin(user1["token"], m_id2) == {}
    test = channel.channel_messages(user1["token"], chan['channel_id'], 0)
    assert test["messages"][1]["is_pinned"] == True
    assert test["messages"][0]["is_pinned"] == True
    other.clear()

# Unsuccessful    
def test_message_pin_invalid_message_id(users):
    """
    Testing that Input Error is raised when the message_id is invalid
    """
    user1 = auth.auth_register("vader@gmail.com", "father", "Anakin", "Skywalker")
    channels.channels_create(user1["token"], "Star Wars", True)
    with pytest.raises(InputError):
        assert message.message_pin(user1["token"], 123415)
    other.clear()
	
def test_message_pin_already_pinned(users):
    """
    Testing that Input Error is raised when user is trying to pin a message
    which has already been pinned
    """
    user1 = auth.auth_register("darthvader@gmail.com", "iamyourfather", "Anakin", "Skywalker")
    chan = channels.channels_create(user1["token"], "Star Wars", True)['channel_id']		
    test_message1 = "Very proud of my new channel!"
    m_id1 = message.message_send(user1["token"], chan, test_message1)['message_id']
    message.message_pin(user1["token"], m_id1)
    with pytest.raises(InputError):
        assert message.message_pin(user1["token"], m_id1)
    other.clear()
    
def test_message_pin_not_member(users):
    """
    Testing that Access Error is raised when user who is not member of the channel
    tries to pin a message
    """
    user1, user2, chan = users
    test_message1 = "Very proud of my new channel!" 
    mess1 = message.message_send(user1["token"], chan['channel_id'], test_message1)

    with pytest.raises(AccessError):
        assert message.message_pin(user2["token"], mess1['message_id'])

    other.clear()
		
def test_message_pin_after_leaving(user1):
    """
    Testing that Access Error is raised when owner of channel leaves and tries to
    pin a message in that channel
    """
    user1, chan = user1
    test_message1 = "Welcome!" 
    mess1 = message.message_send(user1["token"], chan['channel_id'], test_message1)['message_id'] 
    channel.channel_leave(user1["token"], chan['channel_id'])
    with pytest.raises(AccessError):
        assert message.message_pin(user1["token"], mess1)      
    other.clear()	

def test_message_pin_not_owner(users):
    """
    Testing that Access Error is raised when the authorised user is not an owner
    """
    user1, user2, chan = users
    test_message1 = "New channel is created"
    mess1 = message.message_send(user2["token"], chan['channel_id'], test_message1)['message_id']
    message.message_send(user1["token"], chan['channel_id'], test_message1)['message_id']
    with pytest.raises(AccessError):
        assert message.message_pin(user2["token"], mess1)
    other.clear()

###################################################################################################    
# Tests for message_unpin
# Successful
def test_message_unpin_valid(users):
    """
    Testing if multiple messages can be successfully unpinned
    """
    user1, user2, chan = users
    msg1 = "Hey how's it going?"
    msg2 = "I'm going well!"
    mess1 = message.message_send(user1["token"], chan['channel_id'], msg1)['message_id']
    mess2 = message.message_send(user2["token"], chan['channel_id'], msg2)['message_id']
    message.message_pin(user1["token"], mess1) == {}
    message.message_pin(user1["token"], mess2) == {}
    messages = channel.channel_messages(user1["token"], chan['channel_id'], 0)

    assert messages["messages"][0]["is_pinned"] == True
    assert messages["messages"][1]["is_pinned"] == True
    assert message.message_unpin(user1["token"], mess1) == {}
    assert message.message_unpin(user1["token"], mess2) == {}
    messages = channel.channel_messages(user1["token"], chan['channel_id'], 0)
    assert messages["messages"][0]["is_pinned"] == False
    assert messages["messages"][1]["is_pinned"] == False
    other.clear()

# Unsuccessful
def test_message_unpin_invalid_message_id():
    """
    Testing that Input Error is raised when the message_id is invalid
    """
    user1 = auth.auth_register("lucyjang@gmail.com", "lucyjang", "Lucy", "Jang")
    channels.channels_create(user1["token"], "Star Wars", True)
    with pytest.raises(InputError):
        assert message.message_unpin(user1["token"], 123415)
    other.clear()

def test_message_unpin_already_unpinned():
    """
	Testing that Input Error is raised when user attempts to unpin a message
	which is already unpinned
	"""
    user1 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")
    chan = channels.channels_create(user1["token"], "General", True)['channel_id']    
    msg1 = "Hello"
    mess1 = message.message_send(user1["token"], chan, msg1)['message_id']
    message.message_pin(user1["token"], mess1)
    message.message_unpin(user1["token"], mess1)
    with pytest.raises(InputError):
        assert message.message_unpin(user1["token"], mess1)   
    other.clear()
    
def test_message_unpin_never_pinned():
    """
    Testing that Input Error is raised when user attempts to unpin a message 
    which was never pinned
    """
    user1 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")
    chan = channels.channels_create(user1["token"], "General", True)['channel_id']
    msg = "Hello"
    mess = message.message_send(user1["token"], chan, msg)['message_id']
    with pytest.raises(InputError):
        message.message_unpin(user1["token"], mess)   
    other.clear()

def test_message_unpin_not_member(users):
    """
	Testing that Access Error is raised when user who is not member of the channel
	attempts to unpin a message
	"""
    user1, user2, chan_id = users
    msg = "I am invincible"
    mess = message.message_send(user1["token"], chan_id['channel_id'], msg)['message_id']
    message.message_pin(user1["token"], mess)
    with pytest.raises(AccessError):
        assert message.message_unpin(user2["token"], mess)
    other.clear()

def test_message_unpin_after_leaving():
    """
    Testing that Access Error is raised when owner of channel leaves and attempts to
    unpin a message in that channel
    """
    user1 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")
    chan = channels.channels_create(user1["token"], "General", True)['channel_id']
    msg = "Welcome!"
    mess = message.message_send(user1["token"], chan, msg)['message_id']
    message.message_pin(user1["token"], mess)
    channel.channel_leave(user1["token"], chan)
    with pytest.raises(AccessError):
        assert message.message_unpin(user1["token"], mess)
    other.clear()

def test_message_unpin_not_owner(users):
    """
	Testing that Access Error is raised when the authorised user is not an owner
	"""   
    user1, user2, chan = users
    msg = "I am the owner of this channel"
    mess = message.message_send(user1["token"], chan['channel_id'], msg)['message_id']
    message.message_pin(user1["token"], mess)
    with pytest.raises(AccessError):
        message.message_unpin(user2["token"], mess)    
    other.clear()

###################################################################################################     
# Tests for message_sendlater
# Sucessful
def test_message_sendlater_success():
    user = auth.auth_register('apple1@gmail.com', 'paswword' , 'first_name', 'last_name')
    chan = channels.channels_create(user['token'], 'test_channel', True)['channel_id']
    time = time_from_now(60)
    msg = 'Test message from the past!'
    mess = message.message_sendlater(user['token'], chan, msg, time)['message_id']

    message_list = channel.channel_messages(user['token'], chan, 0)
    assert message_list['messages'][0]['message'] == msg
    assert message_list['messages'][0]['message_id'] == mess
    assert message_list['messages'][0]['u_id'] == user['u_id']

    other.clear()

def test_message_sendlater_success_multiple():
    user1 = auth.auth_register('raspberry@gmail.com', 'paswword' , 'rasp', 'berry')
    user2 = auth.auth_register('blueberry@gmail.com', 'password', 'blue', 'berry')
    user3 = auth.auth_register('strawberry@gmail.com', 'password', 'straw', 'berry')
    chan = channels.channels_create(user1['token'], 'test_channel', True)['channel_id']
    channel.channel_join(user2['token'], chan)
    channel.channel_join(user3['token'], chan)

    msg1 = 'Test 1 bleep blop bloop'
    msg2 = 'Test 2 1 0 1 1'
    msg3 = 'Test 3 FLip Flop Slop'
    msg4 = 'Test 4 Gling glong glip'
    # Testing sending messages before others
    time1 = time_from_now(5)
    time2 = time_from_now(2)
    time3 = time_from_now(10)
    time4 = time_from_now(5)
    mess1 = message.message_sendlater(user1['token'], chan, msg1, time1)['message_id']
    mess2 = message.message_sendlater(user2['token'], chan, msg2, time2)['message_id']
    mess3 = message.message_sendlater(user3['token'], chan, msg3, time3)['message_id']
    mess4 = message.message_sendlater(user1['token'], chan, msg4, time4)['message_id']
    
    message_list = channel.channel_messages(user1['token'], chan,  0)
    assert message_list['messages'][3]['message'] == msg1
    assert message_list['messages'][3]['message_id'] == mess1
    assert message_list['messages'][3]['u_id'] == user1['u_id']

    assert message_list['messages'][2]['message'] == msg2
    assert message_list['messages'][2]['message_id'] == mess2
    assert message_list['messages'][2]['u_id'] == user2['u_id']

    assert message_list['messages'][1]['message'] == msg3
    assert message_list['messages'][1]['message_id'] == mess3
    assert message_list['messages'][1]['u_id'] == user3['u_id']

    assert message_list['messages'][0]['message'] == msg4
    assert message_list['messages'][0]['message_id'] == mess4
    assert message_list['messages'][0]['u_id'] == user1['u_id']

    other.clear()
    

def test_send_way_later():
    user1 = auth.auth_register("james@gmail.com", "reddington", "James", "Spader")
    chan1 = channels.channels_create(user1['token'], "Zooper Dooper", False)
    time1 = time_from_now(602)
    time2 = time_from_now(6020)
    mess1 = message.message_sendlater(user1['token'], chan1['channel_id'], "ahoy", time1)
    mess2 = message.message_sendlater(user1['token'], chan1['channel_id'], "yoha", time2)
    assert mess1['message_id'] == 1
    assert mess2['message_id'] == 2
    other.clear()

# Unsucessful
def test_message_sendlater_invalid_channel():
    user1 = auth.auth_register('grape@gmail.com', 'paswword' , 'first_name', 'last_name')
    channels.channels_create(user1['token'], 'test_channel', True)
    time = time_from_now(15)
    msg = 'Test message from the past!'
    with pytest.raises(InputError):
        assert message.message_sendlater(user1['token'], 602, msg, time)
  
    other.clear()

def test_message_sendlater_invalid_message():
    user1 = auth.auth_register('mango@gmail.com', 'paswword' , 'first_name', 'last_name')
    chan = channels.channels_create(user1['token'], 'test_channel', True)['channel_id']

    time = time_from_now(5)
    msg = 'A' * 1001
    with pytest.raises(InputError):
        assert message.message_sendlater(user1['token'], chan, msg, time)

    other.clear()
    
def test_message_sendlater_right_now():
    user1 = auth.auth_register('melon@gmail.com', 'paswword' , 'first_name', 'last_name')
    chan = channels.channels_create(user1['token'], 'test_channel', True)['channel_id']
    
    msg = 'Test message from the future!'
    time = time_from_now(0)
    with pytest.raises(InputError):
        assert message.message_sendlater(user1['token'], chan, msg, time)
  
    other.clear()

def test_message_sendlater_not_in_channel():
    user1 = auth.auth_register('melon@gmail.com', 'paswword' , 'first_name', 'last_name')
    user2 = auth.auth_register('blueberry@gmail.com', 'password', 'first_name', 'last_name')
    chan = channels.channels_create(user1['token'], 'test_channel', True)['channel_id']
    
    msg = 'Test message from the past!'
    time = time_from_now(5)
    with pytest.raises(AccessError):
        assert message.message_sendlater(user2['token'], chan, msg, time)
  
    other.clear()

def test_successful_weather():
    user = auth.auth_register('firework@gmail.com', 'wouldntyouliketoknow', 'waether', 'boy')
    chan = channels.channels_create(user['token'], 'customer', True)['channel_id']
    msg = '/weather Sydney'
    mess = message.message_send(user['token'], chan, msg)['message_id']
    assert mess == 1
    other.clear()

def test_unsucessful_weather():
    user = auth.auth_register('james@james.com', 'Jmaesjames', 'James', 'james')
    chan = channels.channels_create(user['token'], 'jam', True)['channel_id']
    msg = '/weather 123'
    with pytest.raises(InputError):
        assert message.message_send(user['token'], chan, msg)
    other.clear()