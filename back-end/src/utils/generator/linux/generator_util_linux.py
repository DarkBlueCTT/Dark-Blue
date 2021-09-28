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
import pwd
import logging
from subprocess import check_call
from utils.generator.linux.generator_linux import LinuxGenerator
from utils.scoring_engine.shared.shared_util import File, ChallengeQuestion
from utils.scoring_engine.linux.scoring_engine_linux import (
    User,
    Process,
    Package,
    ConfigFile,
)


def create_users(generator: LinuxGenerator) -> None:
    print("Creating users...")
    logging.info("Creating users...")

    user_dict = {}

    # Build a dict that maps user names to user IDs.
    for u in pwd.getpwall():
        user_dict[u[0]] = u[2]

    user_list = user_dict.keys()

    for user in generator.data["users"]:
        logging.debug("Creating user: {}".format(user["name"]))

        if user["name"] in user_list:
            logging.warning("User '{}' already exists.".format(user["name"]))
            make_user_object(generator=generator, user=user)
            continue

        # Build command to create the user.
        command = (
            'sudo useradd -c "User created by Dark Blue CyberPatriot Training Tool" {}'
            .format(user["name"])
        )

        logging.debug(
            "Attempting to create user {} with command: {}".format(
                user["name"], command
            )
        )

        # Call the user creation command.
        result = check_call(command, shell=True)

        logging.debug(
            "Useradd command for user '{}' returned with exit code: {}".format(
                user["name"], result
            )
        )

        # Call should return 0 if successful.
        if result == 0:
            make_user_object(generator=generator, user=user)

            # Check to see if the user needs to be added to sudo, if so add them to the sudo group.
            if user["sudo_initial_state"]:
                command = "sudo usermod -aG sudo {}".format(user["name"])

                logging.debug(
                    "Attempting to add '{}' to sudoers with command: {}".format(
                        user["name"], command
                    )
                )

                # Call the command to add the user to sudo.
                result_sudo = check_call(command, shell=True)

                if result_sudo == 0:  # Return should be 0 if successful.
                    logging.debug(
                        "Successfully added '{}' to sudoers.".format(user["name"])
                    )
                else:
                    logging.error(
                        "Could not add user '{}' to sudo group.".format(user["name"])
                    )
                    generator.scoring_engine.register_generator_message(
                        message="Could not add user '{}' to sudo group.".format(
                            user["name"]
                        )
                    )

        else:  # User add call failed.
            logging.error(
                "Useradd command for user '{}' failed with error code: {}".format(
                    user["name"], result
                )
            )

            generator.scoring_engine.register_generator_message(
                message="Could not create user '{}'.".format(user["name"])
            )


def make_user_object(generator: LinuxGenerator, user: dict) -> None:

    if generator.generator_only:
        return

    user_id = pwd.getpwnam((user["name"])).pw_uid

    new_user = User(
        name=user["name"],
        allowed=user["allowed"],
        is_sudo=user["is_sudo"],
        sudo_initial_state=user["sudo_initial_state"],
        user_id=user_id,
        entry_id=generator.scoring_engine.request_scoring_id(),
        positive_points=user["positive_points"],
        negative_points=user["negative_points"],
    )

    generator.scoring_engine.users.append(new_user)


def create_question_files(generator: LinuxGenerator) -> None:
    logging.info("Creating challenge questions...")

    for file in generator.data["challenge_questions"]:
        path = os.path.join(os.environ["HOME"], "Desktop")
        path = os.path.join(path, file["name"])

        logging.debug(
            "Creating challenge question {} at path: {}".format(file["name"], path)
        )

        if os.path.exists(path):  # Nothing is done if the file already exists.
            logging.warning("Question file '{}' already exists.".format(file["name"]))
            make_question_file_object(generator=generator, file=file, path=path)
        else:  # Else create the file and write the contents as output.
            try:
                out_file = open(path, "w")
                out_file.write(generator.question_file_boilerplate)
                out_file.write(file["question_content"])
                out_file.close()
                make_question_file_object(generator=generator, file=file, path=path)
            except (FileNotFoundError, Exception) as e:
                logging.error(
                    "Could not create question file '{}'".format(file["name"])
                )
                logging.error("Error contents: {}".format(e))
                generator.scoring_engine.register_generator_message(
                    message="Could not create question file: {}".format(file["name"])
                )


def make_question_file_object(generator: LinuxGenerator, file: dict, path: str) -> None:
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


def create_filepaths(generator: LinuxGenerator) -> None:
    print("Creating filepaths...")
    logging.info("Creating filepaths...")

    if generator.scoring_only:
        for file in generator.data["files"]:
            make_file_object(generator=generator, file=file)
        return

    for file in generator.data["files"]:

        # Remove quotes from path if they somehow made it through.
        file["filepath"] = file["filepath"].strip("\"'")

        # TODO: Replace this with a regular expression.
        if file["filepath"][0:8] == "$DESKTOP":
            file["filepath"] = generator.expand_desktop_path(
                original_path=file["filepath"]
            )

        if file["create"]:
            if os.path.exists(file["filepath"]):
                logging.warning(
                    "File already exists at {}, skipping to prevent data loss.".format(
                        file["filepath"]
                    )
                )
                make_file_object(generator=generator, file=file)
            else:  # If there is no file, try to create it.
                try:
                    temp = open(file["filepath"], "w")
                    temp.close()
                    make_file_object(generator=generator, file=file)
                except (FileNotFoundError, NotADirectoryError):
                    logging.error(
                        "Could not create file at {} -- Attempting to generate missing"
                        " directories.".format(file["filepath"])
                    )

                    # Attempt to generate missing directories in filepath.
                    create_flag = make_directory_path(file["filepath"])

                    file["filepath"] = os.path.join(
                        os.environ["HOME"], file["filepath"]
                    )

                    if not create_flag:  # Generating directories still didn't work.
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
                    # The directories were generated successfully, try to
                    # create the file again.
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
        else:  # No create.
            make_file_object(generator=generator, file=file)


