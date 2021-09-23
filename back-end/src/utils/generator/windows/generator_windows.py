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

import logging
from os import environ
from os.path import join
from utils.generator.shared.shared_util_generator import Generator
from utils.scoring_engine.windows.util_windows import ScoringEngine


class WindowsGenerator(Generator):
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

        super().__init__(
            filepath=filepath,
            debug=debug,
            generator_only=generator_only,
            scoring_only=scoring_only,
            log_path=log_path,
            full_debug=full_debug,
            scoring_interval=scoring_interval,
            notifications=notifications,
        )

        self.initialize_data()

        self.scoring_engine = ScoringEngine(
            total_score=self.data["score"],
            scoring_interval=scoring_interval,
            debug=debug,
            debug_config=full_debug,
            notifications=notifications,
        )

        self.readme_path = join(self.scoring_engine.desktop_path, "readme.txt")

    def __str__(self) -> str:
        s = """
        Class: WindowsGenerator
        {}
        {}
        """.format(
            super().__str__(), self.scoring_engine.__str__()
        )
        return s

    def generate_image(self) -> None:
        from utils.generator.windows.generator_util_windows import (
            create_filepaths,
            create_question_files,
            create_users,
            configure_firewall,
            configure_registry,
            configure_services,
            configure_programs,
        )

        self.create_readme()
        create_filepaths(self)
        create_question_files(self)
        create_users(self)
        configure_registry(self)
        configure_services(self)
        configure_programs(self)
        configure_firewall(self)

    def expand_desktop_path(self, original_path: str) -> str:
        desktop_path = join(environ["USERPROFILE"], "Desktop")

        # TODO: Maybe using Regex grouping here instead.
        expanded_path = join(desktop_path, original_path[9:])

        return expanded_path
