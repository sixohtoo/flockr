"""
    pytest: Gives access to pytest command (for testing)
    auth(auth.py): Gives access to auth functions
    channel(channel.py): Gives access to channel functions
    channels(channels.py): Gives access to channel_create
    other(other.py): Gives access to other.clear command
    error(error.py): Gives access to error classes
    user(user.py): Gives access to user functions
    data(data.py): Gives access to global data variable
"""
import pytest
import auth
import user
import other
from error import InputError, AccessError
import data
import os
import shutil
from time import sleep
import re
from subprocess import Popen, PIPE
import signal

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

@pytest.fixture
def user1():
    """
    Pytest fixture that automatically registers a user and returns their info
    """
    user1 = auth.auth_register("kevin@gmail.com", "kh12345", "Kevin", "Huang")
    return user1

def check_name_change(user_info, first, last):
    """
    Checks if set_name has successfully changed name

    Parameters:
        user(int): u_id (Identifier for user)
        first: new first name
        last: new last name

    Returns:
        Nothing 
    """

    profile = user.user_profile(user_info["token"], user_info["u_id"])["user"]
    assert profile["name_first"] == first
    assert profile["name_last"] == last

def check_email_change(user_info, new_email):
    """
    Checks if set_email has successfully changed email

    Parameters:
        user(int): u_id (Identifier for user)
        new_email: new email

    Returns:
        NothingS
    """
    profile = user.user_profile(user_info["token"], user_info["u_id"])["user"]
    assert profile["email"] == new_email
            
def check_handle_changed(user_info, new_handle):
    """
    Checks if set_handle has successfully changed handle

    Parameters:
        user(int): u_id (Identifier for user)
        new_handle: new handle

    Returns:
        Nothing
    """
    profile = user.user_profile(user_info["token"], user_info["u_id"])["user"]
    assert profile["handle_str"] == new_handle   
            
#USER_PROFILE TESTS
#Successful
def test_user_profile_request_self(user1):
    """
    Testing successful uses of user_profile
    focusing on request oneselves profile
    """
    user1_profile = {
            "u_id": 1,
            "email": "kevin@gmail.com",
            "name_first": "Kevin",
            "name_last": "Huang",
            "handle_str": "KevinHuang",
            "profile_img_url": ""
            
        }
    assert user.user_profile(user1["token"], user1["u_id"])["user"] == user1_profile
    other.clear()
    
def test_user_profile_request_others(user1):
    """
    Testing successful uses of user_profile 
    focusing on requesting other users profiles
    """

    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    user1_profile = {
            "u_id": 1,
            "email": "kevin@gmail.com",
            "name_first": "Kevin",
            "name_last": "Huang",
            "handle_str": "KevinHuang", 
            "profile_img_url": "" 
        }
    assert user.user_profile(user2["token"], user1["u_id"])["user"] == user1_profile
    other.clear()
    
#Unsuccessful
def test_user_profile_invalid_token(user1):
    """
    Testing unsuccessful uses of user_profile 
    focusing on invalid tokens
    """
    with pytest.raises(AccessError):
        assert user.user_profile("invalid_token", user1["u_id"])
    other.clear()

def test_user_profile_invalid_uid(user1):
    """
    Testing unsuccessful uses of user_profile     
    focusing on invalid u_id
    """
    invalid_uid = 9
    with pytest.raises(InputError):
        assert user.user_profile(user1["token"], invalid_uid)
    other.clear()
    
#USER_PROFILE_SETNAME TESTS
#Successful
def test_user_setname_valid_name(user1):
    """
    Testing successful uses of user_profile_setname
    focusing on valid names
    """
    user.user_profile_setname(user1["token"], "Awesome", "Joey")
    check_name_change(user1, "Awesome", "Joey")
    other.clear()
    
def test_user_setname_lastname_only(user1):
    """
    Testing successful uses of user_profile_setname
    focusing on changing lastname only
    """
    user.user_profile_setname(user1["token"], "Kevin", "Awesome")
    check_name_change(user1, "Kevin", "Awesome")
    other.clear()

