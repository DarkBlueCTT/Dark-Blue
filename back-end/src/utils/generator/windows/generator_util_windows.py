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
import winreg
import logging
import subprocess
import win32net
import win32netcon
import win32security
from utils.generator.windows.generator_windows import WindowsGenerator
from utils.scoring_engine.shared.shared_util import File, ChallengeQuestion
from utils.scoring_engine.windows.scoring_engine_windows import (
    User,
    Firewall,
    RegistryEntry,
    Service,
    Program,
)


def create_question_files(generator: WindowsGenerator) -> None:

    print("Creating question files...")
    logging.info("Creating question files...")

    if generator.scoring_only:
        for file in generator.data["challenge_questions"]:
            path = os.path.join(os.environ["USERPROFILE"], "Desktop")
            path = os.path.join(path, file["name"] + ".txt")
            make_question_file_object(generator=generator, file=file, path=path)
        return

    for file in generator.data["challenge_questions"]:
        logging.debug("Creating challenge question: {}".format(file["name"]))
        path = os.path.join(os.environ["USERPROFILE"], "Desktop")
        path = os.path.join(path, file["name"] + ".txt")

        if os.path.exists(path):
            logging.warning("Question {} already exists. Skipping.".format(path))
            make_question_file_object(generator=generator, file=file, path=path)
        try:
            out_file = open(path, "w")
            out_file.write(file["question_content"])
            make_question_file_object(generator=generator, file=file, path=path)
        except FileNotFoundError:
            logging.error(
                "Could not create Question file {} at {}".format(file["name"], path)
            )
            generator.scoring_engine.register_generator_message(
                "Could not create question file: {}".format(file["name"])
            )


def make_question_file_object(
    generator: WindowsGenerator, file: dict, path: str
) -> None:

    if generator.generator_only:
        return

    new_file = ChallengeQuestion(
        name=file["name"],
        filepath=path,
        answer=file["answer"],
        entry_id=generator.scoring_engine.request_scoring_id(),
        positive_points=file["points"],
    )

    generator.scoring_engine.challenge_questions.append(new_file)


def create_filepaths(generator: WindowsGenerator) -> None:

    print("Creating filepaths...")
    logging.info("Creating filepaths...")

    if generator.scoring_only:
        for file in generator.data["files"]:
            make_file_object(generator=generator, file=file)
        return

    for file in generator.data["files"]:

        file["filepath"] = file["filepath"].strip("\"'")

        # TODO: Replace this with a better regex expression.
        if file["filepath"][0:8] == "$DESKTOP":
            file["filepath"] = generator.expand_desktop_path(
                original_path=file["filepath"]
            )

        if file["create"]:
            if os.path.exists(file["filepath"]):
                logging.warning(
                    (
                        "File already exists at {}, skipping to prevent data loss."
                    ).format(file["filepath"])
                )
                make_file_object(generator=generator, file=file)
            else:
                try:
                    temp = open(file["filepath"], "w")
                    temp.close()
                    make_file_object(generator=generator, file=file)
                except FileNotFoundError:
                    logging.error(
                        "Could not create file at {} -- Attempting to generate missing"
                        " directories.".format(file["filepath"])
                    )

                    create_flag = make_directory_path(file["filepath"])

                    if not create_flag:
                        logging.error(
                            "Could not create directory path to {}".format(
                                file["filepath"]
                            )
                        )

                        generator.scoring_engine.register_generator_message(
                            message="Could not create file at path: {}".format(
                                file["filepath"]
                            )
                        )

                        continue

                    else:
                        try:
                            temp = open(file["filepath"], "w")
                            temp.close()
                            make_file_object(generator=generator, file=file)
                        except FileNotFoundError:
                            logging.error(
                                "Could not create {} after creating directory path."
                                .format(file["filepath"])
                            )

                            generator.scoring_engine.register_generator_message(
                                message="Could not create file at path: {}".format(
                                    file["filepath"]
                                )
                            )
        else:
            make_file_object(generator=generator, file=file)


def make_directory_path(filepath: str) -> bool:
    path = os.path.split(filepath)[0]
    logging.debug("Attempting to create path: {}".format(path))

    try:
        os.makedirs(path)
    except FileExistsError:
        logging.error("Path {} already exists, file will be skipped.".format(filepath))
        return False

    return True


