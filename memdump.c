#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <windows.h>

#define VERSION 0
#define RAM_SIZE 1024*1024*10// 10MB

void hexDump(FILE *hex_fp, void *addr,int start_addr,int end_addr,int len)
{
    int i;
    unsigned char buff[17];
    unsigned char *pc = (unsigned char*)addr;

    // Process every byte in the data.
    for (i = start_addr; i < end_addr; i++) {
        // Multiple of 16 means new line (with line offset).

        if (((i-start_addr) % 16) == 0) {
            
            if (i != start_addr)
                fprintf(hex_fp,"  %s\n", buff);

           
            fprintf(hex_fp,"  %04x ", i);

        }

        // Now the hex code for the specific character.
        fprintf(hex_fp," %02x", pc[i]);

        // And store a printable ASCII character for later.
        if ((pc[i] < 0x20) || (pc[i] > 0x7e)) {
            buff[(i-start_addr) % 16] = '.';
        } else {
            buff[(i-start_addr) % 16] = pc[i];
        }

        buff[((i-start_addr) % 16) + 1] = '\0';

    }

    // Pad out last line if not exactly 16 characters.
    while (((i-start_addr) % 16) != 0) {
        fprintf(hex_fp,"   ");
        i++;
    }

    // And print the final ASCII bit.
    fprintf(hex_fp,"  %s\n", buff);

}

int main(int argc, char **argv) {
   
    int option = 0,i;
    int interval=0; //default interval is 30 seconds
    int num_files=0;//default dump instances
    int version=99;
    int dump_count = 0;
    double *ptr_mem;
    int start_addr = -1;
    int end_addr = -1;

srand(time(NULL));

    ptr_mem = (double *) malloc(RAM_SIZE);

    for(i=0;i<RAM_SIZE/sizeof(double);i++) {
       ptr_mem[i] = (double) rand() / RAND_MAX; // fill memory with random values

    }

    while ((option = getopt(argc, argv, "s:e:i:n:hV")) != -1) {
        switch (option) {
            case 'h':
                printf("memorydump [Options]\n Options\n");
                printf("-h\t\tShow help\n");
                printf("-s\t\tStart address\n");
                printf("-e\t\tEnd address\n");
                printf("-i\t\tThe Interval\n\t\t1) Interval should be non zero and non negative\n\t\t2) Interval should always be greater than 1\n");
                printf("-n\t\tNumber of times\n\t\t1)Should be more than 1\n");
                printf("-V\t\tShow current version\n");

                exit(1);  
            case 's':
                sscanf(optarg, "%x", &start_addr);
                break;
            case 'e':
                sscanf(optarg, "%x", &end_addr);
                break;
            case 'i':
                interval = atoi(optarg);
                break;
            case 'n':
                num_files = atoi(optarg);
                break;
            case 'V':
                version = VERSION;
                printf("Current version is %d\n",version);
                exit(1);
            default:
                printf("Option incorrect\n");
                return 1;
        }
    }

    char bin_path[MAX_PATH];
    char hex_path[MAX_PATH];

    if(!GetCurrentDirectory(MAX_PATH, bin_path)) {
        printf("Error getting current directory\n");
        exit(1);
    }

    if(!GetCurrentDirectory(MAX_PATH, hex_path)) {
        printf("Error getting current directory\n");
        exit(1);
    }

    strcat(bin_path, "\\bin_files\\");
    strcat(hex_path, "\\hex_files\\");

   

    char filename[MAX_PATH];

    for(i=0;i<num_files;i++) {
        sprintf(filename,"%s\\dump_%d.bin", bin_path, dump_count);
        FILE *dump_file = fopen(filename, "wb");
        if(dump_file == NULL) {
            printf("Error creating dump file %s\n", filename);
            exit(1);
        }

        fwrite(ptr_mem,end_addr-start_addr,1,dump_file);

        sprintf(filename,"%s\\hexDump_%d.hex",hex_path,dump_count);

        FILE *hex_fp = fopen(filename, "w");
        if(hex_fp == NULL) {
            printf("Error creating dump file %s\n", filename);
            exit(1);
        }

        hexDump(hex_fp,ptr_mem,start_addr,end_addr,end_addr-start_addr); // change sizeof(ptr_mem) to RAM_SIZE

        fclose(dump_file);
        fclose(hex_fp);

        start_addr++;
        end_addr++;
        dump_count++;
        sleep(interval);
    }

    free(ptr_mem);
    return EXIT_SUCCESS;
}
