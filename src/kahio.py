"""
math: Gives access to the remainder function
threading: Gives access to multi threading
datetime: Gives access to the datetime functions
data(data.py): Gives access to global data variable
validation(validation.py): Gives access to the premade validations
"""
import math
import threading
import datetime
import data
import validation

def breakdown_message(message):
    """
    Will break the message it its components and return it as a dictionary

    Parameter:
        message(string): The message that needs to be broken down

    Returns:
        question(string): The question section of the message,
        answer(string): A lowercase version of the answer section,
        time(int): An int version of the input time, it is 15 if
                   there was no time section in the message
    """
    question = ""
    answer = ""
    given_time = ""
    message_stage = 0
    for i in message[6:]:
        #Will split up the Input message based of the number of dashs
        if i == "/":
            message_stage += 1
            # Checks the dash number has not exceeded 3
            validation.check_kahio_message_stage(message_stage)
        elif message_stage == 1:
            # In question stage
            question += i
        elif message_stage == 2:
            #In answer stage
            answer += i
        elif message_stage == 3:
            #In timer stage
            given_time += i
    if given_time == "":
        #If no time is specified it is by default set to 15
        given_time = 15
    else:
        #If a time was specified it is checked to be valid and
        #Converted into an integer
        given_time = validation.check_kahio_time(given_time)
    # Checks if question is valid
    validation.check_kahio_question(question)
    # Checks if answer is valid
    answer = validation.check_kahio_answer(answer)
    # Returns the message broken down it its components
    return {
        "question" : question,
        "answer" : answer,
        "time" : given_time
    }

def start_kahio(u_id, channel_id, message):
    """
    Will start a kahio game on the channel and return the new start message

    Parameter:
        u_id(int): The user starting the KAHIO game
        channel_id(int): The channel the KAHIO game is being started in
        message(string): The message that contains the question, answer and
                         may contain the time to wait

    Returns:
        question(string): The question section of the string which will be
                          be the only part printed
    """
    #Checks the u_id is from a owner of the channel
    validation.check_is_channel_owner(u_id, channel_id)

    #Checks a KAHIO game is not already running
    validation.check_kahio_not_running(channel_id)

    #Breaks down the message into its different sections
    message_sections = breakdown_message(message)

    #Gets current time
    time_start = datetime.datetime.now().replace().timestamp()

    #Enters information about the kahio game into the backend
    data.create_kahio(channel_id, u_id, time_start, message_sections["answer"])

    #Begins multithreading recursion and gives a slight delay so the question is posted
    #first
    timer_class = threading.Timer(0.1, kahio_timer, [u_id, channel_id, message_sections["time"]])
    timer_class.start()

    #Stores the timer_class from the multithreading into the backend so it can be stopped
    data.kahio_update_timer_class(channel_id, timer_class)

    #Returns only the message section to be printed
    return message_sections["question"]

def kahio_timer(*args):
    """
    Sends the standup message from the given u_id

    Parameters:
        args[0] (u_id(int)) : The u_id that standup will be sent from
        args[1] (channel_id(int)) : The channel that the message will be sent to
        args[2] (time_remaining(int)) : The time that kahio has remaining

    Returns:
    """
    #Make a message using the u_id from the user that started the KAHIO game
    new_message_id = data.make_message_id()
    new_message = {}
    new_message["message"] = "The kahoi game has " + str(args[2]) + " seconds remaining"
    new_message["u_id"] = args[0]
    new_message["time_created"] = datetime.datetime.now().replace().timestamp()
    new_message["message_id"] = new_message_id
    new_message["reacts"] = [
        {
            "react_id": 1,
            "u_ids": []
        }
    ]

    if args[2] <= 0:
        #If the timer has finished it will print the end message
        data.end_kahio_game(args[1])
        send_kahio_score(args[1], new_message)
        return

    #Inputs the timing message into the channel messages
    data.add_message(new_message, args[1])

    #Stores how long the multithreading wait will be and the time left
    #after the multithreading ends
    time_remaing = args[2]
    time_interval = 0

    if time_remaing <= 5:
        time_interval = 1
    elif math.remainder(time_remaing, 5) == 0:
        time_interval = 5
    else:
        time_interval = int(math.remainder(time_remaing, 5))

    #Removes how long the timer will wait from the time remaining
    time_remaing -= time_interval

    #Calls this function again after time_interval amount of time
    timer_class = threading.Timer(time_interval, kahio_timer, [args[0], args[1], time_remaing])
    timer_class.start()

    #Stores new timer_class so the timer can still be stopped
    data.kahio_update_timer_class(args[1], timer_class)

