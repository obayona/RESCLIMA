#ifndef _DATABASE_H
#define	_DATABASE_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <libpq-fe.h>
#include "datastructs.h"

Station ** getStations();
Variable ** getVariablesByAliases(char** variables_aliases,int n);
int insertMeasures(Measurements* m);

#endif	