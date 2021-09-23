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

import psutil
import winreg
import logging
import win32net
import subprocess
import win32security
from utils.scoring_engine.windows.scoring_engine_windows import (
    Firewall,
    RegistryEntry,
    ScoringEngine,
    Service,
    User,
    Program,
)


def score_users(
    scoring_engine: ScoringEngine, unit_test=False, users_test=None, admins_test=None
) -> None:
    logging.debug("Scoring users...")

    # Check to make sure we have some users in the list.
    if len(scoring_engine.users) == 0:
        logging.critical("User list is empty. Could not score users.")
        return

    # Get a list of all of the users on the system.
    user_dict = {}  # Dictionary which maps the user name to their SID.

    # List which will just contain the names of admin users.
    administrators = []

    if not unit_test:
        user_dict, administrators = get_users()
    if unit_test and users_test is not None and admins_test is not None:
        user_dict = users_test
        administrators = admins_test
    elif unit_test and (users_test is None or admins_test is None):
        return

    logging.debug("User dict: {}".format(user_dict))
    logging.debug("Administrators: {}".format(administrators))

    if len(user_dict) == 0:
        logging.critical("Could not enumerate any users on the system.")
        return

    if len(administrators) == 0:
        logging.warning(
            "Warning: No administrators could be found on the system. Either there are "
            "                none or an error occurred."
        )

    user_list = list(user_dict.keys())

    logging.debug("User list: {}".format(user_list))

    # Iterate over every user in the user list.
    user: User

    for user in scoring_engine.users:

        # User is not in list.
        if user.name not in user_list:
            # User is allowed, remove points.
            m = "User '{}' has been removed.".format(user.name)
            if user.allowed:
                scoring_engine.remove_points(item=user, message=m)
                continue  # We probably don't need to score admin status.

            # User is not allowed, award points.
            elif not user.allowed:
                scoring_engine.award_points(item=user, message=m)
                continue

        # Else user is in the list.
        elif user.name in user_list:
            # User is allowed, but they've been deleted and re-added and therefore have
            # a different SID.
            if user.allowed and user.user_id != user_dict[user.name]:
                m = "User '{}' has been removed.".format(user.name)
                scoring_engine.remove_points(item=user, message=m)

            # User is not allowed, check to see if the user has created them.
            if not user.allowed and user.user_id != user_dict[user.name]:
                m = "User '{}' has been created.".format(user.name)
                scoring_engine.remove_points(item=user, message=m)

        #   Check admin status.
        if user.name in administrators:
            # Award - User needed to be given admin permissions.
            if user.allowed and user.is_admin and not user.admin_initial_state:
                m = "User '{}' is now an administrator.".format(user.name)
                scoring_engine.award_points(item=user, message=m)

            # Remove - User has been given admin permissions.
            if user.allowed and not user.is_admin and not user.admin_initial_state:
                m = "User '{}' is now an administrator.".format(user.name)
                scoring_engine.remove_points(item=user, message=m)

        elif user.name not in administrators:
            # Award - User's admin permissions removed.
            if user.allowed and not user.is_admin and user.admin_initial_state:
                m = "User '{}' is not an administrator.".format(user.name)
                scoring_engine.award_points(item=user, message=m)

            # Remove - User's admin permissions removed.
            if user.allowed and user.is_admin and user.admin_initial_state:
                m = "User '{}' is not an administrator.".format(user.name)
                scoring_engine.remove_points(item=user, message=m)


def get_users() -> tuple[dict, list]:
    user_dict = {}
    administrators = []

    group_list = ["Users", "Administrators"]

    for group in group_list:
        member_data, _, _ = win32net.NetLocalGroupGetMembers(None, group, 2, 0)

        for user in member_data:
            t_sid = win32security.ConvertSidToStringSid(user["sid"])

            name, _, _ = win32security.LookupAccountSid(None, user["sid"])

            user_dict[name] = t_sid

            if group == "Administrators":
                administrators.append(name)

    return user_dict, administrators


def score_programs(scoring_engine: ScoringEngine) -> None:

    logging.debug("Scoring installed programs...")

    installed_programs = get_programs()

    logging.debug("Installed programs: {}".format(installed_programs))

    program: Program
    for program in scoring_engine.programs:

        if program.name in installed_programs:
            # User must install program.
            m = "'{}' is now installed.".format(program.name)
            if not program.installed and program.desired:
                scoring_engine.award_points(item=program, message=m)

        else:
            m = "'{}' is not installed.".format(program.name)
            # User must uninstall program.
            if program.installed and not program.desired:
                scoring_engine.award_points(item=program, message=m)

            # User has falsely uninstalled program.
            if program.installed and program.desired:
                scoring_engine.remove_points(item=program, message=m)


def get_programs() -> list:

    installed_programs = []
    names = []

    keypath = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
    registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)

    key = winreg.OpenKey(registry, keypath)
    i = 0

    while True:
        try:
            subkey = winreg.EnumKey(key, i)
            names.append(subkey)
            i += 1
        except OSError:
            break

    for entry in names:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, keypath + "\\" + entry)
            try:
                value = winreg.QueryValueEx(key, "DisplayName")
                installed_programs.append(value[0])
            except FileNotFoundError:
                pass
        except FileNotFoundError:
            pass

    return installed_programs


