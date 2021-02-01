#! usr/bin/python3
# -*- coding: utf-8 -*-

import smtplib, codecs, random, logging, pathlib, yaml
from unicodedata import normalize
from collections import defaultdict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

path_file = pathlib.Path(__file__).parent
config_file_path = pathlib.Path.joinpath(path_file,"config_kindle_mail.yml")
categories_names = ('Quotes', 'Programming', 'Artículos' )

### __ EMAIL CREDENTIALS __ ###

config = yaml.safe_load(open(config_file_path))
email_address = config["Config"]["address"]
passw = config["Config"]["passw"]
dest = config["Config"]["dest"]

### __ PATHS AND FOLDERS __ ###

root_path = pathlib.Path(config["Paths"]["root_path"]).resolve()   # Path to Main Folder
dirs_generator = root_path.rglob("*.txt")                          # Generator of all txt files in directory and subdirectories 
list_dirs_txt = [str(l) for l in dirs_generator ]                  # Append str of the path of the txt files to list

### __ LOGGING CONFIGURATION __ ###

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
f_handler = logging.FileHandler(config["Paths"]["log_file"])
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('[%(asctime)s] | %(levelname)s | Line: %(lineno)d | Function Name: %(funcName)s | %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

### __ FILES CLASSIFICATION __ ###

def highlights_clasificator(list_of_files_path):
    """Separate files acording to the Categories defined
    """
    categories_dict = defaultdict(list)
    for f in list_of_files_path:
        used = False
        for cat in categories_names:
            if normalize('NFC',cat) in normalize('NFC',f):
                categories_dict[cat].append(f)
                used = True
                break
        if used != True:
            categories_dict["Books"].append(f)
    return categories_dict

def txt_picker(dict):
    """ Random choice of one book
    """
    picked_list = list()
    for values in dict.values():
        picker = random.choice(values)
        picked_list.append(picker)
    return picked_list      

### __ HIGHLIGHTS SELECTION FUNCTION __ ###

def open_clean_select(file_path):
    """Open file and select random lines
    """               
    file_path = pathlib.Path(file_path) 
    file_name = file_path.name

    try:
        logger.info(f'Opening file: {file_name}')
        with codecs.open(file_path, 'r', 'utf-8') as file:  # Open file
            txt = file.read()
    except Exception as exc:
        logger.error(f'Error while opening file: {exc}')
        pass
    
    txt = txt.replace('\ufeff','')                   # Codification at the begining of the txt file
    txt_splited = txt.split('\n')                    # Split string in new lines

    title = txt_splited[0]     # Book title
    body = txt_splited[1:]     # Book highlights
    body_clean = list()        # New list

    for b in body:             # Loop to remove empty highlights from list
        bb = b.strip()
        bb = bb.replace("*","")
        if bb != "":
            body_clean.append(bb)

    try:
        random_index = random.randrange(len(body_clean)-2)  # Select a Random Index from List of Highlights
        final_list = []                        # New list
        if file_name != 'quotes.txt':          # Not Quotes
            for i in range(3):                 # Select 3 continuous highlights based on the Random Index
                iter = random_index+i
                highlight = body_clean[iter]
                final_list.append(highlight)
        else:                                  # Quotes
            highlight = random.choice(body_clean)
            final_list.append(highlight)
    except ValueError:                     # In case there are less than 3 highlights in the txt file
            final_list = body_clean
    
    if file_name == 'quotes.txt':
        title = 'Quote of the day'

    return title, final_list               # Tuple: (Title, [Highlights,])

### __ EMAIL GENERATION __ ###

message = MIMEMultipart()                  # Email object creation
message["Subject"]= "Daily highlights"     # Email subject

def email_message_append(tuple_var):       # Input should be a tuple: (Title, [Highlights,]) 
    """ Generate email content
    """
    title = tuple_var[0]
    final_list = tuple_var[1]

    title_message = """<br>
            <font size='4'><u><b>""" + str(title) + """</b></u></font>
            <br><br><br>"""
    html_message = MIMEText(title_message,'html')
    message.attach(html_message)               # Title of the book, attached to email body message

    for f in final_list:
        line = """<font size='3'><q>""" + str(f) + """</q></font><br><br>"""
        html_message = MIMEText(line,'html')
        message.attach(html_message)           # Higlights, attached to email body message
    
# Email content creation #

def email_generator(files):
    """Open each file, select the random lines and generate the email content
    """
    for txt in files:
        email_message_append(open_clean_select(txt))          

# Server Connection #

def send_email():
    """Conect to server and send the email
    """
    try:
        logger.info('Connecting to email server')
        smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465)        # can be 465 (SSL) or 587
        smtpObj.ehlo()                                           # saying 'hello'to the server
        smtpObj.login(email_address, passw)                          # login to server
        smtpObj.sendmail(email_address, dest, message.as_string())   # sending email
        smtpObj.quit()
        logger.info('Email sent')    
    except Exception as exc:
        logger.error(f'Error while connecting: {exc}')
        pass

if __name__ == "__main__":
    classified_files = highlights_clasificator(list_dirs_txt) 
    selected_files = txt_picker(classified_files) 
    email_generator(selected_files)
    send_email()