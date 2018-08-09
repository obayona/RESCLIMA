#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <curl/curl.h>
#include <jansson.h>
#include "datastructs.h"
#include "database.h"
#include "request.h"



// gcc -o sk2Adapter sky2Adapter.c database.c request.c -I/usr/include/postgresql -I/usr/local/include -L/usr/local/lib -lcurl -lpq -ljansson
// tdbDpM7ktbTRos6iv3C76dQ=

//curl-7.61.0
//jansson-2.11

Measurements* parseMeasurements(int idStation,char* data_json, Variable** variables){
    json_t* source, *measurements, *object, *result;
    json_error_t error;


    source = json_loads(data_json,0,&error);
    //source = json_load_file("result.txt",0,&error);
    source = json_array_get(source,0);
    
    result = json_object();

    measurements = json_object_get(source,"Data");

    object = json_object_get(measurements,"TS");
    const time_t utc_time = (const time_t)json_integer_value(object);
    struct tm * utc_tm = gmtime(&utc_time); 
    char * datetime_str = (char*)malloc(sizeof(char)*20);
    strftime(datetime_str,20,"%Y-%m-%d %H:%M:%S",utc_tm);
    printf("La fecha %s",datetime_str);
    
    Variable** iter = variables;
    while(*iter){
        Variable* variable = *iter;
        char * id = variable->id;
        char * alias = variable->alias;
        char * datatype = variable->datatype;
        object = json_object_get(measurements,alias);
        json_object_set(result,id,object); 
        iter++;
    }


    char* values_str = json_dumps(result,0);
    json_decref(source);

    Measurements* m = (Measurements*)malloc(sizeof(Measurements));
    m->idStation = idStation;
    m->datetime = datetime_str;
    m->values = values_str;

    return m;

}


int main() {
    char *variables_aliases[3]={'\0'};
    variables_aliases[0]="Luminance";
    variables_aliases[1]="Temperature";
    variables_aliases[2]="Humidity";

    Variable ** variables = getVariablesByAliases(variables_aliases,3);

    char token[30];

    Station ** stations = getStations();
    Station ** iter = stations;
    while(*iter!=NULL) {
        Station * station = *iter;
        strcpy(token,station->token);
        int idStation = station->id;
        char * data = getSKY2Data(token);
        //char * data = "eloy";
        Measurements* m = parseMeasurements(idStation,data,variables);
        //printf("**%d %s** %s",m->idStation,m->datetime,m->values);
        insertMeasures(m);
        iter++;
    }


    return 0;
}