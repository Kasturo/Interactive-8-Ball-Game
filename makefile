CC = clang
CFLAGS = -Wall -std=c99 -pedantic
LDFLAGS = -lm

all: libphylib.so phylib_wrap.o _phylib.so

clean:
	rm -f *.o *.so

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -c phylib.c -fPIC -o phylib.o

libphylib.so: phylib.o
	$(CC) phylib.o -shared -o libphylib.so $(LDFLAGS)

phylib_wrap.c phylib.py: phylib.i
	swig -python -o phylib_wrap.c phylib.i

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -fPIC -o phylib_wrap.o -I/usr/include/python3.8

_phylib.so: phylib_wrap.o phylib.o
	$(CC) phylib_wrap.o phylib.o -shared -o _phylib.so $(LDFLAGS)
