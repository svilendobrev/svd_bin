#!/bin/bash
djpeg $1 | pnmgamma $2 > `basename $1 .jpg`.light.pnm

