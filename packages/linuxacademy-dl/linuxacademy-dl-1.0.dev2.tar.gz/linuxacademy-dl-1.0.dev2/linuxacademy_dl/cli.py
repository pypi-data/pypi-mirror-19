# -*- coding: utf-8 -*-
#
#
# This file is a part of 'linuxacademy-dl' project.
#
# Copyright (c) 2016-2017, Vassim Shahir
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

from __future__ import unicode_literals, absolute_import, print_function
from . import __version__, __title__
from .linux_academy import LinuxAcademy
from .exceptions import LinuxAcademyException

import os
import sys
import getpass
import argparse
import logging

logger = logging.getLogger(__title__)


class CLI(object):

    LOG_FORMAT_CONSOLE = '%(levelname)-8s %(message)s'
    LOG_FORMAT_FILE = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'

    def __init__(self):
        self.argparser = self.argparser_init()

    def argparser_init(self):
        parser = argparse.ArgumentParser(
            description='Fetch all the lectures for a Linux Academy '
                        '(linuxacademy.com) course',
            prog=__title__
        )
        parser.add_argument(
            'link',
            help='Link for Linux Academy course',
            action='store'
        )
        parser.add_argument(
            '-u', '--username',
            help='Username / Email',
            default=None, action='store'
        )
        parser.add_argument(
            '-p', '--password',
            help='Password',
            default=None,
            action='store'
        )
        parser.add_argument(
            '-o', '--output',
            help='Output directory',
            default=None, action='store'
        )
        parser.add_argument(
            '--use-ffmpeg',
            help='Download videos from m3u8/hls with ffmpeg (Recommended)',
            action='store_const',
            const=True,
            default=False
        )
        parser.add_argument(
            '-q', '--video-quality',
            help='Select video quality [default is 1080]',
            default='1080',
            action='store',
            choices=['1080', '720', '480', '360']
        )
        parser.add_argument(
            '--debug',
            help='Enable debug mode',
            action='store_const',
            const=True,
            default=False
        )
        parser.add_argument(
            '-v', '--version',
            help='Display the version of %(prog)s and exit',
            action='version',
            version='%(prog)s {version}'.format(version=__version__)
        )
        return parser

    def __init_logger(self, error_level=logging.INFO):
            logger.setLevel(logging.DEBUG)
            console_log = logging.StreamHandler()
            console_log.setLevel(error_level)
            console_log.setFormatter(
                logging.Formatter(self.LOG_FORMAT_CONSOLE)
            )
            logger.addHandler(console_log)

    def main(self):
        args = vars(self.argparser.parse_args())

        username = args['username']
        password = args['password']
        debug = args['debug']

        if debug:
            self.__init_logger(error_level=logging.DEBUG)
        else:
            self.__init_logger()

        output_folder = os.path.abspath(
            os.path.expanduser(args['output']) if args['output'] else ''
        )

        if not username:
            username = input("Username / Email : ")

        if not password:
            password = getpass.getpass(prompt='Password : ')

        try:
            with LinuxAcademy(
                args['link'], username, password,
                output_folder, args['use_ffmpeg'], args['video_quality']
            ) as la:
                la.analyze()
                la.download()
        except LinuxAcademyException as lae:
            logger.error(lae.message)

        except KeyboardInterrupt:
            logger.error("User interrupted the process, exiting...")
        except Exception as e:
            logger.error('Unknown Exception')
            logger.exception(e)
        finally:
            sys.exit(1)
