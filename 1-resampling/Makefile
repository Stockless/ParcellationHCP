CC = gcc -lm

CFLAGS = -c -Wall -O3

all: main

main: resampling.c BundleTools_sp.o BundleTools_sp.h
    gcc -o main BundleTools_sp.o resampling.c

clean:
	rm -rf *o main
