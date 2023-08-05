#Copyright 2016 Andrew Lehmann
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.


import os.path as pth
import os
import sys

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from astropy.table import Table
from scipy.integrate import simps
from math import pi
from math import cos

import constants as CONST
from andrew_misc import question

def radex_reader(molecule, nu1, nu2, Tk, npart, part, n, Tb, col, dv, parm):
    '''
    Returns all the output from RADEX as columns (for the data) and strings
    for the header and units.

    Inputs:
        - molecule [string] : name of emitting molecule, e.g. 'co'
        - nu1 [float]       : lower limit of frequency in GHz, e.g. 50
        - nu2 [float]       : upper limit of frequency in GHz, e.g. 1000
        - Tk [float]        : kinetic temperature of emitting molecule in Kelvin, e.g. 100
        - npart [int]       : integer number of collision partners, e.g. 1
        - part [string]     : name of collisional partner, e.g. 'H2'
        - n [float]         : number density of collisional partner in cm^-3, e.g. 1e4
        - Tb [float]        : background temperature in Kelvin, e.g. 2.73
        - col [float]       : column density of emitting molecule in cm^-2, e.g. 1e20
        - dv [float]        : linewidth across slab in km/s, e.g. 1.5
        - parm [int]        : 0: don't do another calculation, 1: do another calculation

    Outputs:
      Returns a numpy array with the following elements (in order):
        [0]  - Frequency [list of floats]              (GHz)
        [1]  - Wavelength [list of floats]             (um)
        [2]  - Excitation Temperature [list of floats] (K)
        [3]  - Optical Depth  [list of floats]         (dimensionless)
        [4]  - Radiation Temperature [list of floats]  (K)
        [5]  - Upper Population [list of floats]
        [6]  - Lower Population [list of floats]
        [7]  - Flux [list of floats]                   (K*km/s)
        [8]  - Flux [list of floats]                   (erg*cm^2/s)
        [9]  - Names [list of strings]
        [10] - Units [list of strings]
    '''
    inp = open('input.in', 'w')
    
    inp.write(molecule + '.dat \n')
    inp.write('test.dat \n')
    inp.write(str(nu1) + '\n')
    inp.write(str(nu2) + '\n')
    inp.write(str(Tk) + '\n')
    inp.write(str(int(npart)) + '\n')
    inp.write(part + '\n')
    inp.write(str(n) + '\n')
    inp.write(str(Tb) + '\n')
    inp.write(str(col) + '\n')
    inp.write(str(dv) + '\n')
    inp.write(str(parm) + '\n')

    inp.close()
    
    os.system('radex < input.in > /dev/null')
    os.remove('input.in')
    
    output = {
        'upper': [],
        'lower': [],
        'energy': [],
        'frequency': [],
        'wavelength': [],
        'excitation_temperature': [],
        'optical_depth': [],
        'radiation_temperature': [],
        'population_upper': [],
        'population_lower': [],
        'flux_K': [],
        'flux_erg': []
    }

    with open('test.dat') as f:
        for line in f:
            if line[0] == '*':
                continue
            elif line.split()[0] == 'Calculation':
                continue
            elif line.split()[0] == 'LINE':
                continue
            elif line.split()[0] == '(K)':
                continue
            else:
                output['upper'].append(                  line.split()[0]           )
                output['lower'].append(                  line.split()[2]           )
                output['energy'].append(                 float( line.split()[3] )  )
                output['frequency'].append(              float( line.split()[4] )  )
                output['wavelength'].append(             float( line.split()[5] )  )
                output['excitation_temperature'].append( float( line.split()[6] )  )
                output['optical_depth'].append(          float( line.split()[7] )  )
                output['radiation_temperature'].append(  float( line.split()[8] )  )
                output['population_upper'].append(       float( line.split()[9] )  )
                output['population_lower'].append(       float( line.split()[10] ) )
                output['flux_K'].append(                 float( line.split()[11] ) )
                output['flux_erg'].append(                 float( line.split()[12] ) )
    
    # Remove the RADEX output files, given that we've now taken their data
    os.remove('test.dat')    
    os.remove('radex.log')

    # Sort the dictionary in ascending wavelengths
    SortIdx = np.argsort( output['wavelength'] )

    for key in output:
        output[key] = np.array( output[key] )[SortIdx]

    return output
    
    
    
