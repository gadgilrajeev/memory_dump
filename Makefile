all : memdump.c
	gcc -o memdump memorydump.c

clean:
	rm -f memdump
