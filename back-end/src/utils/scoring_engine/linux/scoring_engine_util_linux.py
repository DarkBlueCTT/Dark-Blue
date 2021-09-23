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

import pwd
import psutil
import logging
import subprocess

from utils.scoring_engine.linux.scoring_engine_linux import (
    ScoringEngine,
    User,
    Process,
    Package,
    ConfigFile,
)


def score_users(scoring_engine: ScoringEngine) -> None:

    logging.info("Scoring users...")

    sudoers = []
    user_dict = {}
    user_list = []

    for u in pwd.getpwall():
        user_dict[u[0]] = u[2]

    user_list = user_dict.keys()

    output = subprocess.check_output(
        "grep '^sudo:.*$' /etc/group | cut -d: -f4", shell=True
    ).decode("utf-8")

    for user in output.split(","):
        sudoers.append(user.strip())

    user: User
    for user in scoring_engine.users:
        # User is not in list.
        if user.name not in user_list:
            m = "User '{}' has been removed.".format(user.name)
            # User is not allowed.

            if user.allowed:
                scoring_engine.remove_points(item=user, message=m)

            elif not user.allowed:
                scoring_engine.award_points(item=user, message=m)

        # Else if user is in list.
        elif user.name in user_list:

            # User is allowed, check their ID.
            if user.allowed and user.user_id != user_dict[user.name]:
                scoring_engine.remove_points(
                    item=user, message="User '{}' has been removed.".format(user.name)
                )
            # User is not allowed. Check to see if user created them.
            elif not user.allowed and user.user_id != user_dict[user.name]:
                scoring_engine.remove_points(
                    item=user, message="User '{}' has been created.".format(user.name)
                )

        # Check admin status
        if user.name in sudoers:
            # User needed to be given sudo.
            if user.allowed and user.is_sudo and not user.sudo_initial_state:
                scoring_engine.award_points(
                    item=user,
                    message="User '{}' is in the sudoers group.".format(user.name),
                )

            # User needed sudo removed.
            if not user.is_sudo and not user.sudo_initial_state:
                scoring_engine.remove_points(
                    item=user,
                    message="User '{}' is in the sudoers group.".format(user.name),
                )

        elif user.name not in sudoers:
            # User needed sudo removed.
            if user.allowed and not user.is_sudo and user.sudo_initial_state:
                scoring_engine.award_points(
                    item=user,
                    message="User '{}' is not in the sudoers group.".format(user.name),
                )

            # User sudo permission removed.
            if user.allowed and user.is_sudo and user.sudo_initial_state:
                scoring_engine.remove_points(
                    item=user,
                    message="User '{}' is not in the sudoers group.".format(user.name),
                )


def score_processes(scoring_engine: ScoringEngine) -> None:

    logging.info("Scoring processes...")

    processes = psutil.process_iter()

    process_list = []

    for p in processes:
        process_list.append(p.name())

    process: Process
    for process in scoring_engine.processes:
        logging.debug("Scoring process '{}'".format(process.name))

        logging.debug(
            "TEMP DEBUG: process '{}' Desired: {} Default: {}".format(
                process.name, process.desired_state, process.default_state
            )
        )

        # Process is running
        if process.name in process_list:

            logging.debug(
                "TEMP DEBUG: process '{}' was found running.".format(process.name)
            )

            # Process should be running. (award)
            if not process.default_state and process.desired_state:
                scoring_engine.award_points(
                    item=process,
                    message="Process '{}' has been started.".format(process.name),
                )

            # Process should be stopped. (remove)
            if not process.default_state and not process.desired_state:
                scoring_engine.remove_points(
                    item=process,
                    message="Process '{}' has been started.".format(process.name),
                )

        # Else process is not running
        elif process.name not in process_list:

            logging.debug(
                "TEMP DEBUG: process '{}' is not running.".format(process.name)
            )

            # Process should be running. (remove)
            if process.default_state and process.desired_state:
                scoring_engine.remove_points(
                    item=process,
                    message="Process '{}' has been stopped.".format(process.name),
                )

            # Process should be stopped. (award)
            if process.default_state and not process.desired_state:
                scoring_engine.award_points(
                    item=process,
                    message="Process '{}' has been stopped.".format(process.name),
                )


def score_packages(scoring_engine: ScoringEngine) -> None:
    logging.info("Scoring packages...")

    package: Package
    for package in scoring_engine.packages:
        # The awk command is included as it is because it needed to be a raw string.
        # This was easier than fixing the problem.
        command = "dpkg -l | grep {} | {}".format(package.name, r"awk '{print $2}'")

        logging.debug(
            "Searching for package '{}' with command: {}".format(package.name, command)
        )

        result = subprocess.check_output(command, shell=True).decode("utf-8").split()

        found = False

        if package.name in result:
            found = True

        if found:
            # Package needed to be installed.
            if package.installed and not package.starting_state:
                scoring_engine.award_points(
                    item=package,
                    message="Package '{}' is installed.".format(package.name),
                )

            # Package was wrongfully installed.
            if not package.installed and not package.starting_state:
                scoring_engine.remove_points(
                    item=package,
                    message="Package '{}' was installed.".format(package.name),
                )

        elif not found:
            # Package was wrongfully uninstalled.
            if package.installed and package.starting_state:
                scoring_engine.remove_points(
                    item=package,
                    message="Package '{}' was uninstalled.".format(package.name),
                )

            # Package needed to be uninstalled.
            if not package.installed and package.starting_state:
                scoring_engine.award_points(
                    item=package,
                    message="Package '{}' was uninstalled.".format(package.name),
                )


def score_config_files(scoring_engine: ScoringEngine) -> None:
    logging.info("Scoring configuration files...")

    file: ConfigFile
    for file in scoring_engine.config_files:

        content = None
        logging.debug(
            "TEMP DEBUG: Scoring configuration file at '{}'".format(file.path)
        )

        try:
            in_file = open(file.path, "r")
            content = in_file.read().strip()
            in_file.close()
        except FileNotFoundError:
            logging.warning(
                "Could not open configuration file at '{}'".format(file.path)
            )
        except IOError:
            logging.error(
                "IOError occurred when reading file at path '{}'".format(file.path)
            )
        except Exception as e:
            logging.error(
                "An error occurred while reading configuration file '{}'. Error: {}"
                .format(file.path, e)
            )

        if content is not None:
            logging.debug("Content: {} Filepath: {}".format(content, file.path))

            if content == file.default_value:
                logging.debug(
                    "Content from file at path '{}' matches default value. Content: {}"
                    " Default: {}".format(file.path, content, file.default_value)
                )

            if content == file.positive_value:
                scoring_engine.award_points(
                    item=file,
                    message="'{}' matches positive value: {}".format(
                        file.path, file.positive_value
                    ),
                )
            elif content == file.negative_value:
                scoring_engine.remove_points(
                    item=file,
                    message="'{}' matches negative value: {}".format(
                        file.path, file.negative_value
                    ),
                )
        elif content is None:
            logging.error(
                "No content was read from file at path '{}'".format(file.path)
            )
