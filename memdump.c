#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <windows.h>

#define VERSION 0
#define RAM_SIZE 1024*1024*10 // 10MB

void convertToHex(char *bin_path, char *hex_path, int dump_count, int start_addr, int end_addr) {
    char bin_filename[MAX_PATH];
    char hex_filename[MAX_PATH];

    sprintf(bin_filename, "%s\\dump_%d.bin", bin_path, dump_count);
    sprintf(hex_filename, "%s\\dump_%d.hex", hex_path, dump_count);

    FILE *bin_file = fopen(bin_filename, "rb");
    if(bin_file == NULL) {
        printf("Error opening binary file %s\n", bin_filename);
        exit(1);
    }

    FILE *hex_file = fopen(hex_filename, "w");
    if(hex_file == NULL) {
        printf("Error creating hex file %s\n", hex_filename);
        exit(1);
    }

    unsigned char buffer[16];
    size_t binRead;
    int address = start_addr;

    while((binRead = fread(buffer, sizeof(unsigned char), 16, bin_file)) > 0) {
        fprintf(hex_file, "0x%08X\t", address);
        for(size_t i = 0; i < binRead; i++) {
            fprintf(hex_file, "%02X ", buffer[i]);
        }
        fprintf(hex_file, "\n");
        address += binRead;
    }

    fclose(bin_file);
    fclose(hex_file);
}

int main(int argc, char **argv) {
    int option = 0, i;
    int interval = 30; // default interval is 30 seconds
    int num_files = 0; // default dump instances
    int version = 99;
    int dump_count = 0;
    double *ptr_mem;
    int start_addr = -1;
    int end_addr = -1;

    srand(time(NULL));

    ptr_mem = (double *) malloc(RAM_SIZE);

    for(i = 0; i < RAM_SIZE / sizeof(double); i++) {
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
                printf("Current version is %d\n", version);
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

    strcpy(hex_path, bin_path);
    strcat(bin_path, "\\bin_files\\");
    strcat(hex_path, "\\hex_files\\");

    char filename[MAX_PATH];

    for(i = 0; i < num_files; i++) {
        sprintf(filename, "%s\\dump_%d.bin", bin_path, dump_count);

        FILE *dump_file = fopen(filename, "wb");
        if(dump_file == NULL) {
            printf("Error creating dump file %s\n", filename);
            exit(1);
        }

        fwrite(ptr_mem + start_addr, end_addr - start_addr, 1, dump_file);

        fclose(dump_file);

        convertToHex(bin_path, hex_path, dump_count, start_addr, end_addr);

        start_addr++;
        end_addr++;
        dump_count++;
        sleep(interval);
    }

    free(ptr_mem);
    return EXIT_SUCCESS;
}
