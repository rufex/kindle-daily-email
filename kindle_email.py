#! usr/local/bin/python3
# -*- coding: utf-8 -*-

import smtplib, codecs, random, logging, pathlib, yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

### __ EMAIL CREDENTIALS __ ###

config = yaml.safe_load(open("config_kindle_mail.yml"))
direccion = config["Config"]["direccion"]
passw = config["Config"]["passw"]
dest = config["Config"]["dest"]

### __ PATHS AND FOLDERS __ ###


root_path = pathlib.Path(config["Paths"]["root_path"]).resolve()   # Path to Main Folder
dirs_generator = root_path.rglob("*.txt")                   # Generator of all txt files in directory and subdirectories 
list_dirs_txt = []

for l in dirs_generator:                                    # Append str of the path of the txt files to list
    list_dirs_txt.append(str(l))

### __ LOGGING CONFIGURATION __ ###

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
f_handler = logging.FileHandler(config["Paths"]["log_file"])
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('[%(asctime)s] | %(levelname)s | Line: %(lineno)d | Function Name: %(funcName)s | %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

### __ FILES CLASSIFICATION __ ###

quotes_files = []
articles_files = [] 
programming_files = []
book_files = []

def highlights_clasificator(list_of_files_path):    # Function to classificate files
    for f in list_of_files_path:  
        if 'Quotes' in str(f):
            quotes_files.append(f)
        elif 'Art' in f and 'culos' in f :          # Artículos. Problem with accent
            articles_files.append(f)
        elif 'Programming' in str(f):
            programming_files.append(f)
        else:
            book_files.append(f)

highlights_clasificator(list_dirs_txt)              # Running function to classificate            

book_selected = random.choice(book_files)           # Random choice of one book
article_selected = random.choice(articles_files)
programming_selected = random.choice(programming_files)
quote_selected = random.choice(quotes_files)

### __ HIGHLIGHTS SELECTION FUNCTION __ ###

def open_clean_select(file_path):               
    file_path = pathlib.Path(file_path) 
    file_name = file_path.name

    try:
        logger.info(f'Opening file: {file_name}')
        with codecs.open(file_path, 'r', 'utf-8') as file:  # Open file
            txt = file.read()
    except Exception as exc:
        logger.error(f'Error while opening file: {exc}')
        pass
    
    txt = txt.replace('\ufeff','')                    # Codification at the begining of the txt file
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

email_message_append(open_clean_select(book_selected))          
email_message_append(open_clean_select(article_selected))
email_message_append(open_clean_select(programming_selected))
email_message_append(open_clean_select(quote_selected))

# Server Connection #
try:
    logger.info('Connecting to email server')
    smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465)        # can be 465 (SSL) or 587
    smtpObj.ehlo()                                           # saying 'hello'to the server
    smtpObj.login(direccion, passw)                          # login to server
    smtpObj.sendmail(direccion, dest, message.as_string())   # sending email
    smtpObj.quit()
    logger.info('Email sent')    
except Exception as exc:
    logger.error(f'Error while connecting: {exc}')
    pass
