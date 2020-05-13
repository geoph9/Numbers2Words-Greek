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


import re


def handle_commas(word: str, comma_symbol=",") -> str:
    # If , (comma) is not between two numbers then erase it.
    comma_index = word.find(comma_symbol)
    while comma_index != -1:
        if comma_index == 0:
            word = word[1:]
        elif comma_index == len(word) - 1:  # if it is the last character
            if word[comma_index-1].isdigit():
                word = word.replace(comma_symbol, " κόμμα")  # e.g. if word=102, then we expect another digit after that
            else:
                word = word.replace(comma_symbol, "")
        else:
            word = re.sub(r"\s+", " ", word)
            # --------------- Start ignore spaces ---------------
            # So, for example, if word == 102 , 98 then convert it to 102, 98 and then to 102,98 (remove spaces)
            if word[comma_index-1] == " ":
                word = word[:comma_index-1] + word[comma_index:]
                comma_index -= 1  # The index went one place back
            try:
                if word[comma_index+1] == " ":
                    word = word[:comma_index+1] + word[comma_index+2:]
            except IndexError:
                pass
            # ----------------- End ignore spaces ----------------
            try:
                # Check left and right if they are digits
                if word[comma_index-1].isdigit() and word[comma_index+1].isdigit():
                    # if word=2,98 then convert it to δυο κόμμα ενενήντα οχτώ (keep the comma since it is pronounced)
                    word = word[:comma_index] + " κόμμα " + word[comma_index+1:]
                else:
                    # Otherwise, delete the comma
                    word = word[:comma_index] + " " + word[comma_index+1:]
            except IndexError:
                # Otherwise, delete the comma
                word = word[comma_index-1]
                break
        comma_index = word.find(comma_symbol)
    return word


def handle_hours(word: str):
    # We will assume that the word is an hour if it contains a ":"
    # For example, convert 10:45 to 10 και 45
    # If the minutes are 15 or 30 then the hour will look like:
    #   10:15 -> 10 και τεταρτο
    #   8:30  -> 8 και μιση (and not οχτωμιση)
    if ":" not in word:
        return word
    parts = word.split(":")
    if len(parts) != 2 or "" in parts:
        # Just ignore the ':'
        return word
    word = re.sub(":", " και ", word)
    if parts[1] == "15":
        word = re.sub("15", "τέταρτο", word)
    elif parts[1] == "30":
        word = re.sub("30", "μισή", word)
    return word

