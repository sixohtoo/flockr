"""
    pytest: Gives access to pytest command (for testing)
    auth(auth.py): Gives access to register, login and logout functions
    other(other.py): Gives access to other.clear command
    error(error.py): Gives access to error classes
"""
import pytest
import auth
import other
import user
from error import InputError
import jwt
import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import time


def get_code_from_email():
    """
    Used in tests for password_reset_request.
    This function checks that an email was sent to flockr1531@gmail.com.
    Check test_successful_password_reset_request for why it must be this email
    Code inspired by: https://www.thepythoncode.com/article/reading-emails-in-
    python?fbclid=IwAR2Rxe9plOe7TY-LZdzLnLQwJnoNjudF_cEAgOLTtg2mhBomjKat-ngAs14
    """
    code = None
    # Account credentials
    username = "flockr1531@gmail.com"
    password = "YUut6h8V"
    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    imap.login(username, password)
    _status, messages = imap.select("INBOX")

    # total number of emails
    messages = int(messages[0])

    _res, msg = imap.fetch(str(messages), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            # parse a bytes email into a message object
            # Have to disable pylint because it doesn't recognise 'response' as a tuple
            msg = email.message_from_bytes(response[1])#pylint: disable=unsubscriptable-object
            # decode the email subject
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                # if it's a bytes, decode to str
                subject = subject.decode()
            code = subject
            
    imap.close()
    imap.logout()
    if code is None:
        raise InputError(description='Email has no subject')
    return code


# AUTH_LOGIN tests
# Successful
def test_successful_auth_login():
    """
    Tests successful uses of auth_login
    """
    user = auth.auth_register("snow@white.com", "dwarves", "Snow", "White")
    auth.auth_logout(user["token"])
    user1 = auth.auth_login("snow@white.com", "dwarves")

    user = auth.auth_register("George.Humohrey@bigpond.edu.au", "washington", "George", "Humohrey")
    auth.auth_logout(user["token"])
    user2 = auth.auth_login("George.Humohrey@bigpond.edu.au", "washington")

    user = auth.auth_register("Artur.Hawking@bing.edu.au", "manetherin", "Artur", "Hawking")
    auth.auth_logout(user["token"])
    user3 = auth.auth_login("Artur.Hawking@bing.edu.au", "manetherin")

    assert len(user1) == 2
    assert len(user2) == 2
    assert len(user3) == 2
    assert user1["u_id"] != user2["u_id"]
    assert user1["u_id"] != user3["u_id"]
    assert user2["u_id"] != user3["u_id"]
    assert user1["token"] != user2["token"]
    assert user1["token"] != user3["token"]
    assert user2["token"] != user3["token"]
    
    other.clear()

# Unsuccessful

def test_non_existant_email_auth_login():
    """
    Tests unsuccessful uses of auth_login
    with emails that haven"t been registered
    """
    user = auth.auth_register("tom_ellis@duckduckgoose.com", "project", "Tom", "Ellis")
    auth.auth_logout(user["token"])
    with pytest.raises(InputError):
        assert auth.auth_login("fake.email@duckduckgoose.com", "project")

    user = auth.auth_register("DavidWhitecross@gmail.com", "totenham", "Ronen", "Bhaumik")
    auth.auth_logout(user["token"])
    with pytest.raises(InputError):
        assert auth.auth_login("Ronen@gmail.com", "totenham")

    user = auth.auth_register("Gag.Halfrunt@hhgttg.com", "justzisguy", "Gag", "Halfrunt")
    auth.auth_logout(user["token"])
    with pytest.raises(InputError):
        assert auth.auth_login("GagHalfrunt@hhgttg.com", "justzisguy")

    other.clear()

def test_incorrect_password_auth_login():
    """
    Tests unsuccessful uses of auth_login
    with incorrect passwords
    """
    user = auth.auth_register("Jeltz@vogon.com", "hyperspaceplanningcouncil", "Prostetnic", "Jeltz")
    auth.auth_logout(user["token"])
    with pytest.raises(InputError):
        assert auth.auth_login("Jeltz@vogon.com", "regrettably")

    user = auth.auth_register("LewsTherin@dragon.com.au", "ilenya", "Lews", "Therin")
    auth.auth_logout(user["token"])
    with pytest.raises(InputError):
        assert auth.auth_login("LewsTherin@dragon.com.au", "aviendha")

    user = auth.auth_register("Trent_Zimmerman@council.com.nz", "election", "Trent", "Zimmerman")
    auth.auth_logout(user["token"])
    with pytest.raises(InputError):
        assert auth.auth_login("Trent_Zimmerman@council.com.nz", "lotsofmail")

    other.clear()
# Note: Invalid email/password wasn't tested because even if it was "correct",
# auth_register wouldn't have created the account, so it would fail an assert in
# test_non_existant_emaiL_auth_login.


# AUTH_LOGOUT tests
# Successful
def test_successful_auth_logout():
    """
    Tests successful uses of auth_logout
    """
    user1 = auth.auth_register("hayden@unsw.edu.au", "fanofnano?", "Hayden", "UNSW")
    logout = auth.auth_logout(user1["token"])
    assert logout["is_success"]

    user2 = auth.auth_register("fruit@salad.edu.au", "yummyyummy", "Fruit", "Salad")
    logout = auth.auth_logout(user2["token"])
    assert logout["is_success"]

    other.clear()

# Unsuccessful
def test_unsuccessful_auth_logout():
    """
    Tests unsuccessful uses of auth_logout
    """

    user1 = auth.auth_register("fruit@salad.edu.au", "yum.myyu.mmy", "Fruit", "Salad")
    logout = auth.auth_logout(user1["token"])
    logout = auth.auth_logout(user1["token"])
    assert logout["is_success"] is False

    other.clear()

# AUTH_REGISTER tests
# Successful
def test_successful_auth_register():
    """
    Tests successful uses of auth_register
    """
    user1 = auth.auth_register("elliot@gmail.com", "spooky", "Elliot", "Robb")
    user2 = auth.auth_register("apple@gmail.com", "APPLES", "A", "Fruit")
    user3 = auth.auth_register("pear@yahoo.com", "prickly", "Pear", "Vegetable")
    assert len(user1) == 2
    assert len(user2) == 2
    assert len(user3) == 2
    assert user1["u_id"] != user2["u_id"]
    assert user1["u_id"] != user3["u_id"]
    assert user2["u_id"] != user3["u_id"]
    assert user1["token"] != user2["token"]
    assert user1["token"] != user3["token"]
    assert user2["token"] != user3["token"]

    other.clear()

def test_same_names_auth_register():
    """
    Tests successful uses of auth_register
    when using the same first and last name
    """
    user1 = auth.auth_register("ben@gmail.com", "thisisben", "Ben", "Batson")
    user2 = auth.auth_register("ben1@gmail.com", "thisisalsoben", "Ben", "Batson")
    user3 = auth.auth_register("ben2@gmail.com", "thistooisben", "Ben", "Batson")
    user4 = auth.auth_register("ben3@gmail.com", "ThirdBenIsACharm", "Ben", "Batson")
    user5 = auth.auth_register("ben4@gmail.com", "ForAllBenKind", "Ben", "Batson")
    user6 = auth.auth_register("bentennyson@gmail.com", "BenTen", "Ben", "Batson")
    # Chose random comparisons. Otherwise it'd need 48 asserts (which is un-nessecary)
    assert user2["u_id"] != user5["u_id"]
    assert user1["u_id"] != user3["u_id"]
    assert user4["u_id"] != user1["u_id"]
    assert user6["u_id"] != user3["u_id"]
    assert user2["token"] != user5["token"]
    assert user1["token"] != user3["token"]
    assert user4["token"] != user2["token"]
    assert user6["token"] != user3["token"]

    other.clear()

def test_same_passwords_auth_register():
    """
    Tests successful uses of auth_register
    when using the same password
    """
    user1 = auth.auth_register("hacker@gmail.com", "password", "Alfred", "Hural")
    user2 = auth.auth_register("albert@gmail.com", "password", "Albert", "Einsten")
    user3 = auth.auth_register("zaphod@gmail.com", "password", "Zaphod", "Beeblebrox")
    assert user1["u_id"] != user2["u_id"]
    assert user1["u_id"] != user3["u_id"]
    assert user2["u_id"] != user3["u_id"]
    assert user1["token"] != user2["token"]
    assert user1["token"] != user3["token"]
    assert user2["token"] != user3["token"]
    
    other.clear()

# Unsuccessful

def test_invalid_email_auth_register():
    """
    Tests unsuccessful uses of auth_register
    when using an invalid email
    """
    with pytest.raises(InputError):
        assert auth.auth_register("email", "Mark@gmail.com", "Mark", "Klup")

    with pytest.raises(InputError):
        assert auth.auth_register("Fred@gmail", "123456789", "Fred", "Tolmer")

    with pytest.raises(InputError):
        assert auth.auth_register("@gmail.com", "Adams email", "Aaron", "Cravve")

    with pytest.raises(InputError):
        assert auth.auth_register("john@doe.", "Abpruptly", "John", "Doe")

    with pytest.raises(InputError):
        assert auth.auth_register("Nic123Atgmail.com", "ThisIsASpanishName?", "Nicolas", "Santiago")

    with pytest.raises(InputError):
        assert auth.auth_register("Bob@the@builder.com", "Can we do it?", "Bob", "theBuilder")

    other.clear()


def test_existing_email_auth_register():
    """
    Tests successful uses of auth_register
    when using an existing email
    """
    auth.auth_register("alex@gmail.com", "Ahoy there", "Alex", "Hurkins")
    with pytest.raises(InputError):
        assert auth.auth_register("alex@gmail.com", "Thisissosad", "Alex", "Robbie")

    auth.auth_register("james@hotmail.com.au", "GiantPeach", "James", "Manetherin")
    with pytest.raises(InputError):
        assert auth.auth_register("james@hotmail.com", "Jupiter", "James", "Planetarium")
        assert auth.auth_register("james@hotmail.com", "enter password", "James", "Jameson")

    auth.auth_register("captain@gmail.com", "yoghurt", "Hubert", "Love")
    with pytest.raises(InputError):
        assert auth.auth_register("captain@gmail.com", "captain", "Arthur", "Wolban")

    other.clear()

def test_invalid_password_auth_register():
    """
    Tests successful uses of auth_register
    when using an invalid password
    """
    with pytest.raises(InputError):
        assert auth.auth_register("yellow@gmail.com", "", "Yellow", "Submarine")

    with pytest.raises(InputError):
        assert auth.auth_register("arjun602@gmail.com", "12345", "Arjun", "Mukherjee")

    with pytest.raises(InputError):
        assert auth.auth_register("arid@desert.com", "five", "Monroe", "Smith")

    other.clear()


def test_invalid_first_name_auth_register():
    """
    Tests successful uses of auth_register
    when using an invalid first name
    """
    with pytest.raises(InputError):
        assert auth.auth_register(
            "long@name.com",
            "huuuuge",
            "thisisareallylongnameanditjustkeepsgoingandgoingwhenwillitend",
            "Stevens"
        )

    with pytest.raises(InputError):
        assert auth.auth_register("no@name.com", "Hello, World!", "", "Tapher")

    other.clear()


def test_invalid_last_name_auth_register():
    """
    Tests successful uses of auth_register
    when using an invalid last name
    """
    with pytest.raises(InputError):
        assert auth.auth_register(
            "ripley@optus.com",
            "This is the end.",
            "Hugh",
            "Iamsickoftestingthisfunctionsoitsagoodthingitsdone!"
        )
    with pytest.raises(InputError):
        assert auth.auth_register(
            "first@name.com",
            "antihippopotomonstrosesquippedaliophobia",
            "Jay",
            ""
        )

    other.clear()

def test_successful_passwordreset_request():
    """
    Tests successful uses of password_reset_request
    Note: Have to send it to flockr1531@gmail.com because it has the
    less secure apps option enabled and I know the password for it.
    Otherwise, the user (or pytest) would have to enter the password for the email account.
    """
    user1 = auth.auth_register('flockr1531@gmail.com', 'hellothere', 'Brother', 'Arnold')
    auth.auth_logout(user1['token'])
    assert auth.auth_passwordreset_request('flockr1531@gmail.com') == {}
    time.sleep(2)
    code = get_code_from_email()
    assert code is not None
    other.clear()

def test_incorrect_email_unsuccessful_request():
    """
    Tests unsuccessful uses of passwordreset_request,
    focusing on emails that don't have an account registered to them
    """
    user1 = auth.auth_register('baam@baam.com', 'greetings', 'Good', 'Sir')
    user.user_profile_setemail(user1['token'], 'satay@gmail.com')
    auth.auth_logout(user1['token'])
    with pytest.raises(InputError):
        assert auth.auth_passwordreset_request('elliot@balgara.com') == {}
        assert auth.auth_passwordreset_request('baam@baam.com') == {}
    other.clear()

def test_logged_in_unsuccessful_request():
    """
    Tests unsuccessful uses of passwordreset_request,
    focusing on accounts that are logged in
    """
    auth.auth_register('michealangelo@gmail.com', 'letsgooo', 'Fora', 'Walk')
    with pytest.raises(InputError):
        assert auth.auth_passwordreset_request('michealangelo@gmail.com')
    other.clear()


def test_successful_passwordreset_reset():
    user1 = auth.auth_register('flockr1531@gmail.com', 'thistooksolong', 'one', 'hundred')
    auth.auth_logout(user1['token'])
    auth.auth_passwordreset_request('flockr1531@gmail.com')
    time.sleep(2)
    code = get_code_from_email()
    assert auth.auth_passwordreset_reset(code, 'new_password') == {}
    with pytest.raises(InputError):
        assert auth.auth_login('flockr1531@gmail.com', 'thistooksolong')
    user2 = auth.auth_login('flockr1531@gmail.com', 'new_password')
    assert user1['u_id'] == user2['u_id']
    other.clear()

def test_incorrect_code_unsuccessful_reset():
    """
    Tests unsuccessful uses of passwordreset_reset,
    focusing on incorrect codes
    """
    user1 = auth.auth_register('josh@gmail.com', 'grobin?', 'Whedon', 'Gad')
    auth.auth_logout(user1['token'])
    auth.auth_passwordreset_request('josh@gmail.com')
    with pytest.raises(InputError):
        assert auth.auth_passwordreset_reset('invalid_code', 'plsdontwork')
        assert auth.auth_passwordreset_reset('another_invalid_code', 'good night')
    other.clear()

def test_invalid_new_password_unsuccessful_reset():
    """
    Tests unsuccessful uses of passwordreset_reset,
    focusing on invalid new passwords
    """
    user1 = auth.auth_register('flockr1531@gmail.com', 'password', 'first', 'last')
    auth.auth_logout(user1['token'])
    auth.auth_passwordreset_request('flockr1531@gmail.com')
    time.sleep(2)
    code = get_code_from_email()
    with pytest.raises(InputError):
        assert auth.auth_passwordreset_reset(code, '')
        assert auth.auth_passwordreset_reset(code, '12345')
    other.clear()