import smtplib, codecs, random, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

### __ EMAIL CREDENTIALS __ ###
direccion = "XXXX"
passw = "XXXX"
dest = "XXXX"

### __ HIGHLIGHTS SELECTION __ ###

folders=['Artículos/El Gato y La Caja','Artículos/Japón','Aviación','Economía - Negocios - Inversiones','Ficción','No Ficción', 'Python - Data']
root_path = '/Users/agustin/Dropbox/Libros/Anotaciones y Subrayados/'

bookshelf= []          # Empty list for all books paths
for folder_name in folders:   # loop to get all books paths and add them to list
    folder_path = root_path+folder_name
    book_list = os.listdir(folder_path)
    for book in book_list:
        book_path = folder_path+"/"+book
        bookshelf.append(book_path)

book_selected = random.choice(bookshelf)  # Random choice of one book

f = codecs.open(book_selected, 'r', 'utf-8')  # Open file

txt = f.read()
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
    final_list = []                    # New list
    for i in range(3):                 # Select 3 continuous highlights based on the Random Index
        iter = random_index+i
        highlight = body_clean[iter]
        final_list.append(highlight)
except ValueError:                     # In case there are less than 3 highlights in the txt file
        final_list = body_clean

f.close() # close txt file

### __ EMAIL GENERATION __ ###

message = MIMEMultipart()                  # Email object creation
message["Subject"]= "Daily highlights"     # Email subject

title_message = """<br>
        <font size='4'><u><b>""" + str(title) + """</b></u></font>
        <br><br><br>"""
html_message = MIMEText(title_message,'html')
message.attach(html_message)               # Title of the book, attached to email body message

for f in final_list:
    line = """<font size='3'><q>""" + str(f) + """</q></font><br><br>"""
    html_message = MIMEText(line,'html')
    message.attach(html_message)           # Higlights, attached to email body message

smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465) # can be 465 (SSL) or 587
smtpObj.ehlo() #saying 'hello'to the server
smtpObj.login(direccion, passw)  # login to server
smtpObj.sendmail(direccion, dest, message.as_string()) # sending email
smtpObj.quit()

## To-Do: Error handling. If folder no longer exists?
## To-Do: Take paths and email credentials outside the code.
