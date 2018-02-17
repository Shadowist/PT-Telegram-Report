CONFIG_FILE = "PTReport.cfg"

def receive_cfg():
    '''Reads and saves the config file into a dictionary'''
    output_dict = {}

    with open(CONFIG_FILE) as f:
        for line in f.readlines():
            if '#' not in line and line.strip():
                parsed_line = line.replace(' ', '').split('=')
                output_dict[parsed_line[0]] = parsed_line[1]

    return output_dict

def show_commands():
    '''Returns a string with the list of commands'''

    text = "I support the following commands:\n"
    text += "1. /start\n"

    return text
