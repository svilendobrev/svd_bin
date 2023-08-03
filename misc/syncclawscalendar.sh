#!/bin/sh
khal import --batch /home/svilen/.claws-mail/claws-mail.ics
vdirsyncer sync
