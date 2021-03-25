import pytest
import message
import channel
import auth
import channels
import other
from error import InputError, AccessError

"""
Errors for hangman:
* Person who started can't guess
* Word must be at least 3 letters (Max of 15)
* Can't start with only one person in channel
* Can only guess one letter
* Can't start hangman if already playing
* Can't guess successful letter again
* Can't stop hangman if not admin
* Word must be made of letters
* Can only guess letters
"""

"""
Hangman stages
1. Floor
2. Stick
3. Across thing + noose
4. head
5. body
6. left hand
7. right hand
8. Left foot
9. Right foot (dead)
"""

def start_hangman(word):
    """
    Registers 2 users, creates a channel and starts a hangman game using the given word

    Parameters:
        word(str): Word to be used in hangman

    Returns:
        Tuple containing information about 2 users and the channel_id
    """
    user1 = auth.auth_register('creator@gmail.com', 'creator', 'Word', 'Man')
    user2 = auth.auth_register('guesser@gmail.com', 'guesser', 'Guess', 'Man')
    chan1_id = channels.channels_create(user1['token'], 'manhang', True)['channel_id']
    channel.channel_join(user2['token'], chan1_id)
    msg = '/hangman start ' + word
    message.message_send(user1['token'], chan1_id, msg)
    return (user1, user2, chan1_id)


def assert_hangman_is_over(user, channel_id):
    """
    Uses asserts to show that there is no currently active hangman session in the channel

    Parameters:
        user(dict): A dictionary containing the user token and u_id
        channel_id(int): An authorisation id used to identify channels

    Returns:
        Raises an InputError if there is a currently active hangman session
        Returns nothing if hangman is not currently active
    """
    # Would not raise an InputError if hangman was still going
    with pytest.raises(InputError):
        assert message.message_send(user['token'], channel_id, '/guess z')
    # Would raise an InputError if hangman was still going
    message.message_send(user['token'], channel_id, '/hangman start frederick')
    message.message_send(user['token'], channel_id, '/hangman stop')

def send_hangman_guesses(user, channel_id, guesses):
    """
    Sends a string of guesses as messages 1 letter at a time

    Parameters:
        user(dict): A dictionary containing the user token and u_id
        channel_id(int): An authorisation id used to identify channels
        guesses(str): A string made up of individual hangman guesses

    Returns:
        Nothing (None)
    """
    for letter in guesses:
        msg = '/guess ' + letter
        message.message_send(user['token'], channel_id, msg)

def send_regular_messages(user, channel_id, messages):
    """
    Sends a list of normal messages one at a time

    Parameters:
        user(dict): A dictionary containing the user token and u_id
        channel_id(int): An authorisation id used to identify channels
        message(list): A list made up of individual messages

    Returns:
        Nothing (None)
    """
    for item in messages:
        message.message_send(user['token'], channel_id, item)
    
# SUCCESSFUL
def test_successful_hangman():
    """
    Tests successful a successful game of hangman
    """
    _user1, user2, chan1_id = start_hangman('banana')
    send_hangman_guesses(user2, chan1_id, 'anb')
    assert_hangman_is_over(user2, chan1_id)
    other.clear()


def test_successful_weird_words_hangman():
    """
    Tests a successful game of hangman (using a non-English word)
    """
    _user1, user2, chan_id = start_hangman('aaaaaaaaaaaa')
    send_hangman_guesses(user2, chan_id, 'a')
    assert_hangman_is_over(user2, chan_id)
    other.clear()

def test_send_normal_message_during_hangman():
    _user1, user2, chan_id = start_hangman('chilling')
    send_hangman_guesses(user2, chan_id, 'drive')
    msgs = ['Lets get this', 'hangman dub']
    send_regular_messages(user2, chan_id, msgs)
    other.clear()

def test_successful_loss_hangman():
    """
    Tests a successful game of hangman (ending in a loss)
    """
    _user1, user2, chan_id = start_hangman('elmo')
    send_hangman_guesses(user2, chan_id, 'nbvcxzasd')
    assert_hangman_is_over(user2, chan_id)
    other.clear()

def test_stop_hangman():
    """
    Tests successful hangman cancellations
    """
    # Stopped by admin
    user1, user2, chan_id = start_hangman('xylophone')
    message.message_send(user1['token'], chan_id, '/hangman stop')
    assert_hangman_is_over(user2, chan_id)

    # Stopped by creator
    message.message_send(user2['token'], chan_id, '/hangman start grouchy')
    message.message_send(user2['token'], chan_id, '/hangman stop')
    assert_hangman_is_over(user1, chan_id)
    other.clear()

