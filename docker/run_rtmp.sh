#!/usr/bin/env bash

cd /ps102_multistreamer/ || exit 1
cd rtsp-server || exit 1
./rtsp-simple-server rtsp-simple-server.yml
