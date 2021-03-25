"""
Errors for kahio:
* Person who started can't guess
* Can't start kahio if already playing
* Can't guess the correct answer again
* Can't start kahio if not admin
* Can't end kahio if not admin
* Can't end a game if no game is running
* Have to enter an answer to the question
"""
import time
import datetime
import pytest
import message
import channel
import auth
import channels
import other
from error import InputError, AccessError

@pytest.fixture
def users():
    """
    Pytest fixture that automatically registers a user and returns their info
    """
    user1 = auth.auth_register("kevin@gmail.com", "kh12345", "Kyle", "Huang")
    user2 = auth.auth_register("weogweg@hotmail.com", "egwegewg", "Kevin", "Huang")
    chan = channels.channels_create(user1["token"], "test_channel", True)
    channel.channel_join(user2["token"], chan["channel_id"])
    users_and_channel = (user1, user2, chan)
    return users_and_channel

@pytest.fixture
def users1():
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
def test_send_valid(users1):
    """
    Testing if a single message can be sent and be stored
    """
    user1, chan = users1
    message_exp = "/KAHIO/Question/ A/ 1"
    message_id = message.message_send(user1["token"], chan['channel_id'], message_exp)
    message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)

    assert message_from_channel["messages"][0]["message"] == "Question"
    assert user1["u_id"] == message_from_channel["messages"][0]["u_id"]
    assert message_id["message_id"] == message_from_channel["messages"][0]["message_id"]

    time.sleep(2)

    message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)
    no_correct_message = "Kahio game has ended.\nThe correct answer was a\nNo correct answers"
    assert message_from_channel["messages"][0]["message"] == no_correct_message
    assert user1["u_id"] == message_from_channel["messages"][0]["u_id"]
    other.clear()

def test_send_invalid_start_no_question(users1):
    """
    Tests an error is returned when given a message with no question
    """
    user1, chan = users1
    message_exp = "/KAHIO no_invaldad quezs"
    with pytest.raises(InputError):
        message.message_send(user1["token"], chan['channel_id'], message_exp)
    other.clear()

#Successful
def test_send_answer_valid(users):
    """
    Testing if a single message can be sent and be stored
    """
    user1, user2, chan = users
    message_exp = "/KAHIO/Question/ A/ 10"
    message_id = message.message_send(user1["token"], chan['channel_id'], message_exp)
    message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)

    assert message_from_channel["messages"][0]["message"] == "Question"
    assert user1["u_id"] == message_from_channel["messages"][0]["u_id"]
    assert message_id["message_id"] == message_from_channel["messages"][0]["message_id"]

    message_ans = " A"
    message_id2 = message.message_send(user2["token"], chan['channel_id'], message_ans)

    time.sleep(11)

    message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)
    assert user1["u_id"] == message_from_channel["messages"][0]["u_id"]
    occured = False
    for cur_message in message_from_channel["messages"]:
        if message_id2["message_id"] == cur_message["message_id"]:
            assert cur_message["u_id"] == user1["u_id"]
            assert cur_message["message"] == "KevinHuang guessed the correct answer"
            occured = True
    assert occured is True
    other.clear()

#Successful
def test_send_answer_incorrect(users):
    """
    Testing if a single message can be sent and be stored
    """
    user1, user2, chan = users
    message_exp = "/KAHIO/Question/ A/ 1"
    message_id = message.message_send(user1["token"], chan['channel_id'], message_exp)
    message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)

    assert message_from_channel["messages"][0]["message"] == "Question"
    assert user1["u_id"] == message_from_channel["messages"][0]["u_id"]
    assert message_id["message_id"] == message_from_channel["messages"][0]["message_id"]

    message_ans = " b"
    message_id2 = message.message_send(user2["token"], chan['channel_id'], message_ans)

    time.sleep(2)

    message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)
    message_exp = "Kahio game has ended.\nThe correct answer was a\nNo correct answers"
    assert message_from_channel["messages"][0]["message"] == message_exp
    assert user1["u_id"] == message_from_channel["messages"][0]["u_id"]
    bling = True
    for cur_message in message_from_channel["messages"]:
        if message_id2["message_id"] == cur_message["message_id"]:
            assert cur_message["u_id"] == user2["u_id"]
            assert cur_message["message"] == " b"
            bling = False
    assert bling is False
    other.clear()