def slab_sum(wl, temps, labels, energy, freq, tau, background):
    '''
    Function that takes wavelength and  temperature arrays
    from different slabs and intelligently combines the 
    wavelengths so none are missing and adds the right spectral
    line temperatures.    
    '''
    output = {}
    en,wav,temp = np.array([]),np.array([]),np.array([])
    od,labs = np.array([]),np.array([])
    nu = np.array([])
    
    for e in energy: en  = np.append(en, e)
    for l in labels: labs = np.append(labs, l)
    for w in wl:     wav = np.append(wav, w)
    for t in temps:  temp = np.append(temp, t)
    for n in freq:   nu = np.append(nu, n)
    for o in tau:    od = np.append(od, o)

    for i in xrange(len(wav)):
        try :
            output[labs[i]] += np.array([ 0.0 , temp[i], 0.0, 0.0, 0.0])
        except KeyError as e:
            output[labs[i]] = np.array([ wav[i], temp[i], en[i], nu[i], od[i] ])
    
    x = []
    y = []
    for key in output.keys():
        if output[key][1] > background: 
            x.append(output[key][2])
            y.append(key)

    y = np.array(y)[np.argsort(x)]

    return output, y
##############################################################################
    
    
def cropper(croppee, tolerance):
    '''
    Function that crops the outsides of an array where nothing happens.
    
    Inputs
        - croppee [float array]:    array to be cropped
        - tolerance [scalar float]: fraction of change defining 
          the crop, probably should be less than 0.01   

    Outputs
        - cropL: index of left crop boundary
        - cropR: index of right crop boundary
    '''
    LoopIndex = 0
    while croppee[LoopIndex]/croppee[LoopIndex+1] > 1-tolerance and croppee[LoopIndex]/croppee[LoopIndex+1] < 1+tolerance and LoopIndex < len(croppee)-1:
        cropL = LoopIndex
        LoopIndex = LoopIndex + 1

    LoopIndex = len(croppee) - 1
    while croppee[LoopIndex]/croppee[LoopIndex-1] > 1-tolerance and croppee[LoopIndex]/croppee[LoopIndex-1] < 1+tolerance and LoopIndex > 0:
        cropR = LoopIndex
        LoopIndex = LoopIndex - 1


    return cropL, cropR
##############################################################################




def y_cropper(croppee, fraction, scale):
    '''
    Function that determines the lower and upper bounds of a plot, so
    that the function plotted (croppee) takes up a given fraction of
    the plot, with equal space above and below.

    Inputs
        - croppee [float array/list]: the function being plotted
        - fraction [float]: the fraction of the plot that croppee will
                            fill
    
    Outputs
        - lower value of croppee
        - upper value of croppee
    '''
    k = (1.0 - fraction)/2.0/fraction

    if scale == 'log':
        alpha = (max(croppee)/min(croppee))**k
        return min(croppee)/alpha, max(croppee)*alpha

    if scale == 'lin': 
        alpha = k*(max(croppee)-min(croppee))
        return min(croppee) - alpha, max(croppee) + alpha
##############################################################################




def doppler(f0, vel):
    '''
    Light doppler effect.
    
    Inputs:
        - f0: frequency which is to be doppler shifted (Hz)
        - vel: velocity of motion (km/s)
    '''
    c = CONST.c_cm * 10.**(-5) # Speed of light (km/s)
    return f0*(1. + vel/c)
##############################################################################



def gaussian(x, a, width):
    '''
    Create a smooth gaussian function at a given point.
    
    Inputs
        - x     independent variable
        - a:    center of the gaussian function
        - width:  the FWHM of the gaussian function (same units as x)
    '''
    
    sigma = width/2.35482 # Converts FWHM into standard deviation 
    norm = np.max((1./np.sqrt(np.pi)) * np.exp(-(x-a)**2./2./sigma**2))
    return (1./np.sqrt(np.pi)) * np.exp(-(x-a)**2./2./sigma**2) / norm
##############################################################################





