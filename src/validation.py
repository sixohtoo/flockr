"""
This is a file that checks everything 
data(data.py): Gives access to global data variable
re(regex): Gives access to regex for valid_email

"""
from error import InputError, AccessError
import data
import re
import hashlib
import jwt
import requests
import re

def check_valid_token(token):
    """
    Determine whether supplied token is valid

    Parameters:
        token(string): An authorisation hash

    Returns:
        Raises an error if token is invalid
        Returns u_id if token is valid
    """
    try:
        # If parent function was called using http, token is in ASCII.
        # If parent function was called via command line, token is a byte string.
        # I don't understand why.

        if isinstance(token, bytes):
            token = token.decode("ASCII") # pragma: no cover
        payload = jwt.decode(token, data.get_jwt_secret(), algorithms = ["HS256"])# this line is dead

        correct_token = jwt.encode(payload, data.get_jwt_secret(), algorithm = "HS256")
        correct_str = correct_token.decode("ASCII")

        # Secret is used to confirm if user is logged in or not.
        # It also causes the token to change between sessions. 
        user_secret = data.get_user_secret(payload["u_id"])
        token_secret = payload["session_secret"]
        if token == correct_str and user_secret == token_secret:
            return payload["u_id"]
    except:
        raise AccessError(description = "Token is invalid")
    raise AccessError(description = "User is not logged in")

def check_valid_handle(handle_str):
    """
    Determine whether supplied handle is valid (invalid when handle is less than 3 characters or more than 20 characters)

    Parameters:
        handle_str(string): New handle

    Returns:
        Raises an error if handle is invalid
        Returns nothing if valid handle
    """
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError(description = "Handle is invalid")
    return

def check_valid_email(email):
    """
    Determine whether email is valid.

    Parameters:
        email(string): Email in question

    Returns:
        Raises an error if email is invalid (Doesn't match regex or already in use)
        Returns nothing is valid email
    """
    # If email already taken.
    if data.get_user_with({ "email" : email }) is not None:
        raise InputError(description="Email already in use")
    # Must be standard email (may change to custom later).
    # Regex mostly taken from geeksforgeeks site (linked in spec (6.2)).
    regex = r"^[a-z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}(\.\w{2})?$"
    # If email doesn"t match regex, it"s not valid.
    if not re.search(regex, email):
        raise InputError(description = "Email is invalid")
    return

def check_existing_email(email):
    """
    Determine whether email is used with an account.

    Parameters:
        email(string): Email in question

    Returns:
        Raises an error if email already exists
        Returns nothing if email doesn't exist
    """
    if data.get_user_with({ "email" : email }) is not None:
        raise InputError("Email already in use")
    return

def check_logged_out(u_id):
    """
    Determines whether the user is logged out or not

    Parameters:
        u_id(int): Identifier for a user

    Returns:
        Nothing if user is logged out
        InputError if user is logged in
    """
    if data.check_logged_in(u_id):
        raise InputError(description="User is logged in")

def check_valid_reset_code(reset_code):
    """
    Determines who reset code belongs to

    Parameters:
        reset_code(str): A hash used for resetting a user's password

    Returns:
        User dictionary of whoever has the reset_code
        Raises an error if reset_code doesn't belong to a user
    """
    user = data.get_user_with({'reset_code' : reset_code})
    if user:
        return user
    raise InputError(description='Reset code is not valid')

def check_existing_handle(handle_str):
    """
    Determine whether supplied handle already exists

    Parameters:
        handle_str(string): New handle

    Returns:
        Raises an error if handle already exists
        Returns nothing if handle doesn't exist
    """

    if data.get_user_with({ "handle_str" : handle_str }) is not None:
        raise InputError(description = "Handle already in use")
    return

def check_correct_password(email, password):
    """
    Determines whether password matches account created with given email

    Parameters:
        email(string): Email used for account being logged into
        password(string): Password given

    Returns:
        Raises an error if password doesn't match email
        Returns nothing if password and email match
    """
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    original = data.get_user_with({ "email" : email })
    if original is None:
        raise InputError(description = "Email does not exist")
    if original["password"] != password_hash:
        raise InputError(description = "Password is incorrect")

def check_correct_email(email):
    """
    Determine whether email exists when logging in

    Parameters:
        email(string): Email in question

    Returns:
        Raises an error if email doesn't exist
        Returns nothing if email exists
    """
    if data.get_user_with({ "email" : email }) is not None:
        return
    raise InputError(description = "User does not exist")

def check_valid_name(first, last):
    """
    Determines whether first and last name are allowed

    Parameters:
        first(string): User's given first name
        last(string): User's given last name

    Returns:
        Raises an error if invalid first name
        Returns nothing if valid first name
    """
    # If first name is invalid.
    if len(first) < 1 or len(first) > 50:
        raise InputError("First name is invalid")
    # If last name is invalid.
    if len(last) < 1 or len(last) > 50:
        raise InputError("Last name is invalid")
    return

