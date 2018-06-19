#include <stdio.h>
#include <stdlib.h>
#include <libpq-fe.h>

// gcc -o sk2Adapter sky2Adapter.c -I/usr/include/postgresql -lpq
// tdbDpM7ktbTRos6iv3c76dQ=

void do_exit(PGconn *conn) {
    
    PQfinish(conn);
    exit(1);
}

typedef struct Station{
    int id;
    char * token;
}Station;


Station * getStations(){
    Station * stations = NULL;
    PGconn *conn = PQconnectdb("user=resclima password=resclima dbname=resclima");

    if (PQstatus(conn) == CONNECTION_BAD) {
        
        fprintf(stderr, "Connection to database failed: %s\n",
            PQerrorMessage(conn));
        do_exit(conn);
    }
    
    PGresult *res = PQexec(conn, "SELECT * FROM \"TimeSeries_station\"");    
    
    if (PQresultStatus(res) != PGRES_TUPLES_OK) {

        printf("No data retrieved\n");        
        PQclear(res);
        do_exit(conn);
    }   
    
    int rows = PQntuples(res);
    
    if(rows>0){
        stations = (Station*)malloc(sizeof(Station)*rows);
    }

    for(int i=0; i<rows; i++) {
        
        Station station;
        station.id = 12;
        station.token = "El token";

        stations[i] = station;
        printf("%s %s %s\n", PQgetvalue(res, i, 0), 
            PQgetvalue(res, i, 1), PQgetvalue(res, i, 2));
    }

    for(int i=0; i<rows; i++) {

        Station station = stations[i];
        printf("%d %s\n", station.id, station.token);
    }        

    PQclear(res);
    PQfinish(conn);


    return stations;

}


int main() {
    
    Station * stations = getStations();

    return 0;
}