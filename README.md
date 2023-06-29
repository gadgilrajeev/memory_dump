## Memory Dump

This program is designed to dump the memory of a process into a binary file and then convert it into a hexadecimal format. The program takes command-line argumemnts to specify the start and end addresses of the memory to dump, the interval between dumps, and the number of times to perform the dump. 


## Functions
The converToHex function takes several arguments including the paths to the binary and hexadecimal files, the dump count and the start and end addresses. This function opens the binary file for reading and the hexadecimal file for writing.

## How it works

The program starts by defining several constants,including the version number and the size of the memory to allocate.It then declares a function convertToHex that takes arguments.

The main function starts by declaring variables, including the interval between the dumps, the number of times to perform the dump, and pointers to start and end addresses.It then allocates memory for an array and fills it with random values.

The program then enters a loop that processes command-line arguments using getOpt function. It handles options like 
- -h for help
- -s for starting address
- -e for ending address
- -i for interval, 
- -n for number of times to perform the dump.
 
## How to compile
To compile you will need a C compiler installed on your system. On Windows and Linux, you can use GCC compiler. 

Use the command.

```
make all
```

## How to run on Windows
 
Use the following command: 

```
memdump.exe -s 4 -e 40 -i 5 -n 4
```

## How to run on Linux 

Use the following command:

```
./memdump -s 4 -e 40 -i 5 -n 4
```


