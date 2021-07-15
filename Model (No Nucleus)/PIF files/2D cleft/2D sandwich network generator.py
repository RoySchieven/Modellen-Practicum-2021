# import os
# os.getcwd()
# os.chdir()

import random
from math import sqrt
output_file = "./2d sandwichnetwork ratio10.piff"
lattice_dim = 400  # width and height of the lattice

nof_pd_sw = 2500  #Number of fibres per per direction in the sandwhich
nof_pd_op = 5000  #Number of fibres per per direction in one of the outer parts
nof_cl = 1000  #Number of fibres  in the cleft

cleft_hight =  25  #total hight is twice this number (up and down from middle)
sw_hight = 30 #this is the height on both above and below the cleft

ratio_in_cleft = 7 #this means one in ratio+1 of collagen will get generated in cleft see pp

ratio_in_ld = 5 #this means one in ratio+1 of collagen will get generated in less dense area above the cleft
ratio_in_ld_sw_x= 2 #sw is for the sandwhichpart
ratio_in_ld_sw_y = 9

ratio_in_hd = 3
ratio_in_hd_sw_x= 1
ratio_in_hd_sw_y= 7

struct_chance = 2
cell_id=1

fibre_length_min = 7 # fibre width is taken to be 1 pixel (as in Scianna)
fibre_length_max = 13
fibre_length_sw_x_min= 17
fibre_length_sw_x_max= 23
fibre_length_sw_y_min= 2
fibre_length_sw_y_max= 5
fibre_length_cl_min = 14
fibre_length_cl_max = 20


cell_width = 8
nucleus_width = 4  #cell_width+nucleus_width should be even
n = 9
cluster_radius = int(n/2*cell_width)
cell_count = 3 + 2*nof_pd_sw + nof_cl + 2*nof_pd_op
compartment_count = 3 + 2*nof_pd_sw + nof_cl + 2*nof_pd_op

