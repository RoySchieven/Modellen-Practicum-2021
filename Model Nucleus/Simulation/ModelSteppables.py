from cc3d.core.PySteppables import *
import math
import os
import time
import zlib
import numpy as np

# Toggles
_3d = False # 3D toggle. To toggle 3D, set to True and change some lines in Model.xml
mmp_enabled = False  # NOTE: also comment out MMP DiffusionField tag in XML! Rest is handled in Model.py
growth_mitosis_enabled = True # Handled in Model.py
OutputField_enable = False
leader_follower_enabled = False

# Volume, surface, growth and mitosis parameters
tumor_lambda_volume = 10.0  # from Scianna et al.
tumor_lambda_surface = 2.0  
tumor_growth_rate = 0.05 if (not _3d) else 0.4  # per MCS -- be sure to keep this a float. Growth rate in 3D should be higher for comparable effect
nucleus_lambda_volume = 25.0  # High so nucleus is rigid
nucleus_lambda_surface = 4.0  # High so nucleus is rigid 

# Proteolysis parameters
mmp_offset = 5 if leader_follower_enabled else 50  # The amount of mmp constantly secreted
mmp_offset_leader = 100  # The amount of mmp constantly secreted
mmp_scale_factor = 0.5e-5 if leader_follower_enabled else 5e-5  # Conversion factor from confinement energy to secretion rate
mmp_scale_factor_leader = 10e-5
leader_percentage = 0.10 if leader_follower_enabled else 0  # Value between 0 and 1

collagen_volume_energy = -135.0  # For the VE approach

# Steppable frequencies
growth_mitosis_steppable_frequency = 10  # The higher the cheaper computation
mmpdegradation_steppable_frequency = 10  # mmpdegradation turns out te be extremely expensive
OutputField_frequency = 10  # Outputs all chemical fields into a CSV file

# OutputField parameters
lattice_size = [400,400,1]
fields = ["CTP"]
compression_save_frequency = 10*OutputField_frequency


# To increase speed, consider changing every call to this function to the appropriate function (2d or 3d)
def volume_to_surface(volume):
    if _3d:
        return volume_to_surface3d(volume)
    else:
        return volume_to_surface2d(volume)


_2sqrtpi = 2 * sqrt(math.pi)
def volume_to_surface2d(volume):
    """ Calculates perimeter(="surface") of a pixelated disk having the specified area(="volume").
        This stems from: vol = pi r^2, surface = 8 * r = 8 * sqrt(vol/pi). """
    return _2sqrtpi * sqrt(volume)
 
_4pi_3_4pi_23 = 4 * math.pi * (3/4/math.pi)**(2/3.)
def volume_to_surface3d(volume):
    """ Calculates surface of a pixelated ball having the specified volume.
        This stems from: vol = 4/3 pi r^3, surface = 6*(2r)^2 = _24_3_4pi_23 * vol^(2/3). """
    return _4pi_3_4pi_23 * (volume ** (2 / 3.))

  
class VolumeSurfaceInitialiserSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def start(self):
        # Initialise cell volumes        
        for cell in self.cell_list_by_type(self.NUCLEUS):
            nucleusvolume = cell.volume
            cell.targetVolume = nucleusvolume
            nucleussurface = volume_to_surface(cell.volume)
            cell.targetSurface = nucleussurface
            cell.lambdaVolume = nucleus_lambda_volume
            cell.lambdaSurface = nucleus_lambda_surface
            
        for cell in self.cell_list_by_type(self.TUMOR):
            cell.targetVolume = cell.volume
            cell.targetSurface = volume_to_surface(cell.volume+nucleusvolume) + nucleussurface
            cell.lambdaVolume = tumor_lambda_volume
            cell.lambdaSurface = tumor_lambda_surface

        for cell in self.cell_list_by_type(self.COLLAGEN):
            cell.volumeEnergy = collagen_volume_energy

        # Initialise mitosis threshold. Find random tumor cell:
        tumor_cell = None
        for cell in self.cell_list_by_type(self.TUMOR):
            tumor_cell = cell
            break
        # Set mitosis threshold to twice the tumor cell size (so mitosis occurs when the volume of the non-nucleus part is doubled):
        global mitosis_threshold
        mitosis_threshold = tumor_cell.volume * 2
        # NOTE It is assumed that all cells have the same size!
        
