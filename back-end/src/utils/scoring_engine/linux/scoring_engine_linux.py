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
import pickle
import logging
from subprocess import Popen
from utils.scoring_engine.shared.shared_util import ScorableItem, ScoringEngine


class ScoringEngine(ScoringEngine):
    def __init__(
        self,
        total_score: int,
        scoring_interval: int = 30,
        notifications: bool = False,
        debug: bool = False,
        debug_config: bool = False,
    ) -> None:

        # OS specific data lists:
        self.processes = []
        self.packages = []
        self.config_files = []

        # OS specific other:
        self.notification_queue = NotificationQueue()
        self.desktop_path = os.path.join(os.environ["HOME"], "Desktop")
        self.scoring_report_path = os.path.join(self.desktop_path, "scoringreport.html")
        self.dark_blue_save_path = os.path.join(os.getenv("HOME"), ".darkblue")

        super().__init__(
            total_score=total_score,
            scoring_interval=scoring_interval,
            notifications=notifications,
            debug=debug,
            debug_config=debug_config,
        )

    def __str__(self) -> str:
        s = """
        {}
        """.format(
            super().__str__()
        )
        return s

    def score(self) -> None:
        print("Scoring...")

        from utils.scoring_engine.linux.scoring_engine_util_linux import (
            score_users,
            score_packages,
            score_processes,
            score_config_files,
        )

        from utils.scoring_engine.shared.shared_util import (
            score_challenge_questions,
            score_files,
        )

        self.current_score = 0
        self.scoring_messages = []
        self.configuration_messages = []

        score_users(self)
        score_packages(self)
        score_processes(self)
        score_config_files(self)

        score_challenge_questions(self)
        score_files(self)

        if self.save_enabled:
            self.save()
        elif not self.save_enabled:
            msg = """An error occurred saving scoring engine to disk.
             Saving has been disabled and the scoring
             engine CANNOT be resumed if terminated or the virtual machine
             is powered down or restarted."""
            self.register_config_message(message=msg)

        self.generate_report()

    def save(self, retry=False):
        logging.debug("Attempting to save scoring engine image to disk.")

        path = os.path.join(self.dark_blue_save_path, "dark_blue_scoring_engine.dat")

        try:
            with open(path, "wb") as outfile:
                pickle.dump(self, outfile, pickle.HIGHEST_PROTOCOL)
        except pickle.PickleError:
            logging.critical("PickleError occurred when saving scoring engine to disk.")
        except FileNotFoundError:

            if retry:
                logging.fatal(
                    "Could not locate directory {} during retried saving"
                    " attempt. Saving will be disabled.".format(
                        self.dark_blue_save_path
                    )
                )
                self.save_enabled = False
                return

            logging.warning("Could not locate Dark Blue directory in Appdata Local.")
            logging.debug(
                "Attempting to create path: {}".format(self.dark_blue_save_path)
            )
            os.makedirs(self.dark_blue_save_path)
            logging.debug("Attemptign to retry saving...")
            self.save(retry=True)
        except Exception:
            if retry:
                logging.fatal(
                    "Could not save scoring engine after retry."
                    " Saving will be disabled."
                )
                self.save_enabled = False
                return
            else:
                logging.fatal(
                    "An unknown exception has occurred while saving scoring"
                    " engine to disk. This error was not caught and"
                    " saving will now be disabled."
                )
                self.save_enabled = False
                return

    def queue_notification(self, item: ScorableItem, positive: bool):
        if not self.notifications:
            return
        else:
            self.notification_queue.issue_notification(item=item, positive=positive)


class NotificationQueue:
    def __init__(self, timeout: int = 2):
        self.timeout = timeout

        self.positive_notifications = []
        self.negative_notifications = []

    def issue_notification(self, item: ScorableItem, positive: bool):

        if positive:
            if item.entry_id not in self.positive_notifications:
                self.positive_notifications.append(item.entry_id)

                if item.entry_id in self.negative_notifications:
                    self.negative_notifications.remove(item.entry_id)

                logging.debug(
                    "Displaying notification for scoring ID: {}".format(item.entry_id)
                )

                self.display_notification(positive=True)

        else:
            if item.entry_id not in self.negative_notifications:
                self.negative_notifications.append(item.entry_id)

                if item in self.positive_notifications:
                    self.positive_notifications.remove(item.entry_id)

                logging.debug(
                    "Displaying notification for scoring ID: {}".format(item.entry_id)
                )
                self.display_notification(positive=False)

    def display_notification(self, positive: bool = False):
        message = ""

        if positive:
            message = "You have gained points!"
        else:
            message = "You have lost points."

        # Subprocess call.
        Popen('notify-send -t 1000 \"Dark Blue\" \"{}\"'.format(message), shell=True)


class User(ScorableItem):
    def __init__(
        self,
        name: str,
        allowed: bool,
        is_sudo: bool,
        sudo_initial_state: bool,
        user_id: str,
        entry_id: int,
        positive_points: int,
        negative_points: int,
        positive_message: str = None,
        negative_message: str = None,
    ) -> None:
        self.name = name
        self.allowed = allowed
        self.is_sudo = is_sudo
        self.sudo_initial_state = sudo_initial_state
        self.user_id = user_id

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
        Class: User
        name:                 {}
        allowed:              {}
        is_sudo:              {}
        sudo_initial_state:   {}
        user_id:              {}
        {}
        """.format(
            self.name,
            self.allowed,
            self.is_sudo,
            self.sudo_initial_state,
            self.user_id,
            super().__str__(),
        )
        return s


class Process(ScorableItem):
    def __init__(
        self,
        name: str,
        default_state: bool,
        desired_state: bool,
        entry_id: int,
        positive_points: int,
        negative_points: int,
        positive_message: str = None,
        negative_message: str = None,
    ) -> None:
        self.name = name
        self.default_state = default_state
        self.desired_state = desired_state

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
        Class: Process
        name:             {}
        default_state:    {}
        desired_state:    {}
        {}
        """.format(
            self.name, self.default_state, self.desired_state, super().__str__()
        )
        return s


class Package(ScorableItem):
    def __init__(
        self,
        name: str,
        installed: bool,
        starting_state: bool,
        entry_id: int,
        positive_points: int,
        negative_points: int,
        positive_message: str = None,
        negative_message: str = None,
    ) -> None:
        self.name = name
        self.installed = installed
        self.starting_state = starting_state

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
        Class: Package
        name:            {}
        installed:       {}
        starting_state:  {}
        {}
        """.format(
            self.name, self.installed, self.starting_state, super().__str__()
        )
        return s


class ConfigFile(ScorableItem):
    def __init__(
        self,
        path: str,
        default_value: str,
        positive_value: str,
        negative_value: str,
        create: bool,
        entry_id: int,
        positive_points: int,
        negative_points: int,
        positive_message: str = None,
        negative_message: str = None,
    ) -> None:

        self.path = path
        self.default_value = default_value
        self.positive_value = positive_value
        self.negative_value = negative_value
        self.create = create

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
        Class: ConfigFile
        name:              {}
        path:              {}
        default_value:     {}
        positive_value:    {}
        negative_value:    {}
        create:            {}
        {}
        """.format(
            self.name,
            self.path,
            self.default_value,
            self.positive_value,
            self.negative_value,
            self.create,
            super().__str__(),
        )
        return s
