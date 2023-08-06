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
Runs the Rundown creator
"""
import argparse
from datetime import date
from datetime import timedelta

from top30.handlers import UserInterface
from top30.top_30_creator import Top30Creator
from top30.settings import Settings

SETTINGS = Settings()

def main():
    """
    Main function. Runs the program
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("chart", help="chart to create the rundowns from")
    parser.add_argument("-p", "--previous", help="the previous chart")
    parser.add_argument("-g", "--gui", help="run the graphical version of Top30",
                        action="store_true")
    args = parser.parse_args()
    if args.previous != None:
        previous = args.previous
    else:
        current_date = args.chart[-15:-5].split("-")
        current = date(int(current_date[0]), int(current_date[1]),
                       int(current_date[2]))
        previous_date = current - timedelta(days=7)
        previous = args.chart[:-len("YYYY-MM-DD.docx")] + \
                previous_date.isoformat() + ".docx"

    if args.gui:
        gui = UserInterface()
        gui.run(args.chart, previous)
    else:
        creator = Top30Creator(args.chart, previous)
        print("Creating 30 - 21 rundown...")
        creator.create_rundown(30, 21, "")
        print("Creating 20 - 11 rundown...")
        creator.create_rundown(20, 11, "")
        print("Creating 10 - 2 rundown...")
        creator.create_rundown(10, 2, "")
        print("Creating last week's 10 - 1 rundown...")
        creator.create_rundown(10, 1, "last-week")
