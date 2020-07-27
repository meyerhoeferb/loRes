CC=gcc
CFLAGS=-std=gnu99 -Wall -pedantic -Werror

all:
	$(CC) $(CFLAGS) -o lores lores.c init.c bitboards.c

clean:
	rm -f *.o
	rm -f lores
