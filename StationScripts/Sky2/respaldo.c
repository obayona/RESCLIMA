#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libpq-fe.h>
#include <curl/curl.h>

// gcc -o sk2Adapter sky2Adapter.c -I/usr/include/postgresql -I/usr/local/include -L/usr/local/lib -lcurl -lpq
// tdbDpM7ktbTRos6iv3C76dQ=

void do_exit(PGconn *conn) {
    
    PQfinish(conn);
    exit(1);
}

typedef struct Station{
    int id;
    char * token;
}Station;

struct MemoryStruct {
  char *memory;
  size_t size;
};


Station ** getStations(){
    Station ** stations = NULL;
    PGconn *conn = PQconnectdb("user=obayona password=EloyEcuador93 dbname=resclima");

    if (PQstatus(conn) == CONNECTION_BAD) {
        
        fprintf(stderr, "Connection to database failed: %s\n",
            PQerrorMessage(conn));
        do_exit(conn);
    }
    char * query = "SELECT s.id,s.token "
                   "FROM \"TimeSeries_station\" as s, "  
                   "\"TimeSeries_stationtype\" as st "
                   "WHERE st.brand='BloomSky' and st.model='SKY2' "
                    "and \"stationType_id\"=st.id";
    printf("%s\n",query);

    PGresult *res = PQexec(conn,query);    
    
    if (PQresultStatus(res) != PGRES_TUPLES_OK) {

        printf("No data retrieved\n");        
        PQclear(res);
        do_exit(conn);
    }   
    
    int rows = PQntuples(res);
    printf("%d\n",rows);
    
    if(rows>0){
        int size = (sizeof(Station*))*(rows+1);
        stations = (Station**)malloc(size);
    }

    for(int i=0; i<rows; i++) {
        int idStation = atoi(PQgetvalue(res, i, 0)); 
        char * token  = PQgetvalue(res, i, 1);
        Station* station = (Station*)malloc(sizeof(Station));
        station->id = idStation;
        station->token = token;
        stations[i] = station;
    }
    stations[rows]=NULL;        

    PQclear(res);
    PQfinish(conn);

    return stations;
}


static size_t WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp)
{
  size_t realsize = size * nmemb;
  struct MemoryStruct *mem = (struct MemoryStruct *)userp;
 
  mem->memory = realloc(mem->memory, mem->size + realsize + 1);
  if(mem->memory == NULL) {
    /* out of memory! */ 
    printf("not enough memory (realloc returned NULL)\n");
    return 0;
  }
 
  memcpy(&(mem->memory[mem->size]), contents, realsize);
  mem->size += realsize;
  mem->memory[mem->size] = 0;
 
  return realsize;
}

int getMeasurements(char* token){
    CURL *curl;
    CURLcode res;
    char * url = "https://api.bloomsky.com/api/skydata/.?unit=intl";
    struct MemoryStruct chunk;
    chunk.memory = malloc(1);
    chunk.size = 0;


    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url);
        struct curl_slist *list = NULL;
        int header_size = (sizeof(char))*(strlen(token)+15);
        char * header = (char*)malloc(header_size);
        sprintf(header,"Authorization: %s",token);
        list = curl_slist_append(list, header); 
        curl_easy_setopt(curl,CURLOPT_HTTPHEADER,list);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);
        curl_easy_setopt(curl, CURLOPT_USERAGENT, "libcurl-agent/1.0");
        res = curl_easy_perform(curl);

        if(res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n",curl_easy_strerror(res));
        
        printf("%d\n %s\n",(int)chunk.size,chunk.memory);
        curl_easy_cleanup(curl);
        return 0;
    }
    curl_easy_cleanup(curl);
    return -1;
}

int main() {
    
    Station ** stations = getStations();
    Station ** iter = stations;
    char token[30];
    while(*iter!=NULL) {
        Station * station = *iter;
        strcpy(token,station->token);
        printf("**%s\n", token);
        getMeasurements(token);
        iter++;
    }


    return 0;
}