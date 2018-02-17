from itertools import islice
from ptr_utils import reversed_lines, receive_cfg

LOG_FILE = "ProfitTrailer.log"

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
        
def return_logs(config_dict):
    '''Parses and returns the selected logs.'''

    f = open(LOG_FILE, 'r')
    lines = return_lines(f, 100, config_dict)

    return "\n".join(lines[::-1])
