# Copyright 2016 Arie Bregman
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import argparse


def create_runserver_parser(subparsers, parent_parser):
    """Adds sub-parser for 'runserver'."""

    runserver_parser = subparsers.add_parser(
        "runserver", parents=[parent_parser])

    runserver_parser.add_argument(
        '--jenkins', '-j', dest="jenkins", help='Jenkins URL')
    runserver_parser.add_argument(
        '--username', '-u', dest="username", help='Jenkins username')
    runserver_parser.add_argument(
        '--password', '-p', dest="password", help='Jenkins user password')
    runserver_parser.add_argument(
        '--conf', '-c', dest="config", help='Jino configuration')
    runserver_parser.add_argument(
        '--jobs', dest="jobs", help='Jenkins Jobs YAML', required=True)


def create_drop_parser(subparsers, parent_parser):
    """Adds sub-parser for 'drop'."""

    subparsers.add_parser("drop", parents=[parent_parser])


def create():
    """Returns argparse parser."""

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--debug', required=False, action='store_true',
                               dest="debug", help='Turn DEBUG on')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="parser")

    create_runserver_parser(subparsers, parent_parser)
    create_drop_parser(subparsers, parent_parser)

    return parser