def check_valid_password(password):
    """
    Determines whether password is allowed (invalid when less than 6 characters)

    Parameters:
        password(string): Password given by user

    Returns:
        Raises an error if invalid password
        Returns nothing if valid password
    """
    if len(password) < 6:
        raise InputError(description = "Password is invalid")
    return

def check_user_in_channel(u_id, channel_id):
    """
    Determine whether user is in a particular channel

    Parameters:
        u_id(int): Identifier for user
        channel_id(int): Identifier for channel

    Returns:
        Raises an error if user not in channel
        Returns nothing if user is in channel
    """
    if not data.check_user_in_channel(channel_id, u_id):
        raise AccessError(description = "User is not in channel")

def check_valid_channel_id(channel_id):
    """
    Determines whether given channel_id matches an existing channel

    Parameters:
        channel_id(int): Identifier for a channel

    Returns:
        Raises an error if channel doesn't exist
        Returns nothing if channel exists
    """
    if data.get_channel_info(channel_id) is None:
        raise InputError(description = "Channel does not exist")

def check_valid_u_id(u_id):
    """
    Check if u_id of invitee is valid

    Parameters:
        u_id(int): Identifier for user

    Returns:
        Raises an error if user doesn't exist
        Returns nothing if user exists
    """
    if data.get_user_info(u_id) is None:
        raise InputError(description = "User does not exist")

def check_is_existing_channel_member(u_id, channel_id):
    """
    Check if inviteee is already part of channel

    Parameters:
        u_id(int): Identifier for users
        channel_id(int): Identifier for channels

    Returns:
        Raises an error if user is not part of channel
        Returns nothing if user is part of channel
    """
    if not data.check_user_in_channel(channel_id, u_id):
        raise InputError(description = "User is not part of channel")

def check_is_not_existing_channel_member(u_id, channel_id):
    """
    Check if inviteee is not part of channel yet

    Parameters:
        u_id(int): Identifier for users
        channel_id(int): Identifier for channels

    Returns:
        Returns nothing if user is not part of channel
        Raise an error if user is part of channel
    """
    if data.check_user_in_channel(channel_id, u_id):
        raise InputError(description = "User is already part of channel")

def check_is_channel_owner(user_id, channel_id):
    """
    Determines whether user is an owner of a given channel

    Parameters:
        user_id(int): Identifier for users
        channel_id(int): Identifier for channels

    Returns:
        Raises an error if user is not an owner of channel
        Returns nothing if user is an owner of channel
    """
    if not data.check_channel_owner(channel_id, user_id):
        raise AccessError(description="User is not owner of channel")

def check_isnot_channel_owner(user_id, channel_id):
    """
    Determines whether user is not an owner of a given channel

    Parameters:
        user_id(int): Identifier for users
        channel_id(int): Identifier for channels

    Returns:
        Raises an error if user is an owner of channel
        Returns nothign is user is not an owner of channel
    """
    if data.check_channel_owner(channel_id, user_id):
        raise AccessError(description = "User is owner of channel")

def valid_message(message):
    """
    Raise an input error if the message string is greater then 1000 characters long

    Parameters:
        message(string): The string of the message to be sent
    Returns:
        Raises error if length of message is too long
        Otherwise nothing
    """
    if len(message) > 1000:
        raise InputError(description = "Invalid message")

def valid_message_id(message_id):
    """
    Check that message_id given has a message it refers to in the global variable 

    Parameters:
        message_id(int): The message_id of the channel being checked
    Returns:
    """
    if int(message_id) > data.get_message_num():
        raise InputError(description="Invalid message_id")

def check_message_exists(message_id):
    """
    Checks if message from a channel exists
    
    Parameters:
        message_id(int): The message_id of the channel being checked
    Returns:
        Raises error if message does not exist
        Otherwise return nothing
    """
    chan = data.get_channel_from_message(message_id)
    if chan == None:
        raise InputError(description="Message does not exist")
    return chan

def check_not_pinned(message_id):
    """
    Checks if message is not already pinned
    
    Parameters:
        message_id(int): The message_id of the channel being checked
    Returns: Nothing
    """
    chan = data.get_channel_from_message(message_id)
    message = data.get_message(chan, message_id)
    if message['is_pinned']:
        raise InputError(description="Message is already pinned")

def check_is_pinned(message_id):
    """
    Checks if message is already pinned
    
    Parameters:
        message_id(int): The message_id of the channel being checked
    Returns: Nothing
    """
    chan = data.get_channel_from_message(message_id)
    message = data.get_message(chan, message_id)
    if not message['is_pinned']:
        raise InputError(description="Message is not currently pinned")

