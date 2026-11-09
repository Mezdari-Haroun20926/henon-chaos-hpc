#ifndef HENON_SOLVER_H
#define HENON_SOLVER_H

#include <stdio.h>
#include <stdlib.h>

#define A_DEFAULT 1.4
#define B_DEFAULT 0.3

void run_henon_simulation(int num_iterations, double x0, double y0, const char *filepath);

#endif