def send_kahio_score(channel_id, new_message):
    """
    Sends the end message for the KAHIO game

    Parameters:
        channel_id(int): the channel the game is in
        new_message(message dict): The message dictionary to be sent created
                                   int the timer function

    Returns:
    """
    #Gets the stored answer from the data
    answer = data.return_kahio_answer(channel_id)

    #The firstline of the end print out
    new_message["message"] = "Kahio game has ended.\nThe correct answer was " + answer +"\n"

    #The number of users that correctly guessed the answer
    num_correct_answers = data.return_kahio_num_correct_answers(channel_id)

    if num_correct_answers == 0:
        #If no message was added to the kahio it will not print kahio
        new_message["message"] += "No correct answers"
    else:
        new_message["message"] += str(num_correct_answers) + " correct answers"

    #Adds all stored correct guesses
    new_message["message"] += data.return_kahio_score(channel_id)

    #Puts the message in the channel
    data.add_message(new_message, channel_id)

def kahio_guess(u_id, channel_id, new_message):
    """
    Will check if the message is the correct answer or not If the correct
    message was guessed the user will be appended to the list, otherwise
    the incorrect message will just be treated as a regular guess,
    an error will be raised if the user should already have the answer

    Parameters:
        u_id(int): The u_id of the user guessing
        channel_id(int): The channel_id of channel guess is occuring
        new_message(message dict): The message dict created in the message_send
                                   function
    Returns:
        message_id(int): The message_id of the message added to the channel
    """

    #Checks the user has not already guessed the message
    validation.check_kahio_user_has_answer(channel_id, u_id)

    #Gets the answer
    check_message = validation.check_kahio_answer(new_message["message"])

    #Converts the user input question input into correct answer staging
    answer = data.return_kahio_answer(channel_id)

    #Checks if this guess is correct
    if check_message == answer:
        return kahio_correct_guess(u_id, channel_id, new_message)

    #Displays the guess since it was incorrect
    data.add_message(new_message, channel_id)

    return {
        "message_id": new_message["message_id"],
    }

def kahio_correct_guess(u_id, channel_id, new_message):
    """
    If the correct message was guessed the user will be appended to the list
    an error will be raised if the user should already have the answer

    Parameters:
        u_id(int): The u_id of the user guessing
        channel_id(int): The channel_id of channel guess is occuring
        new_message(message dict): The message dict created in the message_send
                                   function
    Returns:
        message_id(int): The message_id of the message added to the channel
    """

    #Adds the information that this user guessed correctly and gets the message to
    #Display instead of the correct guess
    new_message["message"] = data.correct_kahio_guess(u_id, channel_id, new_message["time_created"])

    #Changes the user the message is being sent from to the user that started the KAHIO game
    new_message["u_id"] = data.return_kahio_starter(channel_id)

    #Adds the message
    data.add_message(new_message, channel_id)

    return {
        "message_id": new_message["message_id"],
    }

def kahio_end(u_id, channel_id):
    """
    Will end the kahio game running on the channel and end the timer

    Paramters:
        u_id(int): The user trying to end the KAHIO game
        channel_id(int): The channel the KAHIO game is running on

    Returns:
        message(string): The message saying the KAHIO game has ended

    """
    #Checks the user is an owner
    validation.check_is_channel_owner(u_id, channel_id)

    #Checks if a KAHIO game is running on this channel
    validation.check_kahio_running(channel_id)

    #Will end the KAHIO game
    data.end_kahio_game(channel_id)

    #Will get the timer class of the multithreading timer to stop it
    timer_class = data.get_kahio_timer_class(channel_id)
    timer_class.cancel()

    return "The KAHIO game has been stopped"
