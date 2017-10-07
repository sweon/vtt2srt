#!/usr/bin/python3
# -*- coding: utf-8 -*-

import glob
import re
import os

vtt_pathname = './*.en.vtt'
vtt_filenames = glob.glob(vtt_pathname)

if vtt_filenames:
    regc = re.compile(r"(\d{2}:\d{2}:\d{2})\.(\d{3}\s+)-->(\s+\d{2}:\d{2}:\d{2})\.(\d{3}\s*)")
    for vtt_filename in vtt_filenames:
        vttfile = open(vtt_filename, 'r')
        srtfile = open(vtt_filename.replace('.en.vtt', '.srt'), 'w')

        linenum = 1
        timeline = False
        lines_so_far = 0
        for line in vttfile:
            match = re.search(regc, line)
            if match or timeline:
                if not timeline:
                    srtfile.write("%d\n" % linenum)
                    linenum += 1
                    lines_so_far += 1
                timeline = True
                if match:
                    line = match.group(1) + ',' + match.group(2) + '-->' + match.group(3) + ',' + match.group(4).strip() + '\n'
                srtfile.write(line)
                lines_so_far += 1
                if len(line.strip()) == 0:
                    timeline = False
                    for i in range(4 - lines_so_far):
                        srtfile.write("\n")
                    lines_so_far = 0

        vttfile.close()
        srtfile.close()

        try:
            os.remove(vtt_filename)
        except OSError:
            pass
