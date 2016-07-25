#!/bin/bash -xue

# Sync files with amazon s3 bucket using aws command line tool

DEST=m.mr-pc.org/ismir16
SRC=2016_Proceedings_ISMIR_Electronic

[ -f $SRC.zip ] && mv $SRC.zip $SRC
aws s3 sync $SRC/ s3://$DEST --grants read=uri=http://acs.amazonaws.com/groups/global/AllUsers
[ -f $SRC/$SRC.zip ] && mv $SRC/$SRC.zip .