def shock_spectrum(x, locations, strengths, widths, background, noise=0.):
    '''
    Function that computes a continuous spectrum of lines function based on
    line locations (wavelength of line), line strength (in arbitrary units),
    line width (km/s?), background level (same units as line strength).
    
    Inputs:
        - x:            list/array of wavelengths for plotting (m)
        - locations:    wavelengths of spectral lines (m)
        - strengths:    line strength in arbitrary units
        - widths:       line widths (km/s)
        - background:   background level of emission (units of strengths)

    Output:
        Array of length(x) with spectral lines and background emission.
    '''
    spec = np.zeros(len(x)) + background # Initial spectrum is just the background
    for i in xrange(0, len(locations)):
        # First convert the line width from km/s into wavelength units
        width_lambda = CONST.c_cm* (1./doppler(CONST.c_m/locations[i], -widths[i]/2.) - 1./doppler(CONST.c_m/locations[i], widths[i]/2.))
        spec += gaussian(np.array(x), locations[i], width_lambda) * strengths[i]
    
    return spec
##############################################################################



def beam_area(FWHMx,FWHMy):
    '''
    Gives the effective beam area (sr) of a radio telescope

    Inputs:
        - FWHMx:    FWHM in x direction (arcsec)
        - FWHMy:    FWHM in y direction (arcsec)

    Output:
        - beam_area:    effective beam area (sr)
    '''
    from math import radians
    from math import pi
    from math import log
    
    return pi/4.0/log(2.0) * FWHMx * FWHMy * radians(1.0/60/60)**2
##############################################################################



