#!/usr/bin/env python
# -*- coding: ascii -*-

import sys
import os
#import unittest

"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'Bradley Phillips (brad.phillips@exemail.com.au)'
__copyright__ = 'Copyright (c) 2017 Bradley Phillips'
__license__ = 'BSD'
__vcs_id__ = '$Id$'
__version__ = '0.0.1'


class EasyArgParse(object):
    def __init__(self, defined_args=None, aliases=None, sys_args=sys.argv[1:]):
        t_defined_args = \
            {
                'help':
                    {
                        'optional': True,
                        'help_text': "The help argument is a 'special' built-in argument which as a minimum should"
                                     + "show this message"
                    }
            }

        if defined_args:
            for item_key, item_value in defined_args.items():
                t_defined_args[item_key.lower()] = \
                    {
                        'optional': item_value['optional'],
                        'help_text': item_value['help_text']
                    }

        self.defined_args = t_defined_args
        special_aliases = {'h': 'help'}

        if aliases:
            self.aliases = self.combine_aliases(aliases, special_aliases)
        else:
            self.aliases = special_aliases

        self.parsed_result = {}
        self.args = sys_args

    def is_float(self, value):
        """
        is_float takes a string,
        will yield false for anything that can be parsed as an integer
        will yield true if it can be parsed as a float
        otherwise will yield false
        :param value : str
        :return : bool
        """

        if value.isdigit(): # don't want a false positive on integers
            return False
        try:
            float(value)
            return True
        except ValueError:
            return False

    def combine_aliases(self, defined, special):
        """
        combines the defined and special aliases
        everything is also converted to lowercase
        :param special:
            special aliases can't be overruled
        :param defined:
        :return:
        """

        t_special = {}
        t_defined = {}

        for a, b in special.items():
            t_special[a.lower()] = b.lower()

        for a, b in defined.items():
            t_defined[a.lower()] = b.lower()

        for a, b in t_special.items():
            t_defined[a] = b

        return t_defined

    def show_help(self, title="", msg=""):
        if title:
            print(title)
            
        if msg:
            print(msg)

        list_of_optional_args = []
        list_of_non_optional_args = []

        for defined_key, defined_value in self.defined_args.items():
            if defined_value["optional"]:
                list_of_optional_args.append(defined_key)
            else:
                list_of_non_optional_args.append(defined_key)

        def print_helper(x):
            switch_strings = ["-", "--", "/"]
            print("\t" + x + ":")
            print("\t\t" + "help:")
            print("\t\t\t" + self.defined_args[x]["help_text"])
            print("\n\t\t" + "aliases:")


            matching_aliases = []
            for a, b in self.aliases.items():
                if b == x:
                    matching_aliases.append(a)

            for a in matching_aliases:
                temp_str = "\t\t\t" + switch_strings[0] + a
                for s in switch_strings[1:]:
                    temp_str += (", " + s + a)
                print(temp_str)

        print("Non-optional Arguments:")
        for argument in list_of_non_optional_args:
            print_helper(argument)

        print("\nOptional Arguments:")
        for argument in list_of_optional_args:
            print_helper(argument)


    def parse(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        # help is assumed false unless present
        self.parsed_result = {'help': False}

        for arg in self.args:

            # Strip out hyphens
            if arg[0:2] == "--":
                arg = arg[2:]

            if arg[0] == "-":
                arg = arg[1:]

            if arg[0] == "/":
                arg = arg[1:]

            split_char = "="
            if arg.find(":") != -1:
                if arg.find("=") == -1 | (arg.find(":") < arg.find("=")):
                    split_char = ":"

            temp_split = arg.split(split_char)
            temp_head = temp_split[0].lower()

            # Get the long name for readability
            if temp_head in self.aliases:
                temp_head = self.aliases[temp_head]

            # unlikely that an argument value will have a '=' (or ':') in it, but i can't help it..
            temp_tail = split_char.join(temp_split[1:])

            # attempt to guess numbers and bools
            self.parsed_result[temp_head] = int(temp_tail) if temp_tail.isdigit() \
                else float(temp_tail) if self.is_float(temp_tail) \
                else True if temp_tail == "" \
                else temp_tail

        # display the help message if the help switch is detected
        if self.parsed_result['help']:
            self.show_help(
                title="Help switch detected",
                msg="Make sure to remove the -h or --help switch next time around"
            )
            sys.exit(0)

        # check that no non-optional arguments are missing
        for defined_key, defined_value in self.defined_args.items():
            if not defined_value["optional"]:
                if not defined_key in self.parsed_result:
                    self.show_help(
                        title="Missing non-optional argument",
                        msg="The argument " + defined_key + " is missing, please check the help provided: "
                    )
                    sys.exit(0xA0)
        # drop the help
        self.parsed_result.pop("help")
        return self.parsed_result

"""
class TestEasyArgParse(unittest.TestCase):
    def setUp(self):
        self.eap = EasyArgParse()
        self.special_aliases = {'h': 'help'}

    def test_is_float_with_float(self):
        test_result = self.eap.is_float("0.254")
        self.assertTrue(test_result)

    def test_is_float_with_int(self):
        test_result = self.eap.is_float("5")
        self.assertFalse(test_result)

    def test_is_float_with_zero(self):
        test_result = self.eap.is_float("0")
        self.assertFalse(test_result)

    def test_is_float_with_char(self):
        test_result = self.eap.is_float("a")
        self.assertFalse(test_result)

    def test_is_float_with_str(self):
        test_result = self.eap.is_float("this is a string")
        self.assertFalse(test_result)

    def test_combine_aliases_with_empty(self):
        test_result = self.eap.combine_aliases(self.special_aliases, {})
        self.assertEqual(test_result, self.special_aliases)

    def test_combine_aliases_with_same(self):
        test_result = self.eap.combine_aliases(self.special_aliases, {'h': 'help'})
        self.assertEqual(test_result, self.special_aliases)

    def test_combine_aliases_attempt_special_overwrite(self):
        test_result = self.eap.combine_aliases(special=self.special_aliases, defined={'h': 'something else'})
        self.assertEqual(test_result, self.special_aliases)

    def test_combine_aliases_add_new_aliases(self):
        test_result = self.eap.combine_aliases(self.special_aliases, {'a': 'apple', 'b': 'banana'})
        self.assertEqual(test_result, {'h': 'help', 'a': 'apple', 'b': 'banana'})

    def test_combine_aliases_mixed_case(self):
        test_result = self.eap.combine_aliases(self.special_aliases, {'H': "HELP"})
        self.assertEqual(test_result, self.special_aliases)

    def tearDown(self):
        pass


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEasyArgParse)
    unittest.TextTestRunner(verbosity=2).run(suite)
    print("Happy Path:")
    eap = EasyArgParse\
            (
                defined_args=
                {
                    'input_dir':
                        {
                            'optional': False,
                            'help_text': "directory containing jpgs"
                        }
                },
                aliases={"i": "input_dir"},
                sys_args=["name_of_the_file.py", "--i=../../photos_folder"][1:]
            ).parse()

    print("\nHelp Switch")
    eap = EasyArgParse\
            (
                defined_args=
                {
                    'input_dir':
                        {
                            'optional': False,
                            'help_text': "directory containing jpgs"
                        }
                },
                aliases={"i": "input_dir"},
                sys_args=["name_of_the_file.py", "/h"][1:]
            ).parse()

    print("\nSad Path - non-optional argument missing")
    eap = EasyArgParse\
            (
                defined_args=
                {
                    'input_dir':
                        {
                            'optional': False,
                            'help_text': "directory containing jpgs"
                        }
                },
                aliases={"i": "input_dir"},
                sys_args=["name_of_the_file.py"][1:]
            ).parse()
"""