def test_user_setname_firstname_only(user1):
    """
    Testing successful uses of user_profile_setname
    focusing on changing firstname only
    """
    user.user_profile_setname(user1["token"], "Awesome", "Huang")
    check_name_change(user1, "Awesome", "Huang")
    other.clear()

def test_user_setname_samename(user1):
    """
    Testing successful uses of user_profile_setname
    focusing on changing to same existing name
    """
    user.user_profile_setname(user1["token"], "Kevin", "Huang")
    check_name_change(user1, "Kevin", "Huang")
    other.clear()
    
#Unsuccessful
def test_user_setname_invalid_token(user1):
    """
    Testing unsuccessful uses of user_profile_setname
    focusing on invalid tokens
    """
    with pytest.raises(AccessError):
        assert user.user_profile_setname("invalid_token", "new", "name")
    other.clear()

def test_user_setname_invalid_firstname(user1):
    """
    Testing unsuccessful uses of user_profile_setname
    focusing on invalid firstnames
    """
    with pytest.raises(InputError):
        assert user.user_profile_setname(user1["token"], "iwbliueblaiublvuaeblriualerugbeiurbgliuebrgiubguiea", "name")

        assert user.user_profile_setname(user1["token"], "", "name")
    other.clear()
    
def test_user_setname_invalid_lastname(user1):
    """
    Testing unsuccessful uses of user_profile_setname
    focusing on invalid lastnames
    """
    with pytest.raises(InputError):
        assert user.user_profile_setname(user1["token"], "new", "niwbliueblaiublvuaeblriualerugbeiurbgliuebrgiubguiea")

        assert user.user_profile_setname(user1["token"], "new", "")
    other.clear()

    
#USER_PROFILE_SETEMAIL TESTS
#Successful
def test_user_setemail_valid_email(user1):
    """
    Testing successful uses of user_profile_setemail
    focusing on valid emails
    """
    user.user_profile_setemail(user1["token"], "newemail@unsw.edu.au")
    check_email_change(user1, "newemail@unsw.edu.au")
    other.clear()
    
#Unsuccessful
def test_user_setemail_invalid_token(user1):
    """
    Testing unsuccessful uses of user_profile_setemail
    focusing on invalid tokens
    """
    with pytest.raises(AccessError):
        assert user.user_profile_setemail("invalid_token", "newemail@unsw.edu.au")
    other.clear()

def test_user_setemail_sameemail(user1):
    """
    Testing unsuccessful uses of user_profile_setemail
    focusing on using same existing email
    """
    with pytest.raises(InputError):
        assert user.user_profile_setemail(user1["token"], "kevin@gmail.com")
    other.clear()

def test_user_setemail_invalid_email(user1):
    """
    Testing unsuccessful uses of user_profile_setemail
    focusing on invalid emails
    """
    with pytest.raises(InputError):
        assert user.user_profile_setemail(user1["token"], "thisisaninvalidemail.com")
        assert user.user_profile_setemail(user1["token"], "invalidemail")
    other.clear()


def test_user_setemail_email_taken(user1):
    """
    Testing unsuccessful uses of user_profile_setemail
    focusing on email already in use
    """
    auth.auth_register("1531grouptask@hotmail.com","amazingstuff", "onefive", "threeone")
    with pytest.raises(InputError):
        assert user.user_profile_setemail(user1["token"], "1531grouptask@hotmail.com")
    other.clear()


#USER_PROFILE_SETHANDLE TESTS
#Successful
def test_user_sethandle_valid_handle(user1):
    """
    Testing successful uses of user_profile_sethandle
    focusing on valid handles
    """
    user.user_profile_sethandle(user1["token"], "newhandle")
    check_handle_changed(user1, "newhandle")
    other.clear()


#Unsuccessful
def test_user_sethandle_invalid_token(user1):
    """
    Testing unsuccessful uses of user_profile_sethandle
    focusing on invalid tokens
    """
    with pytest.raises(AccessError):
        assert user.user_profile_sethandle("invalid_token", "newhandle")
    other.clear()

