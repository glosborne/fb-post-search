"""
fbsearchposts v.01a
by GL Osborne
Last updated: 3/18/2020

Python command line program. Takes specific posts out of Facebook download file for a user's posts
and outputs them to a text file.
See README for instructions.
"""

# import external libraries
import jsonschema

# import standard libraries
import json
import argparse
import time
import os
import re
from pathlib import Path
from functools import partial

# import project files
from fbschema import fbschema

# -----------------------------------------  FUNCTIONS  ----------------------------------------

def strip_emoji(text):
    # from https://gist.github.com/Alex-Just/e86110836f3f93fe7932290526529cd1
    EMOJI_PATTERN = re.compile(
        "["
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"
        "]+")
    return EMOJI_PATTERN.sub(r'', text)


def getjson(filename):

    # Gets the JSON file, fixes it, and validates it

    if filename:

        # fix problem with Facebook json (changes "title" key to "status"
        # because of 'jsonschema', the JSON validation module) and
        # changes encoding

        fix_mojibake_escapes = partial(
            re.compile(rb'\\u00([\da-f]{2})').sub,
            lambda m: bytes.fromhex(m.group(1).decode()))

        with open(filename, 'rb') as binary_data:
            repaired = fix_mojibake_escapes(binary_data.read())
            originalfile = repaired.decode('utf8')
            originalfile = originalfile.replace('\"title\":', '\"status\":')
            originalfile = strip_emoji((originalfile))
            binary_data.close()

        # write corrected data to temp file
        with open('tempfile.json', 'w', encoding='utf-8') as fout:
            fout.write(originalfile)
            fout.close()

        # read in the corrected file and validate it
        with open('tempfile.json', 'r', encoding='utf-8') as tempfile:
            contents = json.load(tempfile)

            try:
                jsonschema.validate(instance=contents, schema=fbschema)
                printfile(contents)
            except jsonschema.exceptions.ValidationError:
                print('JSON file is incorrectly formatted.')
            except:
                print('JSON read error.')


def printfile(contents):

    # Searches JSON for posts and prints results to text file

    searchterm = input('Please enter your search term and press Enter: ')

    if searchterm:

        textfilename = 'search_results.txt'

        i = 0

        with open(textfilename, 'w') as f:

            for entry in contents:
                try:
                    entry['attachments']
                except:
                    try:
                        # make sure the entry is a post to user's own timeline
                        if str('timeline.') not in entry['status']:
                            e = entry['data'][0]['post']
                            e = str(e)
                            e_upper = e.upper()

                            # look for search term and print
                            if (e != '') and (searchterm.upper() in e_upper):
                                # convert timestamp
                                t = time.ctime(entry['timestamp'])
                                # write file
                                f.write(t + '\n\n')
                                f.write(e + '\n\n----------\n\n')
                                i = i + 1
                    except:
                        continue

        # Clean up files and return "finished" notices
        if i > 0:
            print('Search term found. Your file is ready.')
        else:
            os.remove(txtfilename)
            print('Search term not found.')

    elif searchterm == '':
        print('You did not enter a search term.')

    else:
        print('There was a problem. Please try again.')


# -----------------------------------------  MAIN  ---------------------------------------------


# Read in arguments

parser = argparse.ArgumentParser(prog='fbposts', usage='%(prog)s \"filename\"', description='Send Facebook posts to text file.')
parser.add_argument('jsonfile', help='Type your path/filename in single or double quotes.')
args = parser.parse_args()
jsonfile = str(args.jsonfile)
if not jsonfile: parser.print_help()

# Get filename

filename = Path(jsonfile)
if filename.exists():
    getjson(jsonfile)
else:
    print('The entered file does not exist.')

# Clean up temp file
os.remove('tempfile.json')