def radex_lines(solution, mol_list, output_loc, wavelengths=[100, 3000], boundaries=None, image_type='png', quiet=False):
    '''
    Parameters
    ----------
    solution : dict
        dictionary containing shock solution output of pymhdshocks
        
    mol_list : list
        list of molecules you want the radex lines of, e.g. 'CO','HCO+'

    wavelengths : list
        2 element list of wavelengths: lower limit and upper limit (um)
    
    boundaries : list
        if None, then we interactively define the boundaries
    
    Returns
    -------
    lines : dict
        dictionary of integrated line fluxes
    '''
    

    # ERROR: If the molecule list includes a typo or unsupported molecule
    list_accepted=['CO', 'HCN', 'HNC', 'HCO+']
    for x in mol_list:
        #if ((x!= 'CO') and (x!= '13CO') and (x!= 'oH2O') and (x!= 'oH2O_rov')
        #        and (x!= 'pH2O') and (x!= 'pH2O_rov') and (x!= 'H2') and (x!= 'HCO+')):
        if x not in list_accepted:
            print 'You have entered an unsupported molecule (or made a typo).'
            print 'Accepted molecules are:'
            for mol in list_accepted:
                print '  {0:s}'.format(mol)
            quit()

    
    crnt_dir = pth.dirname(pth.abspath(__file__)) # Path directory of this file
    ########################## END SETUP ##################################


















    #######################################################################
    ########################## COMPUTATIONAL BLOCK ########################
    #######################################################################
    z = solution['zarray']
    T = solution['T']
    vnz = solution['vnz']
    vnx = solution['vnx']
    vny = solution['vny']
    viz = solution['viz']
    vix = solution['vix']
    viy = solution['viy']

    vshock = solution['vs']
    n0 = solution['n0']

    # Compute H-nuclei density and pressure through the shocks.
    nH  = n0*vshock/vnz
    pressure = nH * np.array(T)*CONST.kb_erg
    ############################





    ################ SLAB DETERMINATION ###################
    # This allows the user to visually determine the slab length, which
    # will be required to compute the inputs of the radex code.   

    # COMPUTE PRESSURE, TEMPERATURE, DENSITY AS FUNCTION OF Z

    if boundaries==None:

        # To crop the preview plots, find index where pressure stabilises 
        # (post-shock) and where it begins to change (pre-shock).
        cropL,cropR = cropper(pressure, 0.0001)
        leftz  = z[cropL] - (z[cropR] - z[cropL])/2.0
        rightz = z[cropR] + (z[cropR] - z[cropL])/2.0
        ##################################################



        #### Plot to define slab ####

        # Set up while loop to make sure slab boundaries make sense 
        # and user is satisfied.
        slab_ok,slab_total_ok = False, False
        while not slab_total_ok:

            # Plot stuff through the shock so user can see where 
            # to define slabs

            fig,axes=plt.subplots(nrows=3,ncols=1, figsize=(7,11))
            #fig_slab = plt.figure()

            # Pressure plot
            p_low, p_up = y_cropper(pressure, 3.0/4.0, 'log')

            axP = axes[0]
            #plt.title('SHOCK #' + str(x+1) + ': ' + args.directories[x], fontsize=20)

            axP.plot(z[0:len(pressure)], pressure)
            axP.set_yscale('log')
            axP.axis([leftz, rightz, p_low, p_up])
            axP.set_ylabel(r'$\mathrm{Gas \, Pressure \, (dyne/cm}^2)$',
                fontsize = 20)
            #############

            # Temperature plot
            temp_low, temp_up = y_cropper(T, 3.0/4.0, 'log')

            axT = axes[1]

            axT.plot(z[0:len(T)], T, color = 'red')
            axT.set_yscale('log')
            axT.axis([leftz, rightz, temp_low, temp_up])
            axT.set_ylabel(r'$\mathrm{Temperature \, (K)}$', fontsize=20)
            ################

            # Density plot
            top = 10.0*max(n0*vshock/np.array(vnz))
            bottom = 0.1*min(n0 * vshock/np.array(vnz))
            nH_low, nH_up = y_cropper(nH, 3.0/4.0, 'log')

            axN = axes[2]

            axN.plot(z[0:len(vnz)], nH)
            axN.set_yscale('log')
            axN.axis([leftz, rightz, nH_low, nH_up])
            axN.set_xlabel(r'$\mathrm{z \, (cm)}$', fontsize = 20)
            axN.set_ylabel(r'$n_\mathrm{H} \, (\mathrm{cm}^{-3})$', fontsize=20)
            #############

            plt.setp(axP.get_xticklabels(), visible=False)
            plt.setp(axT.get_xticklabels(), visible=False)
            fig.subplots_adjust(left=0.15, bottom=0.06, right=0.95,
                top=0.95, hspace=0.05)

            plt.show(block=False)



            slabs = question(
                'How many (integer) slabs for RADEX? ', type(1), 'a'
            )
            idx = 0
            boundary_temp = []
            for y in xrange(slabs+1):
                slab_ok = False
                while not slab_ok:
                    bound = question(
                            'Define slab boundary ' + str(y+1) + ' (of ' + 
                            str(slabs+1) + ') in cm: ', type(1.0), 'a'
                            )
                    
                    if idx > 0:
                        if bound < boundary_temp[idx-1]:
                            print "This slab boundary was left of the previous boundary. This is not allowed. Try again."
                        else:
                            # Append the given solution if appropriate
                            axP.axvline(x=bound, ls='--', lw=2, color='black')
                            axT.axvline(x=bound, ls='--', lw=2, color='black')
                            axN.axvline(x=bound, ls='--', lw=2, color='black')
                            plt.show(block=False)
                            boundary_temp.append(bound) 
                            idx += 1
                            slab_ok = True
                    else:
                        # Append the given solution
                        boundary_temp.append(bound)
                        idx += 1
                        slab_ok = True
                        axP.axvline(x=bound, ls='--', lw=2, color='black')
                        axT.axvline(x=bound, ls='--', lw=2, color='black')
                        axN.axvline(x=bound, ls='--', lw=2, color='black')
                        plt.show(block=False)

            if idx == (slabs+1): slab_total_ok = True

            check = question(
                        'Go ahead with these boundaries (enter for yes)? ',
                        type('string')
                    )
            if check != '': 
                slab_total_ok = False
                plt.close(fig)
            else:
                boundary = boundary_temp
                

        plt.close()
    else:
        boundary=boundaries
        slabs=len(boundaries)-1


    # Use the slab boundaries in real distance units to define slab 
    # boundary indices (of z array).
    index = []
    for y in xrange(0, slabs+1):
    
        index.append(np.where(z < boundary[y])[0][-1])
            
    dist = [
        (boundary[y+1] - boundary[y]) 
        for y in xrange(0, slabs)
    ]
    
    dist_total = sum(dist) 

    ############ RADEX INPUTS ############
    # Compute some RADEX inputs.
    
    # For the kinetic temperature in a slab, we take the average 
    # temperature in that slab weighted by the number density.
    
    Tkin = [
        np.sum(T[index[y]:index[y+1]]*nH[index[y]:index[y+1]])/np.sum(nH[index[y]:index[y+1]]) for y in xrange(slabs)
    ]
    

    # Compute the average number density of hydrogen nuclei in each slab
    nH_avg = [
        np.average(nH[index[y]:index[y+1]]) for y in xrange(slabs)
    ]
    
    # Compute the column density of hydrogen nuclei in each slab by 
    # integrating the H-nuclei volumn density through the shock
    NH_col = [simps(nH[index[y]:index[y+1]], z[index[y]:index[y+1]]) for y in xrange(slabs)]
    #simps(n*(CONST.c_cm*(p/p0)/(E + CONST.me_g*CONST.c_cm**2))*pdot, p) for n,nH,pdot in zip(nx,nH2,pdot_c)
    

    column={}
    for mol in mol_list:
        nM_avg = [
            np.average(solution['x{0:s}'.format(mol)][index[y]:index[y+1]]*nH[index[y]:index[y+1]]) for y in xrange(slabs)
        ]
        
        column[mol] = [simps(solution['x{0:s}'.format(mol)][index[y]:index[y+1]]*nH[index[y]:index[y+1]], z[index[y]:index[y+1]]) for y in xrange(slabs)]
        
        
    
    # Compute the linewidth (velocity dispersion) of each slab (km/s)
    delv =  [np.abs( vnz[index[y]] - vnz[index[y+1]] ) for y in xrange(slabs)]
    #######################################
    
  
    
    
    
    ### Use slab to define RADEX inputs ###
    beamsize = 4.*pi
    #beamsize = 1.

    # Bottom and top limits of lines figures depend on choice of units  
    background = 0.001
    top = 1.e2
    bottom = background/2.
    intensity = 'Flux(K_km/s)'

    
    # Some RADEX input parameters that are not computed from the shock
    wl_low, wl_up = wavelengths[0]*1.e-6, wavelengths[1]*1.e-6 # Wavelength limits (m)
    freq_low, freq_up = CONST.c_m/wl_up*1.e-9, CONST.c_m/wl_low*1.e-9 # Frequency limits (GHz)
    num_partners = 1
    partner = 'H2'
    T_back = 2.73
    calc_param = 0

    # Array of wavelengths (for plotting)
    wave = np.logspace(
        np.log10(np.min(wl_low)), np.log10(np.max(wl_up)), 50000
    )

    



    # Create master dictionary, which will have an entry for each 
    # molecule in each shock.
    # 
    # master['shock1'] = {
    #   'co': {'$^{12}$CO $1-0$': [wavelengths,line strengths,...],
    #   '13co': {'$^{12}$CO $1-0$': [wavelengths,line strengths,...]},...
    # }
    master = {}
    
    # Create empty array of molecule dependent radex input
    # column:  Average column density of emitting species [cm^-2]

    labs_ord = {}
    # Loop over each molecule
    for molecule in mol_list:
        rad_mol = molecule.lower()
        if molecule == 'h2': continue
        # Compute the column density of emitting species in each slab
                
        
        
        # Call radex reader to get dictionary of outputs for each slab
        # Output of the Rread function is a dictionary with the 
        # following keys that each give a list (of the same length):
        #
        # 'energy': energy of upper level [K]
        # 'frequency': frequency [GHz]
        # 'wavelength': wavelength [um]
        # 'excitation_temperature': excitation temperature [K]
        # 'optical_depth': optical depth
        # 'radiation_temperature': antenna temperature [K]
        # 'flux_K': velocity integrated line strength in K km/s
        # 'flux_erg': velocity integrated line strength in erg/cm^2/s
        # 'upper': upper level of transition
        # 'lower': lower level of transition
        rdx = [
            radex_reader(rad_mol, freq_low, freq_up, Tkin[y], num_partners,
                partner, nH_avg[y], T_back, column[molecule][y],
                delv[y], calc_param)
            for y in xrange(slabs)
        ]
        
        #for thing in rdx[0]:
        #    print thing, len(rdx[0][thing])

        upper = [rdx[y]['upper'] for y in xrange(slabs)]
        tau = [rdx[y]['optical_depth'] for y in xrange(slabs)]
        energy = [rdx[y]['energy'] for y in xrange(slabs)]
        wavelength = [rdx[y]['wavelength'] for y in xrange(slabs)]
        frequency = [rdx[y]['frequency'] for y in xrange(slabs)]

        # Line strength can have units of antenna temperature (K)
        # or flux (K km/s or erg/cm2/s)

        temp = [
            (beamsize/4/np.pi)*rdx[y]['flux_K'] 
            for y in xrange(slabs)
        ]

        ###### DATA DUMP: each slab ######
        for y in xrange(slabs):
            headers = [
                'UpperJ', 
                'Wavelength(um)', 
                'Frequency(GHz)', 
                'tau', 
                intensity
            ]
            
            data = [
                upper[y][::-1], 
                wavelength[y][::-1], 
                frequency[y][::-1], 
                tau[y][::-1], 
                temp[y][::-1]
            ]
            
            slab_table = Table(data, names=headers, meta={'name': 'Spectrum'})
            
            slab_table_path = pth.join(output_loc, 'table_' + molecule + '_s' + str(y+1) + '.dat')
            slab_table.write(slab_table_path, format='ascii')
            print 'Data table written to: ', slab_table_path


        # Sum up the slab contributions and put it in master dictionary
        master[molecule], labs_ord[molecule] = slab_sum(
            wavelength,
            temp,
            upper,
            energy,
            frequency,
            tau,
            background
        )
        
        
        
    
