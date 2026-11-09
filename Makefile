CC = gcc
CFLAGS = -Wall -Wextra -O3 -march=native -Iinclude
LDFLAGS = -lm

SRC = src/main.c src/henon_solver.c src/benchmark.c
OBJ = $(SRC:src/%.c=bin/%.o)
TARGET = bin/henon_sim

all: $(TARGET)

$(TARGET): $(OBJ)
	@mkdir -p bin
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

bin/%.o: src/%.c
	@mkdir -p bin
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -rf bin/* data/*

.PHONY: all clean