def check_channel_is_public(channel_id):
    """
    Check if channel is public or private

    Parameters:
        channel_id(int): The id of channel
    Returns:
    """
    channel = data.get_channel_info(channel_id)
    if channel["is_public"]:
        return
    else:
        raise AccessError(description = "Cannot join private channel")

def check_valid_url(url):
    """
    Check if url given returns a http status of 200

    Parameters:
        url(str): Url to online page
    Returns:
    """
    request = requests.get(url)
    if request.status_code != 200:
        raise InputError(description = "Invalid url")

def check_jpg_in_url(url):
    """
    Check if given url refers to a .jpg file

    Parameters:
        url(str): Url to online page

    Returns:
    """
    request = requests.get(url)
    if request.headers['content-type'] != "image/jpeg":
        raise InputError(description = "Url not a jpg")


def check_dimensions(image,x_start, y_start, x_end, y_end):
    width, height = image.size
    if x_start < 0 or x_end < 0 or y_start< 0 or y_end < 0:
        raise InputError(description = "Invalid dimensions")
    if x_start > x_end or y_start > y_end:
        raise InputError(description = "Invalid dimensions")
    if x_start > width or x_end > width or y_start > height or y_end > height:
        raise InputError(description = "Invalid dimensions")

def check_standup_running(channel_id):
    """
    Checks if there is a standup running in the given channel

    Parameters:
        channel_id(int): The id of channel
    Returns:
        Raises error if the channel doesn't have a standup running
        If it is running it returns nothing
    """
    if not data.check_standup_running(channel_id):
        raise InputError(description="There is no standup running on this channel")

def check_standup_not_running(channel_id):
    """
    Checks if there is a standup running in the given channel

    Parameters:
        channel_id(int): The id of channel
    Returns:
        Raises error if the channel does have a standup running
        If it is not running it returns nothing
    """
    if data.check_standup_running(channel_id):
        raise InputError(description="There is a standup running on this channel")

def check_length_valid(length):
    """
    Checks if the length is valid

    Parameters:
        length(int): The length of a standup
    Returns:
        Raises error if the length is invalid
        If it is valid it returns nothing
    """
    if length <= 0:
        raise InputError(description="The length is invalid")


def check_can_start_hangman(channel_id):
    """
    Checks if its ok to start hangman session

    Parameters:
        channel_id(int): The id of channel
    Returns:
        Raises error if not enough members
        If it is valid it returns nothing
    """
    channel = data.get_channel_info(channel_id)
    if len(channel['members']) < 2:
        raise InputError(description="Not enough people to start hangman")

def check_not_status_message(message_id):
    """
    Checks to make sure that the targeted message isn't the pinned 
    hangman message with the game state
    Parameters:
        message_id(int): unique identifier of message
    returns:
        error if status message is pinned message
        otherwise nothing
    """
    channel_id = data.get_channel_from_message(message_id)
    # Message does not exist
    if channel_id is None:
        return None
    hang_info = data.get_hangman_info(channel_id)
    if hang_info['status_message'] == message_id:
        raise InputError(description="Can't edit/delete hangman status message")

def check_valid_word(word):
    """
    Checks if hangman word is valid
    """
    new_word = re.sub(r'[ \-\']', '', word)
    if not new_word.isalpha() or len(new_word) < 3:
        raise InputError(description="Word is invalid") 

def check_active_hangman(channel_id):
    """
    Checks if a hangman session is active
    """
    channel = data.get_channel_info(channel_id)
    if not channel['hangman']['is_active']:
        raise InputError(description="There is no currently active hangman session")

def check_if_hangman(channel_id, message):
    """
    Checks if channel is in 'hangman' mode
    and if message is a guess

    Parameters:
        channel_id(int): The id of channel

    Returns:
        True if guess is valid
        False if message does not start with /guess
        InputError if message is a guess, but hangamn is not active
    """
    hang_info = data.get_hangman_info(channel_id)
    if not hang_info['is_active'] and message.startswith('/guess '):
        raise InputError(description="Hangman is not active")
    return message.startswith('/guess ')

def check_start_hangman(channel_id, message):
    """
    Checks whether message will/should start a hangman session

    Parameters:
        channel_id(int): The id of channel
        message(str): Contents of the message about to be sent

    Returns:
        True if hangman is not active and message will start it
        False if message is not '/hangman start'
        Raise InputError if message will start hangman, but hangman is already active
    """
    if message.startswith('/hangman start'):
        hangman_info = data.get_hangman_info(channel_id)
        if hangman_info['is_active']:
            raise InputError(description='A hangman session is already active')
        return True
    return False

