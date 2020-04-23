#!/bin/bash
ffmpeg -framerate 1 -i render/%d.jpg -i audio.mp3 -c:a copy -shortest -c:v libx264 -pix_fmt yuv420p -r 25 test.mp4
