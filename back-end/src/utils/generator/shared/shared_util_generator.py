# The Dark Blue CyberPatriot Training Tool
# Copyright (C) 2021 Scott Semian <darkbluedev@gmail.com>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.

import os
import json
import logging
from sys import exit
from abc import abstractmethod
from utils.scoring_engine.shared.shared_util import ChallengeQuestion, File


class Generator:
    def __init__(
        self,
        filepath: str,
        debug: bool = False,
        generator_only: bool = False,
        scoring_only: bool = False,
        log_path: str = None,
        full_debug: bool = False,
        scoring_interval: int = 30,
        notifications: bool = True,
    ) -> None:
        self.filepath = filepath
        self.debug = debug
        self.data = None
        self.scoring_engine = None
        self.generator_only = generator_only
        self.scoring_only = scoring_only
        self.log_path = log_path
        self.full_debug = full_debug
        self.scoring_interval = scoring_interval
        self.notifications = notifications

        self.readme_path = None

        self.question_file_boilerplate = """
--------------------------------------------------------------------------
The question file is meant to test general knowledge or ask a question
about the current image.

Answers are not case sensitive, but must be exactly matched.

Answers should be in the following form:

answer: [EXAMPLE ANSWER]

'answer' must be included with a colon, and is not case sensitive.
--------------------------------------------------------------------------\n\n
"""

    def __str__(self) -> str:
        s = """
        filepath:         {}
        debug:            {}
        generator_only:   {}
        scoring_only:     {}
        log_path:         {}
        full_debug:       {}
        scoring_interval: {}
        notifications:    {}
        """.format(
            self.filepath,
            self.debug,
            self.generator_only,
            self.scoring_only,
            self.log_path,
            self.full_debug,
            self.scoring_interval,
            self.notifications,
        )
        return s

    def initialize_data(self) -> None:
        logging.debug("ImageGenerator: Initializing data file...")

        try:
            data_file = open(self.filepath, "r")
            data = json.load(data_file)

            if data is not None:
                self.data = data

        except (FileNotFoundError, IOError) as e:
            logging.fatal("Could not open data file at path {}".format(self.filepath))
            logging.fatal("Error: {}".format(e))
            print(
                "FATAL ERROR: Could not open data file at path {}".format(self.filepath)
            )
            print("Exiting...")
            exit(-1)

        try:
            format_type = self.data["format"]

            if format_type != "DarkBlue":
                logging.fatal("JSON format specifier does not match.")
                exit(-12)

        except KeyError:
            logging.fatal("No format field is present.")
            exit(-14)

        try:
            os_type = self.data["OS"]

            if os.name == "nt" and os_type != "Windows":
                logging.fatal("OS type is not Windows.")
                exit(-16)
            elif os.name == "posix" and os_type != "Linux":
                logging.fatal("OS type is not Linux.")
                exit(-16)

        except KeyError:
            logging.fatal("No OS field is present.")
            exit(-15)

    def create_readme(self) -> None:
        logging.info("Creating readme...")
        logging.debug("Readme path: {}".format(self.readme_path))

        print("Creating readme...")

        try:
            self.data["readme"]
        except KeyError:
            logging.warning("Could not locate readme data.")
            self.scoring_engine.register_generator_message(
                message="Could not create readme file."
            )
            return

        try:
            with open(self.readme_path, "w") as outfile:
                outfile.write(self.data["readme"])
        except IOError:
            logging.critical(
                "IOError occurred when creating readme file. Readme file may not have"
                " been correctly created."
            )

    @abstractmethod
    def generate_image(self) -> None:
        ...

    @abstractmethod
    def create_question_files(self) -> None:
        ...

    @abstractmethod
    def create_filepaths(self) -> None:
        ...

    @abstractmethod
    def expand_desktop_path(self) -> str:
        ...

    @staticmethod
    def validate_file(file: File) -> bool:
        return False

    @staticmethod
    def validate_question_file(file: ChallengeQuestion) -> bool:
        return False