#######################################################################
################### COMPUTATIONAL BLOCK COMPLETE ######################
#######################################################################












#######################################################################
############################ OUTPUT BLOCK #############################
#######################################################################

    ###### DATA DUMP: astropy ascii table ######
    output = {}
    
    for molecule in mol_list:
        
        line_names = []
        master_wave = []
        master_freq = []
        master_line = []
        master_tau = []
        
        for key in master[molecule].keys():
        
            line_names.append(key)
            master_wave.append(master[molecule][key][0])
            master_freq.append(master[molecule][key][3])
            master_line.append(master[molecule][key][1])
            master_tau.append(master[molecule][key][4])

        line_names = np.array(line_names)[np.argsort(master_freq)]
        master_wave = np.array(master_wave)[np.argsort(master_freq)]
        master_line = np.array(master_line)[np.argsort(master_freq)]
        master_tau = np.array(master_tau)[np.argsort(master_freq)]
        master_freq = np.array(master_freq)[np.argsort(master_freq)]
        
        headers = [
            'UpperJ', 
            'Wavelength(um)', 
            'Frequency(GHz)', 
        #    'tau', 
            intensity
        ]
        
        master_data = [
            line_names, 
            master_wave, 
            master_freq, 
        #    master_tau, 
            master_line
        ]
        
        master_table = Table(master_data, names=headers, meta={'name': 'Spectrum'})
        output[molecule]=master_table

        master_table_path = pth.join(output_loc, 'table_' + molecule + '.dat')
        master_table.write(master_table_path, format='ascii')
        print 'RADEX line table written to: ' + master_table_path

    return output
    '''

    ### TERMINAL: SLAB RADEX PARAMETERS ###
    if not quiet:
        print '----------------------------------------'
        print '- SHOCK PATH: ' + args.directories[x]
        print '----------------------------------------'        
        
        for mol in mol_list:
            if mol == 'h2': continue
            print ' '
            print '    Radiating molecule: ' + mol.upper()
            print '    Collisional partner: ' + partner
            print '    Background temperature:', T_back
            print ' '
            
            for y in xrange(slabs):
                print '    ------------'
                print '       SLAB ' + str(y+1)
                print '    ------------'
                print '        Kinetic temperature: ' + '%.1f' %Tkin[y] + ' K'
                print '        ' + mol.upper() + ' column density: ' + '%.1e' %column[mol][y] + ' cm^-2'
                print '        ' + partner + ' density: ' + '%.1e' %nH[y] + ' cm^-3'
                print '        Linewidth: ' + '%.2f' %delv[y] + ' km/s'
                
            print '    ----------------------------------------'
        print '============================================'
    #######################
        


    ### PARAMETER FILE ###
    with open(
        output_loc + '/parameters.dat','w') as f:
        f.write('---------------------------------------- \n')
        f.write('- SHOCK PATH: ' + args.directories[x] + '\n')
        f.write('---------------------------------------- \n')
        
        for mol in mol_list:
            if mol == 'h2': continue
        
            f.write('\n')
            f.write('    Radiating molecule: ' + mol.upper() + '\n')
            f.write('    Collisional partner: ' + partner + '\n')
            f.write('    Background temperature:' + str(T_back) + ' \n')
            f.write('\n')
    
            for y in xrange(slabs):
                f.write('    ------------ \n')
                f.write('       SLAB ' + str(y+1) + '\n')
                f.write('    ------------ \n')
                f.write('        Kinetic temperature: ' + '%.1f' %Tkin[y] + ' K \n')
                f.write('        ' + mol.upper() + ' column density: ' + '%.1e' %column[mol][y] + ' cm^-2 \n')
                f.write('        H-nuclei column density: ' + '%.1e' %NH_col[y] + ' cm^-2 \n')
                f.write('        ' + partner + ' density: ' + '%.1e' %nH[y] + ' cm^-3 \n')
                f.write('        Linewidth: ' + '%.2f' %delv[y] + ' km/s \n')
            
            f.write( '---------------------------------------- \n')
        f.write( '======================================== \n')
            
    print 'RADEX input parameters: ' + output_loc + '/parameters.dat'
    #######################







    ###### DATA DUMP: latex table ######
    with open(
        output_loc + '/' + cparser.get(
                'Files', 'outfile') + '.tex','w') as f:

        # Write latex preamble
        f.write('\\documentclass[12pt]{report}\n')
        f.write('\\usepackage{amsfonts}\n')
        f.write('\\usepackage{amsmath}\n')
        f.write('\\usepackage{amssymb}\n')
        f.write('\\usepackage{graphicx}\n')
        f.write('\\newcommand{\\kps}{\\text{ km s}^{-1}}\n')
        f.write('\n')
        f.write('\n')

        # Being latex document
        f.write('\\begin{document}\n')
        f.write('\n')
        f.write('\n')

        # Create table
        f.write('\\begin{table} \n')
        f.write('\\centering \n')
        f.write('\\caption{Shock ' + str(x+1) + ' output.} \n')
        f.write('\\begin{tabular}{l l l l} \hline\hline \n')

        # Headers. Depends on unit choice.
        f.write('Line & Wavelength & Frequency & Line Flux \\\ \n')
        f.write(' & ($\\mu$m) & (GHz) & (K km/s) \\\ \hline \n')


        # Loop through each molecule
        for mol in mol_list:
            if mol == 'h2': continue
            for key in labs_ord[mol]:
                    f.write('{0:s} & {1:.2f} & {2:.2f} & {3:.2e}'.format(
                        key,
                        master[mol][key][0], 
                        master[mol][key][3],
                        master[mol][key][1]
                        ) + '\\\ \n'
                    )
        
            f.write('\hline \n')

        f.write('\\end{tabular}\n')
        f.write('\end{table} \n')
        f.write('\n')
        f.write('\n')

        f.write('\\end{document}\n')
    print 'Latex table: ' + output_loc + '/' + cparser.get('Files', 'outfile') + '.tex'
    #######################







    ########### SLAB PLOTS ##############
    # Plot slab boundary figures, so user can see if they were reasonable
    fig_bound = plt.figure(figsize = (7,12))
    gs = gridspec.GridSpec(3, 1)   
    gs.update(left=0.15, right=0.95, bottom = 0.05, top = 0.95, wspace=0.1,hspace=0.0)


    # Pressure plot        
    p_low, p_up = y_cropper(pressure, 3.0/4.0, 'log')
    
    ax = fig_bound.add_subplot(gs[0:1,0:1])
    plt.title('SHOCK: ' + args.directories[x], fontsize = 20)
    ax.plot(z[0:len(pressure)], pressure)
    
    for y in xrange(0,slabs+1):
        ax.axvline(x=boundary[y], color = 'black', linewidth = 2, ls = '--')
        
    for y in xrange(0,slabs):
        ax.annotate(
            '', xy=(boundary[y], 0.6*p_up), xytext = (boundary[y]+dist[y],0.6*p_up),
            arrowprops = {'arrowstyle':'<->'}
            )
        ax.text(boundary[y]+dist[y]/2.0, 0.7*p_up, str(y+1))
        
    ax.set_yscale('log')
    ax.axis([leftz, rightz, p_low, p_up])
    ax.set_ylabel(r'$\mathrm{Gas \, Pressure \, (dyne/cm}^2)$', fontsize = 20)
    plt.setp(ax.get_xticklabels(), visible=False)
    ax.tick_params(which = 'major', length=10, width = 2)
    ax.tick_params(which = 'minor', length=5, width = 2)
    [var.set_linewidth(2) for var in ax.spines.itervalues()]
        
        
    ### Temperature
    temp_low, temp_up = y_cropper(T, 3.0/4.0, 'log')
    
    ax = fig_bound.add_subplot(gs[1:2,0:1])
    
    ax.plot(z[0:len(T)], T, color = 'red')
    ax.set_yscale('log')
    
    for y in xrange(0,slabs+1):
        ax.axvline(x=boundary[y], color = 'black', linewidth = 2, ls = '--')
        
        
    ax.axis([leftz, rightz, temp_low, temp_up])
    ax.set_ylabel(r'$\mathrm{Temperature \, (K)}$', fontsize = 20)
    plt.setp(ax.get_xticklabels(), visible=False)
    ax.tick_params(which = 'major', length=10, width = 2)
    ax.tick_params(which = 'minor', length=5, width = 2)
    [var.set_linewidth(2) for var in ax.spines.itervalues()]


    ### Density
    nH_low, nH_up = y_cropper(density, 3.0/4.0, 'log')
    
    ax = fig_bound.add_subplot(gs[2:3,0:1])
    
    ax.plot(z[0:len(vnz)], density)
    ax.set_yscale('log')
    
    for y in xrange(0,slabs+1):
        ax.axvline(x=boundary[y], color = 'black', linewidth = 2, ls = '--')
        
        
    ax.axis([leftz, rightz, nH_low, nH_up])
    ax.set_xlabel(r'$\mathrm{z \, (cm)}$', fontsize = 20)
    ax.set_ylabel(r'$n_\mathrm{H} \mathrm{\, (cm}^{-3})$', fontsize = 20)
    ax.tick_params(which = 'major', length=10, width = 2)
    ax.tick_params(which = 'minor', length=5, width = 2)
    [var.set_linewidth(2) for var in ax.spines.itervalues()]
    ###########
     

    if not quiet: plt.show(block=False)

    # Save slab figures
    fig_bound.savefig(output_loc + '/slab_def.' + image_type, type = image_type, transparent = False)
    if quiet: plt.close(fig_bound)
    print 'Slab definition: ' + output_loc + '/slab_def.' + image_type
    ####################################

   
   
   
    ###### DATA DUMP: fluxes ######
    with open(output_loc + '/flux.dat','w') as f:
        f.write('{0:1s} {1:1s} {2:1s} {3:1s} {4:1s} {5:1s} {6:1s}'.format(
            'shock', 'vs', 'F(CO) (erg/s/cm^2)', 'F(H2) (erg/s/cm^2)', 
            'F(H2O) (erg/s/cm^2)', 'z1 (cm)', 'z2 (cm)'
            ) + '\n'
        )
        
        f.write('{0:1s} {1:1f} {2:1e} {3:1e} {4:1e} {5:1e} {6:1e}'.format(
                cparser.get('Files', 'outfile'), 
                vshock, flux['co'], flux['h2'], flux['h2o'], 
                boundary[0], boundary[-1]) + '\n'
            )
            
    print 'Flux values written to: ' + output_loc + '/flux.dat'
    
    
    
    headers = ['Shock', 'Vs (km/s)', 'F(CO) (erg/s/cm^2)', 'F(H2) (erg/s/cm^2)', 
            'F(H2O) (erg/s/cm^2)', 'z1 (cm)', 'z2 (cm)']
        
    t = Table([[cparser.get('Files', 'outfile')], 
                [vshock], [flux['co']], [flux['h2']], [flux['h2o']], 
                [boundary[0]], [boundary[-1]]], names=headers, meta={'name': 'Fluxes'})

    t.write(output_loc + '/table_fluxes.dat', format='ascii')
    print 'Data table: ' + output_loc + '/table_fluxes.dat'
    #######################
    


    
    
    if 'h2' not in mol_list:
        ###### DATA DUMP: 12CO optical depths ######
        np.savetxt(output_loc + '/tauCO.dat', np.transpose(tau_labs[x]['co']), fmt='%s %s')
        np.savetxt(output_loc + '/tau13CO.dat', np.transpose(tau_labs[x]['13co']), fmt='%s %s')
        np.savetxt(output_loc + '/tauOH2O.dat', np.transpose(tau_labs[x]['oh2o']), fmt='%s %s')
        np.savetxt(output_loc + '/tauPH2O.dat', np.transpose(tau_labs[x]['ph2o']), fmt='%s %s')
                
        print 'CO optical depth values written to: ' + output_loc + '/tauCO.dat'
        print '13CO optical depth values written to: ' + output_loc + '/tau13CO.dat'
        print 'oH2O optical depth values written to: ' + output_loc + '/tauOH2O.dat'
        print 'pH2O optical depth values written to: ' + output_loc + '/tauPH2O.dat'
        #######################
    
        

    print ''
    print '---------------========***========----------------'
    print '--------------- Have a nice day!  ----------------'
    print '---------------========***========----------------'
    '''

###############################################################################################    