def test_changing_status_message():
    user1, _user2, _chan_id = start_hangman('cameraman')
    find_message = other.search(user1['token'], 'hangman')['messages']
    for found_message in find_message:
        message_id = found_message['message_id']
    with pytest.raises(InputError):
        assert message.message_edit(user1['token'], message_id, 'No more hangman')
        assert message.message_remove(user1['token'], message_id)
    other.clear()

# UNSUCCESSFUL
def test_unsuccessful_creator_guessing():
    """
    Tests an unsuccessful game of hangman,
    focusing on the creator guessing their own word
    """
    creator, _guesser, chan_id = start_hangman('hangman')
    with pytest.raises(InputError):
        assert message.message_send(creator['token'], chan_id, '/guess a')
    other.clear()
    

def test_invalid_words():
    """
    Tests unsuccessful games of hangman,
    focusing on invalid starter words
    """
    long_msg = 'a' * 16
    with pytest.raises(InputError):
        assert start_hangman('')
        assert start_hangman('an')
        assert start_hangman(long_msg)
        assert start_hangman('12243')
        assert start_hangman('hello?')
        assert start_hangman('1two3four')
        assert start_hangman('         ')
    other.clear()


def test_invalid_guess():
    """
    Tests an unsuccessful game of hangman,
    focusing on invalid guesses
    """
    _creator, guesser, chan_id = start_hangman('froot loops')
    message.message_send(guesser['token'], chan_id, '/guess f')
    with pytest.raises(InputError):
        assert message.message_send(guesser['token'], chan_id, '/guess froot')
        assert message.message_send(guesser['token'], chan_id, '/guess')
        assert message.message_send(guesser['token'], chan_id, '/guess oo')
        assert message.message_send(guesser['token'], chan_id, '/guess ')
        assert message.message_send(guesser['token'], chan_id, '/guess ?')
    other.clear()

def test_invalid_number_of_people():
    """
    Tests an unsuccessful game of hangman,
    focusing on starting in a channel with only 1 person
    """
    user1 = auth.auth_register('gday@gnight.com', 'morning', 'Bright', 'Early')
    chan1 = channels.channels_create(user1['token'], 'alone', True)['channel_id']
    with pytest.raises(InputError):
        assert message.message_send(user1['token'], chan1, '/hangman start zaphod')
    other.clear()

def test_invalid_hangman_stop():
    """
    Tests unsuccessful uses of '/hangman stop',
    focusing on no currently active hangman session and not correct permissions
    """
    user1 = auth.auth_register('nope@gmail.com', 'nopenope', 'Nope', 'Nope')
    chan1 = channels.channels_create(user1['token'], 'isolation', True)['channel_id']
    with pytest.raises(InputError):
        message.message_send(user1['token'], chan1, '/hangman stop') # No active hangman
        _creator, guesser, channel2 = start_hangman('beeblebrox')
        message.message_send(guesser['token'], channel2, '/hangman stop') # Not creator/admin
    other.clear()


def test_guess_not_during_hangman():
    """
    Tests unsuccessful hangman guesses,
    focusing on no currently active hangman session
    """
    user1 = auth.auth_register('apple@jack.com', 'banana', 'Grape', 'Mango')
    chan1 = channels.channels_create(user1['token'], 'hoowaa', False)['channel_id']
    with pytest.raises(InputError):
        assert message.message_send(user1['token'], chan1, '/guess s')
    other.clear()
    
def test_remove_status_message():
    user1, _user2, _chan = start_hangman('baboon')
    find_message = other.search(user1['token'], 'hangman')['messages']
    for found_message in find_message:
        message_id = found_message['message_id']
    with pytest.raises(InputError):
        assert message.message_remove(user1['token'], message_id)
    other.clear()

def test_edit_status_message():
    user1, _user2, _chan = start_hangman('dogsandcats')
    find_message = other.search(user1['token'], 'hangman')['messages']
    for found_message in find_message:
        message_id = found_message['message_id']
    msg = "Pacman > Hangman"
    with pytest.raises(InputError):
        assert message.message_edit(user1['token'], message_id, msg)
    other.clear()

def test_start_hangman_during_hangman():
    user1, user2, chan = start_hangman('csebbqtomorrow')
    send_hangman_guesses(user2, chan, "HeLlO")
    with pytest.raises(InputError):
        assert message.message_send(user1['token'], chan, "/hangman start johhnny")
        assert message.message_send(user2['token'], chan, "/hangman stop")
    other.clear()

def test_guess_successful_letters_again():
    _user1, user2, chan = start_hangman("plsfixcoverage")
    send_hangman_guesses(user2, chan, "pls")
    with pytest.raises(InputError):
        assert message.message_send(user2['token'], chan, '/guess p')
        assert message.message_send(user2['token'], chan, '/guess l')
        assert message.message_send(user2['token'], chan, '/guess s')
    other.clear()