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

import argparse

import sys
import os
import glob
import re

from tempfile import mkstemp
from shutil import move

from num2word.utils import handle_commas, handle_hours
from num2word.convert_numbers import convert_numbers



to_plural = lambda word: re.sub("ερα", "ερις", re.sub("τρία", "τρείς", word))  # for 13 and 14 special cases in plural



def convert_sentence(sentence: str, to_lower: bool = False):
    if sentence.strip() == "":
        return sentence
    final_sent = []
    if to_lower:
        sentence = sentence.lower()
    sentence = re.sub(r"\s+", " ", sentence).strip()
    for word_complex in sentence.split():
        # Handle commas (convert to decimals) and handle hours
        word_complex = handle_commas(word_complex)
        word_complex = handle_hours(word_complex)
        for word in word_complex.split():
            # word = word.lower()
            if word == "":
                continue
            # Split words into words and digits (numbers). E.g. είναι2 -> είναι 2.
            match = re.match(r"([a-zα-ωά-ώϊΐϋΰ]+)([0-9]+)", word, re.I)
            if match:
                words = match.groups()
            else:
                words = [word]
            for w in words:
                if w.strip() == "":
                    continue
                # Convert numbers to words (if they exist).
                final_sent.append(convert_numbers(w))
    # Concatenate punctuation (e.g. from "they had 9 . the others had 10 ." to "they had nine. the others had 10.")
    #  -> Note that the space before the dots appears deliberately (check process_word in utils.py).
    final_sent = " ".join(final_sent)
    final_sent = re.sub(r"\s+", " ", final_sent)
    final_sent = re.sub(r"\s\.", ".", final_sent)
    final_sent = re.sub(r"\s\?", "?", final_sent)
    final_sent = re.sub(r"\s\n", "\n", final_sent)
    final_sent = re.sub(r"\s\t", "\t", final_sent)
    # final_sent = re.sub(":", " ", final_sent)
    # final_sent = re.sub(r"\s+", " ", final_sent)
    return final_sent


def _convert_file_contents(filepath: str, out_path: str):
    """ Replaces the numbers of each sentence in the provided input file, to the corresponding 
        greek word.
        Args:
            filepath: The path to the file for which you want to change the numbers to words.
            out_path: The output file where the new content will be saved.
        Returns:
            Nothing
    """
    # ------------------------ CHECK IF FILE EXISTS ---------------------------
    if not os.path.exists(filepath):
        raise FileNotFoundError("Could not locate the path that you provided:", filepath)
    if (not os.path.exists(os.path.dirname(out_path))) and (not os.path.isfile(out_path)):
        raise ValueError("Cannot create {} since its parent directory does not exist.".format(out_path))
    if os.path.samefile(filepath, out_path):
        # Create temporary file which will replace the old one.
        fh, abs_path = mkstemp()
        with os.fdopen(fh, 'w') as newf:
            with open(filepath, "r", encoding="utf-8") as f:
                line = f.readline()
                while line:
                    if line.strip() == "":
                        newf.write("\n")
                    else:
                        newf.write(convert_sentence(line) + "\n")
                    line = f.readline()
        # Remove old file
        os.remove(filepath)
        # Move new file
        move(abs_path, filepath)
        return
    else:
        with open(filepath, "r", encoding="utf-8") as fr:
            with open(out_path, "w", encoding="utf-8") as fw:
                line = fr.readline()
                while line:
                    if line.strip() == "":
                        fw.write("\n")
                    else:
                        fw.write(convert_sentence(line) + "\n")
                    line = fr.readline()


def _replace_file_prompt(filepath: str) -> bool:
    ans = input("Are you sure you want to replace the contents of {}? [Y/N]".format(filepath))
    if ans.lower() in ['y', 'yes', 'sure']:
        return True
    return False


