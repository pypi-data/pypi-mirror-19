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
Creates rundowns from a chart
"""
from top30.settings import Settings
from top30.chart import Chart

from mutagen.oggvorbis import OggVorbis
from pydub import AudioSegment

class Top30Creator:
    """
    Class for creating rundowns from a start to stop
    """
    def __init__(self, chart_file, last_week):
        self.voice_begin_overlap = Settings.voice_start_overlap
        self.voice_end_overlap = Settings.voice_end_overlap
        self.song_length = Settings.song_length
        self.chart = Chart(chart_file)
        self.last_week = Chart(last_week)

    def create_rundown(self, start, end, is_last_week):
        """
        Creates a rundown from start to end (both inclusive). If there is a
        directory that is added to the file paths and the intro/outro names.
        """
        voice_dir = Settings.voice_directory
        prefix = ""
        current_chart = self.chart
        if is_last_week:
            prefix = "last-week_" # Intro/outro handling
            current_chart = self.last_week

        intro = "%s/%s%02d-%02d_intro.ogg" % (voice_dir, prefix, start, end)
        rundown = get_start(intro)
        song_file = current_chart.get(start, 'path')
        rundown = self.add_song(song_file, rundown)

        for i in range(start - 1, end - 1, -1):
            voice_file = voice_dir + "/" + str(i) + ".ogg"
            rundown = self.add_voice(voice_file, rundown)
            song_file = current_chart.get(i, 'path')
            rundown = self.add_song(song_file, rundown)

        outro = "%s/%s%02d-%02d_outro.ogg" % (voice_dir, prefix, start, end)
        rundown = add_end(outro, rundown)
        rundown_name = "rundown-%s%02d-%02d" % (prefix, start, end)
        export(rundown_name, "mp3", rundown)

    def add_voice(self, voice_file, rundown):
        """
        Adds a voice segment to the rundown
        """
        voice = AudioSegment.from_ogg(voice_file)
        rundown = rundown.overlay(voice[:self.voice_begin_overlap],
                                  position=-self.voice_begin_overlap)
        return rundown.append(voice[self.voice_begin_overlap:],
                              crossfade=0.5*1000)

    def add_song(self, song_file, rundown):
        """
        Adds a song segment to the rundown
        """
        start_time = get_start_time(song_file)

        song = AudioSegment.from_ogg(song_file)
        song = song[start_time:start_time + self.song_length]
        song = song.overlay(rundown[-self.voice_end_overlap:])
        return rundown[:-self.voice_end_overlap].append(song, crossfade=0)

    def get_song_length(self):
        """
        Returns the length of the song segment set in the config file
        """
        return self.song_length

    def get_voice_begin_overlap(self):
        """
        Returns the length of the voice overlap set in the config file
        """
        return self.voice_begin_overlap

    def get_voice_end_overlap(self):
        """
        Returns the length of the voice overlap set in the config file
        """
        return self.voice_end_overlap

    def set_song_length(self, song_length):
        """
        Sets the length of the song segment set in the config file
        """
        self.song_length = song_length

    def set_voice_begin_overlap(self, voice_begin_overlap):
        """
        Sets the length of the voice overlap set in the config file
        """
        self.voice_begin_overlap = voice_begin_overlap

    def set_voice_end_overlap(self, voice_end_overlap):
        """
        Sets the length of the voice overlap set in the config file
        """
        self.voice_end_overlap = voice_end_overlap

def get_start_time(filename):
    """
    Returns the start time of song segment in miliseconds. This is read
    from the file's metadata
    """
    song_meta = OggVorbis(filename).tags
    tag = Settings.song_start_tag.lower()
    try:
        time_code = song_meta[tag][0]
    except KeyError:
        time_code = song_meta['comment'][0]
    song_length = float(time_code.split(':')[0]) * 60 + \
                  float(time_code.split(':')[1])
    song_length *= 1000
    return song_length


def get_start(filename):
    """
    Returns the intro voice segment
    """
    return AudioSegment.from_ogg(filename)

def add_end(filename, rundown):
    """
    Adds the outro voice segment
    """
    outro = AudioSegment.from_ogg(filename)
    return rundown.append(outro, crossfade=0)

def export(filename, file_type, rundown):
    """
    Exports the rundown as an audio file
    """
    if not filename.endswith("." + file_type):
        filename = filename + "." + file_type
    rundown.export(filename, format=file_type)
