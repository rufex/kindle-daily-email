#### DESCRIPTION

# Script which choose random txt files from directory (books highlights), and take 3 highlights from it. Then, it generates and sends an email with them.
# I use crontab to run periodically (once a day) the script and receive random highlights.

#### CHANGELOG

# v2 --> Added selection of quote of the day.
# v3 --> Added logging to txt, pathlib for input files, section of articles and defined functions.
# v4 --> Removed email credentials from code and imported moved to YAML file
