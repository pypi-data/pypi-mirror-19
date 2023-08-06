#!/bin/sh
echo "Stopping Alignak backend..."
kill -SIGTERM `cat /tmp/alignak-backend.pid`
sleep 1
echo "Stopped"