with open(output_file, 'w') as f:
    # First fill with Medium
    f.write("0 Medium 0 " + str(lattice_dim - 1) + " 0 " + str(lattice_dim - 1) + " 0 0\n")


    # Fibres in cleft
    for cell_id in range(1, nof_cl + 1):

        k = random.randint(fibre_length_cl_min, fibre_length_cl_max)
        t = random.randint(0,ratio_in_cleft)
        if(t==0):
            x = random.randint(0, lattice_dim - k)
            y1 = random.randint((lattice_dim/2) - cleft_hight - 1, (lattice_dim/2) )
            y2 = random.randint((lattice_dim/2) , (lattice_dim/2) + cleft_hight - 1)
            t = random.randint(0,1)
            if (t==0):
                y = y1
            else:
                y = y2
            f.write(" ".join([str(cell_id), "Collagen", str(x), str(x + k - 1), str(y), str(y), '0 0\n']))
            cell_id += 1

            #possible structure on top of horizontal collagen fibre in cleft
            t = random.randint(0,struct_chance)
            if (t==0 or t==1): #while loop if you want to add extra structures upon structures
                coinflip = random.randint(0,1) # decides wether it's up or down
                xs = random.randint(x, x+k-1)  #decides where the structure should be placed along the collagen fibre
                if (coinflip == 0):
                    ys = y + int(k/3) - 1
                    ks = max(int(k/2),2)
                    offset = random.randint(-ks,0) #decides what the offset in comparison with the previously printed vertical is
                    if (ys<lattice_dim-1): #checks bounds of possible new collagen fibre
                        f.write(" ".join([str(cell_id+1), "Collagen", str(xs), str(xs), str(y), str(ys), '0 0\n']))
                        cell_id += 1
                        if (xs+offset+ks-1<lattice_dim-1 and xs+offset>0): #checks if x goes out of bounds, if not it gets printed
                            f.write(" ".join([str(cell_id+2), "Collagen", str(xs+offset), str(xs+offset+ ks - 1), str(ys), str(ys), '0 0\n']))
                            cell_id += 1

                if (coinflip == 1):
                    ys = y - int(k/3) - 1
                    ks = max(int(k/2),2)
                    offset = random.randint(-ks,0) #decides what the offset in comparison with the previously printed vertical is
                    if (ys>0): #checks bounds of possible new collagen fibre
                        f.write(" ".join([str(cell_id+1), "Collagen", str(xs), str(xs), str(ys), str(y), '0 0\n']))
                        cell_id += 1
                        if (xs+offset+ks-1<lattice_dim-1 and xs+offset>0): #checks if x goes out of bounds, if not it gets printed
                            f.write(" ".join([str(cell_id+2), "Collagen", str(xs+offset) , str(xs+offset+ ks - 1), str(ys), str(ys), '0 0\n']))
                            cell_id += 1



    #This creates the collagen in the sandwhich in the x direction
    for cell_id in range(nof_cl +1 , nof_pd_sw + nof_cl + 1):
        p=random.randint(0,1)   #picks randomly in which sandwhich it is
        if (p==0):
            x = random.randint(0, lattice_dim - fibre_length_sw_x_max- 1)
            y = random.randint((lattice_dim/2)+cleft_hight, (lattice_dim/2)+sw_hight+cleft_hight - 1)

            t = random.randint(0,ratio_in_ld_sw_x) #this takes in account the higher density of collagen 'above' the cleft (w.r.t. the y-axis)
            g=random.randint(fibre_length_sw_x_min,fibre_length_sw_x_max )
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x + g - 1), str(y), str(y),'0 0\n']))

        if (p==1):
            x = random.randint(0, lattice_dim - fibre_length_sw_x_max - 1)
            y = random.randint((lattice_dim/2)-cleft_hight-sw_hight, (lattice_dim/2)- cleft_hight - 1)

            t = random.randint(0,ratio_in_hd_sw_x) #this takes in account the lower density of collagen 'above' the cleft (w.r.t. the y-axis)
            g=random.randint(fibre_length_sw_x_min,fibre_length_sw_x_max)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x + g - 1), str(y), str(y), '0 0\n']))



    #This creates the collagen in the outer parts in the x direction
    for cell_id in range(nof_pd_sw + nof_cl + 2 , nof_pd_sw + nof_cl + nof_pd_op + 2):

        p=random.randint(0,1)
        if (p==0): #this picks randomly in which outer part the collagen is created
            x = random.randint(0, lattice_dim - fibre_length_max - 1)
            y = random.randint(0, (lattice_dim/2)-cleft_hight-sw_hight - 1)

            t = random.randint(0,ratio_in_hd) #this takes in account the lower density of collagen 'above' the cleft (w.r.t. the y-axis)
            d=random.randint(fibre_length_min,fibre_length_max )
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x + d - 1), str(y), str(y), '\n']))

        elif (p==1):
            x = random.randint(0, lattice_dim - fibre_length_max - 1)
            y = random.randint((lattice_dim/2)+cleft_hight+sw_hight, lattice_dim - 1)

            t = random.randint(0,ratio_in_ld) #this takes in account the higher density of collagen 'above' the cleft (w.r.t. the y-axis)
            d=random.randint(fibre_length_min,fibre_length_max )
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x + d - 1), str(y), str(y), '\n']))



    # fibres in sandwhich in y direction
    for cell_id in range(3 + nof_pd_sw + nof_cl + nof_pd_op , 3 + 2*nof_pd_sw + nof_cl + nof_pd_op):

        p=random.randint(0,1) #picks randomly in which sandwhich it is
        if (p==0):
            x = random.randint(0, lattice_dim - 1)
            y = random.randint((lattice_dim/2)+cleft_hight, (lattice_dim/2)+sw_hight+cleft_hight -fibre_length_sw_y_max- 1)

            h =random.randint(fibre_length_sw_y_min,fibre_length_sw_y_max )
            t = random.randint(0,ratio_in_ld_sw_y)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y + h - 1), '\n']))

        if (p==1):
            x = random.randint(0, lattice_dim - 1)
            y = random.randint((lattice_dim/2)-cleft_hight-sw_hight, (lattice_dim/2)- cleft_hight - fibre_length_sw_y_max - 1)

            h =random.randint(fibre_length_sw_y_min,fibre_length_sw_y_max )
            t = random.randint(0,ratio_in_hd_sw_y)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y + h - 1), '\n']))


    #densities outer part in y direction
    for cell_id in range(4 + 2*nof_pd_sw + nof_cl + nof_pd_op , 3 + 2*nof_pd_sw + nof_cl + 2*nof_pd_op ):

        p=random.randint(0,1) #this picks randomly in which outer part the collagen is created
        if (p==0):
            x = random.randint(0, lattice_dim - 1)
            y = random.randint(0, (lattice_dim/2)-cleft_hight-sw_hight -fibre_length_max- 1)

            d=random.randint(fibre_length_min,fibre_length_max )
            t = random.randint(0,ratio_in_hd)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y + d - 1), '\n']))



        elif (p==1):
            x = random.randint(0, lattice_dim - 1)
            y = random.randint((lattice_dim/2)+cleft_hight+sw_hight, lattice_dim - fibre_length_max - 1)

            d=random.randint(fibre_length_min,fibre_length_max )
            t = random.randint(0,ratio_in_ld)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y + d - 1), '\n']))


    # possible code to get wires in y-direction in cleft
    #    elif (y>(lattice_dim/2)-cleft_hight-fibre_length+1 and y<(lattice_dim/2)+cleft_hight-fibre_length+1):
    #        t = random.randint(0,ratio_in_cleft)
    #        if (t==0):
    #            f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y + fibre_length - 1), '0 0\n']))




    for x in range(lattice_dim//2 - cluster_radius, lattice_dim//2 + cluster_radius - cell_width, cell_width):
        for y in range(lattice_dim//2 - cluster_radius, lattice_dim//2 + cluster_radius - cell_width, cell_width):
            # Calculate center of mass
            com_x = x + cell_width / 2.
            com_y = y + cell_width / 2.
            # Check if COM is within cluster radius
            if sqrt((com_x - lattice_dim//2) ** 2 + (com_y - lattice_dim//2) ** 2) > cluster_radius:
                continue

            # If within cluster radius, add cell to PIF file
            # format:  cell# celltype x1 x2 y1 y2 z1 z2
            cell_count += 1
            f.write(" ".join([str(cell_count), "Tumor", str(x), str(x + cell_width - 1),
                              str(y), str(y + cell_width - 1), '0 0\n']))