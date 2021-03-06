CC=gcc
CFLAGS=-std=gnu99 -Wall -pedantic -Werror

all:
	$(CC) $(CFLAGS) lores.c init.c bitboards.c board.c hashkeys.c data.c attack.c io.c -o lores

clean:
	rm -f *.o
	rm -f lores
