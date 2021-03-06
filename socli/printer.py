"""
Contains all functions used for printing.
Uses colorama for formatting.
"""

import subprocess
import sys
import textwrap
import urllib
import json

import colorama
import requests

from socli import search as search, tui as tui

DEBUG = False

# Bold and underline are not supported by colorama.
_BOLD = '\033[1m'
_UNDERLINE = '\033[4m'

palette = [('answer', 'default', 'default'),
           ('title', 'light green, bold', 'default'),
           ('heading', 'light green, bold', 'default'),
           ('metadata', 'dark green', 'default'),
           ('less-important', 'dark gray', 'default'),
           ('warning', 'yellow', 'default')
           ]

if sys.version < '3.0.0':
    global FileNotFoundError
    FileNotFoundError = IOError

    def urlencode(inp):
        return urllib.quote_plus(inp)

    def display_str(inp):
        return inp.encode('utf-8')

    def inputs(str=""):
        sys.stdout.write(str)
        tempx = raw_input()
        return tempx
else:
    def urlencode(inp):
        return urllib.parse.quote_plus(inp)

    def display_str(inp):
        return inp

    def inputs(string=""):
        sys.stdout.write(string)
        tempx = input()
        return tempx


def format_str(string, color):
    return "{0}{1}{2}".format(color, string, colorama.Style.RESET_ALL)


def print_header(string):
    print(format_str(string, colorama.Fore.MAGENTA))


def print_blue(string):
    print(format_str(string, colorama.Fore.BLUE))


def print_green(string):
    print(format_str(string, colorama.Fore.GREEN))


def print_warning(string):
    print(format_str(string, colorama.Fore.YELLOW))


def print_fail(string):
    print(format_str(string, colorama.Fore.RED))


def print_white(string):
    print(format_str(string, colorama.Fore.WHITE))


def make_header(string):
    return format_str(string, colorama.Fore.MAGENTA)


def make_blue(string):
    return format_str(string, colorama.Fore.BLUE)


def make_green(string):
    return format_str(string, colorama.Fore.GREEN)


def make_warning(string):
    return format_str(string, colorama.Fore.YELLOW)


def make_fail(string):
    return format_str(string, colorama.Fore.RED)


def make_white(string):
    return format_str(string, colorama.Fore.WHITE)


def bold(string):
    return format_str(string, _BOLD)


def underline(string):
    return format_str(string, _UNDERLINE)


# For testing exceptions
def showerror(e):
    if DEBUG:
        import traceback
        print("Error name: " + e.__doc__)
        print()
        print("Description: " + str(e))
        print()
        traceback.print_exc()
    else:
        return


def helpman():
    """
    Displays help
    :return:
    """
    colors = {
        "red":"\033[1;31m",
        "green":"\033[1;32m",
        "yellow":"\033[1;33m",
        "blue":"\033[1;34m",
        "purple":"\033[1;35m",
        "white":"\033[1;37m"
    }
    no_color = "\033[0m"

    credit="\033[1;37mSoCLI\033[1;35m is an open source project hosted on github. Don't forget to star it if you liked it. \
    \nUse GitHub issues to report problems: \033[1;37mhttp://github.com/gautamkrishnar/socli\033[1;35m"

    optional_text = {
        "--help or -h":"Displays this help",
        "--query or -q":"If any of the following commands are used then you must specify search query after the query argument",
        "--interactive or -i":"To search in Stack Overflow and display the matching results. You can chose and \
        browse any of the result interactively",
        "--res or -r":"To select and display a result manually and display its most voted answer.\n\n\033[1;33meg: socli \
        --res 2 --query foo bar: Displays the second search result of the query \'foo bar\'",
        "--tag or -t":"To search a query by tag on Stack Overflow.  Visit http://stackoverflow.com/tags to see the list of \
        all tags.\n\033[1;33meg: socli --tag javascript,node.js --query foo bar: Displays the search result of the query \"foo bar\" in \
        Stack Overflow's javascript and node.js tags.",
        "--new or -n":"Opens the Stack Overflow new questions page in your default browser. You can create a new question using it.",
        "--user or -u":"Displays information about the user provided as the next argument(optional). If no argument \
        is provided it will ask the user to enter a default username. Now the user can run the command without the argument."+"\033[1;33m" + \
        " eg: socli -u: Prompts and saves your username. Now you can just run socli -u to see the stats.\
        socli -u 22656: Displays info about user ID 22656",
        "--del or -d":"Deletes the configuration file generated by socli -u command.",
        "--api or -a":"Sets a custom API key for socli",
        "--sosearch or -s":"SoCLI uses google search by default. Use this option to search Stack Overflow directly.",
        "--open-url or -o":"Opens the given url in socli",
        "--version or -v":"Displays the current version of socli"
    }

    print(no_color, colors["white"])
    print("Stack Overflow command line client:\n\n")
    print("\t" * 2, colors["green"], "Usage: socli [", colors["white"], "Argument(s)", colors["green"], "] <", colors["red"], "Search Query", colors["green"], ">\n\n")
    print(colors["purple"], "\033[4m[ Arguments ] (optional):")
    print(no_color)

    for key in optional_text.keys():
        size = len(key)
        print(colors[flagColor], "  ", key, ":", colors[infoColor], textwrap.fill(textwrap.dedent(optional_text[key]).strip(), subsequent_indent=' '*(size+8)))
        print()
    print(no_color)

    print(colors["purple"], "\033[4m< Search Query >:\n\033[0m")
    print(colors["red"], "   Query to search on Stack Overflow\n\n", textwrap.fill("   If no commands are specified then socli will search Stack Overflow and simply displays the first search result's most voted answer.", subsequent_indent='    '), "\n\n    If a command is specified then it will work according to the command.")

    print(colors["purple"], "\n\n   \033[4mExamples:\n\033[0m")
    print(colors["yellow"], "\t", "socli for loop in python\n\t socli -iq while loop in python")
    print(colors["purple"], "\n" + credit)


def display_results(url, dup_link=None, json_output=False):
    """
    Display result page
    :param url: URL of the search result
    :param dup_link: URL to the duplicate question visited from
    :param json_output: JSON output flag
    :return:
    """
    search.random_headers()
    res_page = requests.get(url, headers=search.header)
    search.captcha_check(res_page.url)
    question_title, question_desc, question_stats, answers, comments, dup_url = \
        search.get_question_stats_and_answer_and_comments(url)
    if json_output:
        sys.stdout.write(urllib.parse.unquote(json.dumps({
            'title': question_title,
            'desc': question_desc,
            'stats': question_stats,
            'answers': answers,
            'comments': comments,
            'dup_url': dup_url,
        })))
    else:
        tui.display_header = tui.Header()
        tui.question_post = tui.QuestionPage((url, question_title, question_desc, question_stats, answers, comments, dup_url, dup_link))
        tui.MAIN_LOOP = tui.EditedMainLoop(tui.question_post, palette)
        tui.MAIN_LOOP.run()
