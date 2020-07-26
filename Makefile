CC=gcc
CFLAGS=-std=gnu99 -Wall -pedantic -Werror

all:
	$(CC) $(CFLAGS) -o lores lores.c init.c

clean:
	rm -f *.o
	rm -f lores
