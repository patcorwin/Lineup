'''
Aligns multiple cursors to a the minimum column width according to your tab settings. ex:

    start = 1
    end = 32
    range_offset = 54
    health = 4

Selecting '=' turns into:

    start       = 1
    end         = 32
    range_offset= 54
    health      = 4


Future improvement: Utilize rowcol() to ensure there aren't overlapping cursors in a line.
'''
import sublime_plugin

import math
from collections import namedtuple

Info = namedtuple( 'Info', 'text line_region sel start offset' )


class LineupCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        lines = []
        offsets = []

        indent = self.view.settings().get('tab_size')

        # Gather the position of all the cursors
        for region in self.view.sel():
            
            line_region = self.view.line(region)

            start = min(region.a, region.b)

            offset = start - line_region.a
            lines.append( Info(self.view.substr(line_region), line_region, region, start, offset) )
            offsets.append(offset)

        depth = math.ceil( max(offsets) / float(indent) ) * indent

        # Insert text to align, in reverse so I don't need to worry about an insertion altering the following line.
        for line in reversed(lines):
            head = line.text[:line.offset]
            tail = line.text[line.offset:]

            newline = head + ' ' * (depth - line.offset) + tail

            self.view.replace(edit, line.line_region, newline)

    # This ALSO preserves the selection, which is exactly what I want!