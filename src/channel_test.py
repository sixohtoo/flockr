"""
    pytest: Gives access to pytest command (for testing)
    channel(channel.py): Gives access to channel functions
    auth(auth.py): Gives access to register, login and logout functions
    channels(channels.py): Gives access to channel_create
    other(other.py): Gives access to other.clear command
    error(error.py): Gives access to error classes
"""
import pytest
import channel
import auth
import channels
import other
import message
from error import InputError, AccessError

#Check if invited member is in through channel details
def check_if_member_exists(channel_details, user):
    """
    Determines whether invited member is in the channel

    Parameters:
        channel_details(dictionary): Includes a list of members in the channel
        user(int): u_id (Identifier for user)

    Returns:
        Nothing
    """
    mem = None
    for member in channel_details["all_members"]:
        if member["u_id"] == user["u_id"]:
            mem = member
    assert mem is not None


#Channel_invite tests
#Successful
def test_channel_invite_valid_token():
    """
    Testing successful uses of channel_invite,
    focusing on valid tokens
    """
    valid_token = auth.auth_register("best_group123@gmail.com", "awesome", "best", "group")
    user2 = auth.auth_register("bestest_group123@gmail.com", "awesome", "best", "group")
    new_channel = channels.channels_create(valid_token["token"], "temp_channel", False)
    channel.channel_invite(valid_token["token"], new_channel["channel_id"], user2["u_id"])
    channel_details = channel.channel_details(valid_token["token"], new_channel["channel_id"])
    check_if_member_exists(channel_details, user2)

    other.clear()

def test_channel_invite_valid_channel_id():
    """
    Testing successful uses of channel_invite,
    focusing on valid channel ids
    """
    user1 = auth.auth_register("polarbae23@gmail.com", "grrr123", "polar", "bae")
    user2 = auth.auth_register("wsadwert@yahoo.com", "egegeg", "wsad", "wert")
    valid_channel = channels.channels_create(user1["token"], "temp_channel", False)
    channel.channel_invite(user1["token"], valid_channel["channel_id"], user2["u_id"])
    channel_details = channel.channel_details(user1["token"], valid_channel["channel_id"])
    check_if_member_exists(channel_details, user2)

    other.clear()

def test_channel_invite_valid_u_id():
    """
    Testing successful uses of channel_invite,
    focusing on valid user ids
    """
    user1 = auth.auth_register("iheartunsw@unsw.edu.au", "unsw123", "love", "UNSW")
    valid_u_id = auth.auth_register("iheartusyd@usyd.edu.au", "sydney", "love", "usyd")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    channel.channel_invite(user1["token"], new_channel["channel_id"], valid_u_id["u_id"])
    channel_details = channel.channel_details(user1["token"], new_channel["channel_id"])
    check_if_member_exists(channel_details, valid_u_id)

    other.clear()

def test_private_channel_invite():
    """
    Testing successful uses of channel_invite,
    focusing on private channels
    """
    user1 = auth.auth_register("dog@gmail.com", "awesome", "dog", "puppy")
    user2 = auth.auth_register("cat@gmail.com", "awesome", "cat", "kitty")
    user3 = auth.auth_register("eddyisgay@gmail.com", "eddygay", "eddy", "gay")
    new_private_channel = channels.channels_create(user1["token"], "cool_kids_only", True)
    channel.channel_invite(user1["token"], new_private_channel["channel_id"], user2["u_id"])
    channel.channel_invite(user1["token"], new_private_channel["channel_id"], user3["u_id"])
    channel_details = channel.channel_details(user1["token"], new_private_channel["channel_id"])
    check_if_member_exists(channel_details, user2)
    check_if_member_exists(channel_details, user3)

    other.clear()

