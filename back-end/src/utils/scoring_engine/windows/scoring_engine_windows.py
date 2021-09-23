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
from plyer import notification
from utils.scoring_engine.shared.shared_util import (
    ScorableItem,
    ScoringEngine,
)


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
        self.services = []
        self.firewall = []
        self.programs = []
        self.registry_entries = []

        # OS specific other:
        self.notification_queue = NotificationQueue()
        self.desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
        self.scoring_report_path = os.path.join(self.desktop_path, "scoringreport.html")
        self.dark_blue_save_path = os.path.join(os.getenv("LOCALAPPDATA"), "DarkBlue")

        super().__init__(
            total_score=total_score,
            scoring_interval=scoring_interval,
            notifications=notifications,
            debug=debug,
            debug_config=debug_config,
        )

    def __str__(self) -> str:
        s = """
        Class: ScoringEngine OS: Windows
        {}
        """.format(
            super().__str__()
        )
        return s

    def score(self):
        """Score the virtual machine image."""

        print("Scoring...")

        # Imported here to resolve circular import issue.
        from utils.scoring_engine.windows.util_windows import (
            score_users,
            score_programs,
            score_firewall,
            score_registry_entries,
            score_services,
        )

        from utils.scoring_engine.shared.shared_util import (
            score_challenge_questions,
            score_files,
        )

        self.current_score = 0
        self.scoring_messages = []
        self.configuration_messages = []

        score_users(self)
        score_programs(self)
        score_firewall(self)
        score_registry_entries(self)
        score_services(self)

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
        """Save an image of the scoring engine to disk."""
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

    def debug_configuration(self):
        """Calls the string methods on all classes in order to ensure all
        Python objects are properly initialized."""

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
            # Check to make sure a notification hasn't already been issued.
            if item.entry_id not in self.positive_notifications:
                self.positive_notifications.append(item.entry_id)

                # If there was previously a negative notification, remove it so it can
                # be reissued if needed.
                if item.entry_id in self.negative_notifications:
                    self.negative_notifications.remove(item.entry_id)

                logging.debug(
                    "Displaying notification for scoring ID: {}".format(item.entry_id)
                )

                self.display_notification(positive=True)

        else:  # Notification is negative.
            if item.entry_id not in self.negative_notifications:
                self.negative_notifications.append(item.entry_id)

                if item.entry_id in self.positive_notifications:
                    self.positive_notifications.remove(item.entry_id)

                logging.debug(
                    "Displaying notification for scoring ID: {}".format(item.entry_id)
                )

                self.display_notification(positive=False)

    def display_notification(self, positive: bool = True):

        message = ""

        if positive:
            message = "You have gained points!"
        else:
            message = "You have lost points."

        notification.notify(title="Dark Blue", message=message, timeout=self.timeout)


class User(ScorableItem):
    def __init__(
        self,
        name: str,
        allowed: bool,
        is_admin: bool,
        admin_initial_state: bool,
        user_id: str,
        entry_id: int,
        positive_points: int,
        negative_points: int,
        positive_message: str = None,
        negative_message: str = None,
    ):
        self.name = name
        self.allowed = allowed
        self.is_admin = is_admin
        self.admin_initial_state = admin_initial_state
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
        is_admin:             {}
        admin_initial_state:  {}
        user_id:              {}
        {}
        """.format(
            self.name,
            self.allowed,
            self.is_admin,
            self.admin_initial_state,
            self.user_id,
            super().__str__(),
        )
        return s


class Service(ScorableItem):
    def __init__(
        self,
        name: str,
        common_name: str,
        default_state: bool,
        desired_state: bool,
        startup_state: str,
        desired_startup_state: str,
        entry_id: int,
        positive_points: int,
        negative_points: int,
        positive_message: str = None,
        negative_message: str = None,
    ):

        self.name = name
        self.common_name = common_name
        self.default_state = default_state
        self.desired_state = desired_state
        self.startup_state = startup_state
        self.desired_startup_state = desired_startup_state

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
        Class: Service
        name:                  {}
        common_name:           {}
        default_state:         {}
        desired_state:         {}
        startup_state:         {}
        desired_startup_state: {}
        {}
        """.format(
            self.name,
            self.common_name,
            self.default_state,
            self.desired_state,
            self.startup_state,
            self.desired_startup_state,
            super().__str__(),
        )
        return s


class RegistryEntry(ScorableItem):
    def __init__(
        self,
        key: str,
        key_path: str,
        entry_name: str,
        default_value: str,
        positive_value: str,
        negative_value: str,
        entry_id: int,
        positive_points: int,
        negative_points: int,
        positive_message: str = None,
        negative_message: str = None,
    ):

        self.key = key
        self.key_path = key_path
        self.entry_name = entry_name
        self.default_value = default_value
        self.positive_value = positive_value
        self.negative_value = negative_value

        ScorableItem.__init__(
            self,
            entry_id=entry_id,
            positive_points=positive_points,
            negative_points=negative_points,
            positive_message=positive_message,
            negative_message=negative_message,
        )

        if self.positive_message == "":
            self.positive_message = None
        if self.negative_message == "":
            self.negative_message = None

    def __str__(self) -> str:
        s = """
        Class: RegistryEntry
        key:            {}
        key_path:       {}
        entry_name:     {}
        default_value:  {}
        positive_value: {}
        negative_value: {}
        {}
        """.format(
            self.key,
            self.key_path,
            self.entry_name,
            self.default_value,
            self.positive_value,
            self.negative_value,
            super().__str__(),
        )

        return s


class Firewall(ScorableItem):
    def __init__(
        self,
        name: str,
        desired_state: bool,
        starting_state: bool,
        entry_id: int,
        positive_points: int,
        negative_points: int,
        positive_message: str = None,
        negative_message: str = None,
    ):
        self.name = name
        self.desired_state = desired_state
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
        Class: Firewall
        name:           {}
        desired_state:  {}
        starting_state: {}
        {}
        """.format(
            self.name, self.desired_state, self.starting_state, super().__str__()
        )
        return s


class Program(ScorableItem):
    def __init__(
        self,
        name: str,
        installed: bool,
        desired: bool,
        entry_id: int,
        positive_points: int,
        negative_points: int,
        positive_message: str = None,
        negative_message: str = None,
    ):
        self.name = name
        self.installed = installed
        self.desired = desired

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
        name:      {}
        installed: {}
        desired:   {}
        {}
        """.format(
            self.name, self.installed, self.desired, super().__str__()
        )
        return s
