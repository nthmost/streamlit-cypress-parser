# -*- coding: utf-8 -*-

import re
import sys


class CypressParseError(Exception):
    pass


# =================== #
#   Cypress Lexicon   #

CYPRESS_RUN_START_MARK = "Opening Cypress..."
CYPRESS_RUN_END_MARK = "✓ Reports saved:"

FAIL_MARK = "✖"
SUCCESS_MARK = "✓"      # e.g. ✓ displays an altair chart (2344ms)

REC_START_MARK = "(Run Starting)"   # on single line surrounded by indefinite amt of whitespace 
REC_END_MARK = "(Run Finished)"     # on single line surrounded by indefinite amt of whitespace

FILE_START_MARK = "Running: "        # e.g. Running: altair_chart.spec.ts... 

# =================== #
# Regular expressions #

# https://regexr.com/4odgn
CYPRESS_RE = re.compile("(?P<preamble>.+)" +
                        CYPRESS_RUN_START_MARK +
                        "(?P<records>.+)" +
                        CYPRESS_RUN_END_MARK +
                        "(?P<summary>.+)",
                        re.M | re.S
                       )

# https://regexr.com/4og8u
RECORD_RE = re.compile("\(Run Starting\)(?P<part1>.+?)\(Run Finished\)(?P<part2>.+?)[\=]{10}",
                        re.M | re.S)

def parse_cypress_page(buf):
    """Takes page, returns dictionary containing the logical section of the 
    Cypress return (preamble, records, summary).

    If page cannot be parsed as a Cypress report, raises CypressParseError.
    """
    match = CYPRESS_RE.match(buf)
    if match:
        return match.groupdict()
    raise CypressParseError("Page could not be parsed as a Cypress report.")


def parse_cypress_records(buf):
    """Takes records part of Cypress report page, returns list of CypressRecords.

    If no records can be parsed, raises CypressParseError.
    """
    recs = RECORD_RE.findall(buf)
    if recs:
        from IPython import embed; embed()
        return recs
    raise CypressParseError("No test records could be found in this Cypress report.")


def main(filename):
    with open(filename) as fh:
        buf = fh.read()
        cdict = parse_cypress_page(buf)
        if not cdict:
            return "\nThis doesn't look like a Cypress record.  Giving up!"

        records = parse_cypress_records(cdict['records'])
        return "Found {} records".format(len(records))

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except Exception as err:
        print('Supply a filename as the argument to this script.')
        sys.exit()

    try:
        results = main(filename)
    except CypressParseError as err:
        print(err)
        sys.exit()

print(results)
print('\nDone.')