class MitosisSteppableClusters(MitosisSteppableClustersBase):

    def __init__(self, frequency=growth_mitosis_steppable_frequency):
        MitosisSteppableClustersBase.__init__(self, frequency)

    def step(self, mcs):
        #Obtaining nuclei information
        nucleus_cell = None
        for cell in self.cell_list_by_type(self.NUCLEUS):
            nucleus_cell = cell
            nucleusvolume = nucleus_cell.targetVolume
            nucleussurface = nucleus_cell.targetSurface
            break
        
        #Growth
        for cell in self.cell_list_by_type(self.TUMOR):
            cell.targetVolume += tumor_growth_rate * growth_mitosis_steppable_frequency
            cell.targetSurface = volume_to_surface(cell.targetVolume + nucleusvolume) + nucleussurface

        clusters_to_devide = []
        for cell in self.cell_list:
            if cell.type == self.TUMOR and cell.volume > mitosis_threshold:
                clusters_to_devide.append(cell.clusterId)
 
        for cluster_id in clusters_to_devide:
            self.divide_cluster_along_minor_axis(cluster_id)
            
            # # other valid options - to change mitosis mode leave one of the below lines uncommented (introduces bigger risk of nucleus disappearance)
            # self.divide_cluster_random_orientation(cluster_id)
            # self.divide_cluster_orientation_vector_based(cluster_id, 1, 0, 0)
            # self.divide_cluster_along_major_axis(cluster_id)
            
 
    def update_attributes(self):
        compartment_list_parent = self.get_cluster_cells(self.parent_cell.clusterId)
        for i in range (len(compartment_list_parent)):    
            if compartment_list_parent[i].type == self.NUCLEUS:
                parent_nucleus_volume = compartment_list_parent[i].targetVolume
                parent_nucleus_surface = compartment_list_parent[i].targetSurface
        for i in range(len(compartment_list_parent)):    
            if compartment_list_parent[i].type == self.TUMOR:
                compartment_list_parent[i].targetVolume /= 2.0
                compartment_list_parent[i].targetSurface = volume_to_surface(compartment_list_parent[i].targetVolume + parent_nucleus_volume) + parent_nucleus_surface
        self.clone_parent_cluster_2_child_cluster()
        leader = np.random.random() < leader_percentage
        compartment_list_child = self.get_cluster_cells(self.child_cell.clusterId)
        for i in range (len(compartment_list_child)):
            compartment_list_child[i].dict["MMP_OFFSET"] = mmp_offset_leader if leader else mmp_offset
            compartment_list_child[i].dict["MMP_SCALE_FACTOR"] = mmp_scale_factor_leader if leader else mmp_scale_factor



