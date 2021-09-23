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

import re
import os
import sys
import time
import logging
from shutil import copyfile
from bs4 import BeautifulSoup
from datetime import datetime
from abc import abstractmethod


class ScorableItem:
    """Class that defines an entry on the system that can be scored, contains all
    points and scoring message information."""

    def __init__(
        self,
        entry_id: int,
        positive_points: int,
        negative_points: int,
        positive_message: str = None,
        negative_message: str = None,
    ) -> None:
        self.entry_id = entry_id
        self.positive_points = positive_points
        self.negative_points = negative_points
        self.positive_message = positive_message
        self.negative_message = negative_message

    def __str__(self) -> str:
        s = """
        Class: ScorableItem
        entry_id:            {}
        positive_points:     {}
        negative_points:     {}
        positive_message:    {}
        negative_message:    {}""".format(
            self.entry_id,
            self.positive_points,
            self.negative_points,
            self.positive_message,
            self.negative_message,
        )
        return s


class ScoringEngine:
    def __init__(
        self,
        total_score: int,
        scoring_interval: int = 30,
        notifications: bool = False,
        debug: bool = False,
        debug_config: bool = False,
    ) -> None:
        # Arguments:
        self.total_score = total_score
        self.scoring_interval = scoring_interval
        self.notifications = notifications
        self.debug = debug
        self.debug_config = debug_config

        # Flags:
        self.run = True
        self.save_enabled = True

        # Data values:
        self.scoring_id = 0
        self.current_score = 0

        # Shared data lists:
        self.users = []
        self.files = []
        self.scoring_messages = []
        self.challenge_questions = []
        self.scoring_engine_messages = []

        # Persistent generator list.
        self.generator_messages = []

    def __str__(self) -> str:
        s = """
        Class: ScoringEngine OS: Generic
        total_score:      {}
        scoring_interval: {}
        notifications:    {}
        debug:            {}
        debug_config:     {}
        """.format(
            self.total_score,
            self.scoring_interval,
            self.notifications,
            self.debug,
            self.debug_config,
        )
        return s

    def start(self):
        """Starts the scoring engine, which will score on the given scoring interval."""

        print("Starting scoring engine...")

        if self.debug_config:
            self.debug_configuration()

        while self.run:
            self.score()
            print("Current score: {}".format(self.current_score))
            logging.debug("Sleeping...")
            time.sleep(self.scoring_interval)

    def award_points(self, item: ScorableItem, message=None):
        """Award points for the given ScorableItem, add scoring message and
        queue a notification."""

        # Want to determine if we should use the message
        # from the scoring or from the object itself.
        # Often they may both be present, and might be identical,
        # in this case item.positive_message is preferred.
        if (
            (message is None and item.positive_message is not None)
            or (message is not None and item.positive_message is not None)
            and item.positive_message != ""
        ):
            scoring_message = "[+{}] {}".format(
                item.positive_points, item.positive_message
            )
        elif message is not None and (
            item.positive_message is None or item.positive_message == ""
        ):
            scoring_message = "[+{}] {}".format(item.positive_points, message)
        else:  # Failed case, no messages were given.
            scoring_message = "[+{}] Unspecified message.".format(item.positive_points)

        # Add some debugging output as well. This greatly reduces the number
        # of debugging statements inline.
        logging.debug("AWARD POINTS: {}".format(scoring_message))

        # Set new score.
        self.current_score += item.positive_points
        self.scoring_messages.append(scoring_message)

        # Queue a notification. This method is overwritten by the OS specific engine.
        self.queue_notification(item=item, positive=True)

    def remove_points(self, item: ScorableItem, message=None):
        """Remove points for the given ScorableItem, add scoring message and
        queue a notification."""

        # Same as award points, item.negative_message is preferred.
        if (
            (message is None and item.negative_message is not None)
            or (message is not None and item.negative_message is not None)
            and item.negative_message != ""
        ):
            scoring_message = "[-{}] {}".format(
                item.negative_points, item.negative_message
            )
        elif message is not None and (
            item.negative_message is None or item.negative_message == ""
        ):
            scoring_message = "[-{}] {}".format(item.negative_points, message)
        else:  # No messages given.
            scoring_message = "[-{}] Unspecified message.".format(item.negative_points)

        logging.debug("REMOVE POINTS: {}".format(scoring_message))

        # Set score.
        self.current_score -= item.negative_points
        self.scoring_messages.append(scoring_message)

        self.queue_notification(item=item, positive=False)

    def register_config_message(self, message: str):
        """Adds a message for the configuration list in the scoring report,
        used for scoring engine errors."""
        self.scoring_engine_messages.append(message)
        logging.critical(message)

    def register_generator_message(self, message: str):
        """Adds a message to the generator error list, which persists through each score.
        Used for errors that occurred during image generation."""
        self.generator_messages.append(message)
        logging.critical(message)

    def request_scoring_id(self):
        """Used to assign a scoring ID to a ScorableItem."""
        self.scoring_id += 1
        return self.scoring_id

    def generate_report(
        self, retry: bool = False, dev: bool = False, dev_path: str = None
    ):
        """Edit the scoring report HTML file on the desktop to reflect
        current score and scoring messages."""

        logging.debug("Attempting to generate scoring report...")

        try:
            # Attempt to open the scoring report file.
            outfile = open(self.scoring_report_path, "rb")

            # Get the contents of the file.
            soup = BeautifulSoup(outfile, features="html.parser")
            encoding = (
                soup.original_encoding or "utf-8"
            )  # Save the file encoding in case it's needed.

            # Look for the scoring messages, then reset them.
            scoring_list = soup.find(id="scoring_messages")
            scoring_list.string = ""

            # Find the actual tag that gives the score and set the current score.
            scoring_tag = soup.find(id="score")
            scoring_tag.string = "Score: {}/{}".format(
                self.current_score, self.total_score
            )

            # Find scoring engine configuration messages and reset them.
            configuration_list = soup.find(id="configuration_messages")
            configuration_list.string = ""

            generator_list = soup.find(id="generator_messages")
            generator_list.string = ""

            # Populate the list of scoring messages.
            for message in self.scoring_messages:
                tag = soup.new_tag("li")
                tag.string = message

                if message[1] == "-":
                    tag["style"] = "color: red;"

                scoring_list.append(tag)

            # Populate the list of scoring engine errors.
            for message in self.scoring_engine_messages:
                tag = soup.new_tag("li")
                tag.string = message
                tag["style"] = "color: red;"
                configuration_list.append(tag)

            for message in self.generator_messages:
                tag = soup.new_tag("li")
                tag.string = message
                tag["style"] = "color: red;"
                generator_list.append(tag)

            # Update the scoring timestamp.
            timestamp = soup.find(id="timestamp")
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            timestamp.string = "Last scored: {}".format(current_time)

            # Write the new contents to the file after removing them.
            # outfile.truncate(0) -- Caused an issue where the scoring report
            # would grow in size exponentially with garbage characters at the front.
            outfile.close()
            outfile = open(self.scoring_report_path, "wb")

            outfile.write(soup.encode(encoding=encoding))
            outfile.close()

        except IOError:  # Something went wrong.
            if retry:
                # If we still have problems after a retry, something is wrong.
                logging.critical("Could not open scoring report after retry.")
                return

            # Separate pathway used for dev, because sys._MEIPASS won't be
            # usable since it's not a compiled binary.
            if dev:
                if dev_path is not None:
                    # Try to find and copy the template file, then retry.
                    copyfile(dev_path, self.scoring_report_path)
                    self.generate_report(retry=True, dev=dev, dev_path=dev_path)
                else:
                    logging.critical(
                        "No filepath was supplied to the template file in dev mode."
                    )
                    return
            else:
                # Try to find and copy the template file, then retry.
                try:
                    base_path = sys._MEIPASS
                except Exception:
                    base_path = os.path.abspath(".")
                file_path = os.path.join(base_path, "scoringreport_template.html")
                copyfile(file_path, self.scoring_report_path)
                self.generate_report(retry=True)

    @abstractmethod
    def score(self):
        ...

    @abstractmethod
    def queue_notification(self, item: ScorableItem, positive: bool):
        ...

    @abstractmethod
    def debug_configuration(self):
        ...

    @abstractmethod
    def save(self):
        ...


