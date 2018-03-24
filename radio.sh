#!/bin/bash

sender=$1
sender_url=$( head -n "${sender}" radios.txt | tail -n 1 )
mplayer "${sender_url}" > /dev/null