def test_channel_invite_many_members():
    """
    Testing successful uses of channel_invite,
    focusing on inviting lots of people
    """
    user1 = auth.auth_register("simonpepe@gmail.com", "1234567", "simon", "pepe")
    user2 = auth.auth_register("ezmoney@gmail.com", "1234567", "ez", "money")
    user3 = auth.auth_register("eddyisgay@gmail.com", "eddygay", "eddy", "gay")
    user4 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    user5 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    user6 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    user7 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    user8 = auth.auth_register("hugosullivan@gmail.com", "hs1234", "Hugo", "Sullivan")

    new_channel = channels.channels_create(user1["token"], "rave_club", False)
    channel.channel_invite(user1["token"], new_channel["channel_id"], user2["u_id"])
    channel.channel_invite(user1["token"], new_channel["channel_id"], user3["u_id"])
    channel.channel_invite(user1["token"], new_channel["channel_id"], user4["u_id"])
    channel.channel_invite(user1["token"], new_channel["channel_id"], user5["u_id"])
    channel.channel_invite(user1["token"], new_channel["channel_id"], user6["u_id"])
    channel.channel_invite(user1["token"], new_channel["channel_id"], user7["u_id"])
    channel.channel_invite(user1["token"], new_channel["channel_id"], user8["u_id"])
    channel_details = channel.channel_details(user1["token"], new_channel["channel_id"])

    check_if_member_exists(channel_details, user2)
    check_if_member_exists(channel_details, user3)
    check_if_member_exists(channel_details, user4)
    check_if_member_exists(channel_details, user5)
    check_if_member_exists(channel_details, user6)
    check_if_member_exists(channel_details, user7)
    check_if_member_exists(channel_details, user8)

    other.clear()

def test_different_authorised_users_inviting():
    """
    Testing successful uses of channel_invite,
    focusing on invites from different users
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    user3 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    user4 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    user5 = auth.auth_register("hugosullivan@gmail.com", "hs1234", "Hugo", "Sullivan")

    new_channel = channels.channels_create(user1["token"], "comp1531", False)
    channel.channel_invite(user1["token"], new_channel["channel_id"], user2["u_id"])
    channel.channel_invite(user2["token"], new_channel["channel_id"], user3["u_id"])
    channel.channel_invite(user3["token"], new_channel["channel_id"], user4["u_id"])
    channel.channel_invite(user4["token"], new_channel["channel_id"], user5["u_id"])
    channel_details = channel.channel_details(user1["token"], new_channel["channel_id"])
    check_if_member_exists(channel_details, user1)
    check_if_member_exists(channel_details, user2)
    check_if_member_exists(channel_details, user3)
    check_if_member_exists(channel_details, user4)
    check_if_member_exists(channel_details, user5)

    other.clear()

def test_channel_invite_self_invite():
    """
    Testing successful uses of channel_invite,
    focusing on self invites.
    Nothing is expected to happen.
    """
    user1 = auth.auth_register("ezmoney@gmail.com", "1234567", "ez", "money")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    
    # Expected to do nothing
    with pytest.raises(InputError):
        assert channel.channel_invite(user1["token"], new_channel["channel_id"], user1["u_id"])
    
    other.clear()

def test_channel_invite_existing_member():
    """
    Testing successful uses of channel_invite,
    focusing on inviting users who are already in the channel.
    Nothing is expected to happen
    """
    user1 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    channel.channel_invite(user1["token"], new_channel["channel_id"], user2["u_id"])
    
    # Expected to do nothing
    with pytest.raises(InputError):
        assert channel.channel_invite(user2["token"], new_channel["channel_id"], user1["u_id"])
    
    other.clear()

# Unsuccessful
def test_channel_invite_invalid_token():
    """
    Testing unsuccessful uses of channel_invite,
    focusing on invalid tokens
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice1234", "Kevin", "Huang")
    user2 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    new_public_channel = channels.channels_create(user1["token"], "temp_channel", False)
    
    with pytest.raises(AccessError):
        assert channel.channel_invite(
            "invalid_token",
            new_public_channel["channel_id"],
            user2["u_id"]
        )

    user3 = auth.auth_register("eddyisgay@gmail.com", "eddygay", "eddy", "gay")
    user4 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    new_private_channel = channels.channels_create(user3["token"], "temp_channel", True)
    
    with pytest.raises(AccessError):
        assert channel.channel_invite("another_invalid_token",
                                      new_private_channel["channel_id"],
                                      user4["u_id"])

    other.clear()

