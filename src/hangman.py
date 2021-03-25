
"""
Does hangman stuff
"""
import data
import message
import validation
import hangman_draw
import re
from error import InputError, AccessError

"""
guess
    * check valid
    * Successful
        * Edit pinned message (data.edit_message) an
"""
def init():
    """
    Returns an empty hangman dictionary for channels_create
    """
    return {
        'is_active' : False,
        'u_id' : None,
        'word' : None,
        'guesses' : 0,
        'revealed_word' : None,
        'letters' : [],
        'status_message' : None
    }

def print_start(info):
    """
    Prints starting message of hangman
    """
    user = data.get_user_info(info['u_id'])
    return f"""
    {user['name_first']} has started a game of hangman!
    The word is: {''.join(info['revealed_word'])}
    """
    
def update_info(info, u_id, message_id, word):
    """
    Updates the infomation of hangman game
    """
    info['is_active'] = True
    info['word'] = word
    info['status_message'] = message_id
    reveal = re.sub(r'[^ \-\']', '_', word)
    info['revealed_word'] = []
    info['revealed_word'][:] = reveal
    info['u_id'] = u_id
    info['failures'] = 0
    info['guesses'] = 0
    info['letters'] = []

def start(u_id, channel_id, message, message_id):
    """
    Checks if no standups are in progess and initiates hangman
    """
    # Check can start
    validation.check_can_start_hangman(channel_id)

    msg = message['message']
    buffer = len('/hangman start ')
    word = msg[buffer:].lower()
    #word = ''.join(msg.split(' ')[2:]).lower()

    # Check valid word
    validation.check_valid_word(word)

    # Updates hangman info with that word
    info = data.get_hangman_info(channel_id)
    update_info(info, u_id, message_id, word)
    
    # Prints hangman starting message
    message['message'] = print_start(info)
    data.add_message(message, channel_id)

    message_info = data.get_message(channel_id, message_id)
    message_info['is_pinned'] = True
    return {'message_id' : message_id}

def get_guess(message):
    """
    Lowers numbers of guesses
    """
    return message[7].lower()

def check_hangman_won(word, revealed_word):
    """
    Returns True if word is guessed
    """
    return word == ''.join(revealed_word)

def check_hangman_lost(failures):
    """
    Returns true if failed 9 guesses
    """
    return failures == 9

def victory_message(info):
    """
    Returns victory message
    """
    user = data.get_user_info(info['u_id'])
    name = user['name_first']
    plural = 'es'
    if info['guesses'] == 1:
        plural = ''
    return f"""
    =======================================
    ---------------------------YOU WIN---------------------------
    =======================================
    Congratulations! You won {name}\'s hangman in {info['guesses']} guess{plural}!
    The word was {info['word']}.
    {generate_picture(info)}
    """

def loss_message(info):
    """
    Returns loss message
    """
    user = data.get_user_info(info['u_id'])
    name = user['name_first']
    info['failures'] = 9
    return f"""
     =======================================
    --------------------------GAME OVER-----------------------
    =======================================
    Oh well. You lost {name}\'s hangman in {info['guesses']} guesses :(
    The word was "{info['word']}".
    {generate_picture(info)}
    """

def execute_victory(info):
    """
    Ends hangman session and prints victory message
    """
    message_id = info['status_message']
    info['is_active'] = False
    channel_id = data.find_channel(message_id)
    data.edit_message(channel_id, message_id, victory_message(info))
    info['status_message'] = None
    info['letters'] = []

def execute_loss(info):
    """
    Ends hangman session and prints loss message
    """
    info['is_active'] = False
    info['failures'] += 1
    message_id = info['status_message']
    channel_id = data.find_channel(message_id)
    data.edit_message(channel_id, message_id, loss_message(info))
    info['status_message'] = None
    info['letters'] = []

def execute_correct_guess(info, letter):
    """
    Reveals a letter in guessing word
    """
    for i,c in enumerate(info['word']):
        if c == letter:
            info['revealed_word'][i] = letter
        
def generate_picture(info):
    """
    Prints the hangman picture for each different stage 
    """
    return hangman_draw.draw(info['failures'])

def edit_status(info):
    """
    Changes the status message with updated picture and incorrect letters 
    """
    user = data.get_user_info(info['u_id'])
    msg =  f"""
    {user['name_first']} has started a hangman!
    Word: {''.join(info['revealed_word'])}
    Incorrect letters guessed: {', '.join(info['letters'])}
    {generate_picture(info)}
    """
    message_id = info['status_message']
    channel_id = data.find_channel(message_id)
    data.edit_message(channel_id, message_id, msg)


def execute_incorrect_guess(hangman_info, letter):
    """
    Adds letter to list of guessed letters and adds 1 to failed guesses
    """
    if letter not in hangman_info['letters']:
        hangman_info['letters'].append(letter)
    hangman_info['failures'] += 1

    
def print_updated_status(info):
    """
    Prints the updated status message
    """
    if check_hangman_won(info['word'], info['revealed_word']):
        execute_victory(info)
    elif check_hangman_lost(info['failures']):
        execute_loss(info)
    else:
        edit_status(info)

def guess(u_id, channel_id, message):
    """
    Takes in a guess, if correct, execute correct guess, if not, execute incorrect guess
    """
    hang_info = data.get_hangman_info(channel_id)

    # Check to make sure user didn't start hangman session
    validation.check_guesser_not_creator(u_id, channel_id)

    # Check if valid guess
    validation.check_valid_guess(message)

    # Check if guess is correct, incorrect or repeated
    letter = get_guess(message)
    
    if letter in hang_info['revealed_word']:
        raise InputError(description='Cannot guess already revealed letters')
    hang_info['guesses'] += 1
    if letter in hang_info['word']:
        execute_correct_guess(hang_info, letter)
    else:
        execute_incorrect_guess(hang_info, letter)
    print_updated_status(hang_info)

def stop(u_id, channel_id):
    """
    Stops current game of hangman
    """
    info = data.get_hangman_info(channel_id)

    # Check if hangman is currently active
    validation.check_active_hangman(channel_id)

    # Check if user is owner of channel or status message
    validation.check_stop_permission(u_id, channel_id)

    data.remove_message(info['status_message'], channel_id)
    info['is_active'] = False