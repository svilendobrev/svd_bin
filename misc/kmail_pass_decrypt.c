#include <stdio.h>
#include <stdlib.h>

typedef unsigned short WCHAR;

int wine_utf8_mbstowcs( int flags, const char *src, int srclen, WCHAR *dst, int dstlen );

int uniLen(WCHAR *foo)
{
    int i = 0;
    while (foo[i++]);
    return i;
}

void print_pass(char *pass)
{
    char *encPass = pass + 5;
    int encLen = strlen(encPass);
    unsigned short encUni[1024];
    int i;

    printf("pass=(%i)\n", encLen);

    wine_utf8_mbstowcs(0, encPass, encLen, encUni, sizeof(encUni));

    encLen = uniLen(encUni);

    for (i = 0; i < encLen; i++)
    {
        unsigned short enc = encUni[i];
        char c;

        if (enc < 0x20)
            enc = enc;
        else
            enc = 0x1001F - enc;

        c = enc & 0x00ff;
        printf("%c", c );
    }
    printf("\n");
}

int main(int argc, char **argv)
{
    FILE *confFile;
    char buf[1024];
    confFile = fopen(argv[1], "r");
    if (!confFile)
    {
        fprintf(stderr, "could not open config file '%s'\n", argv[1]);
        return EXIT_FAILURE;
    }
    while (fgets(buf, sizeof(buf), confFile))
    {
        if (strncmp(buf, "pass=", 5) == 0)
        {
            print_pass(buf);
        }
        else
        {
            printf("%s\n", buf);
        }
    }
    fclose(confFile);

    return EXIT_SUCCESS;
}