def cmdline():
    msg = """ Use this script if you want to convert the digits of a file to their equivalent greek words.
              You may provide a path to a text file containing only the transcript of an audio file and the 
              contents of it will be replace with so that there are not digits.
              E.g. If the file contains "100 ευρώ" then it will be converted to "εκατό ευρώ"
              
              You may also provide the path to a directory where transcript files are located and the script 
              will process all of them. Make sure to change the file extension if needed since the default 
              one is .lab. 
              
              If you want to test the script then you may use the -t argument and provide a single word.
              
              NOTE: The files are replaced so please be careful to have a copy of the original ones before
              you run this script.
            
          """
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument("-t", "--test-word", required=False, default=None,
                        help="A test word in order to test the functionality of the script.")
    parser.add_argument("-p", "--path", required=False, default=None,
                        help="Path to a file or a directory containing the text files.")
    parser.add_argument("-e", "--extension", required=False, default=".txt",
                        help="Extension of the text files containing the transcripts.")
    parser.add_argument("-o", "--out-path", required=False, default=None,
                        help="Where the new file/files will be placed. Will only be used "
                             "if you provided the --path option. Cases: "
                             "1. If you provided a file in --path then: "
                             "   a) if --out-path is file like then we will create it."
                             "   b) if --out-path is a directory then we will create a "
                             "      new file with the same name as --path inside --out-path."
                             "2. If you provided a directory in --path then:"
                             "   a) --out-path MUST be the directory when you want your output"
                             "      files to be saved (the names will be saved as before)."
                             "3. If --out-path is not used then we will replace the file after"
                             "   prompting you.")
    args = parser.parse_args()
    if args.test_word is not None:
        print(convert_sentence(args.test_word))
        print("Converted test word, now exiting...")
        sys.exit(0)

    if args.path is None:
        return argparse.ArgumentTypeError("You should provide at least on of the --test-word "
                                          "or --path arguments. Aborting...")
    
    # ------------------------ CHECK IF FILE EXISTS ---------------------------
    if not os.path.exists(args.path):
        raise argparse.ArgumentTypeError("Could not locate the path that you provided: {}.".format(args.path))
    path = os.path.abspath(args.path)

    # Handle out path.
    if args.out_path is not None:
        # Take the path provided in the arguments
        outpath = os.path.abspath(args.out_path)
    else:
        if os.path.isfile(path):
            # use the same directory
            outpath = os.path.dirname(path)
        elif os.path.isdir(path):
            # use the same directory
            outpath = path
        else:
            # The only way we will get here is if --path was not a file, but this would be caught above.
            print("Unexpected Error. Aborting...")
            sys.exit(1)

    # ------------------------ CASE 1: INPUT IS FILE ---------------------------
    if os.path.isfile(path):
        if os.path.isdir(outpath):
            outpath = os.path.join(outpath, os.path.basename(path))
        # Delete previous content or create new file.
        with open(outpath, "w") as f:
            f.write("")
        if os.path.samefile(path, outpath):
            if not _replace_file_prompt(path):
                print("Aborting...")
                sys.exit(1)
        _convert_file_contents(path, outpath)
        print("Success!")
        print("Done processing file:", path)
        print("The output is saved in:", outpath)
        sys.exit(0)
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    
    # ------------------------ CASE 2: INPUT IS DIR ---------------------------
    if os.path.isdir(path) and os.path.isdir(outpath):
        if os.path.samefile(path, outpath):
            if not _replace_file_prompt(path):
                print("Aborting...")
                sys.exit(1)
        text_file_dir = glob.glob(os.path.join(path, "*" + args.extension))
        if len(text_file_dir) == 0:
            raise ValueError("The directory that you provided is empty. Aborting...")
        for text_file in text_file_dir:
            new_out = os.path.join(outpath, os.path.basename(text_file))
            with open(new_out, "w") as f:
                f.write("")
            _convert_file_contents(text_file, new_out)
        print("Success!")
        print("Done processing files from the directory:", path)
        sys.exit(0)
    else:  # outpath is a file while the input path is a directory.
        print("--out-path is not a directory while --path is. If you want to replace the "
              "contents of {} then leave the --out-path option blank.".format(path))
        sys.exit(1)
    print("Unexpected Error. Aborting...")
    sys.exit(1)


if __name__ == '__main__':
    cmdline()
