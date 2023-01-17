
#############################################################################
# Copyright (C) 2023 CrowdWare
#
# This file is part of FlatSiteBuilder.
#
#  FlatSiteBuilder is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  FlatSiteBuilder is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with FlatSiteBuilder.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
import os


class Generator:
    install_directory = ""

    def __init__(self):
        self.content = ""
        self.output_dir = ""

    @staticmethod
    def themesPath():
        return os.path.join(Generator.install_directory, "themes")

    def generateSite(self, win, site, content_to_build = None):
        self.site = site
        self.output_dir = site.output
        site_dir = os.path.join(site.source_path, self.output_dir)