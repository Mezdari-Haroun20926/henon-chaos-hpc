#ifndef HENON_SOLVER_H
#define HENON_SOLVER_H

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Paramètres canoniques de l'attracteur de Hénon
#define A_DEFAULT 1.4
#define B_DEFAULT 0.3

// Prototypes des fonctions du moteur C
void run_henon_simulation(int num_iterations, double x0, double y0, const char *filepath);
void run_henon_divergence(int num_iterations, double x0, double y0, double epsilon, const char *filepath);

#endif
