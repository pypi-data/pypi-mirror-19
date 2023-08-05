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

###################################################
def equilibrium_derivs(z, y, dydz, comps):
    '''
    RHS function for equilibrium ODE solver.

    '''
    from numpy import (log, log10)
    from lehmann_astrochemistry.heating import specific_heat
    from lehmann_astrochemistry.chemistry import chem_rates
    from lehmann_astrochemistry.cooling import n_eff

    #if not comps['quiet']:
    #    print 't={0:.3f} years'.format(z/(365.25*24.*60.*60.))

    dens = {
        key: comps['nH']*10.**y[comps['reactions'][key]['order']+1]
        for key in comps['reactions'].keys()
    }
    
    xM={
        key: 10.**y[comps['reactions'][key]['order']+1]
        for key in comps['reactions'].keys()
    }
    

    dens['e-'] = 0
    xM['e-']=0
    for key in dens:
        if key[-1] == '+':
            dens['e-']+=dens[key]
            xM['e-']+=xM[key]
        if log10(dens[key]) < -100.:
            dens[key] = 1.e-100
            xM[key]=dens[key]/comps['nH']
     
    H2_info = {
        'b' : comps['doppler_b'],
        'uv_field': comps['uv_field'],
        'incidence_factor': comps['f_incidence']
    }
    
    energy=y[0]
    
    temps = {
        'neutral': energy/specific_heat(xM),
        'dust': comps['temps']['dust']
    }
    temps['ion'] = temps['neutral']
    temps['electron'] = temps['neutral']
    
    # reaction rate dictionary
    rate = chem_rates(dens, temps, comps['reaction_types'], comps['reactions'], comps['NH'], H2_info, cr_rate=comps['zeta'], extinction=comps['Av'])
    for key in rate.keys():
        dydz[comps['reactions'][key]['order']+1] = rate[key]/log(10.)/dens[key]

    # temperature derivative
    if not comps['isothermal']:
        # Total cooling (per H nuclei)        
        Lm=0
        for func in comps['cool_funcs']:
            if func[0] == 'dust':
                Lm+=func[1](comps['nH'], temps['neutral'], temps['dust'], comps['Sdust'])/comps['nH']
            else:
                if func[2]=='r':
                    n_effective = n_eff(func[0], comps['nH']*xM['H2'], comps['nH']*xM['H'], dens['e-'], temps['neutral'])
                elif func[2]=='v':
                    n_effective = n_eff(func[0], comps['nH']*xM['H2'], comps['nH']*xM['H'], dens['e-'], temps['neutral'])
                else:
                    n_effective = comps['nH']*xM['H2']
                    
                Lm+=xM[func[0][:-1]]*func[1](n_effective, log10(temps['neutral']))
        ###################################




        # Total heating (per H nuclei)     
        G=0
        for func in comps['heat_funcs']:
            if func[0]=='CR_K14':
                G+=func[1](comps['zeta'], comps['nH'], xM['H'], xM['H2'], xM['e-'])/comps['nH']
                #print 'G(CR_K14): %.3e erg/s/H' %(func[1](comps['zeta'], comps['nH'], xM['H'], xM['H2'], xM['e-'])/comps['nH'])
            elif func[0]=='PE_K14':
                G+=func[1](comps['NH'], chi=comps['uv_field'])/comps['nH']
            elif func[0]=='PE_W03':
                G+=func[1](dens['H'], dens['e-'], temps['neutral'], comps['Av'], G0=comps['uv_field'])/comps['nH']
                #print 'G(PE_W03): %.3e erg/s/H' %(func[1](dens['H'], dens['e-'], temps['neutral'], comps['Av'], G0=comps['uv_field'])/comps['nH'])
            elif func[0]=='H2FORM_HM79':
                G+=func[1](comps['nH'], xM['H'], xM['H2'], temps['neutral'], temps['dust'])/comps['nH']
                #print 'G(H2FORM_HM79): %.3e erg/s/H' %(func[1](comps['nH'], xM['H'], xM['H2'], temps['neutral'], temps['dust'])/comps['nH'])
            elif func[0]=='H2DISS_MS04':
                G+=func[1](comps['uv_field'], comps['Av'], comps['NH']*xM['H2'])/comps['nH']
                #print 'G(H2DISS_MS04): %.3e erg/s/H' %(func[1](comps['uv_field'], comps['Av'], comps['NH']*xM['H2'])/comps['nH'])
        ###################################
        
        
        if (temps['neutral'] <= 9.) and (G-Lm) < 0:
            dydz[0]=0
        else:
            dydz[0]=G-Lm
    else:
        dydz[0]=0