def make_file_object(generator: WindowsGenerator, file: dict) -> None:

    if generator.generator_only:
        return

    new_file = File(
        filepath=file["filepath"],
        exist=file["exist"],
        entry_id=generator.scoring_engine.request_scoring_id(),
        positive_points=file["positive_points"],
        negative_points=file["negative_points"],
    )

    generator.scoring_engine.files.append(new_file)


def create_users(generator: WindowsGenerator) -> None:
    print("Creating users...")
    logging.info("Creating users...")

    if generator.scoring_only:
        for user in generator.data["users"]:
            make_user_object(generator=generator, user=user)
        return

    for user in generator.data["users"]:

        user_info = dict(
            name=user["name"],
            priv=win32netcon.USER_PRIV_USER,
            home_dir=None,
            comment="User generated by the Dark Blue CyberPatriot Training Tool",
            flags=win32netcon.UF_NORMAL_ACCOUNT | win32netcon.UF_SCRIPT,
            script_path=None,
        )

        try:
            logging.debug("Creating user: {}".format(user["name"]))

            win32net.NetUserAdd(None, 1, user_info)
            user_group_info = {"domainandname": user["name"]}

            if user["admin_initial_state"]:
                logging.debug(
                    "Attempting to add user '{}' to Administrators group.".format(
                        user["name"]
                    )
                )
                win32net.NetLocalGroupAddMembers(
                    None, "Administrators", 3, [user_group_info]
                )

            logging.debug("Attempting to add user '{}' to Users.".format(user["name"]))
            win32net.NetLocalGroupAddMembers(None, "Users", 3, [user_group_info])

            make_user_object(generator=generator, user=user)

        except win32net.error as error:
            number, _, _ = error.args

            if number == 2224:
                logging.warning(
                    "User '{}' already exists. Creating user object for the user."
                    .format(user["name"])
                )

                make_user_object(generator=generator, user=user)

            logging.warning("Error creating user '{}': {}".format(user["name"], error))


def query_user_sid(user_name: str) -> int:
    server = None

    for group in ["Users", "Administrators"]:
        member_data, _, _ = win32net.NetLocalGroupGetMembers(server, group, 2, 0)

        for user in member_data:
            t_sid = win32security.ConvertSidToStringSid(user["sid"])

            name, _, _ = win32security.LookupAccountSid(None, user["sid"])

            if name == user_name:
                return t_sid

    return -1


def make_user_object(generator: WindowsGenerator, user: dict) -> None:
    if generator.generator_only:
        return

    sid = query_user_sid(user_name=user["name"])

    user["user_id"] = sid

    if sid == -1:
        generator.scoring_engine.register_generator_message(
            message="Could not find SID for user '{}'.".format(user["name"])
        )

    new_user = User(
        name=user["name"],
        allowed=user["allowed"],
        is_admin=user["is_admin"],
        admin_initial_state=user["admin_initial_state"],
        user_id=user["user_id"],
        entry_id=generator.scoring_engine.request_scoring_id(),
        positive_points=user["positive_points"],
        negative_points=user["negative_points"],
    )

    generator.scoring_engine.users.append(new_user)