def test_user_sethandle_samehandle(user1):
    """
    Testing unsuccessful uses of user_profile_sethandle
    focusing on changing to same existing handle
    """
    with pytest.raises(InputError):
        assert user.user_profile_sethandle(user1["token"], "KevinHuang")
    
    other.clear()
    
def test_user_sethandle_invalid_handle(user1):
    """
    Testing unsuccessful uses of user_profile_sethandle
    focusing on invalid handles
    """
    with pytest.raises(InputError):
        assert user.user_profile_sethandle(user1["token"], "abcdefghijklmnopqrstuvwxyz")
        assert user.user_profile_sethandle(user1["token"], "me")    
    other.clear()

def test_user_sethandle_handle_taken(user1): 
    """
    Testing unsuccessful uses of user_profile_sethandle
    focusing on using existing handle
    """
    auth.auth_register("1531grouptask@hotmail.com","amazingstuff", "onefive", "threeone")
    with pytest.raises(InputError):
        assert user.user_profile_sethandle(user1["token"], "onefivethreeone")
    other.clear()

#USER_PROFILE_UPLOADPHOTO TESTS
"""
NOTE: In these tests, "google.com.au" is used as a placeholder for the local_host url
"""
#Successful
def test_user_uploadphoto_success(user1):
    user.user_profile_uploadphoto(user1["token"],"https://i.redd.it/8rq2umri7cm51.jpg",200,200,1800,2000, "google.com.au")
    #check if new directory exists
    assert os.path.isdir("src/static") is True
    assert os.path.isfile("src/static/1.jpg") is True
    
    other.clear()
    shutil.rmtree("src/static")

#UNSUCCESSFUL
def test_user_uploadphoto_invalid_token(user1):
    with pytest.raises(AccessError):
        assert user.user_profile_uploadphoto("invalid_token", "https://i.redd.it/8rq2umri7cm51.jpg", 200, 200, 300, 300, "google.com.au")
    other.clear()

#Code assumes user at least enters a valid url
def test_user_uploadphoto_invalid_http_status(url):
    user1 = auth.auth_register("kevin@gmail.com", "kh12345", "Kevin", "Huang")
    web = url + "/channels/list?token=apple"
    with pytest.raises(InputError):
        assert user.user_profile_uploadphoto(user1["token"], web, 0, 0, 10, 10, "google.com.au")
    other.clear()
    

def test_user_uploadphoto_invalid_dimensions(user1):
    with pytest.raises(InputError):
        assert user.user_profile_uploadphoto(user1["token"], "https://i.redd.it/8rq2umri7cm51.jpg", 1000, 200, 5000, 6000, "google.com.au")
        assert user.user_profile_uploadphoto(user1["token"], "https://i.redd.it/8rq2umri7cm51.jpg", 1000, 200, 100, 100, "google.com.au")

    other.clear()

def test_user_uploadphoto_negative_dimensions(user1):
    with pytest.raises(InputError):
        assert user.user_profile_uploadphoto(user1["token"], "https://i.redd.it/8rq2umri7cm51.jpg", -1, 200, 100, 100, "google.com.au")
        assert user.user_profile_uploadphoto(user1["token"], "https://i.redd.it/8rq2umri7cm51.jpg", 1000, -1, 100, 100, "google.com.au")
    other.clear()

def test_user_uploadphoto_flipped_dimensions(user1):
    with pytest.raises(InputError):
        assert user.user_profile_uploadphoto(user1["token"], "https://i.redd.it/8rq2umri7cm51.jpg", 1000, 200, 100, 500, "google.com.au")
        assert user.user_profile_uploadphoto(user1["token"], "https://i.redd.it/8rq2umri7cm51.jpg", 1000, 200, 1100, 100, "google.com.au")
    other.clear()


def test_user_uploadphoto_not_jpg(user1):
    
    with pytest.raises(InputError):
        assert user.user_profile_uploadphoto(user1["token"], "https://google.com.au", 1000, 200, 5000, 6000, "google.com.au")
    other.clear()
