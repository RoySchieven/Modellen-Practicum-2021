import random
from math import sqrt
output_file = "./3d collagen60000_threeparts_constantratio_1.piff"
lattice_dim = 200  # width and height of the lattice
no_of_fibres_per_direction = 60000  # total number: twice this number (in x and y directions)

ratio_in_cleft = 20 #this means one in ratio+1 of collagen will get generated in cleft
cleft_hight = 30 #total hight is twice this number (up and down from middle)

ratio_in_ld = 4 #this means one in ratio+1 of collagen will get generated in less dense area above the cleft

fibre_ratio = 2
fibre_length = 10  # fibre width is taken to be 1 pixel (as in Scianna)


cell_width = 8
n = 5
cluster_radius = int(n/2*cell_width)
cell_count = no_of_fibres_per_direction*3

with open(output_file, 'w') as f:
    # First fill with Medium
    f.write("0 Medium 0 " + str(lattice_dim - 1) + " 0 " + str(lattice_dim - 1) +" 0 " + str(lattice_dim - 1) + '\n')
    # Fibres in x direction
    for cell_id in range(1, no_of_fibres_per_direction + 1):
        # Choose random position
        x = random.randint(0, lattice_dim - fibre_length)
        y = random.randint(0, lattice_dim - 1)
        z = random.randint(0, lattice_dim - 1)

        if (y>(lattice_dim/2)-cleft_hight and y<(lattice_dim/2)+cleft_hight):
            t = random.randint(0,ratio_in_cleft)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x + fibre_length - 1), str(y), str(y), str(z), str(z), '\n']))

        elif (y>=(lattice_dim/2)+cleft_hight):
            t = random.randint(0,ratio_in_ld)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x + fibre_length - 1), str(y), str(y), str(z), str(z), '\n']))

        else:
            f.write(" ".join([str(cell_id), "Collagen", str(x), str(x + fibre_length - 1), str(y), str(y), str(z), str(z), '\n']))
    # Fibres in y direction
    for cell_id in range(1 + no_of_fibres_per_direction, 2 * no_of_fibres_per_direction + 1):
        # Choose random position
        x = random.randint(0, lattice_dim - 1)
        y = random.randint(0, lattice_dim - fibre_length)
        z = random.randint(0, lattice_dim - 1)

        if (y>(lattice_dim/2)-cleft_hight and y<(lattice_dim/2)+cleft_hight):
            t = random.randint(0,ratio_in_cleft)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y + fibre_length - 1), str(z), str(z), '\n']))
        elif (y>=(lattice_dim/2)+cleft_hight):
            t = random.randint(0,ratio_in_ld)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y + fibre_length - 1), str(z), str(z), '\n']))
        else:
            f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y + fibre_length - 1), str(z), str(z), '\n']))

    # Fibres in z direction
    for cell_id in range(1 + 2 * no_of_fibres_per_direction, 3 * no_of_fibres_per_direction + 1):
        # Choose random position
        x = random.randint(0, lattice_dim - 1)
        y = random.randint(0, lattice_dim - 1)
        z = random.randint(0, lattice_dim - fibre_length)

        if (y>(lattice_dim/2)-cleft_hight and y<(lattice_dim/2)+cleft_hight):
            t = random.randint(0,ratio_in_cleft)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y), str(z), str(z + fibre_length - 1), '\n']))
        elif (y>=(lattice_dim/2)+cleft_hight):
            t = random.randint(0,ratio_in_ld)
            if (t==0):
                f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y), str(z), str(z + fibre_length - 1), '\n']))
        else:
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