def configure_firewall(generator: WindowsGenerator) -> None:

    print("Configuring firewall profiles...(this may take a while to actually apply)")
    logging.info("Configuring firewall profiles...")

    if generator.scoring_only:
        for firewall in generator.data["firewall"]:
            make_firewall_object(generator=generator, firewall=firewall)
        return

    firewall_status_list = []

    # Returns in order: Domain, Private, Public.
    result = subprocess.getoutput("netsh advfirewall show allprofiles state")

    for entry in result.split()[5::6]:
        if entry == "ON":
            firewall_status_list.append(True)
        elif entry == "OFF":
            firewall_status_list.append(False)

    status_dict = {
        "domain": firewall_status_list[0],
        "private": firewall_status_list[1],
        "public": firewall_status_list[2],
    }

    for firewall in generator.data["firewall"]:
        # Enable profile
        if not status_dict[firewall["name"]] and firewall["starting_state"]:
            command = (
                "powershell.exe Set-NetFirewallProfile -Profile {} -Enabled True"
                .format(firewall["name"])
            )

            ret = subprocess.Popen(command)

            if ret.returncode != 0:
                logging.warning(
                    "Subprocess call to enable firewall profile {} returned with"
                    " non-zero exit code: {}".format(firewall["name"], ret.returncode)
                )

                generator.scoring_engine.register_generator_message(
                    message="Could not enable {} firewall profile".format(
                        firewall["name"]
                    )
                )

        # Disable profile
        if status_dict[firewall["name"]] and not firewall["starting_state"]:
            command = (
                "powershell.exe Set-NetFirewallProfile -Profile {} -Enabled False"
                .format(firewall["name"])
            )

            ret = subprocess.Popen(command)

            if ret.returncode != 0:
                logging.warning(
                    "Subprocess call to disable firewall profile {} returned with"
                    " non-zero exit code: {}".format(firewall["name"], ret.returncode)
                )

                # Temporarily remove this because using a non-blocking method means the
                # return code isn't available yet.

                # generator.scoring_engine.register_generator_message(
                #     message="Could not disable {} firewall profile.".format(
                #         firewall["name"]
                #     )
                # )

        make_firewall_object(generator=generator, firewall=firewall)


def make_firewall_object(generator: WindowsGenerator, firewall: dict) -> None:
    if generator.generator_only:
        return

    new_firewall = Firewall(
        name=firewall["name"],
        desired_state=firewall["desired_state"],
        starting_state=firewall["starting_state"],
        entry_id=generator.scoring_engine.request_scoring_id(),
        positive_points=firewall["positive_points"],
        negative_points=firewall["negative_points"],
    )

    generator.scoring_engine.firewall.append(new_firewall)


def configure_registry(generator: WindowsGenerator) -> None:

    print("Configuring registry entries...")
    logging.info("Configuring registry entries...")

    if generator.scoring_only:
        for entry in generator.data["registry"]:
            make_registry_object(generator=generator, entry=entry)
        return

    try:
        registry_hklm = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        registry_hkcu = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    except OSError:
        logging.critical(
            "Could not connect to registry. Registry configuration will be skipped."
        )

        generator.scoring_engine.register_config_message(
            message="Could not connect to registry. Registry configuration was skipped."
        )
        return

    for entry in generator.data["registry"]:

        registry = None
        key = None

        if entry["key"] == "HKEY_LOCAL_MACHINE":
            registry = registry_hklm
            key = winreg.HKEY_LOCAL_MACHINE
        elif entry["key"] == "HKEY_CURRENT_USER":
            registry = registry_hkcu
            key = winreg.HKEY_CURRENT_USER

        # if create
        if entry["create"]:
            #   Check to see if it exists
            exists = check_registry_key(entry)

            logging.debug(
                "Attempting to create/modify registry key: {}  Exists: {}".format(
                    entry["entry_name"], exists
                )
            )

            if exists:
                try:
                    key = winreg.OpenKey(
                        registry, entry["key_path"], 0, winreg.KEY_ALL_ACCESS
                    )

                    value = winreg.QueryValueEx(key, entry["entry_name"])
                    key_type = value[1]
                    winreg.SetValueEx(
                        key, entry["entry_name"], 0, key_type, entry["default_value"]
                    )

                except ValueError:
                    try:
                        winreg.SetValueEx(
                            key,
                            entry["entry_name"],
                            0,
                            key_type,
                            int(entry["default_value"]),
                        )
                    except (TypeError, FileNotFoundError, WindowsError) as e:
                        logging.error(
                            "Error occurred when modifying registry key: {}. Error: {}"
                            .format(entry["entry_name"], e.args)
                        )
                except (TypeError, FileNotFoundError, WindowsError) as e:
                    logging.error(
                        "Error occurred when modifying registry key: {}. Error: {}"
                        .format(entry["entry_name"], e.args)
                    )

                value = winreg.QueryValueEx(key, entry["entry_name"])[0]

                if (
                    value == entry["default_value"]
                    or value == int(entry["default_value"], 10)
                    or value == int(entry["default_value"], 16)
                ):
                    logging.debug(
                        "Successfully modified value of '{}' to '{}'".format(
                            entry["entry_name"], entry["default_value"]
                        )
                    )
                else:
                    logging.warning(
                        "Failed to modify value of '{}' to '{}'".format(
                            entry["entry_name"], entry["default_value"]
                        )
                    )

                    generator.scoring_engine.register_generator_message(
                        message=(
                            "Failed to set default value of '{}' for registry key '{}'"
                            .format(entry["default_value"], entry["entry_name"])
                        )
                    )

                make_registry_object(generator=generator, entry=entry)

            else:
                winreg.CreateKey(key, entry["key_path"])

                open_key = winreg.OpenKey(
                    key, entry["key_path"], 0, winreg.KEY_ALL_ACCESS
                )

                winreg.SetValueEx(
                    open_key,
                    entry["entry_name"],
                    0,
                    winreg.REG_SZ,
                    entry["default_value"],
                )

                winreg.CloseKey(open_key)

                make_registry_object(generator=generator, entry=entry)
        else:  # No create
            make_registry_object(generator=generator, entry=entry)