def test_channel_invite_invalid_channel_id():
    """
    Testing unsuccessful uses of channel_invite,
    focusing on invalid tokens
    """
    user1 = auth.auth_register("best_group123@gmail.com", "awesome", "best", "group")
    user2 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    channels.channels_create(user1["token"], "temp_channel", False)
    invalid_channel_id = 123456789 # Random number
    
    with pytest.raises(InputError):
        assert channel.channel_invite(user1["token"], invalid_channel_id, user2["u_id"])

    other.clear()

def test_channel_invite_invalid_u_id():
    """
    Testing unsuccessful uses of channel_invite,
    focusing on invalid user ids
    """
    user1 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    auth.auth_register("hugosullivan@gmail.com", "hs1234", "Hugo", "Sullivan")
    invalid_u_id = -123456789
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    
    with pytest.raises(InputError):
        assert channel.channel_invite(user1["token"], new_channel["channel_id"], invalid_u_id)

    other.clear()

def test_channel_invite_unauthorised_user():
    """
    Testing unsuccessful uses of channel_invite,
    focusing on unauthorised users
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice1234", "Kevin", "Huang")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    user3 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    
    with pytest.raises(AccessError):
        assert channel.channel_invite(user2["token"], new_channel["channel_id"], user3["u_id"])

    other.clear()

#*******************************************************************************
# Channel_details_tests
# Successful
def test_channel_details_valid_token():
    """
    Testing successful uses of channel_details
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice1234", "Kevin", "Huang")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    channel_details = channel.channel_details(user1["token"], new_channel["channel_id"])
    member = [{
        "u_id": 1,
        "name_first": "Kevin",
        "name_last": "Huang",
        "profile_img_url": ""
    }]
    assert channel_details["name"] == "temp_channel"
    assert channel_details["owner_members"] == member
    assert channel_details["all_members"] == member

    other.clear()

def test_channel_details_valid_channel_id():
    """
    Testing successful uses of channel_details
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice1234", "Kevin", "Huang")
    valid_channel_id = channels.channels_create(user1["token"], "temp_channel", False)
    channel_details = channel.channel_details(user1["token"], valid_channel_id["channel_id"])
    member = [
        {
            "u_id": 1,
            "name_first": "Kevin",
            "name_last": "Huang",
            "profile_img_url": ""
        }
    ]
    assert channel_details["name"] == "temp_channel"
    assert channel_details["owner_members"] == member
    assert channel_details["all_members"] == member

    other.clear()

def test_channel_details_multiple_members():
    """
    Testing successful uses of channel_details without any errors
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "kh1234", "Kevin", "Huang")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    user3 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    user4 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    user5 = auth.auth_register("hugosullivan@gmail.com", "hs1234", "Hugo", "Sullivan")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    channel.channel_invite(user1["token"], new_channel["channel_id"], user2["u_id"])
    channel.channel_invite(user1["token"], new_channel["channel_id"], user3["u_id"])
    channel.channel_invite(user1["token"], new_channel["channel_id"], user4["u_id"])
    channel.channel_invite(user1["token"], new_channel["channel_id"], user5["u_id"])

    channel_details = channel.channel_details(user1["token"], new_channel["channel_id"])
    owner_members = [
        {
            "u_id": 1,
            "name_first": "Kevin",
            "name_last": "Huang",
            "profile_img_url": ""
        }
    ]
    all_members = [
        {
            "u_id": 1,
            "name_first": "Kevin",
            "name_last": "Huang",
            "profile_img_url": ""
        },
        {
            "u_id": 2,
            "name_first": "Lucy",
            "name_last": "Jang",
            "profile_img_url": ""
        },
        {
            "u_id": 3,
            "name_first": "Ricky",
            "name_last": "Mai",
            "profile_img_url": ""
        },
        {
            "u_id": 4,
            "name_first": "Elliot",
            "name_last": "Rotenstein",
            "profile_img_url": ""
        },
        {
            "u_id": 5,
            "name_first": "Hugo",
            "name_last": "Sullivan",
            "profile_img_url": ""
        }
    ]
    assert channel_details["name"] == "temp_channel"
    assert channel_details["owner_members"] == owner_members
    assert channel_details["all_members"] == all_members

    other.clear()

