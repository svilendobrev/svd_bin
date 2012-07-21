#!/usr/bin/perl
while (<>) {
    $/=\1; print ord() if ord() < 32 && ord()!=9 && ord() !=10;
}