def check_registry_key(entry: dict) -> bool:
    registry = None

    if entry["key"] == "HKEY_LOCAL_MACHINE":
        registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    elif entry["key"] == "HKEY_CURRENT_USER":
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)

    if registry is None:
        return False

    key = None

    try:
        key = winreg.OpenKey(registry, entry["key_path"])
        _ = winreg.QueryValueEx(key, entry["entry_name"])

    except FileNotFoundError:
        return False

    if key is not None:
        return True

    return False


def make_registry_object(generator: WindowsGenerator, entry: dict) -> None:
    if generator.generator_only:
        return

    new_entry = RegistryEntry(
        key=entry["key"],
        key_path=entry["key_path"],
        entry_name=entry["entry_name"],
        default_value=entry["default_value"],
        positive_value=entry["positive_value"],
        negative_value=entry["negative_value"],
        entry_id=generator.scoring_engine.request_scoring_id(),
        positive_points=entry["positive_points"],
        negative_points=entry["negative_points"],
        positive_message=entry["positive_message"],
        negative_message=entry["negative_message"],
    )

    generator.scoring_engine.registry_entries.append(new_entry)


def configure_services(generator: WindowsGenerator) -> None:

    print("Configuring services...")
    logging.info("Configuring services...")

    try:
        generator.data["services"]
    except KeyError:
        logging.warning(
            "Services field is not detected. Service configuration will be skipped."
        )
        generator.scoring_engine.register_generator_message(
            message="Services field was not found. Services were not configured."
        )

    for service in generator.data["services"]:
        make_service_object(generator=generator, service=service)


def make_service_object(generator: WindowsGenerator, service: dict) -> None:
    if generator.generator_only:
        return

    new_service = Service(
        name=service["name"],
        common_name=service["common_name"],
        default_state=service["default_state"],
        desired_state=service["desired_state"],
        startup_state=service["startup_state"],
        desired_startup_state=service["desired_startup_state"],
        entry_id=generator.scoring_engine.request_scoring_id(),
        positive_points=service["positive_points"],
        negative_points=service["negative_points"],
        positive_message=service["positive_message"],
        negative_message=service["negative_message"],
    )

    generator.scoring_engine.services.append(new_service)


def configure_programs(generator: WindowsGenerator) -> None:

    print("Configuring programs...")
    logging.info("Configuring programs...")

    try:
        generator.data["programs"]
    except KeyError:
        logging.warning(
            "Programs field is not detected. programs configuration will be skipped."
        )
        generator.scoring_engine.register_generator_message(
            message="Programs field was not found. programs were not configured."
        )

    for program in generator.data["programs"]:
        make_programs_object(generator=generator, program=program)


def make_programs_object(generator: WindowsGenerator, program: dict) -> None:
    if generator.generator_only:
        return

    new_program = Program(
        name=program["name"],
        installed=program["installed"],
        desired=program["desired"],
        entry_id=generator.scoring_engine.request_scoring_id(),
        positive_points=program["positive_points"],
        negative_points=program["negative_points"],
    )

    generator.scoring_engine.programs.append(new_program)
