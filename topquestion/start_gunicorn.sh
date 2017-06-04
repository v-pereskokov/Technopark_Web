#!/bin/sh

CONF=$1
APP=$2
ROOT=/var/www/topquestion

cd $ROOT
exec gunicorn -c $ROOT/topquestion/$CONF --bind localhost:8081 topquestion.$APP:application

