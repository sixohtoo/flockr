"""
Contains common "user story" tests
Will test error conditions that a user can reasonably do as in a user cannot pass in
an incorrect token

re(regex): Gives access to regex for valid_email
pytest(pytest module): Gives access to pytest command
"""
import story_functions as sf
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import pytest



# Fixture which gets the URL of the server and starts it
@pytest.fixture
def url():
    """
    Allows pytest to create a new server.
    Returns url for new server.
    """
    url_re = re.compile(r" \* Running on ([^ ]*)")
    server = Popen(["python3", "src/server.py"], stderr = PIPE, stdout = PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")


def test_edit_profile_and_messages(url):
    """
    Tests editing everything that can be edited
    """

    # Fred and Alan register
    Fred = sf.register_user("Fred","Smith", "fred@gmail.com", "Freddo", url)
    Alan = sf.register_user("Alan","Borm", "alan@yahoo.com", "Boromir", url)

    sf.assert_different_people(Fred, Alan)

    # Fred creates channel 'welcome'
    chan1 = sf.create_channel(Fred['token'], "Welcome", True, url)
    assert chan1 == 1

    # Fred sends message to empty channel
    mess1 = sf.send_message(Fred["token"], chan1, "Hello nobody :(", url)
    assert mess1 == 1

    # Alan join channel
    join1 = sf.join_channel(Alan['token'], chan1, url)
    assert join1 == {}

    # Fred deletes message
    rem1 = sf.remove_message(Fred['token'], mess1, url)
    assert rem1 == {}

    # Alan sends a message
    mess2 = sf.send_message(Alan['token'], chan1, "Good morning Fred!", url)
    assert mess2 == 2

    # Fred changes his name unsuccessfully
    name_change1 = sf.change_name(Fred['token'], 
        "I wonder how long my name should be. Is there a limit or nah",
        "Wazco", url)
    assert name_change1['message'] == "<p>First name is invalid</p>"
    assert name_change1['code'] == 400

    # Fred changes his last name successfully
    name_change2 = sf.change_name(Fred['token'], "Howard", "Wazco", url)
    assert name_change2 == {}

    # Fred changes his handle unsuccessfully
    handle_change1 = sf.change_handle(Fred['token'], "AlanBorm", url)
    assert handle_change1['message'] == "<p>Handle already in use</p>"
    assert handle_change1['code'] == 400 

    # Fred tries again
    handle_change2 = sf.change_handle(Fred['token'], "HW", url)
    assert handle_change2['message'] == "<p>Handle is invalid</p>"
    assert handle_change2['code'] == 400 

    # Fred successfully changes his handle
    handle_change3 = sf.change_handle(Fred['token'], "WazcoWizard", url)
    assert handle_change3 == {}

    # Alan edits his original message
    edit1 = sf.edit_message(Alan['token'], mess2, "Good morning Howard!", url)
    assert edit1 == {}

    # Ex-Fred (now Howard) gets annoyed (sends attempted message)
    msg = "A" * 1001
    mess3 = sf.send_message(Fred['token'], chan1, msg, url)
    assert mess3["message"] ==  "<p>Invalid message</p>"
    assert mess3['code'] == 400

    # Howard is now angry (sends messages)
    msg2 = ">:( " * 200
    mess4 = sf.send_message(Fred['token'], chan1, msg2, url)
    assert mess4 == 3

    # Alan checks the message history using channel_messages
    history1 = sf.check_messages(Alan['token'], chan1, 0, url)
    assert history1["messages"][0]["message"] == ">:( " * 200
    assert history1["messages"][1]["message"] == "Good morning Howard!"
    assert history1["start"] == 0
    assert history1["end"] == -1

def test_registering_login_and_logout(url):
    """
    Tests an attempt to register with invalid details (password, email, first name, last name) including:
    * auth_register
    * auth_logout
    * channel_create
    
    """
    #Yanik trying to register with password that is too short
    reg1 = sf.register_user("Yanik", "Gulm", "bbq@gmail.com", "123", url)
    assert reg1["message"] == "<p>Password is invalid</p>"
    assert reg1["code"] == 400
    
    
    #Yanik trying to register with invalid email
    reg2 = sf.register_user("Yanik", "Gulm", "yanik1@gmailcom", "123Ters", url)
    assert reg2["message"] == "<p>Email is invalid</p>"
    assert reg2["code"] == 400
    
    #Yanik tries to register with invalid first name
    name1 = "Yanik" * 20
    reg3 = sf.register_user(name1, "Gulm", "bbq@gmail.com", "123Ters", url)
    assert reg3["message"] == "<p>First name is invalid</p>"
    assert reg3["code"] == 400
    
    #Yanik tries to register with invalid last name 
    name2 = "Gulm" * 20
    reg4 = sf.register_user("Yanik", name2, "bbq@gmail.com", "123Ters", url)
    assert reg4["message"] == "<p>Last name is invalid</p>"
    assert reg4["code"] == 400
    
    #Yanik successfully registers
    Yanik = sf.register_user("Yanik", "Gulm", "bbq@gmail.com", "123Ters", url)

    #Arthur trying to register with Yanik's email
    reg5 = sf.register_user("Arthur", "Holmes", "bbq@gmail.com", "HMMMMM", url)
    assert reg5["message"] == "<p>Email already in use</p>"
    assert reg5["code"] == 400

    #Yanik creates a new channel called "My First Channel" and joins
    chan1 = sf.create_channel(Yanik['token'], "My First Channel", True, url)
    assert chan1 == 1
    
    #Yanik successfully logs out
    logout1 = sf.logout_user(Yanik['token'], url)
    assert logout1['is_success'] == True

    
def test_hostile_takeover(url):
    """
    Tests using commands with different channel permissions
    and changing profile attributes
    """
    # Joe and Henry register accounts
    Joe = sf.register_user("Joe", "Gostt", "ttsogoej@liamg.moc", "sdrawkcab", url)
    Henry = sf.register_user("Henry", "Prill", "henry@gmail.com", "word pass", url)

    sf.assert_different_people(Joe, Henry)

    # Henry makes a new channel (General)
    chan1 = sf.create_channel(Henry['token'], "General", False, url)
    assert chan1 == 1

    # Henry invites Joe
    invite1 = sf.invite_channel(Henry['token'], chan1, Joe['u_id'], url)
    assert invite1 == {}

    # Joe says "goodbye"
    mess1 = sf.send_message(Joe['token'], chan1, "Goodbye >:)", url)
    assert mess1 == 1

    # Joe (owner of Flockr) removes Henry's owner privileges
    remowner1 = sf.remove_owner(Joe['token'], chan1, Henry['u_id'], url)
    assert remowner1 == {}

    # Henry tries to get owner privileges back
    addowner1 = sf.add_owner(Henry['token'], chan1, Henry['u_id'], url)
    assert addowner1['message'] == "<p>User is not owner of channel</p>"
    assert addowner1['code'] == 400

    # Henry leaves channel
    leave1 = sf.leave_channel(Henry['token'], chan1, url)
    assert leave1 == {}

    # Henry logs out
    logout1 = sf.logout_user(Henry['token'], url)
    assert logout1 == { "is_success" : True }

    # Joe edits message
    edit1 = sf.edit_message(Joe['token'], mess1, "I win.", url)
    assert edit1 == {}

    # Joe leaves channel
    leave2 = sf.leave_channel(Joe['token'], chan1, url)
    assert leave2 == {}

    # Joe creates new channel (General)
    chan2 = sf.create_channel(Joe['token'], "General", False, url)
    assert chan2 == 2

    # Joe changes his name
    name1 = sf.change_name(Joe['token'], "The", "KING", url)
    assert name1 == {}

    # Joe changes his email
    email1 = sf.change_email(Joe['token'], 'theKING@gmail.com', url)
    assert email1 == {}

    # Joe changes his handle
    handle1 = sf.change_handle(Joe['token'], "WeAreNumberOne", url)
    assert handle1 == {}

    # Joe logs off
    logout2 = sf.logout_user(Joe['token'], url)
    assert logout2 == { "is_success" : True }

    # Joe logs in successfully
    new_Joe = sf.login_user("theKING@gmail.com", "sdrawkcab", url)
    assert len(new_Joe) == 2
    assert new_Joe["token"] is not None
    assert new_Joe["token"] != Joe["token"] # Could potentially fail 1 in 100,000 times
    assert new_Joe["u_id"] == Joe["u_id"]

    # Joe admired his new profile
    profile1 = sf.check_profile(new_Joe['token'], new_Joe['u_id'], url)
    expected_user = {
        "name_first" : "The",
        "name_last" : "KING",
        "u_id" : 1,
        "email" : "theking@gmail.com",
        "handle_str" : "WeAreNumberOne",
        "profile_img_url" : ''
    }
    
    #expected_profile ={ "user" : expected_user }
    assert profile1 == expected_user#expected_profile

    # Joe logs out
    logout3 = sf.logout_user(new_Joe['token'], url)
    assert logout3 == { "is_success" : True }

def test_editing_removing_messages(url):
    """
    Tests a user going on a message editing and removing spree:
    * auth_register
    * channels_create (public)
    * channel_join
    * channe_messages
    * message_send 
    * message_remove
    * message_edit
    * channel_addowner
    """

    # Paul and Seal register
    Paul = sf.register_user("Paul", "Schlamp", "rs@bigpond.com", "m23rdewf2DE", url)
    Seal = sf.register_user("Seal", "Sire", "FireSire@hotmail.com", "phlem$#PHLEM", url)

    sf.assert_different_people(Paul, Seal)
    
    # Paul creates a channel "General"
    chan1 = sf.create_channel(Paul['token'], "Misc", True, url)
    assert chan1 == 1
    
    # Seal joins the channel "Misc"
    join1 = sf.join_channel(Seal['token'], chan1, url)
    assert join1 == {}

    # Paul and Seal send messages to each other in "Misc"
    msg1 = "First rule in general channel do not talkaboutgeneralchannel"
    mess1 = sf.send_message(Seal['token'], chan1, msg1, url)
    assert mess1 == 1
    
    msg2 = "Second Rule ... First rule again"
    mess2 = sf.send_message(Paul['token'], chan1, msg2, url)
    assert mess2 == 2
    
    msg3 = "You seem bad at this"
    mess3 = sf.send_message(Seal['token'], chan1, msg3, url)
    assert mess3 == 3

    # Paul addes Seal as an owner of "Misc"
    addowner1 = sf.add_owner(Paul['token'], chan1, Seal['u_id'], url)
    assert addowner1 == {}

    # Seal calls for a list of all messages in "Misc"
    messages1 = sf.check_messages(Seal['token'], chan1, 0, url)
    assert len(messages1['messages']) == 3
    assert messages1["end"] == -1 

    # Seal edits a message
    msg4 = "New message YaYaYaYa" 
    for sent_message in messages1['messages']:
        edit = sf.edit_message(Seal['token'], sent_message['message_id'], msg4, url)
        assert edit == {}

    messages2 = sf.check_messages(Seal['token'], chan1, 0, url)
    assert len(messages2['messages']) == 3
    assert messages2["end"] == -1

    # Check message_edit worked
    for sent_message in messages2["messages"]:
        assert sent_message["message"] == msg4

    # Slam registers and joins the channel "Misc"
    Slam = sf.register_user("Slam","Bam","nam@bigpond.net", "rightEOUS!ath", url)

    join2 = sf.join_channel(Slam['token'], chan1, url)
    assert join2 == {}

    # Slam sends a message to "Misc"
    msg5 = "I love your channel"
    mess4 = sf.send_message(Slam['token'], chan1, msg5, url)
    assert mess4 == 4

    # Slam deletes their message

    """Mimics how a person would find and delete a message"""
    search1 = sf.search_message(Slam['token'], "love", url)
    assert len(search1) == 1

    for message in search1:
        found_message = message['message_id']
    rem1 = sf.remove_message(Slam['token'], found_message, url)
    assert rem1 == {}

    # Slam sends a new message to "Misc"
    msg6 = "I REALLY love your channel"
    mess5 = sf.send_message(Slam['token'], chan1, msg6, url)
    assert mess5 == 5

    # Seal removes the message
    rem2 = sf.remove_message(Seal['token'], mess5, url)
    assert rem2 == {}

    messages3 = sf.check_messages(Seal['token'], chan1, 0, url)
    assert len(messages3['messages']) == 3

def test_admin_permission_change(url):
    """
    Tests whether an owner of Flockr is an owner of all channels they've joined
    """

    # Jack and Jill register
    Jack = sf.register_user("Jack", "Smith", "jsmith@gmail.com", "jackjack123", url)
    Jill = sf.register_user("Jill", "Smith", "jillsmith12@gmail.com", "jilljill123", url)

    sf.assert_different_people(Jack, Jill)

    # Jack makes Jill an owner/admin of Flockr
    change_perm1 = sf.change_permission(Jack['token'], Jill['u_id'], 1, url)
    assert change_perm1 == {}

    # Jack creates and joins a channel "Jack"s channel"
    chan1 = sf.create_channel(Jack['token'], "Jack's Channel", True, url)
    assert chan1 == 1

    # Jill joins the channel
    join1 = sf.join_channel(Jill['token'], chan1, url)
    assert join1 == {}

    # Jack checks for the owners of "Jack's Channel"
    channel_details = sf.channel_info(Jack['token'], chan1, url)

    assert channel_details["name"] == "Jack's Channel"
    assert channel_details["owner_members"][0]["u_id"] == Jack["u_id"]
    assert channel_details["all_members"][0]["u_id"] == Jack["u_id"] 
    assert channel_details["all_members"][1]["u_id"] == Jill["u_id"]

def test_admin_permission_change_invalid(url):
    """
    Tests invalid inputs of changing owner/admin permissions
    """

    # Jack and Jill register
    Jack = sf.register_user("Jack", "Smith", "jsmith@gmail.com", "jackjack123", url)
    Jill = sf.register_user("Jill", "Smith", "jillsmith12@gmail.com", "jilljill123", url)
    sf.assert_different_people(Jack, Jill)

    # Jack attempts change Jill's permissions with nvalid permission_id value
    change_perm1 = sf.change_permission(Jack['token'], Jill['u_id'], 3, url)
    assert change_perm1["message"] == "<p>Permission id is not a valid value</p>"
    assert change_perm1["code"] == 400

    # Jack attempts to make a non-existent member an owner/admin
    change_perm2 = sf.change_permission(Jack['token'], "invalid_uid", 1, url)
    assert change_perm2["message"] == "<p>Target user does not exist</p>"
    assert change_perm2["code"] == 400

    # Jill attempts to change Jack"s permissions
    change_perm3 = sf.change_permission(Jill['token'], Jack['u_id'], 2, url)
    assert change_perm3["message"] == "<p>User is not owner of Flockr</p>"
    assert change_perm3["code"] == 400


def test_invalid_user_inputs(url):
    """
    Tests realistic invalid inputs from a user.
    e.g Entering an incorrect password is realistic
    but passing an incorrect token is not very realistic
    because the user has little control over that
    """
    # Jack registers
    Jack = sf.register_user("Jack", "Smith", "jsmith@gmail.com", "jackjack123", url)

    # Jack attempts to change his first name to a short name
    name1 = sf.change_name(Jack['token'], '', 'Smith', url)
    assert name1["message"] == "<p>First name is invalid</p>"
    assert name1["code"] == 400

    # Jack attempts to change his first name to a longer name
    msg1 = "JacksJacksJacksJacksJacksJacksJacksJacksJacksJacksJacks"
    name2 = sf.change_name(Jack['token'], msg1, "Smith", url)
    assert name2["message"] == "<p>First name is invalid</p>"
    assert name2["code"] == 400

    # Jack attempts to change his last name to a shorter name
    name3 = sf.change_name(Jack['token'], 'Jack', '', url)
    assert name3["message"] == "<p>Last name is invalid</p>"
    assert name3["code"] == 400

    # Jack attempts to change his last name to a longer name
    msg2 = "SmithSmithSmithSmithSmithSmithSmithSmithSmithSmithSmithSmith"
    name4 = sf.change_name(Jack['token'], 'Jack', msg2, url)
    assert name4["message"] == "<p>Last name is invalid</p>"
    assert name4["code"] == 400

    # Jack attempts to change his email
    email1 = sf.change_email(Jack['token'], 'jsmithgmail.com', url)
    assert email1["message"] == "<p>Email is invalid</p>"
    assert email1["code"] == 400

    # Jim registers
    Jim = sf.register_user("Jim","Smath", "js@gmail.com", "pasffef2U", url)

    # Jack attempts to change his email to Jim's
    email2 = sf.change_email(Jack['token'], 'js@gmail.com', url)
    assert email2["message"] == "<p>Email already in use</p>"
    assert email2["code"] == 400

    # Jack attempts to change his handle shorter
    handle1 = sf.change_handle(Jack['token'], 'si', url)
    assert handle1["message"] == "<p>Handle is invalid</p>"
    assert handle1["code"] == 400

    # Jack attempts to make his handle longer
    msg3 = 'SisinSisinSisinSisinSisin'
    handle2 = sf.change_handle(Jack['token'], msg3, url)
    assert handle2["message"] == "<p>Handle is invalid</p>"
    assert handle2["code"] == 400

    # Jim and Jack change their handles to be the same
    msg4 = "jsjsjsjs"
    handle3 = sf.change_handle(Jack['token'], msg4, url)
    assert handle3 == {}

    handle4 = sf.change_handle(Jim['token'], msg4, url)
    assert handle4["message"] == "<p>Handle already in use</p>"
    assert handle4["code"] == 400

    # Jack creates a channel "jackattacka"
    chan1 = sf.create_channel(Jack['token'], "jackattacka", True, url)
    assert chan1 == 1

    # Jack sends some messages to "jackattacka"
    long_string = "602" * 1000
    mess1 = sf.send_message(Jack['token'], chan1, long_string, url)
    assert mess1["message"] == "<p>Invalid message</p>" 
    assert mess1["code"] == 400

    msg5 = "fefebfoebfnijfcnshoffjZDfnJH"
    mess2 = sf.send_message(Jack['token'], chan1, msg5, url)
    assert mess2 == 1

    # Jim joins "jackattacka"
    join1 = sf.join_channel(Jim['token'], chan1, url)
    assert join1 == {}

    # Jim attempts to remove a message
    rem1 = sf.remove_message(Jim['token'], mess2, url)
    assert rem1["message"] == "<p>User is not creator or owner</p>"
    assert rem1["code"] == 400

    # Jim attempts to edit a message
    edit1 = sf.edit_message(Jim['token'], mess2, "We win these", url)
    assert edit1["message"] == "<p>User is not creator or owner</p>"
    assert edit1["code"] == 400

    # Jack attempts to edit a message
    edit2 = sf.edit_message(Jack['token'], mess2, long_string, url)
    assert edit2["message"] == "<p>Invalid message</p>"
    assert edit2["code"] == 400

def test_list_users_and_channels(url):
    """
    Tests listing of all channels, channels of the user and all users on Flockr
    """
    # Jack and Jill register
    Jack = sf.register_user("Jack", "Smith", "jsmith@gmail.com", "jackjack123", url)
    Jill = sf.register_user("Jill", "Smith", "jillsmith12@gmail.com", "jilljill123", url)
    sf.assert_different_people(Jack, Jill)

    # Jack gets a list of all users
    users = sf.user_list(Jack['token'], url)
    assert users[0]["u_id"] == Jack["u_id"]
    assert users[1]["u_id"] == Jill["u_id"]

    # Jack creates and joins the channels "First" and "Second"
    chan1 = sf.create_channel(Jack['token'], "First", True, url)
    chan2 = sf.create_channel(Jack['token'], "Second", True, url)
    assert chan1 == 1
    assert chan2 == 2

    # Jack calls for a list of all channels in Flockr
    listall1 = sf.channel_listall(Jack['token'], url)
    channels_listall_result = [
        {
            "channel_id" : 1,
            "name" : "First",
        },
        {
            "channel_id": 2,
            "name" : "Second"
        }
    ]

    assert listall1 == channels_listall_result

    # Jill joins "Second Channel"
    join1 = sf.join_channel(Jill['token'], chan2, url)
    assert join1 == {}

    # Jill calls for a list of all channels she has joined
    listin1 = sf.channel_list(Jill['token'], url)
    channels_list_result = [
        {
            "channel_id": 2,
            "name" : "Second"
        }
    ]
    # assert listin1 == {"channels" : channels_list_result}
    assert listin1 == channels_list_result

def test_message_interactions(url):
    """
    Tests every different thing you can do to a message
    """
    # Testing with owner permissinos
    user1 = sf.register_user("Jeffrey", "Hoits", "jeffsemail@gmail.com", "gambling", url)
    assert user1['u_id'] == 1

    chan1 = sf.create_channel(user1['token'], "Testing testing 123", False, url)
    assert chan1 == 1

    mess1 = sf.send_message(user1['token'], chan1, "RADIOACTIVE -- DO NOT TOUCh", url)
    assert mess1 == 1

    pin1 = sf.pin_message(user1['token'], mess1, url)
    assert pin1 == {}

    react1 = sf.react_message(user1['token'], mess1, 1, url)
    assert react1 == {}

    edit1 = sf.edit_message(user1['token'], mess1, 'pls stay pinned', url)
    assert edit1 == {}

    messages = sf.check_messages(user1['token'], chan1, 0, url)
    assert messages['messages'][0]['is_pinned']

    unpin1 = sf.unpin_message(user1['token'], mess1, url)
    assert unpin1 == {}

    unreact1 = sf.unreact_message(user1['token'], mess1, 1, url)
    assert unreact1 == {}

    # Testing with member permissions
    user2 = sf.register_user("Member", "ofGroup", "member@liamg.com", "member", url)
    sf.assert_different_people(user1, user2)

    pin2 = sf.pin_message(user2['token'], mess1, url)
    assert pin2['message'] == "<p>User is not owner of channel</p>"
    assert pin2['code'] == 400

    react2 = sf.react_message(user1['token'], mess1, 1, url)
    assert react2 == {}

    edit2 = sf.edit_message(user1['token'], mess1, 'pls stay pinned', url)
    assert edit2 == {}

    messages = sf.check_messages(user1['token'], chan1, 0, url)
    assert not messages['messages'][0]['is_pinned']

    unpin2 = sf.unpin_message(user2['token'], mess1, url)
    assert unpin2['message'] == "<p>Message is not currently pinned</p>"
    assert unpin2['code'] == 400


    unreact1 = sf.unreact_message(user1['token'], mess1, 1, url)
    assert unreact1 == {}

    rem1 = sf.remove_message(user2['token'], mess1, url)
    assert rem1['message'] == "<p>User is not creator or owner</p>"
    assert rem1['code'] == 400

    rem2 = sf.remove_message(user1['token'], mess1, url)
    assert rem2 == {}

def test_interacting_with_standup_message(url):
    user = sf.register_user("Standup", "Guy", "comedy@bigpond.com", "comedygold", url)
    assert user['u_id'] == 1

    chan1 = sf.create_channel(user['token'], "LAUGH", False, url)
    assert chan1 == 1

    # Create a standup and send messages to it
    stan1 = sf.start_standup(user['token'], chan1, 2, url)
    assert stan1 != {} and stan1 != None

    check1 = sf.get_standup(user['token'], chan1, url)
    assert check1['is_active']
    assert check1['time_finish'] == stan1

    mess1 = sf.send_standup(user['token'], chan1, "This is the end", url)
    assert mess1 == {}

    mess2 = sf.send_standup(user['token'], chan1, "Message 2 :/", url)
    assert mess2 == {}

    check2 = sf.get_standup(user['token'], chan1, url)
    assert check2 == check1

    # Sleep for more than standup to account for bad internet
    sleep(3)

    # Standup is finished
    check3 = sf.get_standup(user['token'], chan1, url)
    assert check3 != check1
    assert not check3['is_active']

    # Find standup message (none of the sf return message_id)
    messages = sf.check_messages(user['token'], chan1, 0, url)
    assert len(messages['messages']) == 1
    mess1 = messages['messages'][0]['message_id']
    assert mess1 == 1

    # Check if can interact with a standup message
    pin1 = sf.pin_message(user['token'], mess1, url)
    assert pin1 == {}

    react1 = sf.react_message(user['token'], mess1, 1, url)
    assert react1 == {}

    edit1 = sf.edit_message(user['token'], mess1, 'STANDUP == BAD', url)
    assert edit1 == {}

    rem1 = sf.remove_message(user['token'], mess1, url)
    assert rem1 == {}

    unpin1 = sf.unpin_message(user['token'], mess1, url)
    assert unpin1['message'] == "<p>Message does not exist</p>"
    assert unpin1['code'] == 400

    unreact1 = sf.unreact_message(user['token'], mess1, 1, url)
    assert unreact1['message'] == '<p>Message does not exist</p>'
    assert unreact1['code'] == 400

def test_interacting_with_sendlater_message(url):
    user = sf.register_user("Sned", "Ltaer", "msg@gmail.com", "notnow", url)
    assert user['u_id'] == 1

    chan1 = sf.create_channel(user['token'], "Cahnnel", True, url)
    assert chan1 == 1

    msg = "Hopefully this will arive soon"
    mess1 = sf.send_later(user['token'], chan1, msg, sf.time_from_now(2), url)
    assert mess1 == 1

    sleep(2)

    pin1 = sf.pin_message(user['token'], mess1, url)
    assert pin1 == {}

    react1 = sf.react_message(user['token'], mess1, 1, url)
    assert react1 == {}

    edit1 = sf.edit_message(user['token'], mess1, 'SEDNLATRE != GOOD', url)
    assert edit1 == {}

    rem1 = sf.remove_message(user['token'], mess1, url)
    assert rem1 == {}

    unpin1 = sf.unpin_message(user['token'], mess1, url)
    assert unpin1['message'] == "<p>Message does not exist</p>"
    assert unpin1['code'] == 400

    unreact1 = sf.unreact_message(user['token'], mess1, 1, url)
    assert unreact1['message'] == '<p>Message does not exist</p>'
    assert unreact1['code'] == 400

def test_http_hangman(url):
    creator = sf.register_user("The", "Creator", "Gabe@gmail.com", "gamers", url)
    guesser = sf.register_user("The", "Guesser", "Guesser@gmail.com", "Kahoot", url)
    sf.assert_different_people(creator, guesser)

    chan1 = sf.create_channel(creator['token'], "channel name", True, url)
    assert chan1 == 1

    join1 = sf.join_channel(guesser['token'], chan1, url)
    assert join1 == {}

    msg1 = "/hangman start fut"
    hang_mess = sf.send_message(creator['token'], chan1, msg1, url)
    assert hang_mess == 1

    msg2 = "/guess a"
    mess2 = sf.send_message(guesser['token'], chan1, msg2, url)
    assert mess2 == 2

    msg3 = "/guess u"
    mess3 = sf.send_message(guesser['token'], chan1, msg3, url)
    assert mess3 == 3

    msg4 = "/guess u"
    mess4 = sf.send_message(guesser['token'], chan1, msg4, url)
    assert mess4['message'] == "<p>Cannot guess already revealed letters</p>"
    assert mess4['code'] == 400

    msg5 = "/guess F"
    mess5 = sf.send_message(guesser['token'], chan1, msg5, url)
    assert mess5 == 5

    # Hangman already started in this channel
    msg6 = "/hangman start dontworkpls"
    mess6 = sf.send_message(guesser['token'], chan1, msg6, url)
    assert mess6['message'] == "<p>A hangman session is already active</p>"
    assert mess6['code'] == 400

    # Create new channel and start hangman there
    chan2 = sf.create_channel(guesser['token'], "hangman time", False, url)
    assert chan2 == 2

    inv1 = sf.invite_channel(guesser['token'], chan2, creator['u_id'], url)
    assert inv1 == {}

    msg7 = msg6
    mess7 = sf.send_message(guesser['token'], chan2, msg7, url)
    assert mess7 == 7

    msg8 = "/guess t"
    mess8 = sf.send_message(guesser['token'], chan1, msg8, url)
    assert mess8 == 8

    msg9 = msg6
    mess9 = sf.send_message(guesser['token'], chan1, msg9, url)
    assert mess9 == 9

def test_mix_normal_sendlater_messages(url):
    user = sf.register_user("Normal", "Sendlater", "message@gmail.com", "fingerscrossed", url)
    assert user['u_id'] == 1

    chan1 = sf.create_channel(user['token'], "hello there sir", True, url)
    assert chan1 == 1

    mess1 = sf.send_message(user['token'], chan1, "now", url)
    assert mess1 == 1

    time1 = sf.time_from_now(10)
    mess2 = sf.send_later(user['token'], chan1, "10", time1, url)
    assert mess2 == 2

    mess3 = sf.send_message(user['token'], chan1, "Now again", url)
    assert mess3 == 3

    time2 = sf.time_from_now(5)
    mess4 = sf.send_later(user['token'], chan1, "5", time2, url)
    assert mess4 == 4

    time3 = sf.time_from_now(15)
    mess5 = sf.send_later(user['token'], chan1, "15", time3, url)
    assert mess5 == 5

# def test_interacting_with_unsent_message(url):
#     user = sf.register_user("Voodoo", "Priest", "magic@magic.com", "spooky", url)
#     assert user['u_id'] == 1