class bcolors:
    HEADER      = '\033[95m'
    OKBLUE      = '\033[94m'
    OKCYAN      = '\033[96m'
    OKGREEN     = '\033[92m'
    WARNING     = '\033[93m'
    FAIL        = '\033[91m'
    BOLD        = '\033[1m'
    UNDERLINE   = '\033[4m'

    RED         = '\033[31m'
    GREEN       = '\033[32m'
    BLUE        = '\033[34m'
    CYAN        = '\033[36m'
    MAGENTA     = '\033[35m'
    YELLOW      = '\033[33m'
    BLACK       = '\033[30m'
    WHITE       = '\033[37m'

    END         = '\033[0;0m'
    BOLD        = '\033[1m'
    REVERSE     = '\033[2m'

    BG_BLACK    = '\033[40m'
    BG_RED      = '\033[41m'
    BG_GREEN    = '\033[42m'
    BG_YELLOW   = '\033[43m'
    BG_BLUE     = '\033[44m'
    BG_MAGENTA  = '\033[45m'
    BG_CYAN     = '\033[46m'
    BG_WHITE    = '\033[47m'


class bicons:
    GLOBAL  = f'🌎'
    PRIVATE = f'📧'
    SERVER  = f'🤖'
    USER    = f'👤'

bscopes = {
    'GLOBAL':   f'{bcolors.BG_BLUE}{bcolors.WHITE}    {bicons.GLOBAL}  {bcolors.END}{bcolors.BLUE}',
    'PRIVATE':  f'{bcolors.BG_WHITE}{bcolors.WHITE}    {bicons.PRIVATE}  {bcolors.END}{bcolors.WHITE}',
    'SERVER':   f'{bcolors.BG_RED}{bcolors.WHITE}    {bicons.SERVER}  {bcolors.END}{bcolors.RED}',
    'USER':     f'{bcolors.BG_BLUE}{bcolors.WHITE}    {bicons.USER}  {bcolors.END}{bcolors.BLUE}',
}

def build_message_text(scope, author, text):
    return f'{bscopes[scope]} {author}  {bcolors.END}  {text}'

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9879
COMMANDS    = {
    "QUIT":     '/q',
    "PRIVATE":  '/p'
}