def check_if_stop_message(message):
    """
    Checks if message is intended to stop active hangman session

    Parameters:
        message(str): Contents of the message about to be sent

    Returns:
        True if message == '/hangman start'
        Else False
    """
    return message == '/hangman stop'

def check_stop_permission(u_id, channel_id):
    """
    Checks if user has permission to use '/hangman stop'

    Parameters:
        u_id(int): Identifier used for users
        channel_id(int): Identifier used for channels

    Returns:
        Nothing if user has permission
        Raises InputError if user does not have permission
    """
    channel = data.get_channel_info(channel_id)
    hang_info = data.get_hangman_info(channel_id)
    if u_id not in channel['owners'] and hang_info['u_id'] != u_id: # pragma: no cover
        raise InputError(description="User does not have permission to use command")

def check_guesser_not_creator(u_id, channel_id):
    """
    Checks whether a user is guessing their own word

    Parameters:
        u_id(int) : An identifier for users
        channel_id(int): An identifier for channels
        
    Returns:
        InputError if the guesser also started the hangman session
        Nothing if the guesser and starter are different users
    """
    status_message = data.get_hangman_status_message(channel_id)
    if status_message['u_id'] == u_id:
        raise InputError(description='Users can not guess their own word')

def check_valid_guess(message):
    """
    Checks that the message is '/guess ' and then a letter
    """
    if len(message) != 8 or not message[7].isalpha():
        raise InputError(description='Guess is not valid')

def check_valid_react(react_id):
    """
    Determines if react_id is valid

    Parameters:
        react_id(int)

    Returns:
        Nothing if valid react
        InputError react not found
    """
    if data.check_valid_react(react_id) is False:
        raise InputError(description="invalid react_id")

def check_is_reacted_already(channel_id, message_id, react_id, u_id):
    """
    Checks if user has already reacted to message

    Parameters:
        channel_id(int): id of channel
        message_id(int):id of message
        react_id(int): id of react
        u_id(int): id of user
    Returns:
        Raises error if user has already reacted to message
        If it is valid it returns nothing
    """
    if data.check_user_already_reacted(channel_id, message_id, react_id, u_id) is True:
        raise InputError(description='User has already reacted to this message')

def check_has_not_reacted(channel_id, message_id, react_id, u_id):
    """
    Checks if user has not yet reacted to message

    Parameters:
        channel_id(int): id of channel
        message_id(int):id of message
        react_id(int): id of react
        u_id(int): id of user
    Returns:
        Raises error if message has not been reacted to by user
        If it is valid it returns nothing
    """
    if data.check_user_already_reacted(channel_id, message_id, react_id, u_id) is False:
        raise InputError(description='User has already reacted to this message')



def check_weather_call(message):
    """
    checks whether the user is calling for the weather
    """
    return message.startswith("/weather ")

def check_kahio_message_stage(message_stage):
    """

    """
    if (message_stage > 3):
        raise InputError(description="Invalid kahio start message")

def check_kahio_time(time):
    """
    Check if valid time has been inputed
    """
    if time[0] == " ":
        time = time[1:]
    if not time.isdigit():
        raise InputError(description="Time given is invalid")
    time = int(time)
    return time

def check_kahio_question(question):
    """
    Checks if valid question has been inputed
    """
    if question == "":
        raise InputError(description="Question given is invalid")

def check_kahio_answer(answer):
    """
    Check if answer is correct
    """
    if answer == "":
        raise InputError(description="Answer given is invalid")
    if answer[0] == " ":
        answer = answer[1:]
    if answer[-1] == " ":
        answer = answer[:-1]
    return answer.lower()

def check_kahio_not_running(channel_id):
    """
    Checks if there is a kahio running in the given channel

    Parameters:
        channel_id(int): The id of channel
    Returns:
        Raises error if the channel doesn't have a kahio running
        If it is running it returns nothing
    """
    if data.check_kahio_running(channel_id):
        raise InputError(description="There is already a kahio running on this channel")

def check_kahio_running(channel_id):
    """
    Checks if there is a kahio running in the given channel

    Parameters:
        channel_id(int): The id of channel
    Returns:
        Raises error if the channel  has a kahio  game running
        If it is running it returns nothing
    """
    if not data.check_kahio_running(channel_id):
        raise InputError(description="There isn't a kahio running on this channel")

def check_kahio_user_has_answer(channel_id, u_id):
    """
    Checks if the user has the answer of the kahio game running in the given channel

    Parameters:
        channel_id(int): The id of channel
        u_id(int): The id of the user guessing
    Returns:
        Raises error if the user has already got the correct
        answer from the kahio game
    """
    if data.user_already_got_answer(channel_id, u_id):
        raise InputError(description="The user already has the answer")
