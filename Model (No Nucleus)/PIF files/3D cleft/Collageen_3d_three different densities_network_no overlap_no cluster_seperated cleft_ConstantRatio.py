# import os
# os.getcwd()
# os.chdir()

import random
from math import sqrt
output_file = "./3d collagen60000_threeparts_network_nooverlap_nocluster_seperated cleft_constantratio_1.piff"
lattice_dim = 200  # width and height of the lattice

n_f_pd_sw = 400000  # total number per part is : thrice this number (in x, y and z directions), this doest not take in account only a fraction actually gets placed
n_f_pd_op = 300000	#number of fibres per direction for the sandwhich, outer parts and cleft
n_f_c = 50000

cleft_hight =  22  #total hight is twice this number (up and down from middle)
sw_hight = 0

ratio_in_cleft =  10 #this means one in ratio+1 of collagen will get generated in cleft see pp
ratio_in_ld = 7 #this means one in ratio+1 of collagen will get generated in less dense area above the cleft
ratio_in_ld_sw_x = 3 #sw is for the sandwhichpart for the lower density part, the x and y direction have different ratios
ratio_in_ld_sw_y = 5

ratio_in_hd = 5
ratio_in_hd_sw_x= 2 #sw is for the sandwhichpart for the higher density part, the x and y direction have different ratios
ratio_in_hd_sw_y= 4

fibre_length = 8  # fibre width is taken to be 1 pixel (as in Scianna)
fibre_length_sw_x = 20
fibre_length_sw_y = 9

x_net_min=8   #these are the minimal and maximal width and height of the network in the cleft. The broadness is taken to be 1 pixel
x_net_max=18
y_net_min=2
y_net_max=5
y2_net_max=y_net_max #this is the maximal value for height of callagen above and under the tumor (w.r.t. the y-axis)
y2_net_min= y_net_min

#values for the cluster of cells/tumor
cell_width = 8
n = 5
cluster_radius = int(n/2*cell_width)
cell_count = (n_f_pd_sw+ n_f_pd_op)*3 + n_f_c

#this calculates the area on
#  ((lattice_dim//2)+cleft_hight -y2_net_min -1 + y2_net_max) - (lattice_dim//2 + cluster_radius- y2_net_max)=
ar_ac = 2* (cleft_hight+-y2_net_min -1 + y2_net_max)
ar_op = 2*cleft_hight* (lattice_dim - 2*cluster_radius)
ar_tot = ar_ac + ar_op
ratio_cluster= ar_tot//ar_ac

