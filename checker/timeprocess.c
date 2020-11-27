// Time Stamp Processor

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
typedef unsigned int ui;
typedef struct Behavior {
    int time;
    ui pc;
    int dst;
    ui addr;
    ui data;
}Behavior;

#define GETS_LIM 10000
bool my_gets(char *dest, FILE *fp) {
    char c = 0, *p = dest;
    int cnt = 0;
    while ((c = fgetc(fp)) != EOF && c != '\n' && cnt < GETS_LIM)
        *(p++) = c, cnt++;
    *p = 0;
    if (c == EOF && p == dest) return false;
    while ((*(p - 1)) == '\r' || (*(p - 1)) == '\n')
        *(--p) = 0;
    return true;
}

bool parseLine(const char *src, Behavior *beh) {
    const char *p = src;
    while (*p != 0 && !(*p >= '0' && *p <= '9') && (*p != '@'))
        p++;
    Behavior tmp;
    if (*p == '@') {
        tmp.time = -1;
        int sc1 = sscanf(p, "@%x: $%d <= %x", &tmp.pc, &tmp.addr, &tmp.data);
        int sc2 = sscanf(p, "@%x: *%x <= %x", &tmp.pc, &tmp.addr, &tmp.data);
        if (sc1 != 3 && sc2 != 3) {
            return false;
        }
        else if (sc1 == 3) {
            tmp.dst = 0;
            *beh = tmp;
            return true;
        }
        else {
            tmp.dst = 1;
            *beh = tmp;
            return true;
        }
    }
    else {
        int sc1 = sscanf(p, "%d@%x: $%d <= %x", &tmp.time, &tmp.pc, &tmp.addr, &tmp.data);
        int sc2 = sscanf(p, "%d@%x: *%x <= %x", &tmp.time, &tmp.pc, &tmp.addr, &tmp.data);
        if (sc1 != 4 && sc2 != 4) {
            return false;
        }
        else if (sc1 == 4) {
            tmp.dst = 0;
            *beh = tmp;
            return true;
        }
        else {
            tmp.dst = 1;
            *beh = tmp;
            return true;
        }
    }
}

void dispBehavior(const Behavior *b) {
    if (b->time != -1)
        printf("%d", b->time);
    if (b->dst == 0) {
        printf("@%08x: $%2d <= %08x", b->pc, b->addr, b->data);
    }
    else {
        printf("@%08x: *%08x <= %08x", b->pc, b->addr, b->data);
    }
}

bool nextValidLine(Behavior *beh, FILE *fp) {
    char line[GETS_LIM + 5];
    bool flg = true;
    // Behavior tmp = {0, 0, 0, 0, 0};
    while (1) {
        flg = my_gets(line, fp);
        if (flg == 0) 
            return false;
        flg = parseLine(line, beh);
        if (!flg)
            continue;
        else 
            return true;
    }
}

int curr_time = -1;
Behavior currb;
Behavior curr_grf, curr_dm;
int has_grf = 0, has_dm = 0;

int main()
{
    bool flg = true;
    while ((flg = nextValidLine(&currb, stdin))) {
        if (currb.time == -1) {
            dispBehavior(&currb);
            printf("\n");
        }
        else {
            if (currb.time == curr_time) {
                if (currb.dst == 0) {
                    if (!has_grf) {
                        has_grf = 1;
                        curr_grf = currb;
                    }
                }
                else {
                    if (!has_dm) {
                        has_dm = 1;
                        curr_dm = currb;
                    }
                }
            }
            else {
                if (has_grf) {
                    dispBehavior(&curr_grf);
                    printf("\n");
                    has_grf = 0;
                }
                if (has_dm) {
                    dispBehavior(&curr_dm);
                    printf("\n");
                    has_dm = 0;
                }
                if (currb.dst == 0) {
                    if (!has_grf) {
                        has_grf = 1;
                        curr_grf = currb;
                    }
                }
                else {
                    if (!has_dm) {
                        has_dm = 1;
                        curr_dm = currb;
                    }
                }
                curr_time = currb.time;
            }
        }
    }

    return 0;
}