###################################################















    
###################################################
def equilibrium(
        chem_list,
        logtime,
        steps,
        temps,
        params,
        reaction_types,
        cool_funcs=None,
        heat_funcs=None,
        CVODE_params=None,
        quiet=False
    ):
    '''
    logtime=9,
    steps=1000,
    temps = {
        'neutral': 10.,
        'ion': 10.,
        'electron': 10.,
        'dust': 10.
        },
    params={
        'nH' : 1.e3,
        'Sdust': 0.1e-6*1.0e2,
        'cr_rate' : 2.e-16, 
        'extinction' : 10.,
        'uv_field' : 1.0,
        'cloud_fwhm': 1.0,
        'incidence_factor': 0.5,
        'isothermal': True
        },
    reaction_types={
        'NN': True, # Neutral-neutral (done)
        'IN': True, # Ion-neutral (done)
        'DR': True, # Dissociative recombination (done)
        'CP': True,  # Direct cosmic-ray proton dissociation/ionization (done)
        'RR': True, # Radiative recombination (done)
        'RA': True, # Radiative association (done)
        'PH': True, # Direct photo dissociation/ionization (done)
        'CR': True, # Indirect cosmic-ray photo dissocation/ionization (prasad-tarafdar) (done)
        'AD': True,  # Associative detachment (done)
        'DG': True,  # Reactions on dust grains (done)
        'H2D': True  # Dissociation of molecular hydrogen (done)
        },
    cool_funcs=None,
    heat_funcs=None,
    quiet=False
    '''
    from numpy import zeros, logspace, array, log10
    from scikits.odes import ode
    from lehmann_astrochemistry.heating import specific_heat
    from lehmann_astrochemistry.chemistry import doppler_factor

    if not quiet:
        print
        print ' EQUILIBRIUM!'
        print

    y0 = zeros(len(chem_list.keys())+1)
    xM={}
    if not quiet:
        print '------------------------------------------'
        print
        print ' (log10 of) Initial Abundances'
    for key in chem_list.keys():
        y0[chem_list[key]['order']+1] = log10(chem_list[key]['init'])
        xM[key]= chem_list[key]['init']
        if not quiet:
            print '  {0:s}: {1:.3f}'.format(key, y0[chem_list[key]['order']+1])
    if not quiet:
        print '------------------------------------------'
    
    #y0[0]=log10(temps['neutral']) # zeroth variable is temperature
    #y0[0]=log10(specific_heat(xM)*temps['neutral']) # zeroth variable is gas energy
    y0[0]=specific_heat(xM)*temps['neutral'] # zeroth variable is gas energy
    
    
    comps={
        'temps' : temps,
        'reactions' : chem_list,
        'nH' : params['nH'],
        'Sdust' : params['Sdust'],
        'zeta' : params['cr_rate'], 
        'Av' : params['extinction'],
        'NH' : params['columnH'],
        'uv_field' : params['uv_field'],
        'doppler_b':  doppler_factor(params['cloud_fwhm']),
        'f_incidence': params['incidence_factor'],
        'reaction_types': reaction_types,
        'isothermal': params['isothermal'],
        'cool_funcs': cool_funcs,
        'heat_funcs': heat_funcs,
        'quiet': quiet
    }
    
    
    times = logspace(0., logtime, steps)
    if CVODE_params == None:
        max_steps = 50000
        min_step_size = 0.0
    else:
        max_steps = CVODE_params['max_steps']
        min_step_size = CVODE_params['min_step_size']
    
    solver = ode('cvode', equilibrium_derivs, user_data=comps, max_steps=max_steps, min_step_size= min_step_size)
    result = solver.solve(times*365.25*24.*60.*60., y0)

    sol_length=len(result[2])
    
    solution={
        'times': times[:sol_length]
    }
    
    xe=zeros(sol_length)
    
    for species in chem_list:
        solution['{0:s}'.format(species)]=10.**array([result[2][i][chem_list[species]['order']+1] for i in xrange(sol_length)])
        
        if species[-1] == '+':
            xe += array(solution[species][:sol_length])
    solution['e-']=xe
        
    energy= array([result[2][i][0] for i in xrange(sol_length)])
    
    temp=[]
    degrees_list=['H','H2','H+','He','He+','e-']
    
    for i in xrange(len(energy)):
        xM={}
        for species in degrees_list:
            if species in solution.keys():
                xM[species] = solution[species][i]
        
        temp.append(energy[i]/specific_heat(xM))
        
    solution['temperature']=temp
    
    return solution
###################################################
