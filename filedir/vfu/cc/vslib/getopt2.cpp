/*
 *  $Header: /cvs/vslib/getopt2.cpp,v 1.2 2001/10/28 13:53:02 cade Exp $
 *
 *  Copyright (C) 1994 Arno Schaefer
 *
 *  AU: Auswertung der Kommandozeile, der POSIX-Version von getopt ()
 *  nachempfunden.
 *
 *  PO: ANSI C
 */

/*
 * Changed by <cade@biscom.net> on 12.march.1998,12.feb.2000:
 * when reach non option string return `+' w. optarg set to this string
 * instead of return `-1'
 * Changed code marked `+++ cade +++' and end w. `=== cade ==='
 *
 * $Id: getopt2.cpp,v 1.2 2001/10/28 13:53:02 cade Exp $
 *
 */

#include <stdio.h>
#include <string.h>

#include "getopt2.h"


/* Globale Variablen */

char *optarg;
int optind = 1;
int opterr = 1;
int optopt;
int optc = '?';
int opt_use_slash = 0;
int opterr_report = 1;

static char *nextarg = NULL;


/* Funktion */

int getopt2(int argc, char *argv[], char *optstring)

/*
 *  AU: Auswertung der Kommandozeile
 *
 *  VB: argc und argv sind die Parameter, die an main () uebergeben werden.
 *  optstring ist ein String, der die Zeichen enthaelt, die als
 *  Optionen erkannt werden. Wenn ein Zeichen von einem Doppelpunkt
 *  gefolgt wird, hat die Option ein Argument, das direkt auf das Zeichen
 *  folgt oder durch Space davon getrennt ist. Gueltige Optionszeichen
 *  sind alle druckbaren Zeichen ausser '?', ' ' und ':'.
 *
 *  optind ist der Index auf das naechste Element von argv[], das
 *  bearbeitet wird.
 *
 *  opterr ist ein Flag, das festlegt, ob bei Fehlern Fehlermeldungen
 *  ausgegeben werden.
 *
 *  optarg ist ein Zeiger auf das Argument, wenn eine Option ein
 *  Argument hat.
 *
 *  optopt enthaelt bei Fehlern das Optionszeichen, das den Fehler aus-
 *  geloest hat.
 *
 *  NB: Rueckgabewert ist das jeweils naechste Optionszeichen, oder -1 am
 *  Ende der Optionsliste.
 *
 *  Die Optionsliste ist zu Ende, wenn argv[optind] NULL ist, oder
 *  argv[optind] nicht mit '-' (oder '/') beginnt, oder argv[optind]
 *  ein einzelnes "-" ist. In diesem Fall wird optind nicht erhoeht.
 *  Das Ende der Optionsliste kann mit "--" erzwungen werden, dann ist
 *  argv[optind] das erste Argument nach "--".
 *
 *  FB: Ein '?' wird zurueckgegeben, wenn ein Optionszeichen nicht in
 *  optstring enthalten war oder ein ungueltiges Optionszeichen
 *  uebergeben wurde ('?' oder ':'). Ausserdem bei einem fehlenden
 *  Argument, wenn das erste Zeichen von optstring kein ':' ist.
 *
 *  Ein ':' wird zurueckgegeben bei einem fehlenden Argument, wenn
 *  das erste Zeichen von optstring ein ':' ist.
 */

{
    char *search;

    optarg = NULL;

    if (nextarg == NULL)
    {
        nextarg = argv[optind];

        if (nextarg == NULL)
        {
            return (-1);
        }

        if (*nextarg != '-')
        {
            /* +++ cade +++ */
            optarg = nextarg;
            nextarg = NULL;
            optind++;
            return('+');
            /* === cade === */
            /* return (-1); // this is the original code */
        }

        nextarg++;

    } /* if */

    optopt = *nextarg++;

    if (optopt == 0)
    {
        return (-1);
    }

    optind++;

    if (optopt == '-' && *nextarg == 0)
    {
        return (-1);
    }

    if (optopt == ':' || optopt == '?')
    {
        if (opterr)
        {
          if (opterr_report)
            fprintf
            (
                stderr,
                "%s: illegal option -- %c\n",
                argv[0],
                optopt
            );
        }

        return ('?');

    } /* if */

    search = strchr (optstring, optopt);

    if (search == NULL)
    {
        if (opterr)
        {
          if (opterr_report)
            fprintf
            (
                stderr,
                "%s: illegal option -- %c\n",
                argv[0],
                optopt
            );
        }
        return ('?');
    } /* if */

    if (*nextarg == 0)
    {
        nextarg = NULL;
    }

    if (search[1] != ':')
    {
        if (nextarg != NULL)
        {
            optind--;
        }

        return (optopt);
    }

    if (nextarg != NULL)
    {
        optarg = nextarg;
        nextarg = NULL;
        return (optopt);
    }

    optarg = argv[optind];

    if (optind == argc)
    {
        if (opterr)
        {
          if (opterr_report)
            fprintf
            (
                stderr,
                "%s: option requires an argument -- %c\n",
                argv[0],
                optopt
            );
        } /* if */

        if (optstring[0] == ':')
        {
            return (':');
        }
        else
        {
            return ('?');
        }

    } /* if */

    else
    {
        optind++;
    }

    return (optopt);

} /* getopt () */
