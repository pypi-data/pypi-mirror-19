#!/bin/sh
echo "Stopping Alignak WebUI..."
kill -SIGTERM `cat /tmp/alignak-webui.pid`
sleep 1
echo "Stopped"
