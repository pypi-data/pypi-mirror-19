###########################################################################
# Top30 is Copyright (C) 2016-2017 Kyle Robbertze <krobbertze@gmail.com>
#
# Top30 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# Top30 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Top30.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################
"""
Manages the settings that are used while running
"""
class Settings:
    """
    Holds the settings for the top30 module
    """
    #TODO: move to yaml file or similar
    song_length = 10 * 1000
    song_start_tag = "description"
    song_directory = "/home/kyle/projects/top30/db/songs"

    voice_start_overlap = 300
    voice_end_overlap = 1400
    voice_directory = "/home/kyle/projects/top30/db/voice"

    debug = False

class ConfigurationError(Exception):
    """
    Default config error class
    """
    pass