def score_services(scoring_engine: ScoringEngine) -> None:

    logging.debug("Scoring services...")

    service: Service
    for service in scoring_engine.services:
        try:
            result = psutil.win_service_get(service.name)
        except psutil.NoSuchProcess:
            logging.warning("Service {} was not found.".format(service.name))

        if result is not None:

            # Service is not running.
            if result.status() == "stopped":
                logging.debug("Service {} is stopped.".format(service.name))

                m = "Service '{}' is stopped.".format(service.name)

                # Service must be stopped.
                if (
                    service.desired_state == "stopped"
                    and service.default_state == "running"
                ):
                    scoring_engine.award_points(item=service, message=m)

                # Service is falsely stopped.
                if (
                    service.desired_state == "running"
                    and service.default_state == "running"
                ):
                    scoring_engine.remove_points(item=service, message=m)

            # Service is running.
            elif result.status() == "running":
                m = "Service '{}' is running.".format(service.name)
                # Service must be started.
                if service.desired_state and not service.startup_state:
                    scoring_engine.award_points(item=service, message=m)

                # Service is falsely started.
                if not service.desired_state and not service.startup_state:
                    scoring_engine.remove_points(item=service, message=m)

            # Else service is ???.
            else:
                logging.warning(
                    "Service '{}' is in an unknown state.".format(service.name)
                )


def score_registry_entries(scoring_engine: ScoringEngine) -> None:

    logging.debug("Scoring registry entries...")

    try:
        registry_hklm = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        registry_hkcu = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    except OSError:
        logging.critical(
            "Could not connect to registry. Registry scoring will be skipped."
        )
        scoring_engine.register_config_message(
            message="Could not connect to registry. Registry was not scored."
        )
        return

    entry: RegistryEntry
    for entry in scoring_engine.registry_entries:
        key = None

        if entry.key == "HKEY_LOCAL_MACHINE":
            try:
                key = winreg.OpenKey(registry_hklm, entry.key_path)
            except FileNotFoundError:
                logging.error(
                    "Could not locate keypath: {} in HKEY_LOCAL_MACHINE.".format(
                        entry.key_path
                    )
                )

        elif entry.key == "HKEY_CURRENT_USER":
            try:
                key = winreg.OpenKey(registry_hkcu, entry.key_path)
            except FileNotFoundError:
                logging.error(
                    "Could not locate keypath: {} in HKEY_LOCAL_MACHINE.".format(
                        entry.key_path
                    )
                )

        if key is not None:
            value = None

            try:
                value = winreg.QueryValueEx(key, entry.entry_name)[0]
            except FileNotFoundError:
                logging.error(
                    "Could not find registry key {} in {}\\{}".format(
                        entry.entry_name, entry.key, entry.key_path
                    )
                )

            dec_value = hex_value = None

            try:
                dec_value = int(entry.positive_value, base=10)
                hex_value = int(entry.positive_value, base=16)
            except ValueError:
                pass
            except TypeError:
                pass

            # Matches positive value in some form.
            if (
                value == entry.positive_value
                or value == dec_value
                or value == hex_value
            ):

                scoring_engine.award_points(
                    item=entry,
                    message=(
                        "Registry entry {} matches positive value '{}' in either str,"
                        " dec, or hex mode.".format(
                            entry.entry_name, entry.positive_value
                        )
                    ),
                )

            try:
                dec_value = int(entry.negative_value, base=10)
                hex_value = int(entry.negative_value, base=16)
            except ValueError:
                pass
            except TypeError:
                pass

            if (
                value == entry.negative_value
                or value == dec_value
                or value == hex_value
            ):

                scoring_engine.remove_points(
                    item=entry,
                    message=(
                        "Registry entry '{}' matches negative value {} in either str,"
                        " dec, or hex mode.".format(
                            entry.entry_name, entry.negative_value
                        )
                    ),
                )

            # Checking for the default case is just for debugging and
            # doesn't award points.
            # This could likely just be removed in the future if desired.
            try:
                dec_value = int(entry.default_value, base=10)
                hex_value = int(entry.default_value, base=16)
            except ValueError:
                pass
            except TypeError:
                pass

            if (
                value == entry.default_value
                or dec_value == entry.default_value
                or hex_value == entry.default_value
            ):
                logging.debug(
                    "{} value matches default value '{}' in str, hex, "
                    " or dec form.".format(entry.entry_name, entry.default_value)
                )


def score_firewall(
    scoring_engine: ScoringEngine, unit_test: bool = False, test_dict: dict = None
) -> None:

    logging.debug("Scoring firewall profiles...")

    firewall_dict = {}
    firewall_status_list = []
    firewall_list = ["domain", "private", "public"]

    result = subprocess.getoutput("netsh advfirewall show allprofiles state")
    split_result = result.split()

    for entry in split_result[5::6]:
        firewall_status_list.append(entry)

    for index, item in enumerate(firewall_status_list):
        status = None
        if item == "ON":
            status = True
        elif item == "OFF":
            status = False

        firewall_dict[firewall_list[index]] = status

    if unit_test:
        firewall_dict = test_dict

    firewall: Firewall
    for firewall in scoring_engine.firewall:

        # Gain points -- Firewall is enabled.
        if (
            firewall_dict[firewall.name]
            and not firewall.starting_state
            and firewall.desired_state
        ):
            scoring_engine.award_points(
                item=firewall,
                message="{} firewall profile is now enabled.".format(
                    firewall.name.capitalize()
                ),
            )

        # Lose points -- Firewall is disabled.
        elif (
            not firewall_dict[firewall.name]
            and firewall.starting_state
            and firewall.desired_state
        ):
            scoring_engine.remove_points(
                item=firewall,
                message="{} firewall profile is now disabled.".format(
                    firewall.name.capitalize()
                ),
            )
