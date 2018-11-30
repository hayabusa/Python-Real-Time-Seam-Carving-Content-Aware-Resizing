import cv2
import numpy as np
from MatWrp import MatWrp

class Core(object):
    def get_w(self, optimum_energy, seam_energy, i, j, row):
        return seam_energy.mat[row][i] * optimum_energy.mat[row + 1][j]
    
    def get_seams(self, energy, k):
        seam_energy = MatWrp()
        seam_energy.set_shape(energy)

        optimum_energy = MatWrp()
        optimum_energy.set_shape(energy)

        self.calc_optimum_dynamics(energy, optimum_energy)

        seams = [[] for i in range(energy.width())]
        for i in range(energy.width()):
            seam_energy.mat[0][i] = energy.mat[0][i]
            seams[i].reverse()
            seams[i].append(i)

        matches = [[] for i in range(energy.width())]
        for row in range(energy.height() - 1):
            self.calc_matches(energy, optimum_energy, seam_energy, matches, row)
            self.increase_seams(energy, optimum_energy, matches, seam_energy, seams, row)

        weighted_seams = []
        for i in range(len(seams)):
            weighted_seams.append([seam_energy.mat[energy.height() - 1][i], seams[i]])
        
        weighted_seams.sort(key=lambda x:x[0])

        res = []
        for i in range(len(weighted_seams)):
            res.append(weighted_seams[i][1])

        return res

    def increase_seams(self, energy, optimum_energy, matches, seam_energy,  seams, row):
        x = energy.width() - 1
        while (x >= 0):
            if x == 0:
                last_match = 0
            else:
                last_match = matches[x - 1]

            if (matches[x] == last_match + self.get_w(optimum_energy, seam_energy, x, x, row)):
                seams[x].append(x)
                seam_energy.mat[row + 1][x] = seam_energy.mat[row][x] + energy.mat[row + 1][x]
                x -= 1
            else:
                seams[x - 1].append(x)
                seams[x].append(x - 1)
                seams[x], seams[x - 1] = seams[x - 1], seams[x]
                seam_energy.mat[row + 1][x - 1] = seam_energy.mat[row][x] + energy.mat[row + 1][x - 1]
                seam_energy.mat[row + 1][x] = seam_energy.mat[row][x - 1] + energy.mat[row + 1][x]
                x -= 2

    def calc_optimum_dynamics(self, inwrp, dynamics):
        h = inwrp.height()
        w = inwrp.width()

        for i in range(w):
            dynamics.mat[h - 1][i] = inwrp.mat[h - 1][i]

        for curr_row in range(h - 2, -1, -1):
            for curr_col in range(0, w):
                curr_min = dynamics.mat[curr_row + 1][curr_col] + inwrp.mat[curr_row + 1][curr_col]

                val_to_exam = 0

                for delta in (-1 ,1):
                    if (delta + curr_col < w and delta + curr_col >= 0):
                        val_to_exam = dynamics.mat[curr_row + 1][curr_col + delta] + inwrp.mat[curr_row + 1][curr_col]
                    if (curr_min > val_to_exam):
                        curr_min = val_to_exam

                dynamics.mat[curr_row][curr_col] = curr_min

    def calc_matches(self, energy, optimum_energy, seam_energy, matches, row):
        matches[0] = self.get_w(optimum_energy, seam_energy, 0, 0, row)
        matches[1] = max(matches[0] + self.get_w(optimum_energy, seam_energy, 1, 1, row),
                                  self.get_w(optimum_energy, seam_energy, 0, 1, row) +
                                  self.get_w(optimum_energy, seam_energy, 1, 0, row))

        for col in range(2, energy.width()):
            w1 = matches[col - 1] + self.get_w(optimum_energy, seam_energy, col, col, row)
            w2 = matches[col - 2] + self.get_w(optimum_energy, seam_energy, col, col - 1, row) + self.get_w(optimum_energy, seam_energy, col - 1, col, row)
                                
            matches[col] = max(w1, w2)

    def process_seams(self, fromWrp, seams, delete_mode):
        if delete_mode == True:
            w_delta = -len(seams)
        else:
            w_delta =  len(seams)
        out = MatWrp()
        if fromWrp.transpose == True:
            out.blank_image(fromWrp.mat.row() + w_delta, fromWrp.mat.col(), fromWrp.mat.dtype)
        else:
            out.blank_image(fromWrp.mat.row(), fromWrp.mat.col() + w_delta, fromWrp.mat.dtype)

        out.set_orientation(fromWrp)
        for row in range(fromWrp.height()):
            pool = []
            