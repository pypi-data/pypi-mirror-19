#!/usr/bin/python
"""itpe_generator.py - this script is used to generate the HTML for the ITPE
Master Post on Dreamwidth.

ITPE is the Informal Twitter Podfic Exchange. See the 2013 Master Post for more
details and an example of what the script is used for:
http://amplificathon.dreamwidth.org/2452363.html
"""

from collections import namedtuple
import csv
import os
import re
import sys

try:
    from jinja2 import Template, Environment, FileSystemLoader
except ImportError:
    print("You need the jinja2 and MarkupSafe modules installed to run this "
          "script.  Exiting.")
    sys.exit(1)

#------------------------------------------------------------------------------
# We need this to handle special characters in the CSV
#------------------------------------------------------------------------------
reload(sys)
sys.setdefaultencoding('utf-8')

#------------------------------------------------------------------------------
# Module constants
#------------------------------------------------------------------------------
# Name of the file that will be read and the file that will be created. These
# should be saved in the same path as the script
# INPUT_FILE = 'itpe_treats.csv'
# OUTPUT_FILE = 'itpe_treats.html'

# Headings for the CSV fields. These don't have to exactly match the spelling/
# spacing of the CSV, but the order should be the same. We define a set of
# heading names here so that we have consistent names to use in the script
HEADINGS = [
    'from_user',
    'for_user',
    'cover_art',
    'cover_artist',
    'editor',
    'title',
    'title_link',
    'authors',
    'fandom',
    'pairing',
    'warnings',
    'length',
    'mp3_link',
    'podbook_link',
    # 'ao3_link',
    'podbook_compiler'
]

Podfic = namedtuple('Podfic', HEADINGS)

#------------------------------------------------------------------------------
# Filters for Jinja2
#------------------------------------------------------------------------------

def condense_into_line(text):
    """Given a block of HTML split over multiple lines, this function reduces
    it to a single line of rendered text.
    """
    # Split the text into lines and remove any leading whitespace
    lines = [line.lstrip() for line in text.split('\n')]
    return ''.join(lines)

#------------------------------------------------------------------------------
# Logging-style functions
#------------------------------------------------------------------------------

class colors:
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def warning(warning_str):
    """Currently this just prints an ordinary string. I considered giving it a
    color, but couldn't find a color which worked in my console.
    """
    print("  " + warning_str)

def error(error_str):
    """Print a string in WARNING red and exit the script."""
    print("  " + colors.FAIL + error_str + colors.ENDC)
    print("  Script exiting.")
    sys.exit(1)

#------------------------------------------------------------------------------
# If you link to another user on Dreamwidth, you can use a <user> tag, and
# they'll annotate the link with a small icon to show that it's a Dreamwidth
# account. You can also specify a site attribute with a variety of services,
# and they'll likewise annotate the link. See Dreamwidth FAQs for more info:
#
# http://www.dreamwidth.org/support/faqbrowse?faqid=87
#
# Our templates use a compact syntax, prefixing a username with an abbreviation
# and a slash, e.g. "tw/alexwlchan". The dict below gives the list of known
# abbreviations, and the dreamwidth_user_link() function renders a user link.
#------------------------------------------------------------------------------
SITE_PREFIXES = {
    'ao3':  'archiveofourown.org',
    'blog': 'blogspot.com',
    'dj':   'deadjournal.com',
    'del':  'delicious.com',
    'dev':  'deviantart.com',
    'dw':   'dreamwidth.org',
    'da':   'da',
    'etsy': 'etsy.com',
    'ff':   'fanfiction.net',
    'ink':  'inksome.com',
    'ij':   'insanejournal.com',
    'jf':   'journalfen.com',
    'last': 'last.fm',
    'lj':   'livejournal.com',
    'pin':  'pinboard.in',
    'pk':   'plurk.com',
    'rvl':  'ravelry.com',
    'tw':   'twitter.com',
    'tum':  'tumblr.com',
    'wp':   'wordpress.com'
}

userlink_bare = Template("<user name={{name}}>")
userlink_site = Template("<user name={{name}} site={{site}}>")

SPECIAL_CASE_NAMES = [
    '(various)',
    'anonymous'
]

def dreamwidth_user_link(user_str):
    """Renders a short username string into an HTML <user> link."""
    # If there's a space in the user string, then just drop through a raw
    # string (e.g. "the podfic community")
    print(user_str)
    if (" " in user_str) or (user_str.lower() in SPECIAL_CASE_NAMES):
        return user_str

    # If there aren't any slashes, then treat it as a Dreamwidth user
    if "/" not in user_str:
        warning("No site specified for user %s, so defaulting to a Dreamwidth "
                "link." % user_str)
        return userlink_bare.render(name=user_str)

    # If there's one slash, split the string and try to work out what the site
    # is
    elif user_str.count("/") == 1:
        short_site, name = user_str.split("/")

        # Try to look it up, but default to Dreamwidth if it isn't found
        try:
            site = SITE_PREFIXES[short_site]
        except KeyError:
            warning("Unrecognised site prefix for user %s, so default to "
                    "Dreamwidth." % user_str)
            site = "dreamwidth.org"

        # If it is a Dreamwidth user, then we don't need to specify the 'site'
        # attribute, so don't include it
        if site == "dreamwidth.org":
            return userlink_bare.render(name=name)
        else:
            return userlink_site.render(name=name, site=site)