with open(output_file, 'w') as f:
    # First fill with Medium
    f.write("0 Medium 0 " + str(lattice_dim - 1) + " 0 " + str(lattice_dim - 1) +" 0 " + str(lattice_dim - 1) + '\n')

    # Network in cleft
    for cell_id in range(1, n_f_c + 1):

        # Choose random position such that the netwerk isn't created in the cluster

        l=random.randint(0,2)
        if (l==0): #this places the netwerk to the left of the cluster (w.r.t the x-axis). The y-values are such that it is placed in the cleft and the values for z is a random value up to the dimension length. The y_net_max term is to make sure the network isn't created into the sandwhich part.
            x = random.randint(0, lattice_dim//2 - cluster_radius- x_net_max -1)
            y = random.randint((lattice_dim//2)-cleft_hight, (lattice_dim//2)+cleft_hight -y_net_max -1)
            z = random.randint(0, lattice_dim - 1)

        if (l==1):  #this places the netwerk to the right of the cluster (w.r.t the x-axis) analogous to the above code
            x = random.randint(lattice_dim//2 + cluster_radius+1, lattice_dim - x_net_max-1)
            y = random.randint((lattice_dim//2)-cleft_hight, (lattice_dim//2)+cleft_hight -y_net_max -1)
            z = random.randint(0, lattice_dim - 1)

        if (l==2): #this places the network 'above' and 'below' the cluster (w.r.t. the z-axis). The x-values are the same as the cluster. The y-values are such that the network is in the cleft.

            h= random.randint(0,1)
            if (h==0): #this places the network 'below' the cluster (w.r.t. the z-axis)
                g=random.randint(0,1) #this is to compensate for the fact that the area considerd is twice as small as the previous areas
                if (g==0):
                    x = random.randint(lattice_dim//2 - cluster_radius -x_net_max, lattice_dim//2 + cluster_radius)
                    y = random.randint((lattice_dim//2)-cleft_hight, (lattice_dim//2)+cleft_hight -y_net_max -1)
                    z = random.randint(0, lattice_dim//2 - cluster_radius-1)

            if (h==1): #this places the network 'above' the cluster (w.r.t. the z-axis)
                g=random.randint(0,1)
                if (g==0):
                    x = random.randint(lattice_dim//2 - cluster_radius -x_net_max, lattice_dim//2 + cluster_radius )
                    y = random.randint((lattice_dim//2)-cleft_hight, (lattice_dim//2)+cleft_hight -y_net_max -1)
                    z = random.randint(lattice_dim//2 + cluster_radius+1, lattice_dim - 1)

        t = random.randint(0,ratio_in_cleft)
        if (t==0):

            s = random.randint(x_net_min,x_net_max) #this chooses a random length of the network in the x-axis
            u = random.randint(y_net_min,y_net_max) #this chooses a random length of the network in the y-axis

            #this creates the lines of collagen that lie in the x-axis, the distance between the two lines is the length of the network in the y-axis
            f.write(" ".join([str(cell_id), "Collagen", str(x), str(x + s ), str(y), str(y), str(z), str(z), '0 0\n']))
            f.write(" ".join([str(cell_id), "Collagen", str(x), str(x + s ), str(y+u), str(y+u), str(z), str(z), '0 0\n']))

            #this creates the lines of collagen that lie in the y-axis
            f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y + u ), str(z), str(z), '0 0\n']))
            f.write(" ".join([str(cell_id), "Collagen", str(x+s), str(x+s), str(y), str(y + u ), str(z), str(z), '0 0\n']))


        #this creates the network 'under' and 'above' the cluster (w.r.t. the y-axis)
        b= random.randint(0, ratio_cluster) #the ratio is to compensate for the fact that this considers a small surface compared to the areas considered in the above code
        if (b==0):
            j= random.randint(0,1)
            if (j==0): #the x and z values are the same as the cluster. The y-value is under the cluster
                x = random.randint(lattice_dim//2 - cluster_radius -x_net_max, lattice_dim//2 + cluster_radius )
                y = random.randint((lattice_dim//2)-cleft_hight-y_net_max, lattice_dim//2 - cluster_radius-y2_net_min -1)
                z = random.randint(lattice_dim//2 - cluster_radius, lattice_dim//2 + cluster_radius )
            if (j==1):  #the x and z values are the same as the cluster. The y-value is above the cluster
                x = random.randint(lattice_dim//2 - cluster_radius -x_net_max, lattice_dim//2 + cluster_radius )
                y = random.randint( lattice_dim//2 + cluster_radius- y2_net_max, (lattice_dim//2)+cleft_hight -y2_net_min -1)
                z= random.randint(lattice_dim//2 - cluster_radius, lattice_dim//2 + cluster_radius )

        t = random.randint(0,ratio_in_cleft) #this is completely analogous to before
        if (t==0):

            s = random.randint(x_net_min,x_net_max)
            u = random.randint(y2_net_min,y2_net_max)

            f.write(" ".join([str(cell_id), "Collagen", str(x), str(x + s ), str(y), str(y), str(z), str(z), '0 0\n']))
            f.write(" ".join([str(cell_id), "Collagen", str(x), str(x + s ), str(y+u), str(y+u), str(z), str(z), '0 0\n']))


            f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y + u ), str(z), str(z), '0 0\n']))
            f.write(" ".join([str(cell_id), "Collagen", str(x+s), str(x+s), str(y), str(y + u ), str(z), str(z), '0 0\n']))


    #fibres in sandwhich and outer parts in x direction
    for cell_id in range(n_f_c +1 , n_f_pd_sw + n_f_c + 1):


        p=random.randint(0,1)   #picks randomly in which sandwhich it is
        if (p==0):
            x = random.randint(0, lattice_dim - fibre_length_sw_x- 1)
            y = random.randint((lattice_dim/2)+cleft_hight, (lattice_dim/2)+sw_hight+cleft_hight )
            z = random.randint(0, lattice_dim - 1)
        if (p==1):
            x = random.randint(0, lattice_dim - fibre_length_sw_x- 1)
            y = random.randint((lattice_dim/2)-cleft_hight-sw_hight, (lattice_dim/2)- cleft_hight )
            z = random.randint(0, lattice_dim - 1)

        if (y>=(lattice_dim/2)+cleft_hight and y<(lattice_dim/2)+sw_hight+cleft_hight):
            t = random.randint(0,ratio_in_ld_sw_x) #this takes in account the higher density of collagen 'above' the cleft (w.r.t. the y-axis)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x + fibre_length_sw_x - 1), str(y), str(y), str(z), str(z), '0 0\n']))

        elif (y>=(lattice_dim/2)-cleft_hight-sw_hight and y<(lattice_dim/2)- cleft_hight):
            t = random.randint(0,ratio_in_hd_sw_x) #this takes in account the lower density of collagen 'above' the cleft (w.r.t. the y-axis)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x + fibre_length_sw_x - 1), str(y), str(y), str(z), str(z), '0 0\n']))

    #This creates the collagen in the outer parts in the x direction
    for cell_id in range(n_f_pd_sw + n_f_c + 2 , n_f_pd_sw + n_f_c + n_f_pd_op + 2):

        p=random.randint(0,1)
        if (p==0): #this picks randomly in which outer part the collagen is created
            x = random.randint(0, lattice_dim - fibre_length - 1)
            y = random.randint(0, (lattice_dim/2)-cleft_hight-sw_hight - 1)
            z = random.randint(0, lattice_dim - 1)
        elif (p==1):
            x = random.randint(0, lattice_dim - fibre_length - 1)
            y = random.randint((lattice_dim/2)+cleft_hight+sw_hight, lattice_dim - 1)
            z = random.randint(0, lattice_dim - 1)

        if (y>=(lattice_dim/2)+cleft_hight+sw_hight):
            t = random.randint(0,ratio_in_ld) #this takes in account the higher density of collagen 'above' the cleft (w.r.t. the y-axis)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x + fibre_length - 1), str(y), str(y), str(z), str(z), '\n']))

        elif (y<=(lattice_dim/2)-cleft_hight-sw_hight):
            t = random.randint(0,ratio_in_hd) #this takes in account the lower density of collagen 'above' the cleft (w.r.t. the y-axis)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x + fibre_length - 1), str(y), str(y), str(z), str(z), '\n']))


    # fibres in sandwhich in y direction
    for cell_id in range(3 + n_f_pd_sw + n_f_c + n_f_pd_op , 3 + 2* n_f_pd_sw + n_f_c + n_f_pd_op):

        p=random.randint(0,1) #picks randomly in which sandwhich it is
        if (p==0):
            x = random.randint(0, lattice_dim - 1)
            y = random.randint((lattice_dim/2)+cleft_hight, (lattice_dim/2)+sw_hight+cleft_hight )
            z = random.randint(0, lattice_dim - 1)
        if (p==1):
            x = random.randint(0, lattice_dim - 1)
            y = random.randint((lattice_dim/2)-cleft_hight-sw_hight, (lattice_dim/2)- cleft_hight )
            z = random.randint(0, lattice_dim - 1)

        if (y>=(lattice_dim/2)+cleft_hight and y<(lattice_dim/2)+sw_hight+cleft_hight):
            t = random.randint(0,ratio_in_ld_sw_y)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y + fibre_length_sw_y - 1), str(z), str(z), '\n']))

        elif (y>(lattice_dim/2)-cleft_hight-sw_hight and y<(lattice_dim/2)- cleft_hight):
            t = random.randint(0,ratio_in_hd_sw_y)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y + fibre_length_sw_y - 1), str(z), str(z), '\n']))

    #densities outer part in y direction
    for cell_id in range(3 + 2*n_f_pd_sw + n_f_c + n_f_pd_op , 3 + 2* n_f_pd_sw + n_f_c + 2*n_f_pd_op):

        p=random.randint(0,1) #this picks randomly in which outer part the collagen is created
        if (p==0):
            x = random.randint(0, lattice_dim - 1)
            y = random.randint(0, (lattice_dim/2)-cleft_hight-sw_hight -fibre_length- 1)
            z = random.randint(0, lattice_dim - 1)
        elif (p==1):
            x = random.randint(0, lattice_dim - 1)
            y = random.randint((lattice_dim/2)+cleft_hight+sw_hight, lattice_dim - fibre_length - 1)
            z = random.randint(0, lattice_dim - 1)

        if (y>=(lattice_dim/2)+cleft_hight+sw_hight):
            t = random.randint(0,ratio_in_ld)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y + fibre_length - 1), str(z), str(z), '\n']))

        elif (y<=(lattice_dim/2)-cleft_hight-sw_hight):
            t = random.randint(0,ratio_in_hd)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y + fibre_length - 1), str(z), str(z), '\n']))


    #fibres in z direction in outer parts
    for cell_id in range(4 + 2* n_f_pd_sw + n_f_c + 2*n_f_pd_op, 4 + 2* n_f_pd_sw + n_f_c + 3*n_f_pd_op):

        x = random.randint(0, lattice_dim - 1)
        y = random.randint(0, lattice_dim - 1)
        z = random.randint(0, lattice_dim - fibre_length)


        if (y>=(lattice_dim/2)+cleft_hight+sw_hight):
            t = random.randint(0,ratio_in_ld)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y), str(z), str(z + fibre_length - 1), '\n']))
        elif (y<(lattice_dim/2)-cleft_hight-sw_hight):
            t = random.randint(0,ratio_in_ld)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y), str(z), str(z + fibre_length - 1), '\n']))


    for x in range(lattice_dim//2 - cluster_radius, lattice_dim//2 + cluster_radius - cell_width, cell_width):
        for y in range(lattice_dim//2 - cluster_radius, lattice_dim//2 + cluster_radius - cell_width, cell_width):
            for z in range(lattice_dim//2 - cluster_radius, lattice_dim//2 + cluster_radius - cell_width, cell_width):
                # Calculate center of mass
                com_x = x + cell_width / 2.
                com_y = y + cell_width / 2.
                com_z = z + cell_width //2
                # Check if COM is within cluster radius
                if sqrt((com_x - lattice_dim//2) ** 2 + (com_y - lattice_dim//2) ** 2 + (com_y - lattice_dim//2)**2) > cluster_radius:
                    continue

                # If within cluster radius, add cell to PIF file
                # format:  cell# celltype x1 x2 y1 y2 z1 z2
                cell_count += 1
                f.write(" ".join([str(cell_count), "Tumor", str(x), str(x + cell_width - 1),
                                str(y), str(y + cell_width - 1), str(z), str(z + cell_width - 1), '\n']))