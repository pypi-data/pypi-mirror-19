# A basic configuration file parser module
# Written by Francesco Palumbo aka phranz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import re



class ParseException(Exception):

    def __init__(self, ln, msg):
        self.lineno  = ln
        self.message = msg


class NoRulesProvided(Exception):
    pass


def parse(flpath, rules=None, fsep_char='=', comm_char='#'):
    '''
    Returns a dictionary with parsed data.

    Arguments:
    
        flpath: config file path

        rules:  dictionary containing options to
                be parsed as keys and regexes as values; 
                ex: {'min': r'\d\d', 'max': r'[0-9]' }

        fsep_char: character separator (default '=')

        comm_char: comment character (default '#')

    Exceptions:

        NoRulesProvided: in case rules are not given

        ParseException: specific message with error line number

    '''

    if not rules:
        raise NoRulesProvided
    
    data = {}

    with open(flpath, 'r') as f:
        for i, line in enumerate(f, 1):

            line = line.strip().replace('\t', '')

            if not line.isprintable():
                raise ParseException(i, 'non printable characters detected.')

            if line.startswith(comm_char) or not line:
                continue

            try:
                k, v = line.split(fsep_char)

            except ValueError:
                raise ParseException(i, 'syntax error!')
   
            k = k.strip()
            v = v.strip()

            if k not in rules.keys():
                raise ParseException(i, '"%s" is not an option.' % k)

            if not re.match(rules[k], v):
                raise ParseException(i, '"%s" is not a valid type.' % v)

            data[k] = v

    return data



if __name__ == '__main__':


    rules = {'min': r'[1-3][0-9]',
             'max': r'/.*?'}

    print(parse('test', rules, '=', '#'))
