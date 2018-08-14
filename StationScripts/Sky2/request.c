#include "request.h"

struct MemoryStruct {
  char *memory;
  size_t size;
};


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

char* getSKY2Data(char* token){
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

        curl_easy_cleanup(curl);
        return chunk.memory;
    }
    curl_easy_cleanup(curl);
    return NULL;
}