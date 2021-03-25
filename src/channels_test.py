"""
    pytest: Gives access to pytest command (for testing)
    auth(auth.py): Gives access to auth functions
    channel(channel.py): Gives access to channel functions
    channels(channels.py): Gives access to channel_create
    other(other.py): Gives access to other.clear command
    error(error.py): Gives access to error classes
"""
import pytest
import auth
import channel
import channels
import other
from error import InputError, AccessError

# Tests for channels_list:
def test_channels_list():
    """
    Testing successful uses of channels_list without any errors
    """
    user = auth.auth_register("testmail@gmail.com", "password", "first_name", "last_name")
    channels.channels_create(user["token"], "test_channel", True)
    list_result = channels.channels_list(user["token"])["channels"]
    assert list_result[0]["channel_id"] == 1
    assert list_result[0]["name"] == "test_channel"

    user2 = auth.auth_register("another_test@hotmail.com", "password123", "first_name", "last_name")
    channels.channels_create(user2["token"], "test_channel_two", True)
    channels.channels_create(user2["token"], "test_channel_three", True)
    list_result2 = channels.channels_list(user2["token"])["channels"]
    assert list_result2[0]["channel_id"] == 2
    assert list_result2[0]["name"] == "test_channel_two"
    assert list_result2[1]["channel_id"] == 3
    assert list_result2[1]["name"] == "test_channel_three"

    other.clear()


def test_channels_list_invalid_token():
    """
    Testing unsuccessful uses of channels_list,
    focusing on invalid tokens
    """
    user = auth.auth_register("testmailtest@gmail.com", "password121", "first_name", "last_name")
    channels.channels_create(user["token"], "test_channel", True)
    with pytest.raises(AccessError):
        assert channels.channels_list("invalid_token")

    user2 = auth.auth_register("test2@hotmail.com", "password12321", "first_name", "last_name")
    channels.channels_create(user2["token"], "test_channel_two", True)
    channels.channels_create(user2["token"], "test_channel_three", True)
    with pytest.raises(AccessError):
        assert channels.channels_list("another_invalid_token")

    other.clear()


# Tests for channels_listall:
def test_channels_listall():
    """
    Testing successful uses of channels_listall without any errors
    """
    user = auth.auth_register("abc123@gmail.com", "passwordabc", "first_name", "last_name")
    new_channel = channels.channels_create(user["token"], "my_channel", True)
    list_result = channels.channels_listall(user["token"])["channels"]
    assert list_result[0]["channel_id"] == 1
    assert list_result[0]["name"] == "my_channel"

    user2 = auth.auth_register("xyz456@gmail.com", "passwordxyz", "first_name", "last_name")
    channel.channel_join(user2["token"], new_channel["channel_id"])
    channels.channels_create(user2["token"], "our_channel", True)
    list_result2 = channels.channels_listall(user2["token"])["channels"]
    assert list_result2[0]["channel_id"] == 1
    assert list_result2[0]["name"] == "my_channel"
    assert list_result2[1]["channel_id"] == 2
    assert list_result2[1]["name"] == "our_channel"

    other.clear()

def test_channels_listall_invalid_token():
    """
    Testing unsuccessful uses of channels_listall,
    focusing on invalid tokens
    """
    user = auth.auth_register("abc123abc@gmail.com", "passwordabc1", "first_name", "last_name")
    new_channel = channels.channels_create(user["token"], "my_channel", True)
    with pytest.raises(AccessError):
        assert channels.channels_listall("invalid_token")

    user2 = auth.auth_register("xyz456xyz@gmail.com", "passwordxyz1", "first_name", "last_name")
    channel.channel_join(user2["token"], new_channel["channel_id"])
    channels.channels_create(user2["token"], "our_channel", True)
    with pytest.raises(AccessError):
        assert channels.channels_listall("another_invalid_token")

    other.clear()


# Tests for channels_create:
# Successful
def test_channels_create_name_valid():
    """
    Testing successful uses of channels_create without any errors
    """

    user = auth.auth_register("testmail@gmail.com", "passwordpassword", "first_name", "last_name")
    channels.channels_create(user["token"], "test_name", True)
    list_result = channels.channels_list(user["token"])["channels"]
    assert list_result[0]["channel_id"] == 1
    assert len(list_result[0]["name"]) < 20

    user2 = auth.auth_register("mailtest@gmail.com", "passwordword", "first_name", "last_name")
    channels.channels_create(user2["token"], "test_name_two", False)
    list_result2 = channels.channels_list(user2["token"])["channels"]
    assert list_result2[0]["channel_id"] == 2
    assert len(list_result2[0]["name"]) < 20

    other.clear()

# Unsuccessful
def test_channels_create_name_error():
    """
    Testing unsuccessful uses of channels_create,
    focusing on invalid channel names
    """
    user = auth.auth_register("testmail123@gmail.com", "passwordpass", "first_name", "last_name")
    with pytest.raises(InputError):
        assert channels.channels_create(user["token"], "test_name_12345678910x", True)

    user2 = auth.auth_register("mailtest123@gmail.com", "passwpassword", "first_name", "last_name")
    with pytest.raises(InputError):
        assert channels.channels_create(user2["token"], "test_name_0987654321x", False)

    other.clear()

def test_channels_create_invalid_token():
    """
    Testing unsuccessful uses of channels_create,
    focusing on invalid tokens
    """
    auth.auth_register("testmail12321@gmail.com", "passwordpass1", "first_name", "last_name")
    with pytest.raises(AccessError):
        assert channels.channels_create("invalid_token", "test_name1", True)

    auth.auth_register("mailtest12321@gmail.com", "passwpassword1", "first_name", "last_name")
    with pytest.raises(AccessError):
        assert channels.channels_create("another_invalid_token", "test_name1", False)

    other.clear()
