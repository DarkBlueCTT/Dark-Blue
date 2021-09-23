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
import ctypes
import pickle
import logging
from sys import exit
from argparse import ArgumentParser, Namespace


def init_argparse() -> ArgumentParser:
    parser = ArgumentParser(
        description=(
            "Allows for command line configuration of the Dark Blue generator and"
            " scoring engine."
        )
    )

    parser.add_argument(
        "-f", "--filepath", type=str, help="Path to Dark Blue JSON file."
    )

    parser.add_argument(
        "-c",
        "--command-line",
        help=(
            "(Not implemented, GUI in progress) Set generator and scoring engine to"
            " run in command-line only mode instead of GUI mode."
        ),
        action="store_true",
    )

    parser.add_argument(
        "-s",
        "--scoring-only",
        help=(
            "Do not run the generator, instead only configure and run the scoring"
            " engine."
        ),
        action="store_true",
    )

    parser.add_argument(
        "-g",
        "--generator-only",
        help=(
            "The generator will run without configuring or running the scoring engine."
        ),
        action="store_true",
    )

    parser.add_argument(
        "-d",
        "--debug",
        help="Enables debug logging output for generator and scoring engine.",
        action="store_true",
    )

    parser.add_argument(
        "-v",
        "--full-debug",
        help=(
            "(Not implemented) Scoring engine will write the configuration of each"
            " object to the HTML scoring report"
        ),
        action="store_true",
    )

    parser.add_argument(
        "-l",
        "--log",
        type=str,
        help="Path to where the log file will be written.",
    )

    parser.add_argument(
        "-i", "--interval", type=int, help="Length of scoring engine interval."
    )

    parser.add_argument(
        "-n",
        "--notifications",
        help="Disables notifications. Notifications are enabled by default.",
        action="store_false",
    )

    parser.add_argument(
        "-r",
        "--resume",
        help="Resumes scoring a saved scoring engine image.",
        action="store_true",
    )

    return parser


def init_generator_windows(args: Namespace):
    from utils.generator.windows.generator_windows import WindowsGenerator

    scoring_interval = 30

    if args.interval is not None:
        scoring_interval = args.interval

    generator = WindowsGenerator(
        filepath=args.filepath,
        debug=args.debug,
        generator_only=args.generator_only,
        scoring_only=args.scoring_only,
        log_path=args.log,
        full_debug=args.full_debug,
        scoring_interval=scoring_interval,
        notifications=args.notifications,
    )

    return generator


def init_generator_linux(args: Namespace):
    from utils.generator.linux.generator_linux import LinuxGenerator

    scoring_interval = 30

    if args.interval is not None:
        scoring_interval = args.interval

    generator = LinuxGenerator(
        filepath=args.filepath,
        debug=args.debug,
        generator_only=args.generator_only,
        scoring_only=args.scoring_only,
        log_path=args.log,
        full_debug=args.full_debug,
        scoring_interval=scoring_interval,
        notifications=args.notifications,
    )

    return generator


def check_arguments(args: Namespace) -> True:
    if args.filepath is None and not args.scoring_only and not args.resume:
        print("Please specify path to a Dark Blue JSON configuration file.")
        return False

    return True


def data_warning() -> bool:

    print(
        "\nWARNING: READ THE FOLLOWING CAREFULLY.\n\nRunning the generator MAY RESULT"
        " IN LOSS OF DATA OR OPERATING SYSTEM FUNCTIONALITY.\nBy using the Dark Blue"
        " CyberPatriot Training Tool, you assume full risk for the use of the tool as"
        " specified in the license agreement.\nDark Blue SHOULD ONLY BE USED ON VIRTUAL"
        " MACHINES created for the purpose of training.\n"
    )

    response = input(
        "\nPlease verify you have read the above, and understand that any data on this"
        " current system may be destroyed by entering yes or no [y/N]: "
    )

    if response.lower() in ["yes", "y", "accept", "ok", "okay"]:
        return True
    else:
        return False


def resume_scoring():

    print("Attempting to resume scoring engine from saved image...")

    saved_path = None

    if os.name == "nt":
        saved_path = os.path.join(os.environ["LOCALAPPDATA"], "DarkBlue")
    elif os.name == "posix":
        saved_path = os.path.join(os.environ["HOME"], ".darkblue")

    if os.path.exists(saved_path):
        scoring_engine_path = os.path.join(saved_path, "dark_blue_scoring_engine.dat")

        if os.path.exists(scoring_engine_path):

            try:
                with open(scoring_engine_path, "rb") as input_file:
                    scoring_engine = pickle.load(input_file)

                    if scoring_engine is not None:
                        scoring_engine.start()
            except Exception as e:
                logging.critical(
                    "Could not resume scoring engine. Error message: {}".format(e)
                )
                print(
                    "Error: Could not resume scoring engine.\nError during resume: {}"
                    .format(e)
                )
                exit(-10)


def initialize_logger(args: Namespace) -> None:
    # Defaults for log level and log path.
    log_path = "darkblue.log"
    log_level = 20

    # Initialize logger to specified path if the logging flag is set.
    if args.log is not None and args.log != "":
        log_path = args.log

    if args.debug:
        log_level = 10

    try:
        logging.basicConfig(
            filename=log_path,
            level=log_level,
            filemode="w",
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
    except FileNotFoundError:
        print(
            "\nERROR: Could not start logger with the specified path: {}".format(
                log_path
            )
        )
        print(
            "Logging currently can't create missing directories in the path, so any"
            " directories may have to be created manually."
        )
        print(
            "Logger will initialize using the default path in the same directory as the"
            " Dark Blue executable."
        )

        logging.basicConfig(
            filename="darkblue.log",
            level=log_level,
            filemode="w",
            format="%(asctime)s - %(levelname)s - %(message)s",
        )


def main():
    parser = init_argparse()
    args = parser.parse_args()

    valid = check_arguments(args=args)
    initialize_logger(args=args)

    if not valid:
        exit(-1)

    if not args.scoring_only and not args.resume and os.name == "nt":
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

        if not is_admin:
            print(
                "\nPlease run Dark Blue from an Administrator prompt. The generator"
                " requires administrative privileges.\n"
            )
            exit(-1)

    if args.command_line and not args.scoring_only and not args.resume:
        acknowledgement = data_warning()

        if not acknowledgement:
            print("Exiting...")
            exit(-2)

    if not args.resume:
        generator = None

        if os.name == "nt":
            generator = init_generator_windows(args=args)
        elif os.name == "posix":
            generator = init_generator_linux(args=args)

        if generator is None:
            print("Generator could not be initialized.")
            exit(-20)

        if args.full_debug:
            print(generator)

        generator.generate_image()

        generator.scoring_engine.start()
    elif args.resume:
        resume_scoring()


if __name__ == "__main__":
    main()