def make_directory_path(filepath: str) -> bool:
    # Get the end of the filepath.
    path = os.path.split(filepath)[0]
    logging.debug("Attempting to create path: {}".format(path))

    path = os.path.join(os.environ["HOME"], path)

    try:
        os.makedirs(path)
    except FileExistsError:
        logging.error("Path {} already exists, file will be skipped".format(path))
        return False

    return True


def make_file_object(generator: LinuxGenerator, file: str) -> None:
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


def create_processes(generator: LinuxGenerator) -> None:
    print("Creating processes...")
    logging.info("Creating processes...")

    if generator.scoring_only:
        for process in generator.data["processes"]:
            make_process_object(generator=generator, process=process)
        return

    for process in generator.data["processes"]:
        if process["create_dummy"]:
            # Create a dummy process that does nothing other than add an entry to ps.
            command = "perl -MPOSIX -e '$0=\"{}\"; pause' &".format(process["name"])

            result = check_call(command, shell=True)

            logging.debug(
                "Dummy process creation for process '{}' returned with code: {}".format(
                    process["name"], result
                )
            )
        make_process_object(generator=generator, process=process)


def make_process_object(generator: LinuxGenerator, process: str) -> None:
    if generator.generator_only:
        return

    new_process = Process(
        name=process["name"],
        default_state=process["default_state"],
        desired_state=process["desired_state"],
        entry_id=generator.scoring_engine.request_scoring_id(),
        positive_points=process["positive_points"],
        negative_points=process["negative_points"],
        positive_message=process["positive_message"],
        negative_message=process["negative_message"],
    )

    generator.scoring_engine.processes.append(new_process)


def configure_config_files(generator: LinuxGenerator) -> None:
    print("Configuring config files (proc interface)...")
    logging.info("Configuring config files (proc interface)...")

    if generator.scoring_only:
        for file in generator.data["config_files"]:
            make_config_file_object(generator=generator, file=file)
        return

    for file in generator.data["config_files"]:
        # Strip out quotes.
        file["filepath"] = file["filepath"].strip("\"'")

        if file["create"]:

            logging.debug(
                "Attempting to modify configuration file '{}' to default value {}"
                .format(file["filepath"], file["default_value"])
            )

            try:
                # This worked better than using open.
                command = "echo {} | sudo tee {}".format(
                    file["default_value"], file["filepath"]
                )
                result = check_call(command, shell=True)
                logging.debug(
                    "Modification of {} returned exit code {}".format(
                        file["filepath"], result
                    )
                )
                make_config_file_object(generator=generator, file=file)
            except FileNotFoundError:
                logging.error(
                    "Could not open configuration file at path: {}".format(
                        file["filepath"]
                    )
                )
            except IOError:
                logging.error(
                    "IOError occurred when modifying configuration file at path: {}"
                    .format(file["filepath"])
                )
            except Exception as e:
                logging.error(
                    "Error occurred when modifying configuration file at path: {}."
                    " Error: {}".format(file["filepath"], e)
                )

            try:  # Read the file afterwards to see if it changed.
                in_file = open(file["filepath"], "r")
                value = in_file.read().strip()

                if value != file["default_value"]:
                    logging.error(
                        "Could not modify configuration file at path: {}".format(
                            file["filepath"]
                        )
                    )
                    generator.scoring_engine.register_generator_message(
                        message="Could not read configuration file at path: {}".format(
                            file["filepath"]
                        )
                    )
                elif value == file["default_value"]:
                    logging.debug(
                        "Successfully modified config file at {}".format(
                            file["filepath"]
                        )
                    )
            except FileNotFoundError:
                pass

        else:
            make_config_file_object(generator=generator, file=file)


def make_config_file_object(generator: LinuxGenerator, file: str) -> None:
    if generator.generator_only:
        return

    new_file = ConfigFile(
        path=file["filepath"],
        default_value=file["default_value"],
        positive_value=file["positive_value"],
        negative_value=file["negative_value"],
        create=file["create"],
        entry_id=generator.scoring_engine.request_scoring_id(),
        positive_points=file["positive_points"],
        negative_points=file["negative_points"],
        positive_message=file["positive_message"],
        negative_message=file["negative_message"],
    )

    generator.scoring_engine.config_files.append(new_file)


def configure_packages(generator: LinuxGenerator) -> None:
    # No automatic configuration is done currently.
    print("Configuring packages...")
    logging.info("Configuring packages...")

    for package in generator.data["packages"]:
        make_package_object(generator=generator, package=package)


def make_package_object(generator: LinuxGenerator, package: str) -> None:
    if generator.generator_only:
        return

    new_package = Package(
        name=package["name"],
        installed=package["desired"],
        starting_state=package["installed"],
        entry_id=generator.scoring_engine.request_scoring_id(),
        positive_points=package["positive_points"],
        negative_points=package["negative_points"],
    )

    generator.scoring_engine.packages.append(new_package)