class MMPSecretionSteppable(SecretionBasePy):
    # Docs: https://compucell3dreferencemanual.readthedocs.io/en/latest/secretion.html
    def __init__(self, frequency=1):
        SecretionBasePy.__init__(self, frequency)

    def start(self):
        for cell in self.cell_list_by_type(self.TUMOR):
            leader = np.random.random() < leader_percentage
            print("leader" if leader else "follower")
            cluster_id = cell.clusterId
            compartment_list = self.get_cluster_cells(cluster_id)
            for i in range (len(compartment_list)):
                compartment_list[i].dict["MMP_OFFSET"] = mmp_offset_leader if leader else mmp_offset
                compartment_list[i].dict["MMP_SCALE_FACTOR"] = mmp_scale_factor_leader if leader else mmp_scale_factor


    def step(self, mcs):
        secretor = self.get_field_secretor("MMP")
        for cell in self.cell_list_by_type(self.TUMOR):
            # Secretion rate depends on cell confinement
            # Secretion rate should be increasing function of "cell.targetVolume - cell.volume" but
            # should be 0 when  cell.targetVolume - cell.volume < 0.

            # The following expression is quadratic because it was inspired by the volume-energy term
            # The surface energy contribution is commented out.
            confinement_energy = tumor_lambda_volume * max(cell.targetVolume - cell.volume, 0) ** 2  
            # + tumor_lambda_surface * max(cell.targetSurface - cell.surface, 0) ** 2

            # Add offset and scale appropriately
            secr_rate = (confinement_energy + cell.dict["MMP_OFFSET"]) * cell.dict["MMP_SCALE_FACTOR"]

            # MMP is secreted at secr_rate at all pixels that are neighbour of a collagen pixel.
            secretor.secreteOutsideCellAtBoundaryOnContactWith(cell, secr_rate, [self.COLLAGEN])
        
        for cell in self.cell_list_by_type(self.NUCLEUS):
            confinement_energy = nucleus_lambda_volume * max(cell.targetVolume - cell.volume, 0) ** 2  

            secr_rate = (confinement_energy + cell.dict["MMP_OFFSET"]) * cell.dict["MMP_SCALE_FACTOR"]

            secretor.secreteOutsideCellAtBoundaryOnContactWith(cell, secr_rate, [self.COLLAGEN])


class MMPDegradationSteppable(SteppableBasePy):
    def __init__(self, frequency=mmpdegradation_steppable_frequency):
        SteppableBasePy.__init__(self, frequency)

    def start(self):
        # Find medium cell object (to replace collagen pixels with)
        for cell in self.cell_list:
            if cell.type == self.MEDIUM:
                self.medium_cell = cell
                break

    def step(self, mcs):
        mmp = CompuCell.getConcentrationField(self.simulator, "MMP")

        for cell in self.cell_list_by_type(self.COLLAGEN):
            for pixel in self.get_copy_of_cell_pixels(cell):
                if mmp.get(pixel) >= 1: # TODO Maybe add some stochastic factor into this?
                    # Replace Collagen by Medium:
                    self.cell_field[pixel.x, pixel.y, pixel.z] = self.medium_cell
                    # Remove MMP:
                    mmp.set(pixel, 0)


class OutputFieldsSteppable(SteppableBasePy):
    def __init__(self, frequency=OutputField_frequency):
        SteppableBasePy.__init__(self, frequency)

    def step(self,mcs):
        start = time.time()
        if OutputField_enable:
            python_path = os.path.dirname(os.path.abspath(__file__))
            path = python_path+"/Fields_output"
            if not os.path.exists(path):
                os.makedirs(path)
            number_of_fields = len(fields)
            f = []
            field_data= []
            if _3d:
                size = (number_of_fields,lattice_size[0],lattice_size[1],lattice_size[2])
            else:
                size = (number_of_fields,lattice_size[0],lattice_size[1],1)
            data= np.zeros(size)

            for field in fields:
                f.append(open("".join((path,"/Output_",field,"{:04d}".format(mcs),"unc",".txt")),"wb"))
                field_data.append(CompuCell.getConcentrationField(self.simulator, field))
            for i in range(0,size[1]):
                for j in range(0,size[2]):
                    for k in range (0,size[3]):
                       for l in range (0,number_of_fields):
                           data[l,i,j,k] = field_data[l][i,j,k]
            for i in range(0,number_of_fields):
                data[i].astype("float16").tofile(f[i])
                f[i].close()
            print("Saving all chemical fields took %f seconds" % (time.time()-start))


            if (mcs+OutputField_frequency)%compression_save_frequency == 0:
                for field in fields:
                    uncompressed = []
                    for filename in sorted(os.listdir(path)):
                        if (filename.endswith("unc.txt") and field in filename):
                            file = open(os.path.join(path,filename),"rb")
                            uncompressed.append(file.read())
                            file.close()
                            os.remove(os.path.join(path,filename))

                    compressed = zlib.compress(np.array(b"".join(uncompressed)),1)
                    g = open("".join((path,"/Output_",field,"{:04d}".format(mcs+OutputField_frequency-compression_save_frequency),".txt")),"wb")
                    g.write(compressed)
                    g.close()