def split_username_links(name_str):
    """Takes a comma-separated string of names, and returns a comma-separated
    string of <user> links.
    """
    usernames = [name.strip() for name in name_str.split(',')]
    userlinks = [dreamwidth_user_link(name) for name in usernames]
    return ', '.join(userlinks)

#------------------------------------------------------------------------------
# Mainline program function
#------------------------------------------------------------------------------
def main():

    #--------------------------------------------------------------------------
    # Set up command line flags and options.
    #--------------------------------------------------------------------------
    from optparse import OptionParser

    class MyParser(OptionParser):
        """We subclass OptionParser so I can have newlines in the epilog."""
        def format_epilog(self, formatter):
            return str(self.epilog)

    parser = MyParser(
        description="This is a script for generating the HTML for the #ITPE "
                    "master post on Dreamwidth.",
        epilog="""
Example usage:

  ./itpe_generator.py -i itpe_main.csv -o itpe_main.html

Written by Alex Chan <alex@alexwlchan.net>.  Consult the
README for more configuration options or notes.""")
    parser.add_option("-i", "--input", dest="INPUT_FILE",
                      help="name of the CSV file containing the ITPE data (no "
                           "spaces please)", metavar="INPUT_FILE")
    parser.add_option("-o", "--output", dest="OUTPUT_FILE",
                      help="name of the HTML file to write (no spaces please)",
                      metavar="OUTPUT_FILE")
    parser.add_option("-w", "--width", default="500px",
                      help="width of the cover art in px (default 500px)")
    (options, args) = parser.parse_args()

    #--------------------------------------------------------------------------
    # Input verification - check that everything is set up correctly
    #--------------------------------------------------------------------------
    # Check that the user supplied any arguments
    if (options.INPUT_FILE is None) and (options.OUTPUT_FILE is None):
        print("Use the --input and --output flags to run the script.  Run "
              "with -h or --help for a usage message.")
        sys.exit(1)

    # If the user only supplied one argument, correct them accordingly
    if (options.INPUT_FILE is None) and (options.OUTPUT_FILE is None):
        print("Both the --input and --output flags are required for the "
              "script.  Run with -h or --help for a usage message.")
        sys.exit(1)

    # Strip everything except the digits from the width option, then append
    # 'px' for the CSS attribute
    options.width = re.sub("[^0-9]", '', options.width) + "px"

    # Check that the CSV file exists and we can actually read from it
    if not os.path.isfile(options.INPUT_FILE):
        error("Can't find the input file %s." % options.INPUT_FILE)

    # Check that the CSV file is open for reading, and check that each row is
    # the correct length
    with open(options.INPUT_FILE, 'r') as csvfile:
        itpereader = csv.reader(csvfile, delimiter=',')
        for idx, row in enumerate(itpereader):

            # The first row is headings, so we skip it
            if idx == 0:
                continue

            if len(row) < len(HEADINGS):
                error("Row %d does not have enough fields.  There should be "
                      "%d fields: %s." % (idx, len(HEADINGS), HEADINGS))
            elif len(row) > len(HEADINGS):
                error("Row %d has too many fields.  If some of the entries in "
                      "this row contain commas, then please wrap those entries "
                      "in double quotes (\"\").")

    #--------------------------------------------------------------------------
    # Set up the Jinja2 environment
    #--------------------------------------------------------------------------
    env = Environment(loader=FileSystemLoader(''),
                      trim_blocks=True)

    env.filters['condense'] = condense_into_line
    env.filters['userlink'] = dreamwidth_user_link
    env.filters['splitnames'] = split_username_links

    template = env.get_template('templates/podfic.html')

    #--------------------------------------------------------------------------
    # If we reach this point, then we know that every row has the correct
    # length, so we can create Podfic() instances without worrying about the
    # number of arguments (order is assumed to be correct).
    #--------------------------------------------------------------------------
    podfic_html = list()

    with open(options.INPUT_FILE, 'r') as csvfile:
        itpereader = csv.reader(csvfile, delimiter=',')
        for idx, row in enumerate(itpereader):

            # The first row is headings, so we skip it
            if idx == 0:
                continue

            print("Processing row %d..." % idx)
            podfic = Podfic(*row)
            podfic_html.append(template.render(podfic=podfic,
                                               width=options.width))

    #--------------------------------------------------------------------------
    # Write the HTML out to disk
    #--------------------------------------------------------------------------
    with open(options.OUTPUT_FILE, 'w') as outfile:
        outfile.write('\n<br>\n'.join(podfic_html))

    print("Success!  ITPE HTML has been written to %s." % options.OUTPUT_FILE)

if __name__ == '__main__':
    main()
