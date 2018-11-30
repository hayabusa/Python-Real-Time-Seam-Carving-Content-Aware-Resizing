import cv2
import numpy as np
from MatWrp import MatWrp

class Core():
    def get_w(self, optimum_energy, seam_energy, i, j, row):
        return seam_energy[row][i] * optimum_energy[row + 1][j]
    
    def get_seams(self, energy, k):
        seam_energy = MatWrp()
        seam_energy.set_shape(energy)

        optimum_energy = MatWrp()
        optimum_energy.set_shape(energy)

        self.calc_optimum_dynamics(energy, optimum_energy)

    def calc_optimum_dynamics(self, inwrp, dynamics):
        h = inwrp.height()
        w = inwrp.width()

        for i in range(w):
            dynamics[h - 1][i] = inwrp[h - 1][i]

        for curr_row in range(h - 2, -1, -1):
            for curr_col in range(0, w):
                curr_min = dynamics[curr_row + 1][curr_col] + inwrp[curr_row + 1][curr_col]

                for delta in (-1 ,1):
                    if (delta + curr_col < w and delta + curr_col >= 0):
                        val_to_exam = dynamics[curr_row + 1][curr_col + delta] + inwrp[curr_row + 1][curr_col]
                    if (curr_min > val_to_exam):
                        curr_min = val_to_exam

                dynamics[curr_row][curr_col] = curr_min

    def calc_matches(self, energy, optimum_energy, seam_energy, matches, row):
        
