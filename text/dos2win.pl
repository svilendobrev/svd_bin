#!/usr/bin/perl
while (<>) { y/\200-\277\300-\377/\300-\377\200-\277/; print; }
