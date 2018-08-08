#include "database.h"


Station ** getStations(){
    Station ** stations = NULL;
    PGconn *conn = PQconnectdb("user=obayona password=EloyEcuador93 dbname=resclima");

    if (PQstatus(conn) == CONNECTION_BAD) {
        fprintf(stderr, "Connection to database failed: %s\n",
            PQerrorMessage(conn));
    	PQfinish(conn);
    }
    char * query = "SELECT s.id,s.token "
                   "FROM \"TimeSeries_station\" as s, "  
                   "\"TimeSeries_stationtype\" as st "
                   "WHERE st.brand='BloomSky' and st.model='SKY2' "
                    "and \"stationType_id\"=st.id";

    PGresult *res = PQexec(conn,query);    
    
    if (PQresultStatus(res) != PGRES_TUPLES_OK) {
        printf("No data retrieved\n");        
        PQclear(res);
    	PQfinish(conn);
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