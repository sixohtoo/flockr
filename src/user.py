"""
data(data.py): Gives access to global data variable
error(error.py): Gives access to error classes
auth(auth.py): Gives access to check valid names and emails
channel(channel.py): Gives access to valid_u_id function
re(regex): Gives access to regex for valid_email
"""
import data
import validation
from PIL import Image
import urllib.request
import os.path
from flask import request


def user_profile(token, u_id):
    """
    Check whether user is valid and for a valid user, returns information 
    about their user_id, email, first name, last name, and handle
    
    Parameters:
        token(string): An authorisation hash
        u_id(int): Identifier for user
        
    Returns:
        Dictionary with information about user
    """
    #Check for valid token
    validation.check_valid_token(token)
           
    #Check for valid u_id
    validation.check_valid_u_id(u_id) 
        
    #Everything valid, proceed with getting profile details

    user = data.get_user_info(u_id)
    profile = {
        "u_id" : user["u_id"],
        "email" : user["email"],
        "name_first" : user["name_first"],
        "name_last" : user["name_last"],
        "handle_str" : user["handle_str"],
        "profile_img_url" : user["profile_img_url"]
    }
    return {"user" : profile}
 

    
def user_profile_setname(token, name_first, name_last):
    """
    Check whether use is valid and for a valid user, update their name
    
    Parameters:
        token(string): An authorisation hash
        name_first(string): new first name
        name_last(stirng): new last name
        
    Returns:
        Nothing
    """
    #Check for valid token
    u_id = validation.check_valid_token(token)
        
    #Check for valid name
    validation.check_valid_name(name_first, name_last)
           
    #Everything valid, proceed with changing name
    user = data.get_user_info(u_id)
    data.update_user(user, {"name_first": name_first,"name_last":name_last})  
    return {}
        
def user_profile_setemail(token, email):
    """
    Check whether use is valid and for a valid user, update their handle
    
    Parameters:
        token(string): An authorisation hash
        email(string): New email
        
    Returns:
        Nothing
    """
    #Check for valid token
    u_id = validation.check_valid_token(token)
        
    #Check for valid email
    validation.check_valid_email(email.lower())
        
    #Everything valid, proceed with changing email
        
    user = data.get_user_info(u_id) 
    data.update_user(user, {"email": email.lower()})
    return {}
  
def user_profile_sethandle(token, handle_str):
    """
    Check whether use is valid and for a valid user, update their handle
    
    Parameters:
        token(string): An authorisation hash
        handle_str(string): New Handle
        
    Returns:
        Nothing
    """
    #Check for valid token
    u_id = validation.check_valid_token(token)
        
    #Check for valid handle    
    validation.check_valid_handle(handle_str)
           
    
    #Check for existing handle 
    validation.check_existing_handle(handle_str)
        
    #Everything valid, proceed with changing handle
    user = data.get_user_info(u_id) 
    data.update_user(user, {"handle_str": handle_str})
    return {}

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, host_url):
    """
    Given a valid user, image url and dimensions, crops the image and stores i as a profile picture
    
    Parameters:
        token(string): An authorisation hash
        image_url(string): url of image
        x_start, x_end, y_start, y_end (int): dimensions to crop
        
    Returns:
        Nothing
    """
    #Check for valid token
    u_id = validation.check_valid_token(token)

    #Check for valid url
    validation.check_valid_url(img_url)

    #Check if url is jpg
    validation.check_jpg_in_url(img_url)

    #Create profile_pic directory if it doesn't exist
    path = "src/static"
    if os.path.isdir(path) == False:
        os.mkdir(path)
    #Get image
    urllib.request.urlretrieve(img_url, f"src/static/{u_id}.jpg")

    #Check if dimensions are valid
    profile_pic = Image.open(f"src/static/{u_id}.jpg")
    validation.check_dimensions(profile_pic, x_start, y_start, x_end, y_end)

    #Everything valid, proceed with cropping and saving image
    cropped = profile_pic.crop((x_start, y_start, x_end, y_end))
    cropped.save(f"src/static/{u_id}.jpg")

    data.update_user_img(host_url,token)
    
    return {}