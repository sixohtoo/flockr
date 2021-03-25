EXTRA STUFF

Hangman
    * /hangman start word
        * Starts a game of hangman using 'word' as the word.
        * 'word' can have spaces, dashes and apostophes (which user's don't need to guess)
        * Hangman status gets pinned
    * /guess letter
        * Allows the user to guess a letter in the current hangman session
        * If letter is correct, all occurences of the letter is revealed
        * If guess is incorrect, hangman drawing updates
        * 9th incorrect guess will end the game
    * /hangman stop
        * Admins or the hangman 'creator' can stop an active hangman session
        * Used primarily to fix pinned messages or when word is not appropriate
    * hangman.py
        * Where most of the code is stored.
        * Contains 3 main functions (start, guess, stop) and other helper functions
    * hangman_draw.py
        * Where the hangman drawing for each stage is stored.
        * Gets called after every hangman guess
    * hangman_test.py
        * Where all the hangman tests are
    * Also edited:
        * message.py (Determine whether message is normal, guess, start or stop)
        * validation.py (Determine whether user can use each command)
        * data.py (Interacts directly with the hangman state in each channel)
    * Possible errors (All taken care of):
        * Creator can't guess their own word
        * Hangman word must be between 3 and 15 letters
        * Can only guess 1 letter at a time
        * Words and guesses must be letters only (No numbers, punctuation, etc)
            * Words can have spaces, dashes and apostrophes
        * Can't start a hangman session when one is already running
        * Can't guess the same successful letter multiple times
        * Can't use '/hangman stop' if not an owner or hangman starter
    * Assumptions (Not tested):
        * Can't start hangman during a standup
        * Can't start a standup during hangman
        * Can't use message_sendlater for hangman related messages

Weather
    * /weather location
        * Returns the weather at that location
        * Tries to guess what location you meant if slightly incorrect
            * eg "/weather sydne" would return the weather of Sydney
    * Errors (taken care of)
        * Very incorrect locations will raise an InputError
            * eg "/weather 602" would raise an InputError

Reacts
    * Added 3 new reacts (heart, star and thumbDown)
    * Learnt (some) npm and very basic NodeJS
    * Made the heart red
    * Made the star yellow
    * Can only react once on each message 
    * Created a new file for each react
        * src/components/Message/MessageReact2
        * src/components/Message/MessageReact3
        * src/components/Message/MessageReact4
    * Edited src/components/Message/index.js (to add each react)

KAHIO
    */KAHIO/ Question / Answer / length(optional)
        *Only the question will be printed
        *The game is over when the given (if no length of time the game runs for 15 
        *seconds) length of time has finished, the function will give
        *periodically posts in chat a timing warning 
        *every 5 seconds until the final 5 seconds when it is every second 
        *When the timer ends a list of users times who got the question right and there places
        *is posted by moderator who started the game.
    *Guess:
        *Once a KAHIO game has started every guess posted is treated as a guess
        *a normalised version of the guess (removes spaces capitalisation) is compared 
        *against the correct answer 
        *If correct then the time since the question was asked and user is stored, 
        *the function then posts from the moderator who started the game's
        *account that the user just answered correctly 
        *If incorrect it is just posted in chat
        *Once a user "knows the answer" so either started the game or guessed correctly
        *They cannot post in the chat until the game has finished
    */KAHIO/END
        *This will end the KAHIO game on the channel if it is running
    *Edited
        *Other.py to add to other clear to stop KAHIO game timer
        *data.py to add functions that store and retrieve KAHIO game data
        *validatation.py to add functions that check input is valid from validation.py
        *message.py to add checks to call the functions of the KAHIO commands
    *Errors checked for
        * Can only start a KAHIO game if user is channel owner
        * Cannot start another KAHIO game during a KAHIO game
        * Must have a question and answer section of the start kahio message
        * Can only guess if user is not user that started KAHIO game or user that already  
        * guessed correctly
        * Can only end KAHIO game if there is a KAHIO game currently running
        * Can only end KAHIO game if user is owner of channel
        * Can only add number to time section of the KAHIO start command
        * Cannot input negative number into time section of KAHIO start command
    * Assumptions (Not tested):
        * Can't start KAHIO game during a standup
        * Can't start a standup during KAHIO game
        * Can't use message_sendlater for KAHIO related messages
        * Can't start a KAHIO game during a hangman game
        * Can't start a hangman game during a KAHIO game
        * Can't edit a message during KAHIO game
     