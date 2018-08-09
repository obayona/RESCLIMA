#include "database.h"


Station ** getStations(){
    Station ** stations = NULL;
    PGconn *conn = PQconnectdb("user=obayona password=EloyEcuador93 dbname=resclima");

    if (PQstatus(conn) == CONNECTION_BAD) {
        fprintf(stderr, "Connection to database failed: %s\n",
            PQerrorMessage(conn));
    	PQfinish(conn);
    }
    char * query = "SELECT s.id,s.token,s.frequency "
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
    
    if(rows>0){
        int size = (sizeof(Station*))*(rows+1);
        stations = (Station**)malloc(size);
    }

    for(int i=0; i<rows; i++) {
        int idStation = atoi(PQgetvalue(res, i, 0)); 
        char * token  = PQgetvalue(res, i, 1);
        float frequency = atof(PQgetvalue(res, i, 2));
        Station* station = (Station*)malloc(sizeof(Station));
        station->id = idStation;
        station->token = token;
        station->frequency = frequency;
        stations[i] = station;
    }
    stations[rows]=NULL;        

    PQclear(res);
    PQfinish(conn);

    return stations;
}


//
Variable * _getVariableByAlias(char* variable_alias){
	
	PGconn *conn = PQconnectdb("user=obayona password=EloyEcuador93 dbname=resclima");

    if (PQstatus(conn) == CONNECTION_BAD) {
        fprintf(stderr, "Connection to database failed: %s\n",
            PQerrorMessage(conn));
    	PQfinish(conn);
    }
    char * query = "SELECT v.id,v.alias,v.datatype "
                   "FROM \"TimeSeries_variable\" as v "  
                   "WHERE v.alias=$1";

    const char *values[2] = {variable_alias};
    int lengths[1] = {strlen(variable_alias)};
    int binary[1] = {0};

    PGresult *res = PQexecParams(conn,query,1,NULL,values,lengths,binary,0);
    
    if (PQresultStatus(res) != PGRES_TUPLES_OK) {
        printf("No data retrieved\n");        
        PQclear(res);
    	PQfinish(conn);
    }   
    
    int rows = PQntuples(res);
    
    if(rows<=0){
        return NULL;
    }
    Variable* variable = (Variable*)malloc(sizeof(Variable));
    char * id = (char*)malloc(sizeof(char)*50);
    strcpy(id,PQgetvalue(res, 0, 0));
    variable->id = id;
    char * alias = (char*)malloc(sizeof(char)*50);
    strcpy(alias,PQgetvalue(res, 0, 1));
    variable->alias = alias;
     char * datatype = (char*)malloc(sizeof(char)*20);
    strcpy(datatype,PQgetvalue(res, 0, 2));
    variable->datatype = datatype;
    PQclear(res);
    PQfinish(conn);

    return variable;
}


// Busca en la base de datos las variables
// mediante su alias y
// retorna un arreglo de las variables encontradas
Variable ** getVariablesByAliases(char** variables_aliases,int n){
	Variable ** variables = NULL;
	int size = (sizeof(Variable*))*(n+1);
	variables = (Variable**)malloc(size);
    char variable_alias[50];
    int i;
    for(i=0;i<n;i++){
    	strcpy(variable_alias,variables_aliases[i]);
    	Variable* variable = _getVariableByAlias(variable_alias);
    	printf("%s\n",variable->alias);
    	variables[i]=variable;
    }
    variables[n]=NULL;
    return variables;
}


int insertMeasures(Measurements* m){
	PGconn *conn = PQconnectdb("user=obayona password=EloyEcuador93 dbname=resclima");

    if (PQstatus(conn) == CONNECTION_BAD) {
        fprintf(stderr, "Connection to database failed: %s\n",
            PQerrorMessage(conn));
    	PQfinish(conn);
    }
    int idStation = htonl(m->idStation);
	char * datetime = m->datetime;
	char * readings = m->values;

    char * query = "INSERT INTO \"TimeSeries_measurement\""
    			   "(\"idStation_id\",\"datetime\",\"readings\") "
                   "VALUES($1::integer,$2::timestamp,$3::json)";

    const char *values[3] = {(char *)&idStation,datetime,readings};
    int lengths[3] = {sizeof(idStation),strlen(datetime),strlen(readings)};
    int binary[3] = {1,0,0};

    PGresult *res = PQexecParams(conn,query,3,NULL,values,lengths,binary,0);
    
    if (PQresultStatus(res) != PGRES_TUPLES_OK) {
        printf("No data retrieved\n");
        printf("%s\n", PQerrorMessage(conn));        
        PQclear(res);
    	PQfinish(conn);
    } 
    return 0;  
}