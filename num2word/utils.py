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


from num2word.convert_numbers import convert_numbers
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
    try:
        if int(parts[0]) < 1 or int(parts[0]) > 12:
            # then it is not an hour
            return word
    except Exception as e:
        # print("Exception:", e)
        pass
    word = re.sub(":", " και ", word)
    if parts[0] == "1": word = re.sub("1", "μία", word[0]) + word[1:]
    elif parts[0] == "3": word = re.sub("3", "τρείς", word[0]) + word[1:]
    elif parts[0] == "4": word = re.sub("4", "τέσσερις", word[0]) + word[1:]
    if parts[1] == "15":
        word = re.sub("15", "τέταρτο", word)
    elif parts[1] == "30":
        word = re.sub("30", "μισή", word)
    return word


_standard_ordinals = {
    1: "πρώτ",
    2: "δεύτερ",
    3: "τρίτ",
    4: "τέταρτ",
    5: "πέμπτ",
    6: "έκτ",
    7: "έβδομ",
    8: "όγδο",
    9: "ένατ",
    20: "εικοστ",
    30: "τριαντακοστ",
    40: "τεσσαρακοστ",
    50: "πεντηκοστ",
    60: "εξηκοστ",
    70: "εβδομηκοστ",
    80: "ογδοηκοστ",
    90: "ενενηκοστ",
    100: "εκατοστ",
    200: "διακοσιοστ",
    300: "τριακοσιοστ",
    400: "τετρακοσιοστ",
    500: "πεντακοσιοστ",
    600: "εξακοσιοστ",
    700: "εφτακοσιοστ",
    800: "οχτακοσιοστ",
    900: "εννιακοσιοστ",
    1000: "χιλιοστ"
}

def intonate(syllabel):
    out = syllabel
    if 'ο' in syllabel: out = re.sub("ο", "ό", syllabel)
    if 'ι' in syllabel: out = re.sub("ι", "ί", syllabel)
    if 'α' in syllabel: out = re.sub("α", "ά", syllabel)
    if 'η' in syllabel: out = re.sub("η", "ή", syllabel)
    if 'ε' in syllabel: out = re.sub("ε", "έ", syllabel)
    if 'υ' in syllabel: out = re.sub("υ", "ύ", syllabel)
    if 'ω' in syllabel: out = re.sub("ω", "ώ", syllabel)
    return out


def convert_ordinals(word):
    out_words = ""
    for w in word.split(" "):
        # Step 1: Separate the word from the number (e.g. 10ος -> (10, ος)])
        words = re.split(r"(\d+)", w)  # may have spaces
        words = (w for w in words if w.strip() != "")  # remove spaces from list
        try:
            number, suffix = words
            number = int(number)
        except ValueError:  
            # This is not an ordinal since it is either sth like 10α10 (probably some typo)
            #       OR
            # sth like να10 (the word is first)
            out_words += w + " "
            continue
        if suffix.lower() not in ['ος', 'ες', 'ο', 'η', 'α', 'οι']: out_words += w + " "; continue
        if number < 1: out_words += w + " "; continue
        if 1 <= number <= 9: out_words += _standard_ordinals[number] + suffix + " "; continue
        if number in _standard_ordinals.keys(): out_words += _standard_ordinals[number] + intonate(suffix) + " "; continue  # catch 20, 30, 40...
        if number in [10, 11, 12]: out_words += convert_numbers(str(number)) + "τ" + suffix + " "; continue
        if 13 <= number <= 19: out_words+= "δέκατ" + suffix + " " + _standard_ordinals[int(str(number)[-1])] + suffix + " "; continue
        try:
            num_of_digits = len(str(number))
            # e.g. from 23ος keep the 2 and write εικοστός (which is 2 * 10^(2-1))
            # e.g. from 401ος keep the 4 and write τετρακοσιοστός (which is 4 * 10^(3-1)) (3 is the number of digits in 401)
            out =  _standard_ordinals[int(str(number)[0]) * (10**(num_of_digits-1))] + intonate(suffix)
            for i in range(1, num_of_digits):  # for the remaining digits
                temp_word = str(number)[i:] + suffix
                if temp_word.startswith("0"): continue  # e.g. if word is "103ος" then in this loop we will start from 03 and we want to ignore the 0
                out += " " + convert_ordinals(temp_word)
                break
            out_words += out
        except KeyError:
            # This will happen if a number bigger than 1999 is given
            out_words += w
        out_words += " "
    return out_words.strip()