class ChallengeQuestion(ScorableItem):
    def __init__(
        self,
        name: str,
        filepath: str,
        answer: str,
        entry_id: int,
        positive_points: int,
        positive_message: str = None,
    ):
        self.name = name
        self.filepath = filepath
        self.answer = answer

        ScorableItem.__init__(
            self,
            entry_id=entry_id,
            positive_points=positive_points,
            negative_points=0,
            positive_message=positive_message,
            negative_message="",
        )

    def __str__(self) -> str:
        s = """
        Class: ChallengeQuestion
        name:        {}
        filepath:    {}
        answer:      {}
        {}
        """.format(
            self.name, self.filepath, self.answer, super().__str__()
        )

        return s


class File(ScorableItem):
    def __init__(
        self,
        filepath: str,
        exist: bool,
        entry_id: int,
        positive_points: int,
        negative_points: int,
        positive_message: str = None,
        negative_message: str = None,
    ):
        self.filepath = filepath
        self.exist = exist

        ScorableItem.__init__(
            self,
            entry_id=entry_id,
            positive_points=positive_points,
            negative_points=negative_points,
            positive_message=positive_message,
            negative_message=negative_message,
        )

    def __str__(self) -> str:
        s = """
        Class: File
        filepath: {}
        exist:    {}
        {}
        """.format(
            self.filepath, self.exist, super().__str__()
        )

        return s


def score_challenge_questions(
    scoring_engine: ScoringEngine, unit_test=False, test_response=None
):
    file: ChallengeQuestion
    for file in scoring_engine.challenge_questions:
        logging.debug("Expected answer: {}".format(file.answer))
        try:
            # Skip reading response data if we're running the unit test.
            if unit_test is False:
                f = open(file.filepath, "r")
                line = f.read().strip().lower()
            else:
                line = test_response

            answer_regex = re.compile(r"(answer:\s*)(.+)")
            result = re.findall(answer_regex, line)

            for response in result:
                answer = response[1]

                if answer == file.answer.lower():
                    scoring_engine.award_points(
                        item=file,
                        message="Question {} was answered correctly.".format(file.name),
                    )
        except IOError:
            logging.warning(
                "IOError occurred when reading file at {}".format(file.filepath)
            )
        except FileNotFoundError:
            logging.warning("Could not find file at {}".format(file.filepath))
        except Exception as e:
            logging.warning(
                "Unspecified exception occurred when reading file at {}".format(
                    file.filepath
                )
            )
            logging.warning(e)


def score_files(scoring_engine: ScoringEngine):

    file: File
    for file in scoring_engine.files:
        if os.path.exists(file.filepath):
            logging.debug("File exists: {}".format(file.filepath))

        else:
            if file.exist:
                scoring_engine.remove_points(
                    item=file, message="{} was deleted.".format(file.filepath)
                )

            elif not file.exist:
                scoring_engine.award_points(
                    item=file, message="{} was deleted.".format(file.filepath)
                )
