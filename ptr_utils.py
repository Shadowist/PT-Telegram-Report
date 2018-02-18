CONFIG_FILE = "PTReport.cfg"
LOG_FILE = "ProfitTrailer.log"

def receive_cfg():
    '''Reads and saves the config file into a dictionary'''
    output_dict = {}

    with open(CONFIG_FILE) as f:
        for line in f.readlines():
            if '#' not in line and line.strip():
                parsed_line = line.replace(' ', '').rstrip('\n').split('=')

                if parsed_line[1].title() == "True":
                    parsed_line[1] = True
                elif parsed_line[1].title() == "False":
                    parsed_line[1] = False

                output_dict[parsed_line[0]] = parsed_line[1]

    return output_dict

def show_commands():
    '''Returns a string with the list of commands'''

    text = "The following commands are supported:\n"
    text += "1. /start\n"
    text += "2. /report - Generates logs using the supplied configuration.\n"
    text += "3. /donate\n"
    text += "4. /help\n"
    

    return text

############################################################################
# Reverse File Read
############################################################################
import os

def reversed_lines(file):
    '''Generate the lines of file in reverse order.'''
    part = ''
    for block in reversed_blocks(file):
        for c in reversed(block):
            if c == '\n' and part:
                yield part[::-1]
                part = ''
            part += c
    if part: yield part[::-1]

def reversed_blocks(file, blocksize=4096):
    '''Generate blocks of file's contents in reverse order.'''
    file.seek(0, os.SEEK_END)
    here = file.tell()
    while 0 < here:
        delta = min(blocksize, here)
        here -= delta
        file.seek(here, os.SEEK_SET)
        yield file.read(delta)