def test_timer_messages(users1):
    """
    Testing The correct series of messages is printed in the channel
    """
    user1, chan = users1
    message_exp = "/KAHIO/Question/ A/ 6"
    message_id = message.message_send(user1["token"], chan['channel_id'], message_exp)
    message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)

    assert message_from_channel["messages"][0]["message"] == "Question"
    assert user1["u_id"] == message_from_channel["messages"][0]["u_id"]
    assert message_id["message_id"] == message_from_channel["messages"][0]["message_id"]
    time.sleep(0.4)
    for i in range(0, 5):
        message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)
        assert message_from_channel["messages"][0]["message"] == f"The kahoi game has {6-i} seconds remaining"
        assert user1["u_id"] == message_from_channel["messages"][0]["u_id"]

        time.sleep(1)
    time.sleep(1)
    message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)
    message_exp = "Kahio game has ended.\nThe correct answer was a\nNo correct answers"
    assert message_from_channel["messages"][0]["message"] == message_exp
    assert user1["u_id"] == message_from_channel["messages"][0]["u_id"]
    other.clear()

def test_not_user_kahio_start(users):
    """
    Will test an error is raised when not an owner tries to start a kahio game
    """
    _user1, user2, chan = users
    message_exp = "/KAHIO/Question/ A/ 1"
    with pytest.raises(AccessError):
        message.message_send(user2["token"], chan['channel_id'], message_exp)
    other.clear()

def test_starter_answers(users1):
    """
    Will test if an error is raised when the kahio game starter tries to answer the question
    """
    user1, chan = users1
    message_exp = "/KAHIO/Question/ A/ 10"
    message.message_send(user1["token"], chan['channel_id'], message_exp)
    time.sleep(1)
    with pytest.raises(InputError):
        message.message_send(user1["token"], chan['channel_id'], "a")
    other.clear()

def test_already_answer_answers(users):
    """
    Will test if an error is raised when the kahio game answer tries to answer the question again
    """
    user1, user2, chan = users
    message_exp = "/KAHIO/Question/ A/ 1"
    message.message_send(user1["token"], chan['channel_id'], message_exp)
    message.message_send(user2["token"], chan['channel_id'], "a")
    with pytest.raises(InputError):
        message.message_send(user2["token"], chan['channel_id'], "a")
    other.clear()

def test_kahio_game_already_started(users1):
    """
    Testing that when a kahio game is tried to start it has already been started an error is raised
    """
    user1, chan = users1
    message_exp = "/KAHIO/Question/ A/ 5"
    message.message_send(user1["token"], chan['channel_id'], message_exp)
    with pytest.raises(InputError):
        message.message_send(user1["token"], chan['channel_id'], message_exp)
    other.clear()

def test_kahio_stop_valid(users1):
    """
    Testing that the kahio game can be stopped by a valid owner
    """
    user1, chan = users1
    message_exp = "/KAHIO/Question/ A/ 5"
    message.message_send(user1["token"], chan['channel_id'], message_exp)

    message_id = message.message_send(user1["token"], chan['channel_id'], "/KAHIO/END")
    message_from_channel = channel.channel_messages(user1["token"], chan['channel_id'], 0)

    assert message_from_channel["messages"][0]["message"] == "The KAHIO game has been stopped"
    assert user1["u_id"] == message_from_channel["messages"][0]["u_id"]
    assert message_id["message_id"] == message_from_channel["messages"][0]["message_id"]
    other.clear()

def test_kahio_stop_not_owner(users):
    """
    Testing that an error is raised when not an owner tries to stop the kahio game
    """
    user1, user2, chan = users
    message_exp = "/KAHIO/Question/ A/ 5"
    message.message_send(user1["token"], chan['channel_id'], message_exp)

    with pytest.raises(AccessError):
        message.message_send(user2["token"], chan['channel_id'], "/KAHIO/END")
    other.clear()

def test_kahio_stop_no_game(users1):
    """
    Testing that an error is raised when not an owner tries to stop the kahio game
    """
    user1, chan = users1

    with pytest.raises(InputError):
        message.message_send(user1["token"], chan['channel_id'], "/KAHIO/END")
    other.clear()

def test_kahio_input_no_answer(users1):
    """
    Testing an input error is raised if no answer is given to the question in the inital
    start statement
    """
    user1, chan = users1

    with pytest.raises(InputError):
        message.message_send(user1["token"], chan['channel_id'], "/KAHIO/ question")
    other.clear()
