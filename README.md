## Daily Highlights mail

> Email generator for highlights made with a Kindle device. The highlights were previously classified and stored in separate TXT files using another script.

# Description

Script which choose random TXT files from directory (books highlights) and take up to 3 lines of text from each of them. Then, it generates and sends an email with them.
It should be possible to adapt it to select diferent text files from your drive and generated random emails, not only for Kindle higlights, as it was originally intended for.
I use crontab to run periodically (once a day) the script and receive random highlights.

# YAML file

Name:config_kindle_mail.yml

Structure:

```
Config:
  direccion: {email account}
  passw: {password}
  dest: {email account receiver}

Paths:
  root_path: {directory where files are stored}
  log_file: {path to log file}
```

# CHANGELOG

v2 --> Added selection of quote of the day.
v3 --> Added logging to txt, pathlib for input files, section of articles and defined functions.
v4 --> Removed email credentials from code and moved to a YAML file
