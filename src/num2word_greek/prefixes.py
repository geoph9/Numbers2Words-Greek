# MIT License
#
# Copyright (c) [year] [fullname]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


_prefixes = {
    "1digit": {
        "0": "μηδέν",
        "1": "ένα",  # μια, ένας
        "2": "δύο",
        "3": "τρία",  # τρεις
        "4": "τέσσερα",  # τέσσερις
        "5": "πέντε",
        "6": "έξι",
        "7": "εφτά",
        "8": "οχτώ",
        "9": "εννιά"
    },
    "2digit": {
        "10": "δέκα",
        "11": "έντεκα",
        "12": "δώδεκα",
        "1": "δεκα",
        "20": "είκοσι",
        "2": "εικοσι",
        "30": "τριάντα",
        "3": "τριαντα",
        "40": "σαράντα",
        "4": "σαραντα",
        "50": "πενήντα",
        "5": "πενηντα",
        "60": "εξήντα",
        "6": "εξηντα",
        "70": "εβδομήντα",
        "7": "εβδομηντα",
        "80": "ογδόντα",
        "8": "ογδοντα",
        "90": "ενενήντα",
        "9": "ενενηντα"
    },
    "3digit": {
        "100": "εκατό",
        "1": "εκατόν",
        "200": "διακόσια",
        "2": "διακοσια",
        "300": "τριακόσια",
        "3": "τριακοσια",
        "400": "τετρακόσια",
        "4": "τετρακοσια",
        "500": "πεντακόσια",
        "5": "πεντακοσια",
        "600": "εξακόσια",
        "6": "εξακοσια",
        "700": "εφτακόσια",
        "7": "εφτακοσια",
        "800": "οχτακόσια",
        "8": "οχτακοσια",
        "900": "εννιακόσια",
        "9": "εννιακοσια",
    }
}

_plural_forms = {
    "0": "μηδέν",
    "1": "ένα",
    "2": "δυο",
    "3": "τρεις",
    "4": "τέσσερις",
    "5": "πέντε",
    "6": "έξι",
    "7": "εφτά",
    "8": "οχτώ",
    "9": "εννιά"
}

# Update with 4 digits
_prefixes['4digit'] = {'1': 'χίλια'}
_prefixes['4digit'].update({key: (_plural_forms[key] + " χιλιάδες").strip() for key, val in _prefixes['1digit'].items()
                            if key != "1"})

# For 10, 11, 12, 20, 30, 40, ..., 90 take the prefixes from the 2 digit pronunciations
#   and convert them to 10000, 11000, 12000, 20000, ..., 90000
_prefixes['5digit'] = {key + "000": val + " χιλιάδες" for key, val in _prefixes['2digit'].items() if len(key) > 1}

# Update for 6 digits. Replace "διακόσια" with "διακόσιες" in order to bring to plural form
_prefixes['6digit'] = {key + "000": val[:-2] + "ιες" + " χιλιάδες" for key, val in _prefixes['3digit'].items()}

