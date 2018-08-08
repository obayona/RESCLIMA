#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <jansson.h>
#include "station.h"
#include "database.h"
#include "request.h"



// gcc -o sk2Adapter sky2Adapter.c database.c request.c -I/usr/include/postgresql -I/usr/local/include -L/usr/local/lib -lcurl -lpq -ljansson
// tdbDpM7ktbTRos6iv3C76dQ=

//curl-7.61.0
//jansson-2.11

char* parseMeasurements(char* data_json){
    json_t* source, *measurements, *value, *result;
    json_error_t error;


    //source = json_loads(data_json,0,&error);
    source = json_load_file("result.txt",0,&error);
    source = json_array_get(source,0);
    
    result = json_object();

    value = json_object_get(source,"UTC");
    json_object_set_new(result,"UTC",value);
    measurements = json_object_get(source,"Data");

    char variables[3][50];
    strcpy(variables[0],"Luminance");
    strcpy(variables[1],"Temperature");
    strcpy(variables[2],"Humidity"); 
    int i=0;
    for(i=0;i<3;i++){
        char * variable = variables[i];
        value = json_object_get(measurements,variable);
        json_object_set(result,variable,value);    
    }
    json_dump_file(result,"data.json",0);
    json_decref(source);
    return NULL;

}


int main() {
    
    Station ** stations = getStations();
    Station ** iter = stations;
    char token[30];
    while(*iter!=NULL) {
        Station * station = *iter;
        strcpy(token,station->token);
        printf("**%s\n", token);
        //char * data = getSKY2Data(token);
        char * data = "eloy";
        parseMeasurements(data);
        iter++;
    }


    return 0;
}