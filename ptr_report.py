from itertools import islice
from ptr_utils import reversed_lines, receive_cfg

from datetime import date
from datetime import datetime

LOG_FILE = "ProfitTrailer.log"

def get_log(file, days=1):
    '''Returns logs stretching back to the specified date.'''
    string_export = []
    start_date_grabbed = False
    start_date = None
    end_date = None
    test_date = None

    for line in reversed_lines(file):
        adjusted = line.rstrip('\n')
        if '\tat ' in adjusted or 'java' in adjusted: # Java error
            string_export.append(adjusted)
        else:
            if not start_date_grabbed:
                d_list = list(map(int, adjusted.split(' ')[0].split('-')))
                start_date = date(d_list[0], d_list[1], d_list[2])
                string_export.append(adjusted)
                start_date_grabbed = True
            else:
                d_list = list(map(int, adjusted.split(' ')[0].split('-')))
                test_date = date(d_list[0], d_list[1], d_list[2])
                string_export.append(adjusted)
        
        if start_date and test_date:
            if ((start_date - test_date).days >= days):
                del string_export[-1]
                break
            else:
                end_date = test_date

    summary = summarize_log(string_export, days, end_date, start_date)

    return summary

def summarize_log(log, days, start_date, end_date):
    ''' Provides a simple sumarization of overall logs. '''
    string_export = ""

    normal_heartbeats = 0
    cache_heartbeats = 0
    dca_heartbeats = 0
    config_changes = 0
    enough_vol = 0
    exceed_bal = 0
    apikey_invalid = 0
    java_errors = 0

    for line in log:
        if "Normal Heartbeat" in line:
            normal_heartbeats += 1
        elif "Cache Heartbeat" in line:
            cache_heartbeats += 1
        elif "DCA Heartbeat" in line:
            dca_heartbeats += 1
        elif "There is not enough volume" in line:
            enough_vol += 1
        elif "Detected configuration changes" in line:
            config_changes += 1
        elif "APIKEY_INVALID" in line:
            apikey_invalid += 1
        elif "Buy will exceed min buy balance" in line:
            exceed_bal += 1
        elif "java" in line:
            java_errors += 1

    string_export = "{} Day Report\n".format(days)
    string_export += "Start Date: {}\n".format(start_date)
    string_export += "End Date: {}\n".format(end_date)
    string_export += "====================\n"
    string_export += "{} Normal Heartbeats\n".format(normal_heartbeats)
    string_export += "{} Cache Heartbeats\n".format(cache_heartbeats)
    string_export += "{} DCA Heartbeats\n".format(dca_heartbeats)
    string_export += "{} config changes\n".format(config_changes)
    string_export += "{} not enough volume events\n".format(enough_vol)
    string_export += "{} buy exceed balance events\n".format(exceed_bal)
    string_export += "{} APIKEY_INVALID events\n".format(apikey_invalid)
    string_export += "{} Java events\n".format(java_errors)

    return string_export

def return_lines(file, num, config_dict):
    string_export = []
    for line in islice(reversed_lines(file), num):
        if check_config(config_dict, line):
            string_export.append(line.rstrip('\n'))
    return string_export

def check_config(config_dict, line):
    # Heartbeats
    if config_dict['ignore_cache_heartbeat']:
        if "Cache Heartbeat" in line:
            return False
    if config_dict['ignore_dca_heartbeat']:
        if "DCA Heartbeat" in line:
            return False
    if config_dict['ignore_normal_heartbeat']:
        if "Normal Heartbeat" in line:
            return False

    # Orders
    if config_dict['ignore_buy_orders']:
        if "Buy order" in line:
            return False
    if config_dict['ignore_sell_orders']:
        if "Sell order" in line:
            return False
    if config_dict['ignore_get_orders']:
        if "Get order information" in line:
            return False

    # Util
    if config_dict['ignore_config_changes']:
        if "INFO Util - Detected configuration changes" in line:
            return False

    # Normal Strategy Runner
    if config_dict['ignore_normal_api_problems']:
        if "NormalStrategyRunner - API Problems?" in line:
            return False

    if config_dict['ignore_config_changes']:
        if "INFO NormalStrategyRunner - There is not enough volume to buy" in line:
            return False

    if config_dict['ignore_normal_pairs']:
        if "INFO NormalStrategyRunner - Normal Pair -" in line:
            return False

    # DCA Strategy Runner
    if config_dict['ignore_dca_api_problems']:
        if "DCAStrategyRunner - API Problems?" in line:
            return False

    # API Key
    if config_dict['ignore_apikey_invalid']:
        if "APIKEY_INVALID" in line:
            return False

    # Telegram
    if config_dict['ignore_telegram_errors']:
        if "ERROR TelegramService" in line:
            return False

    # Java
    if config_dict['ignore_java_errors']:
        if "java" in line:
            return False

    return True
        
def return_logs(config_dict, args):
    '''Parses and returns the selected logs.'''
    f = open(LOG_FILE, 'r')
    log = get_log(f, int(args[0]))
    # report = summarize_log(log, int(args[0]))
    f.close()

    return log