import random
from math import sqrt
output_file = "C:\\users\\roysc\\downloads\\ru-modellenpracticum-master\\ru-modellenpracticum-master\\Model\\PIF files/nucleuszonderiets.piff"  # make sure to use the right path
lattice_dim = 400  # width and height of the lattice
cell_width = 8
nucleus_width = 4  #cell_width+nucleus_width should be even
n = 9
cluster_radius = int(n/2*cell_width)
cell_count = no_of_fibres_per_direction*2+1
compartment_count= no_of_fibres_per_direction*2+1

# See https://compucell3dreferencemanual.readthedocs.io/en/latest/pif_initializer.html#pif-initializer
# for PIF file structure:
#    cell# celltype x1 x2 y1 y2 z1 z2

with open(output_file, 'w') as f:
    f.write("Include Clusters\n")
    # First fill with Medium
    f.write(" ".join(["0 0 Medium 0 " + str(lattice_dim - 1) + " 0 " + str(lattice_dim - 1) + " 0 0\n"]))

    f.write(" ".join([str(0), str(0), "Medium", str(lattice_dim//2-3), str(lattice_dim//2+3), str(0), str(lattice_dim - 1), '0 0\n']))
        
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
            compartment_count += 2
            f.write(" ".join([str(cell_count), str(compartment_count), "Tumor", str(x), str(x + cell_width - 1),
                              str(y), str(y + cell_width - 1), '0 0\n']))    
            f.write(" ".join([str(cell_count), str(compartment_count+1), "Nucleus", str(x+int((cell_width-nucleus_width)/2)), str(x + int((cell_width+nucleus_width)/2) - 1),
                              str(y+int((cell_width-nucleus_width)/2)), str(y + int((cell_width+nucleus_width)/2) - 1), '0 0\n']))                                  
                              