# Unsuccessful
def test_channel_details_invalid_token():
    """
    Testing unsuccessful uses of channel_details,
    focusing on invalid tokens
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "kh1234", "Kevin", "Huang")
    auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    with pytest.raises(AccessError):
        assert channel.channel_details("Invalid Token", new_channel["channel_id"])

    other.clear()

def test_channel_details_invalid_channel_id():
    """
    Testing unsuccessful uses of channel_details,
    focusing on invalid channel ids
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "kh1234", "Kevin", "Huang")
    channels.channels_create(user1["token"], "temp_channel", False)
    invalid_channel_id = 123456789
    with pytest.raises(InputError):
        assert channel.channel_details(user1["token"], invalid_channel_id)

    other.clear()

def test_channel_details_unauthorised_user():
    """
    Testing unsuccessful uses of channel_details,
    focusing on unauthorised users
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "kh1234", "Kevin", "Huang")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    with pytest.raises(AccessError):
        assert channel.channel_details(user2["token"], new_channel["channel_id"])
        
    other.clear()

#**************************************************************************************
# Checks a token with authority can join a channel
def test_channel_join_valid():
    """
    Testing successful uses of channel_join without any errors
    """
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    test_user2 = auth.auth_register("thebumble@hotmail.com", "password", "Bumble", "Bee")
    test_user3 = auth.auth_register("cliffbooth@hotmail.com", "password", "Cliff", "Jumper")
    test_channel_id1 = channels.channels_create(user_channel_creater["token"], "test", True)

    # Checks a user can join a public channel 
    channel.channel_join(test_user1["token"], test_channel_id1["channel_id"])
    channel.channel_join(test_user2["token"], test_channel_id1["channel_id"])
    channel.channel_join(test_user3["token"], test_channel_id1["channel_id"])
    list_result1 = channels.channels_list(test_user1["token"])["channels"]
    list_result2 = channels.channels_list(test_user2["token"])["channels"]
    list_result3 = channels.channels_list(test_user3["token"])["channels"]
    assert list_result1[0]["channel_id"] == test_channel_id1["channel_id"]
    assert list_result2[0]["channel_id"] == test_channel_id1["channel_id"]
    assert list_result3[0]["channel_id"] == test_channel_id1["channel_id"]
    test_public_channel_details = channel.channel_details(test_user1["token"],
                                                          test_channel_id1["channel_id"])

    member1 = None
    for member in test_public_channel_details["all_members"]:
        if member["u_id"] == test_user1["u_id"]:
            member1 = member
    assert member1 is not None
    member2 = None
    for member in test_public_channel_details["all_members"]:
        if member["u_id"] == test_user2["u_id"]:
            member2 = member
    assert member2 is not None
    member3 = None
    for member in test_public_channel_details["all_members"]:
        if member["u_id"] == test_user3["u_id"]:
            member3 = member
    assert member3 is not None

    other.clear()

# Test for an invalid channel id
def test_channel_join_invalid_channel():
    """
    Testing unsuccessful uses of channel_join,
    focusing on invalid channel ids
    """
    invalid_channel_id = "invalid_id"
    test_user1 = auth.auth_register("testHotRod@hotmail.com", "password", "Hot", "Rod")
    with pytest.raises(InputError):
        assert channel.channel_join(test_user1["token"], invalid_channel_id)
    list_result1 = channels.channels_list(test_user1["token"])["channels"]
    assert not list_result1

    other.clear()


# Test for an invalid token
# Assumes that the token is from an actual player
def test_channel_join_invalid_token():
    """
    Testing unsuccessful uses of channel_join,
    focusing on invalid channel ids
    """
    test_user1 = auth.auth_register("Breeeak@hotmail.com", "password", "Trail", "Breaker")
    user_channel_creater = auth.auth_register("creater@bigpond.com", "password", "Ultra", "Magnus")
    test_channel_private = channels.channels_create(user_channel_creater["token"], "test", False)
    with pytest.raises(AccessError):
        assert channel.channel_join(test_user1["token"], test_channel_private["channel_id"])

    other.clear()

# Tests that an error will appear if the user is already in the channel
def test_channel_join_invalid_user():
    """
    Testing unsuccessful uses of channel_join,
    focusing on users who are already in the channel
    """
    test_user1 = auth.auth_register("firefly@hotmail.com", "password", "Fire", "Flight")
    user_channel_creater = auth.auth_register("street@smart.com", "password", "Street", "Wise")
    test_channel_id = channels.channels_create(user_channel_creater["token"], "test", True)
    channel.channel_join(test_user1["token"], test_channel_id["channel_id"])
    with pytest.raises(InputError):
        assert channel.channel_join(test_user1["token"], test_channel_id["channel_id"])

    other.clear()
    
#*******************************************************************************

# Channel_messages tests
# Test for valid channel_id
def test_channel_messages_valid_channel():
    """
    Testing successful uses of channel_messages without any errors
    """
    user1 = auth.auth_register("lucyjang@gmail.com", "lucyj123", "Lucy", "Jang")
    auth.auth_register("monstersinc@gmail.com", "boo123", "James", "Sullivan")
    new_channel = channels.channels_create(user1["token"], "test channel", True)
    messages = channel.channel_messages(user1["token"], new_channel["channel_id"], 0)
    assert not messages["messages"]

    other.clear()
    
def test_channel_messages_over_50messages():
    """
    Testing a successful use of channel_messages,
    with over 50 messages in the channel
    """
    user1 = auth.auth_register("lucyjang@gmail.com", "lucyj123", "Lucy", "Jang")
    new_channel = channels.channels_create(user1["token"], "test channel", True)
    for _num_messages in range(0,56):
        message.message_send(user1["token"], new_channel["channel_id"], "i'm awesome")    
    messages = channel.channel_messages(user1["token"], new_channel["channel_id"], 0)
    assert messages["end"] == 50
    
    other.clear()
    
# Unsuccessful
def test_channel_messages_invalid_channel():
    """
    Testing unsuccessful uses of channel_messages,
    focusing on invalid channel id
    """
    user1 = auth.auth_register("monstersinc@gmail.com", "boo123", "Mike", "Wazowski")
    channels.channels_create(user1["token"], "test channel", True)

    invalid_channel_id = 1234
    with pytest.raises(InputError):
        assert channel.channel_messages(user1["token"], invalid_channel_id, 0)

    other.clear()

def test_channel_messages_invalid_start():
    """
    Testing unsuccessful uses of channel_messages,
    focusing on incorrect "start" values
    """
    user1 = auth.auth_register("monstersinc@gmail.com", "boo123", "James", "Sullivan")
    new_channel = channels.channels_create(user1["token"], "test channel", True)

    with pytest.raises(InputError):
        assert channel.channel_messages(user1["token"], new_channel["channel_id"], 50)
        assert channel.channel_messages(user1["token"], new_channel["channel_id"], -1)

    other.clear()


def test_channel_messages_not_member():
    """
    Testing unsuccessful uses of channel_messages,
    focusing on unauthorised users
    """
    user1 = auth.auth_register("lucyjang@gmail.com", "lucyj123", "Lucy", "Jang")
    user2 = auth.auth_register("monstersinc@gmail.com", "boo123", "James", "Sullivan")
    new_channel = channels.channels_create(user1["token"], "test channel", False)

    channel.channel_messages(user1["token"], new_channel["channel_id"], 0)
    with pytest.raises(AccessError):
        assert channel.channel_messages(user2["token"], new_channel["channel_id"], 0)

    other.clear()

# Test for invalid token
def test_channel_messages_invalid_token():
    """
    Testing unsuccessful uses of channel_messages,
    focusing on invalid tokens
    """
    user1 = auth.auth_register("lucyjang@gmail.com", "lucyj12", "Lucy", "Jang")
    user2 = auth.auth_register("validuser@gmail.com", "volcano123", "Mike", "Wazowski")
    new_channel = channels.channels_create(user1["token"], "test channel", False)

    with pytest.raises(AccessError):
        channel.channel_messages(user2["token"], new_channel["channel_id"], 0)

    other.clear()

# Channel_leave tests
# Test for valid channel id
def test_channel_leave_valid():
    """
    Testing successful uses of channel_leave without any errors
    """
    user1 = auth.auth_register("lucyjang@gmail.com", "lucyj123", "Lucy", "Jang")
    auth.auth_register("validuser@gmail.com", "volcanologist23", "Kevin", "Huang")
    new_channel = channels.channels_create(user1["token"], "test channel", True)

    assert channel.channel_leave(user1["token"], new_channel["channel_id"]) == {}

    other.clear()


def test_channel_leave_invalid():
    """
    Testing unsuccessful uses of channel_leave,
    focusing on invalid channel id
    """
    invalid_channel_id = ""
    user1 = auth.auth_register("lucyjang@gmail.com", "lucyj123", "Lucy", "Jang")
    channels.channels_create(user1["token"], "test channel", True)
    with pytest.raises(InputError):
        channel.channel_leave(user1["token"], invalid_channel_id)
        list_result = channels.channels_list(user1["token"])
        assert len(list_result) != invalid_channel_id

    other.clear()

def test_channel_leave_not_existing():
    """
    Testing unsuccessful uses of channel_leave,
    focusing on leaving non existant channels
    """
    user1 = auth.auth_register("lucyjang@gmail.com", "lucyj12", "Lucy", "Jang")
    new_channel = channels.channels_create(user1["token"], "test channel", True)
    channel.channel_leave(user1["token"], new_channel["channel_id"])
    with pytest.raises(AccessError):
        channel.channel_leave(user1["token"], new_channel["channel_id"])

    other.clear()

def test_channel_leave_invalid_token():
    """
    Testing unsuccessful uses of channel_leave,
    focusing on invalid tokens
    """
    user1 = auth.auth_register("lucyjang@gmail.com", "lucyj12", "Lucy", "Jang")
    user2 = auth.auth_register("validuser@gmail.com", "vulture123", "Mike", "Wazowski")
    new_channel = channels.channels_create(user1["token"], "test channel", True)

    with pytest.raises(AccessError):
        channel.channel_leave(user2["token"], new_channel["channel_id"])

    other.clear()

#*******************************************************************************
# Channel_invite tests
# Tests the function works when the conditions are valid
def test_channel_addowner_valid():
    """
    Testing successful uses of channel_addowner without any errors
    """
    creator = auth.auth_register("bechcomber@bigpond.com", "password", "Beach", "Comber")
    test_user1 = auth.auth_register("streaksahead@hotmail.com", "password", "Blue", "Streak")
    test_user2 = auth.auth_register("alert@hotmail.com", "password", "Red", "Alert")
    test_user3 = auth.auth_register("screener@hotmail.com", "password", "Smoke", "Screen")
    priv_channel = channels.channels_create(creator["token"], "test_channel_id1", False)
    channel_id = priv_channel["channel_id"]
    channel.channel_invite(creator["token"], channel_id, test_user1["u_id"])
    channel.channel_invite(creator["token"], channel_id, test_user2["u_id"])
    channel.channel_invite(creator["token"], channel_id, test_user3["u_id"])
    channel.channel_addowner(creator["token"], channel_id, test_user1["u_id"])
    channel.channel_addowner(creator["token"], channel_id, test_user2["u_id"])
    channel.channel_addowner(creator["token"], channel_id, test_user3["u_id"])
    
    # Asserts would fail if channel_addowner didn"t work
    assert channel.channel_removeowner(creator["token"], channel_id, test_user1["u_id"]) == {}
    assert channel.channel_removeowner(creator["token"], channel_id, test_user2["u_id"]) == {}
    assert channel.channel_removeowner(creator["token"], channel_id, test_user3["u_id"]) == {}
    other.clear()

# Unsuccessful
def channel_addowner_invalid_owner():
    """
    Testing unsuccessful uses of channel_addowner,
    focusing on members who are already owners
    """
    user_channel_creater = auth.auth_register("backout@bigpond.com", "password", "Out", "Back")
    test_user = auth.auth_register("poweerglider87@hotmail.com", "password", "Power", "Glide")
    test_channel_private = channels.channels_create(user_channel_creater["token"], "test", False)
    channel.channel_invite(user_channel_creater["token"], test_channel_private, test_user["u_id"])
    channel.channel_addowner(user_channel_creater["token"], test_channel_private, test_user["u_id"])
    with pytest.raises(InputError):
        assert channel.channel_addowner(user_channel_creater["token"],
                                        test_channel_private,
                                        test_user["u_id"]
                                       )
    other.clear()


def channel_addowner_invalid_channel():
    """
    Testing successful uses of channel_addowner,
    focusing on invalid channel ids
    """
    user_channel_creater = auth.auth_register("omegaup@bigpond.com", "password", "Omega", "Supreme")
    test_user = auth.auth_register("gater@hotmail.com", "password", "Tail", "Gate")
    private = channels.channels_create(user_channel_creater["token"], "test", False)
    with pytest.raises(InputError):
        assert channel.channel_addowner(user_channel_creater["token"], private, test_user["u_id"])
        
    other.clear()


def channel_addowner_invalid_owner_not_in_channel():
    """
    Testing unsuccessful uses of channel_addowner,
    focusing on members who are not in the channel
    """
    user_channel_creater = auth.auth_register("starport@bigpond.com", "password", "Broad", "Side")
    invalid_creator = auth.auth_register("aircat@bigpond.com", "password", "Sky", "Lynx")
    test_user = auth.auth_register("stormboy@hotmail.com", "password", "Sand", "Storm")
    private = channels.channels_create(user_channel_creater["token"], "test", False)
    channel.channel_invite(user_channel_creater["token"], private, test_user["u_id"])
    with pytest.raises(AccessError):
        assert channel.channel_addowner(invalid_creator["token"], private, test_user["u_id"])
        
    other.clear()

def channel_addowner_invalid_owner_not_owner():
    """
    Testing unsuccessful uses of channel_addowner,
    focusing on members who are not in the channel
    """
    user_channel_creater = auth.auth_register("arraid@bigpond.com", "password", "Air", "Raid")
    invalid_creater = auth.auth_register("bart@bigpond.com", "password", "Slimg", "Shot")
    test_user = auth.auth_register("airdiver@hotmail.com", "password", "Sky", "Dive")
    test_private = channels.channels_create(user_channel_creater["token"], "test", False)
    channel.channel_invite(user_channel_creater["token"], test_private, test_user["u_id"])
    channel.channel_invite(user_channel_creater["token"], test_private, invalid_creater["u_id"])
    with pytest.raises(AccessError):
        assert channel.channel_addowner(invalid_creater["token"], test_private, test_user["u_id"])
        
    other.clear()

#*******************************************************************************
# Tests the function works when the conditions are valid
def test_channel_removeowner_valid():
    """
    Testing successful uses of channel_removeowner without any errors
    """
    # same as test_channel_addowner_valid because they"re testing different functions
    creator = auth.auth_register("bechcomber@bigpond.com", "password", "Beach", "Comber")
    test_user1 = auth.auth_register("streaksahead@hotmail.com", "password", "Blue", "Streak")
    test_user2 = auth.auth_register("alert@hotmail.com", "password", "Red", "Alert")
    test_user3 = auth.auth_register("screener@hotmail.com", "password", "Smoke", "Screen")
    priv_channel = channels.channels_create(creator["token"], "test_channel_id1", False)
    channel_id = priv_channel["channel_id"]
    channel.channel_invite(creator["token"], channel_id, test_user1["u_id"])
    channel.channel_invite(creator["token"], channel_id, test_user2["u_id"])
    channel.channel_invite(creator["token"], channel_id, test_user3["u_id"])
    channel.channel_addowner(creator["token"], channel_id, test_user1["u_id"])
    channel.channel_addowner(creator["token"], channel_id, test_user2["u_id"])
    channel.channel_addowner(creator["token"], channel_id, test_user3["u_id"])
    
    assert channel.channel_removeowner(creator["token"], channel_id, test_user1["u_id"]) == {}
    assert channel.channel_removeowner(creator["token"], channel_id, test_user2["u_id"]) == {}
    assert channel.channel_removeowner(creator["token"], channel_id, test_user3["u_id"]) == {}
    
    other.clear()
    
def channel_removeowner_invalid_owner():
    """
    Testing unsuccessful uses of channel_removeowner,
    focusing on people who aren't owners
    """
    creater = auth.auth_register("backout@bigpond.com", "password", "Out", "Back")
    test_user = auth.auth_register("poweerglider87@hotmail.com", "password", "Power", "Glide")
    test_private = channels.channels_create(creater["token"], "test_channel_id", False)
    channel.channel_invite(creater["token"], test_private, test_user["u_id"])
    
    with pytest.raises(InputError):
        assert channel.channel_removeowner(creater["token"], test_private, test_user["u_id"])
        
    other.clear()


def channel_removeowner_invalid_channel():
    """
    Testing unsuccessful uses of channel_removeowner,
    focusing on invalid channel ids
    """
    creater = auth.auth_register("omegaup@bigpond.com", "password", "Omega", "Supreme")
    test_user = auth.auth_register("gater@hotmail.com", "password", "Tail", "Gate")
    channel_private = channels.channels_create(creater["token"], "test", False)
    with pytest.raises(InputError):
        assert channel.channel_removeowner(creater["token"], channel_private, test_user["u_id"])
        
    other.clear()

def channel_removeowner_invalid_owner_not_in_channel():
    """
    Testing unsuccessful uses of channel_removeowner,
    focusing on remover not in the channel
    """
    channel_creater = auth.auth_register("starport@bigpond.com", "password", "Broad", "Side")
    invalid_creater = auth.auth_register("aircat@bigpond.com", "password", "Sky", "Lynx")
    test_user = auth.auth_register("stormboy@hotmail.com", "password", "Sand", "Storm")
    test_private = channels.channels_create(channel_creater["token"], "test", False)
    channel.channel_invite(channel_creater["token"], test_private, test_user["u_id"])
    channel.channel_addowner(channel_creater["token"], test_private, test_user["u_id"])
    
    with pytest.raises(AccessError):
        assert channel.channel_addowner(invalid_creater["token"], test_private, test_user["u_id"])
        
    other.clear()

# Tests that the token being used to remove the member an owner
# is from someone in the channel and is a owner
def channel_removeowner_invalid_owner_not_owner():
    """
    Testing unsuccessful uses of channel_removeowner,
    focusing on remover not being an owner
    """
    creater = auth.auth_register("arraid@bigpond.com", "password", "Air", "Raid")
    invalid_creater = auth.auth_register("bart@bigpond.com", "password", "Slimg", "Shot")
    test_user = auth.auth_register("airdiver@hotmail.com", "password", "Sky", "Dive")
    test_private = channels.channels_create(creater["token"], "test_channel_id", False)
    channel.channel_invite(creater["token"], test_private, test_user["u_id"])
    channel.channel_invite(creater["token"], test_private, invalid_creater["u_id"])
    channel.channel_addowner(creater["token"], test_private, test_user["u_id"])
    
    with pytest.raises(AccessError):
        assert channel.channel_addowner(invalid_creater["token"], test_private, test_user["u_id"])
        
    other.clear()
