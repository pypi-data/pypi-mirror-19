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
def initialise(rates, abundances):
    '''
    Returns a dictionary of reaction rates and initial abundances.
    
    Parameters
    ----------
    rates : str
        rates file absolute path
    abundances : str
        abundances file absolute path
        
    Output:
        - dictionary of the form:
        
    chemistry = {
        'H': {
            'formation_2B': [
                ['O', 'H2', 3.13e-13, 2.70, 3150.0],
                ['OH', 'H2', 6.99e-14, 2.80, 1950.0]
            ],
            'formation_PD': [
                ['O', 'H2', 3.13e-13, 2.70, 3150.0],
                ['OH', 'H2', 6.99e-14, 2.80, 1950.0]
            ],
            'destruction_2B': [
                ['OH', 6.99e-14, 2.80, 1950.0],
                ['H', 1.59e-11, 1.20, 9160.0]
            ]
        },
        ... other species
    }
    
        for each species, there should be 2 body formation and
        destruction rate coefficients in entries 'formation_2B' and
        'destruction_2B', 
    '''
    from astropy.table import Table
    from numpy import append, where, intersect1d
    
    
    # Read in files
    reaction_headers = [
        'index',
        'reactant1',
        'reactant2',
        'blank1',
        'product1',
        'product2',
        'product3',
        'blank2',
        'alpha',
        'beta',
        'gamma',
        'source',
        'temp_low',
        'temp_up',
        'error',
        'blank3'
    ]
    
    rate_table = Table.read(rates, format = 'ascii', names=reaction_headers, fast_reader=False)
    abundances_table = Table.read(abundances, format = 'ascii')
    #print rate_table
    
    species_list = [x for x in abundances_table['col2']]
    try:
        species_list.remove('e-')
    except:
        pass
        
    photon_all = append(where(rate_table['reactant1'] == 'PHOTON')[0], where(rate_table['reactant2'] == 'PHOTON')[0])
    crphot_all = append(where(rate_table['reactant1'] == 'CRPHOT')[0], where(rate_table['reactant2'] == 'CRPHOT')[0])
    crp_all = append(where(rate_table['reactant1'] == 'CRP')[0], where(rate_table['reactant2'] == 'CRP')[0])
    
    notphot = intersect1d(where(rate_table['reactant1'] != 'PHOTON')[0], where(rate_table['reactant2'] != 'PHOTON')[0])
    notcr = intersect1d(where(rate_table['reactant1'] != 'CRPHOT')[0], where(rate_table['reactant2'] != 'CRPHOT')[0])
    notcrp = intersect1d(where(rate_table['reactant1'] != 'CRP')[0], where(rate_table['reactant2'] != 'CRP')[0])
    twobody = intersect1d(intersect1d(notphot,notcr),notcrp)
    
    reactions = {}
    
    # Set up the dictionary, where each entry is for a chemical species
    for i,species in enumerate(species_list):
    
        init = abundances_table['col3'][where(abundances_table['col2']==species)[0]]
        
        reactions[species] = {
            'order': i,
            'init': float(init),
            'protons': abundances_table['col4'][where(abundances_table['col2']==species)[0]][0],
            'form_NN': [], # formation via neutral-neutral reactions
            'form_IN': [], # formation via ion-neutral reactions
            'form_CE': [], # formation via charge exchange reactions
            'form_DR': [], # formation via dissociative recombination reactions
            'form_RR': [], # formation via radiative recombination reactions
            'form_RA': [], # formation via radiative association reactions
            'form_PH': [], # formation via photon process reactions
            'form_CP': [], # formation via direct cosmic ray reactions
            'form_CR': [], # formation via cosmic ray induced photon reactions
            'form_AD': [], # formation via associative detachment reactions
            'destr_NN': [], # destruction via neutral-neutral reactions
            'destr_IN': [], # destruction via ion-neutral reactions
            'destr_CE': [], # destruction via charge exchange reactions
            'destr_DR': [], # destruction via dissociative recombination reactions
            'destr_RR': [], # destruction via radiative recombination reactions
            'destr_RA': [], # destruction via radiative association reactions
            'destr_PH': [], # destruction via photon process reactions
            'destr_CP': [], # destruction via direct cosmic ray reactions
            'destr_CR': [], # destruction via cosmic ray induced photon reactions
            'destr_AD': [], # destruction via associative detachment reactions
            'form_DG': [], # formation on dust grains
            'destr_DG': [], # destruction on dust grains
            'form_H2D': [], # formation of H by H2 photodissociation
            'destr_H2D': [] # destruction of H2 by photodissociation
        }



    # Initialise the electron number density by adding up the ions
    '''
    ne_0 = 0
    for species in species_list:
        if species[-1] == '+':
            ne_0 += reactions[species]['init']
    reactions['e-']['init'] = ne_0
    '''




    # ASSUMPTION: photon, crp and crphoton reactions are written in the
    # forms:
    #   A + PHOTON -> products  (photodissociation)
    #   A + PHOTON -> B + e-  (photoionisation)
    #   A + CRP -> products (direct cosmic ray ionisation/dissociation)
    #   A + CRPHOT -> products (prasad & tarafdar mechanism)
    #   A + e- -> products (dissociative/radiative recombination)
    # 
    # i.e., the non-molecule reactant is in the second position. you
    # must edit the code below if this isn't the case!
    
   
    
    for reaction in rate_table:
        if reaction[3] == '#':
            # ignore one particular reaction H+H->H2, because I think
            # it's a grain reaction and I don't know what to do with it  
            #continue

            ## EXPERIMENTAL DUST REACTION HERE
            reactions[reaction[1]]['destr_DG'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                    
            reactions[reaction[2]]['destr_DG'].append({
                    'reactants':[reaction[1],reaction[2]],
                    'products':[reaction[4], reaction[5], reaction[6]],
                    'coeffs': [reaction[8], reaction[9], reaction[10]],
                    'Trange': [reaction[12],reaction[13]],
                    'Tcheck': False
                })
                
            reactions[reaction[4]]['form_DG'].append({
                    'reactants':[reaction[1],reaction[2]],
                    'products':[reaction[4], reaction[5], reaction[6]],
                    'coeffs': [reaction[8], reaction[9], reaction[10]],
                    'Trange': [reaction[12],reaction[13]],
                    'Tcheck': False
                })
            
            if reaction[5] != '#':
                reactions[reaction[5]]['form_DG'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
    ### PHOTON PROCESSES
        elif reaction[2] == 'PHOTON':
            # this reaction destroys the molecule by photodissociation 
            # or photoionisation. we need only the 2 reaction rate 
            # coefficients
        
            if reaction[5] == 'e-':
                # Photoionization case
                reactions[reaction[1]]['destr_PH'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })            
                
                reactions[reaction[4]]['form_PH'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                    
                if (reaction[6] and reaction[6]!='e-'):
                    reactions[reaction[6]]['form_PH'].append({
                            'reactants':[reaction[1],reaction[2]],
                            'products':[reaction[4], reaction[5], reaction[6]],
                            'coeffs': [reaction[8], reaction[9], reaction[10]],
                            'Trange': [reaction[12],reaction[13]],
                            'Tcheck': False
                        })
            ## H2 photodissociation is special case
            elif reaction[1]=='H2':
                reactions[reaction[1]]['destr_H2D'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })            
                
                reactions[reaction[4]]['form_H2D'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })            
                
                reactions[reaction[5]]['form_H2D'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
            else:
                # Photodissociation case
                reactions[reaction[1]]['destr_PH'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })            
                
                reactions[reaction[4]]['form_PH'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                    
                reactions[reaction[5]]['form_PH'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                    
                if (reaction[6] and reaction[6]!='e-'):
                    reactions[reaction[6]]['form_PH'].append({
                            'reactants':[reaction[1],reaction[2]],
                            'products':[reaction[4], reaction[5], reaction[6]],
                            'coeffs': [reaction[8], reaction[9], reaction[10]],
                            'Trange': [reaction[12],reaction[13]],
                            'Tcheck': False
                        })
                 
    ### DIRECT COSMIC RAY PROCESSES   
        elif reaction[2] == 'CRP':
            # this reaction destroys the molecule by direct cosmic ray
            # dissociation or ionisation. we need only the 1 reaction 
            # rate coefficient
            
            if reaction[5] == 'e-':
                # Ionization case
                reactions[reaction[1]]['destr_CP'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                
                reactions[reaction[4]]['form_CP'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                
                if reaction[6]:
                    reactions[reaction[6]]['form_CP'].append({
                            'reactants':[reaction[1],reaction[2]],
                            'products':[reaction[4], reaction[5], reaction[6]],
                            'coeffs': [reaction[8], reaction[9], reaction[10]],
                            'Trange': [reaction[12],reaction[13]],
                            'Tcheck': False
                        })
            else:
                # Dissociation case
                reactions[reaction[1]]['destr_CP'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                
                reactions[reaction[4]]['form_CP'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                
                reactions[reaction[5]]['form_CP'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                
                if reaction[6] and (reaction[6] != 'e-'):
                    reactions[reaction[6]]['form_CP'].append({
                            'reactants':[reaction[1],reaction[2]],
                            'products':[reaction[4], reaction[5], reaction[6]],
                            'coeffs': [reaction[8], reaction[9], reaction[10]],
                            'Trange': [reaction[12],reaction[13]],
                            'Tcheck': False
                        })



            
    ### SECONDARY COSMIC RAY PROCESSES (Prasad & Tarafdar mechanism)
        elif reaction[2] == 'CRPHOT':
            # this reaction destroys the molecule by cosmic ray induced
            # photodissociation or photoionisation. we need the 3 
            # reaction rate coefficients
            
            
            if reaction[5] == 'e-':
                # Ionization case
                reactions[reaction[1]]['destr_CR'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                
                reactions[reaction[4]]['form_CR'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                
                if reaction[6]:
                    reactions[reaction[6]]['form_CR'].append({
                            'reactants':[reaction[1],reaction[2]],
                            'products':[reaction[4], reaction[5], reaction[6]],
                            'coeffs': [reaction[8], reaction[9], reaction[10]],
                            'Trange': [reaction[12],reaction[13]],
                            'Tcheck': False
                        })
            else:
                # Dissociation case
                reactions[reaction[1]]['destr_CR'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                
                reactions[reaction[4]]['form_CR'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                
                reactions[reaction[5]]['form_CR'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                
                if reaction[6]:
                    reactions[reaction[6]]['form_CR'].append({
                            'reactants':[reaction[1],reaction[2]],
                            'products':[reaction[4], reaction[5], reaction[6]],
                            'coeffs': [reaction[8], reaction[9], reaction[10]],
                            'Trange': [reaction[12],reaction[13]],
                            'Tcheck': False
                        })
        
        ### RECOMBINATION PROCESSES
        elif reaction[2] == 'e-':
            # this reaction destroys the molecule by radiative or
            # dissociative recombination. we need the 3 reaction rate 
            # coefficients for the 2 body rate. there may be 3 products
            # in the recombination case, so we check for that
            
            # if a photon is in the products, then it is radiative
            # recombination, otherwise it is dissociative. for 
            # formation by radiative recombination, we need the 
            # reacting partner (not e-).
            if reaction[5] == 'PHOTON':
                
                reactions[reaction[1]]['destr_RR'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                
                reactions[reaction[4]]['form_RR'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                
                if reaction[6]:
                    reactions[reaction[6]]['form_RR'].append({
                            'reactants':[reaction[1],reaction[2]],
                            'products':[reaction[4], reaction[5], reaction[6]],
                            'coeffs': [reaction[8], reaction[9], reaction[10]],
                            'Trange': [reaction[12],reaction[13]],
                            'Tcheck': False
                        })

            else:
                
                if reaction[5] == 'e-':
                    # THE ONE GODDAMN REACTION THAT THIS HAPPENS MUST BE ACCOUNTED FOR
                    reactions[reaction[1]]['destr_DR'].append({
                            'reactants':[reaction[1],reaction[2]],
                            'products':[reaction[4], reaction[5], reaction[6]],
                            'coeffs': [reaction[8], reaction[9], reaction[10]],
                            'Trange': [reaction[12],reaction[13]],
                            'Tcheck': False
                        })
                    
                    
                    reactions[reaction[4]]['form_DR'].append({
                            'reactants':[reaction[1],reaction[2]],
                            'products':[reaction[4], reaction[5], reaction[6]],
                            'coeffs': [reaction[8], reaction[9], reaction[10]],
                            'Trange': [reaction[12],reaction[13]],
                            'Tcheck': False
                        })
                    
                    if reaction[6]:
                        reactions[reaction[6]]['form_DR'].append({
                                'reactants':[reaction[1],reaction[2]],
                                'products':[reaction[4], reaction[5], reaction[6]],
                                'coeffs': [reaction[8], reaction[9], reaction[10]],
                                'Trange': [reaction[12],reaction[13]],
                                'Tcheck': False
                            })
                
                else:
                    reactions[reaction[1]]['destr_DR'].append({
                            'reactants':[reaction[1],reaction[2]],
                            'products':[reaction[4], reaction[5], reaction[6]],
                            'coeffs': [reaction[8], reaction[9], reaction[10]],
                            'Trange': [reaction[12],reaction[13]],
                            'Tcheck': False
                        })
                    
                    
                    reactions[reaction[4]]['form_DR'].append({
                            'reactants':[reaction[1],reaction[2]],
                            'products':[reaction[4], reaction[5], reaction[6]],
                            'coeffs': [reaction[8], reaction[9], reaction[10]],
                            'Trange': [reaction[12],reaction[13]],
                            'Tcheck': False
                        })
                    reactions[reaction[5]]['form_DR'].append({
                            'reactants':[reaction[1],reaction[2]],
                            'products':[reaction[4], reaction[5], reaction[6]],
                            'coeffs': [reaction[8], reaction[9], reaction[10]],
                            'Trange': [reaction[12],reaction[13]],
                            'Tcheck': False
                        })
                    
                    if reaction[6] and (reaction[6] != 'e-'):
                        reactions[reaction[6]]['form_DR'].append({
                                'reactants':[reaction[1],reaction[2]],
                                'products':[reaction[4], reaction[5], reaction[6]],
                                'coeffs': [reaction[8], reaction[9], reaction[10]],
                                'Trange': [reaction[12],reaction[13]],
                                'Tcheck': False
                            })



        ### RADIATIVE ASSOCIATION
        elif reaction[5] == 'PHOTON':
            # If PHOTON is amongst the products, then we have radiative
            # recombination or association. We already took care of the
            # recombination case, so we assume that only association is
            # left. This is a two-body reaction, so we need the 
            # reactants and the 3 rate coefficients (formation case) or
            # just 1 reactant and 3 rate coefficients (destr. case).                
            reactions[reaction[1]]['destr_RA'].append({
                    'reactants':[reaction[1],reaction[2]],
                    'products':[reaction[4], reaction[5], reaction[6]],
                    'coeffs': [reaction[8], reaction[9], reaction[10]],
                    'Trange': [reaction[12],reaction[13]],
                    'Tcheck': False
                })
                
            reactions[reaction[2]]['destr_RA'].append({
                    'reactants':[reaction[1],reaction[2]],
                    'products':[reaction[4], reaction[5], reaction[6]],
                    'coeffs': [reaction[8], reaction[9], reaction[10]],
                    'Trange': [reaction[12],reaction[13]],
                    'Tcheck': False
                })
                
            reactions[reaction[4]]['form_RA'].append({
                    'reactants':[reaction[1],reaction[2]],
                    'products':[reaction[4], reaction[5], reaction[6]],
                    'coeffs': [reaction[8], reaction[9], reaction[10]],
                    'Trange': [reaction[12],reaction[13]],
                    'Tcheck': False
                })
                
            if reaction[6]:
                reactions[reaction[6]]['form_RA'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })





        ### ASSOCIATIVE DETACHMENT
        elif reaction[5] == 'e-':
            # One more case exists with an electron product, that is
            # the associative detachment case. This is a two body
            # reaction of the form A + B -> C + e- (+D)
            
            reactions[reaction[1]]['destr_AD'].append({
                    'reactants':[reaction[1],reaction[2]],
                    'products':[reaction[4], reaction[5], reaction[6]],
                    'coeffs': [reaction[8], reaction[9], reaction[10]],
                    'Trange': [reaction[12],reaction[13]],
                    'Tcheck': False
                })
                
            reactions[reaction[2]]['destr_AD'].append({
                    'reactants':[reaction[1],reaction[2]],
                    'products':[reaction[4], reaction[5], reaction[6]],
                    'coeffs': [reaction[8], reaction[9], reaction[10]],
                    'Trange': [reaction[12],reaction[13]],
                    'Tcheck': False
                })
                
            reactions[reaction[4]]['form_AD'].append({
                    'reactants':[reaction[1],reaction[2]],
                    'products':[reaction[4], reaction[5], reaction[6]],
                    'coeffs': [reaction[8], reaction[9], reaction[10]],
                    'Trange': [reaction[12],reaction[13]],
                    'Tcheck': False
                })
                
            if reaction[6]:
                reactions[reaction[6]]['form_AD'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })





        ### ION-NEUTRAL AND NEUTRAL-NEUTRAL REACTIONS
        else:
            # everything else are neutral-neutral or ion-neutral 2 body
            # reactions. so we check for that. we need the 3 reaction
            # rate coefficients. for destruction we need to know the
            # reaction partner. for formation we need to know both
            # reactants.
            
            
            if (reaction[1][-1] == '+' or reaction[2][-1] == '+'):
            
                reactions[reaction[1]]['destr_IN'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                    
                reactions[reaction[2]]['destr_IN'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                    
                reactions[reaction[4]]['form_IN'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                    
                reactions[reaction[5]]['form_IN'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                    
                if reaction[6]:
                    reactions[reaction[6]]['form_IN'].append({
                            'reactants':[reaction[1],reaction[2]],
                            'products':[reaction[4], reaction[5], reaction[6]],
                            'coeffs': [reaction[8], reaction[9], reaction[10]],
                            'Trange': [reaction[12],reaction[13]],
                            'Tcheck': False
                        })

            ### NEUTRAL-NEUTRAL REACTIONS
            else:
                reactions[reaction[1]]['destr_NN'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                    
                reactions[reaction[2]]['destr_NN'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                    
                reactions[reaction[4]]['form_NN'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                    
                reactions[reaction[5]]['form_NN'].append({
                        'reactants':[reaction[1],reaction[2]],
                        'products':[reaction[4], reaction[5], reaction[6]],
                        'coeffs': [reaction[8], reaction[9], reaction[10]],
                        'Trange': [reaction[12],reaction[13]],
                        'Tcheck': False
                    })
                    
                if reaction[6]:
                    reactions[reaction[6]]['form_NN'].append({
                            'reactants':[reaction[1],reaction[2]],
                            'products':[reaction[4], reaction[5], reaction[6]],
                            'coeffs': [reaction[8], reaction[9], reaction[10]],
                            'Trange': [reaction[12],reaction[13]],
                            'Tcheck': False
                        })
            


    # go through reactions database and check for reactions that are
    # duplicates due to temperature range thing    
    for species in species_list:
        for react_type in reactions[species]:
            reaction = reactions[species][react_type]
            if type(reaction) != type([]):
                continue
            if len(reaction) <= 1:
                continue

            for i in xrange(len(reaction)):
                for j in xrange(i+1,len(reaction)):
                    if sorted(reaction[i]['reactants']) != sorted(reaction[j]['reactants']):
                        continue
                    if sorted(reaction[i]['Trange']) == sorted(reaction[j]['Trange']):
                        continue
                    if sorted(reaction[i]['products']) == sorted(reaction[j]['products']):
                        reactions[species][react_type][i]['Tcheck'] = True
                        reactions[species][react_type][j]['Tcheck'] = True
                        reactions[species][react_type][i]['Trange'].append(min(reactions[species][react_type][i]['Trange'][0],reactions[species][react_type][j]['Trange'][0]))
                        reactions[species][react_type][j]['Trange'].append(min(reactions[species][react_type][i]['Trange'][0],reactions[species][react_type][j]['Trange'][0]))
                        reactions[species][react_type][i]['Trange'].append(max(reactions[species][react_type][i]['Trange'][1],reactions[species][react_type][j]['Trange'][1]))
                        reactions[species][react_type][j]['Trange'].append(max(reactions[species][react_type][i]['Trange'][1],reactions[species][react_type][j]['Trange'][1]))


    info = {
            'species': len(abundances_table['col2']),
            'twobody': len(twobody),
            'photon': len(photon_all),
            'crphoton': len(crphot_all),
            'crproton': len(crp_all)
        }
        
        
    return reactions,info
###################################################################################
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
###################################################
def thermal_rate(alpha, beta, gamma, T, floor=-50):
    '''
    Compute the thermal reaction rate coefficient of two body reactions.
    Rate cofficients are expressed in the form
     k = alpha (T/300)^beta  exp(-gamma/T)  (cm^3/s)
     
    Parameters
    ----------
    alpha : float
        rate parameter
    beta : float
        rate parameter
    gamma : float
        rate parameter
    T : float
        temperature (K)
    floor : float
        log10 of the lowest allowed rate
        
    Returns
    -------
    rate : float
        the rate coefficient (cm^3/s)
    '''
    from numpy import exp, log10
    
    rate = alpha*(T/300.0)**beta*exp(-gamma/T)
    if log10(rate) < floor:
        return 10.**floor
    else:
        return rate
###################################################









###################################################
def two_body_reaction(coefficients, reactants, temperature):
    '''
    Give the reaction rate for two body reaction.
    
    Parameters
    ----------
    coefficients : list
        list of alpha, beta, gamma as defined in UMIST database in that order
    reactants : list
        length 2 list of reactant number densities (cm^-3)
    temperature : float
        temperature for two-body thermal reaction rate
    
    Returns
    -------
    k(T) : float
        reaction rate (cm^3/s)
    
    '''    

    nA = reactants[0]
    nB = reactants[1]
    
    alpha = coefficients[0]
    beta = coefficients[1]
    gamma = coefficients[2]
    
    k = thermal_rate(alpha, beta, gamma, temperature)*nA*nB
    
    return k
###################################################




    
    
    







###################################################
def prasad_tarafdar(T, cr_rate, cr_0, alpha, beta, gamma, albedo, floor=-50):
    '''
    Photodissociation via Prasad-Tarafdar mechanism 
    rates from rate95, originally from from Gredel etc
        9.  H2O + photon --> OH + H
       10.  OH  + photon --> O  + H
       11.  O2  + photon --> O + O
    
      Rates below from rate95 database, they should be same as Gredel etc
      prefactor of 2.5 is 1/(1-grain albedo) for albedo = 0.6
      Correction factor of 1.3*1.4 from Maloney et al.
    '''
    from numpy import log10
    
    #return 1.3*1.4/(1.-albedo)*cr_rate*p_rate*xA
    rate = alpha*(T/300.)**beta*gamma/(1.-albedo)*(cr_rate/cr_0)
    if log10(rate) < floor:
        return 10.**floor
    else:
        return rate
###################################################
    
    
    
    
    
    
    
    

###################################################
def photoreaction(Av, alpha, gamma, chi=1.0, incidence_factor=1.0, floor=-50):
    '''
    Photoionisation or photodissociation. Rate coefficient
    of the form
        k = alpha exp(-gamma Av)   (s^-1)

    Parameters
    ----------
    Av : float
        extinction
    alpha : float
        rate coefficient
    gamma : float
        rate coefficient
    chi : float
        UV field in units of draine
    incidence_factor : float
        1 for isotropic radiation
        1/2 for illumination on one side

    Output:
        - rate [float]: rate coefficient (s^-1)
    '''
    from numpy import exp, log10
    
    rate = incidence_factor*chi*alpha*exp(-gamma*Av)
    
    if log10(rate) < floor:
        return 10.**floor
    else:
        return rate
###################################################








###################################################
def doppler_factor(FWHM):
    '''
    Doppler broadening factor.
    
    Parameters
    ----------
    FWHM : float
        linewidth of molecular cloud (km/s)?
    
    Returns
    -------
    b : float
        b = FWHM/(4 ln2)^1/2
    '''
    from numpy import log
    
    return FWHM/(4.*log(2.))**0.5
###################################################






###################################################
def self_shielding_H2(NH2, b=1.0):
    '''
    We use the formulation of Draine and Bertoldi 1996.
    '''
    from numpy import exp
    x = NH2/5e14
    # Self shielding factor
    f_shield = 0.965/(1.+x/b)**2. + 0.035/(1.+x)**0.5*exp(-8.5e-4*(1.+x)**0.5)
    
    return f_shield
###################################################





###################################################
def H2_diss(H2diss0, tau1000, b, NH2, floor=-50):
    '''
    Photodissociation of molecular hydrogen. 
    We use the formulation of Draine and Bertoldi 1996
    which includes self-shielding.

    Parameters
    ----------
    H2diss0 : float
        the dissociation rate in the absence of dust extinction
        or self-shielding
    tau1000 : float
        optical depth for attenuation of the radiation field by
        dust at 1000 angstrom
    b : float
        doppler broadening parameter
            b = FWHM/(4 ln2)^1/2
        b is given in units of km/s
    NH2 : float
        column density of H2 (cm^-2)
    floor : float
        log10 of the lowest allowed rate

    Output:
        - rate [float]: rate coefficient (s^-1)
    '''
    from numpy import exp, log10
    
    x = NH2/5e14
    # Self shielding factor
    f_shield = 0.965/(1.+x/b)**2. + 0.035/(1.+x)**0.5*exp(-8.5e-4*(1.+x)**0.5)
    #print 'x: {0:.3e} | shield: {1:.5f}'.format(x, f_shield)
    rate = H2diss0*f_shield*exp(-tau1000)
    
    if log10(rate) < floor:
        return 10.**floor
    else:
        return rate
###################################################






###################################################
def sticking_coefficient(Tgas, Tdust):
    '''
    Sticking coefficient given by Hollenbach and Mckee (1979). This
    measures the fraction of H atoms that stick to a grain when
    they collide.
    
    Parameters
    ----------
    Tgas : float
        gas temperature
    Tdust : float
        dust temperature
    
    Returns
    -------
    S : float
        fraction of hydrogen atoms that stick to grain
    '''
    S = 1./(1.+0.4*(Tgas/100.+Tdust/100.)**0.5 + 0.2*(Tgas/100.) + 0.08+(Tgas/100.)**2.)
    
    return S
###################################################






###################################################
def evaporation_coefficient(Tdust, NI_on_NT=1.e-4, D_on_k=600.):
    '''
    Evaporation coefficient given by Hollenbach and Mckee (1979). This
    measures the fraction of H atoms that stick to a grain when
    they collide.
    
    Parameters
    ----------
    Tgas : float
        gas temperature
    Tdust : float
        dust temperature
    
    Returns
    -------
    S : float
        fraction of hydrogen atoms that stick to grain
    '''
    from numpy import exp
    
    f = 1./(1. + (1./NI_on_NT)*exp(-D_on_k/Tdust))
    
    return f
###################################################


###################################################
def H2_formation_HM79(Tgas, Tdust, alpha=5.20E-17, beta=0.50):
    '''
    Formation of H2 on dust grains. We use the formulae of 
    Hollenbach and Mckee (1979).
    
    Parameters
    ----------
    Tgas : float
        gas temperature (K)
    Tdust : float
        gas temperature (K)
    
    Returns
    -------
    k_H2 : float
        rate coefficient for H2 formation on dust grains
        cm^3 s^-1
    '''
    f = evaporation_coefficient(Tdust)
    S = sticking_coefficient(Tgas, Tdust)
    
    k_H2 = alpha*(Tgas/300.)**beta*f*S
    
    return k_H2
    
###################################################




###################################################
def chem_rates(densities, temperatures, reaction_types, reactions, columnH, H2_info, cr_rate=1.36e-17, extinction=15., floor=-40, species_test=''):
    '''
    Compute abundance derivatives based on chemical reaction rates.
    
    Parameters
    ----------
    dens : dict
        dictionary of number densities where keys are species names
    temperatures : dict
        dictionary of 3 temperatures with keys
            
            'neutral' : float
                neutral temperature, for neutral-neutral two-body reactions
            'ion' : float
                effective temperature for ion-neutral reactions (THIS IS NOT
                THE ION TEMPERATURE)
            'electron' : float
                effective temperature for electron recombination reactions
                
    reaction_types : dict
        dictionary of reaction modules with keys:
        
            'NN' : bool
                activate neutral-neutral reactions
            'IN' : bool
                activate ion-neutral reactions
            'CE' : bool
                activate charge exchange reactions
            'DR' : bool
                activate dissociative recombination reactions
            'RR' : bool
                activate radiative recombination reactions
            'RA' : bool
                activate radiative association reactions
            'PH' : bool
                activate photoreactions
            'CP' : bool
                activate direct cosmic-ray reactions
            'CR' : bool
                activate indirect cosmic-ray photoreactions
            'AD' : bool
                activate associative detachment reactions
    
    reactions : dict
        dictionary of reactions with species as keys, then for each
        species, reactions[species] is a dictionary with keys
        
            'form_NN' : list
                formation via neutral-neutral reactions
            'form_IN': list
                formation via ion-neutral reactions
            'form_CE': list
                formation via charge exchange reactions
            'form_DR': list
                formation via dissociative recombination reactions
            'form_RR': list
                formation via radiative recombination reactions
            'form_RA': list
                formation via radiative association reactions
            'form_PH': list
                formation via photon process reactions
            'form_CP': list
                formation via direct cosmic ray reactions
            'form_CR': list
                formation via cosmic ray induced photon reactions
            'form_AD': list
                formation via associative detachment reactions
            'destr_NN': list
                destruction via neutral-neutral reactions
            'destr_IN': list
                destruction via ion-neutral reactions
            'destr_CE': list
                destruction via charge exchange reactions
            'destr_DR': list
                destruction via dissociative recombination reactions
            'destr_RR': list
                destruction via radiative recombination reactions
            'destr_RA': list
                destruction via radiative association reactions
            'destr_PH': list
                destruction via photon process reactions
            'destr_CP': list
                destruction via direct cosmic ray reactions
            'destr_CR': list
                destruction via cosmic ray induced photon reactions
            'destr_AD': list
                destruction via associative detachment reactions
    H2_info : dict
        some quantities needed for the H2 dissociation rate.
        this dictionary has keys
            
            'H2diss0' : float
                the dissociation rate in the absence of dust extinction
                or self-shielding
            'tau1000' : float
                optical depth for attenuation of the radiation field by
                dust at 1000 angstrom
            'b' : float
                doppler broadening parameter
                    b = FWHM/(4 ln2)^1/2
                b is given in units of km/s
            'NH2' : float
                column density of H2 (cm^-2)
            
    cr_rate : float
        cosmic ray ionization rate, default is 1.36e-17 s^-1 (H^-1?)
    extinction : float
        dust extinction at visible wavelengths, default is 15
    floor : float
        log10 of lowest allowable rate coefficient
    
    Returns
    -------
    rate : dict
        dictionary of rates per volume at which species (key) is being 
        created or destroyed (source term S(M) in the documentation)
    '''

    Tn = temperatures['neutral']
    Ti = temperatures['ion']
    Te = temperatures['electron']
    Td = temperatures['dust']
    
    rate = {}    
    for species in densities.keys():
        if species == 'e-':
            continue
            
        rate[species] = 0


        ################ Neutral-neutral reactions ##############
        if reaction_types['NN']:
            # Temperature for neutral-neutral reactions is the neutral temperature
            temp = temperatures['neutral']
            for reaction in reactions[species]['form_NN']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (temp < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (temp > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue
                        
                nA = densities[reaction['reactants'][0]]
                nB = densities[reaction['reactants'][1]]
                rate[species] += two_body_reaction(reaction['coeffs'], reactants=[nA,nB], temperature=temp)

            for reaction in reactions[species]['destr_NN']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (Tn < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (Tn > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue

                nA = densities[reaction['reactants'][0]]
                nB = densities[reaction['reactants'][1]]
                rate[species] -= two_body_reaction(reaction['coeffs'], reactants=[nA,nB], temperature=temp)
            ########################
            
            
            

        ######### Ion-neutral reactions #########
        if reaction_types['IN']:
            # Temperature for ion-neutral reactions is the effective temperature
            # that is weighted by ions and neutrals, and includes a term for ion-neutral drift
            temp = temperatures['ion']
            for reaction in reactions[species]['form_IN']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (temp < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (temp > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue
                        

                nA = densities[reaction['reactants'][0]]
                nB = densities[reaction['reactants'][1]]
                rate[species] += two_body_reaction(reaction['coeffs'], reactants=[nA,nB], temperature=temp)

            for reaction in reactions[species]['destr_IN']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (Tn < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (Tn > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue
                        
                nA = densities[reaction['reactants'][0]]
                nB = densities[reaction['reactants'][1]]
                rate[species] -= two_body_reaction(reaction['coeffs'], reactants=[nA,nB], temperature=temp)
        ########################

            
            

        ######### Dissociative recombination #########
        if reaction_types['DR']:
            # Temperature for recombination reactions is the electron temperature
            temp = temperatures['electron']
            for reaction in reactions[species]['form_DR']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (temp < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (temp > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue
                        
                nA = densities[reaction['reactants'][0]]
                nB = densities[reaction['reactants'][1]]
                rate[species] += two_body_reaction(reaction['coeffs'], reactants=[nA,nB], temperature=temperatures['electron'])

            for reaction in reactions[species]['destr_DR']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (Tn < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (Tn > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue
                        
                nA = densities[reaction['reactants'][0]]
                nB = densities[reaction['reactants'][1]]
                rate[species] -= two_body_reaction(reaction['coeffs'], reactants=[nA,nB], temperature=temp)
        ########################
        
        
        

        ######### Radiative recombination #########
        if reaction_types['RR']:
            # Temperature for recombination reactions is the electron temperature
            temp = temperatures['electron']
            for reaction in reactions[species]['form_RR']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (temp < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (temp > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue                     

                nA = densities[reaction['reactants'][0]]
                nB = densities[reaction['reactants'][1]]
                
                rate[species] += two_body_reaction(reaction['coeffs'], reactants=[nA,nB], temperature=temp)

            for reaction in reactions[species]['destr_RR']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (Tn < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (Tn > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue                     

                nA = densities[reaction['reactants'][0]]
                nB = densities[reaction['reactants'][1]]
                
                rate[species] -= two_body_reaction(reaction['coeffs'], reactants=[nA,nB], temperature=temp)
        ########################





        ######### Radiative association #########
        if reaction_types['RA']:
            for reaction in reactions[species]['form_RA']:
                # Set temperature as ion-neutral effective temperature if one of the reactants
                # is an ion, otherwise set it to the neutral temperature
                if (reaction['reactants'][0][-1] == '+') or (reaction['reactants'][1][-1] == '+'):
                    temp = temperatures['ion']
                else:
                    temp = temperatures['neutral']
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (temp < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (temp > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue

                nA = densities[reaction['reactants'][0]]
                nB = densities[reaction['reactants'][1]]
                
                rate[species] += two_body_reaction(reaction['coeffs'], reactants=[nA,nB], temperature=temp)

            for reaction in reactions[species]['destr_RA']:
                # Set temperature as ion-neutral effective temperature if one of the reactants
                # is an ion, otherwise set it to the neutral temperature
                if (reaction['reactants'][0][-1] == '+') or (reaction['reactants'][1][-1] == '+'):
                    temp = temperatures['ion']
                else:
                    temp = temperatures['neutral']
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (temp < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (temp > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue

                nA = densities[reaction['reactants'][0]]
                nB = densities[reaction['reactants'][1]]
                
                rate[species] -= two_body_reaction(reaction['coeffs'], reactants=[nA,nB], temperature=temp)
        ########################
        
        
        
        
        
        ######### Associative detachment #########
        if reaction_types['AD']:
            # temperature for associative detachment reactions is neutral temperature
            temp = temperatures['neutral']
            for reaction in reactions[species]['form_AD']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (temp < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (temp > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue                     

                nA = densities[reaction['reactants'][0]]
                nB = densities[reaction['reactants'][1]]
                
                rate[species] += two_body_reaction(reaction['coeffs'], reactants=[nA,nB], temperature=temp)

            for reaction in reactions[species]['destr_AD']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (temp < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (temp > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue                     

                nA = densities[reaction['reactants'][0]]
                nB = densities[reaction['reactants'][1]]
                
                rate[species] -= two_body_reaction(reaction['coeffs'], reactants=[nA,nB], temperature=temp)
        ########################
        
        
        
        
        
        
        


        ######### Direct cosmic-ray dissociation or ionization ######### 
        if reaction_types['CP']:
            for reaction in reactions[species]['form_CP']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (Tn < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (Tn > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue   

                nM = densities[reaction['reactants'][0]]
                alpha = reaction['coeffs'][0]

                rate[species] += alpha*nM

                if species == species_test:
                    print('form_CP: {0:.4e}'.format(alpha*nM))

            # CR photon destruction reactions (prasad-tarafdar mechanism)
            for reaction in reactions[species]['destr_CP']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (Tn < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (Tn > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue      

                nM = densities[reaction['reactants'][0]]
                alpha = reaction['coeffs'][0]

                rate[species] -= alpha*nM

                if species == species_test:
                    print('destr_CP: {0:.4e}'.format(alpha*nM))
            ########################



        ######### CR photon formation reactions (prasad-tarafdar mechanism) ######### 
        if reaction_types['CR']:
            for reaction in reactions[species]['form_CR']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (Tn < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (Tn > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue         

                nM = densities[reaction['reactants'][0]]

                alpha = reaction['coeffs'][0]
                beta = reaction['coeffs'][1]
                gamma = reaction['coeffs'][2]

                rate[species] += prasad_tarafdar(temperatures['neutral'], cr_rate, 1.36e-17, alpha, beta, gamma, 0.6)*nM

            # CR photon destruction reactions (prasad-tarafdar mechanism)
            for reaction in reactions[species]['destr_CR']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (Tn < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (Tn > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue   

                nM = densities[reaction['reactants'][0]]

                alpha = reaction['coeffs'][0]
                beta = reaction['coeffs'][1]
                gamma = reaction['coeffs'][2]

                rate[species] -= prasad_tarafdar(temperatures['neutral'], cr_rate, 1.36e-17, alpha, beta, gamma, 0.6)*nM
            ########################



        ######### Photo dissociation or ionization ######### 
        if reaction_types['PH']:
            for reaction in reactions[species]['form_PH']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (Tn < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (Tn > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue          

                nM = densities[reaction['reactants'][0]]

                alpha = reaction['coeffs'][0]
                gamma = reaction['coeffs'][2]

                rate[species] += photoreaction(extinction, alpha, gamma)*nM


            for reaction in reactions[species]['destr_PH']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (Tn < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (Tn > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue

                nM = densities[reaction['reactants'][0]]

                alpha = reaction['coeffs'][0]
                gamma = reaction['coeffs'][2]
                
                rate[species] -= photoreaction(extinction, alpha, gamma)*nM
        ########################
            
            
            
            
        
        ################ H2 Photodissociation ##############
        if reaction_types['H2D']:
            for reaction in reactions[species]['form_H2D']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (Tn < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (Tn > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue          

                nM = densities[reaction['reactants'][0]]
                alpha = reaction['coeffs'][0]
                gamma = reaction['coeffs'][2]
                H2diss0 = photoreaction(0.0, alpha, gamma, H2_info['uv_field'], H2_info['incidence_factor'], floor=floor)
                xH2 = 0.5*(1.-densities['H']/(densities['H'] + 2*densities['H2']))
                NH2 = columnH*xH2
                tau1000 = reaction['coeffs'][2]*extinction

                rate[species] += H2_diss(H2diss0, tau1000, H2_info['b'], NH2, floor=floor)*nM


            for reaction in reactions[species]['destr_H2D']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (Tn < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (Tn > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue

                nM = densities[reaction['reactants'][0]]
                #xH2 = densities['H2']/(densities['H'] + densities['H2'])
                alpha = reaction['coeffs'][0]
                gamma = reaction['coeffs'][2]
                H2diss0 = photoreaction(0.0, alpha, gamma, H2_info['uv_field'], H2_info['incidence_factor'], floor=floor)
                xH2 = 0.5*(1.-densities['H']/(densities['H'] + 2*densities['H2']))
                NH2 = columnH*xH2
                tau1000 = reaction['coeffs'][2]*extinction
                #print NH2
                
                #print 'H2diss0: {0:.3e} | alpha: {1:.3e} | tau/Av: {2:.3f} | xH2: {3:.3e} | NH2: {4:.3e} | tau1000: {5:.3e}'.format(H2diss0, alpha, gamma, xH2, NH2, tau1000)
                
                #print 'Av: {0:.3e} | xH2: {1:.3e} | NH2: {2:.3e}'.format(extinction, xH2, NH2)
                #print 'Av: {0:.2e} | k_diss: {1:.3e}'.format(extinction,H2_diss(H2_info['H2diss0'], H2_info['tau1000'], H2_info['b'], H2_info['NH2'], floor=floor))
                rate[species] -= H2_diss(H2diss0, tau1000, H2_info['b'], NH2, floor=floor)*nM
        ########################
            
        
        
        ################ Reactions on dust-grains ##############
        if reaction_types['DG']:
            # Temperature for dust-grain reactions is the neutral temperature
            temp = temperatures['neutral']
            for reaction in reactions[species]['form_DG']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (temp < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (temp > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue
                        
                nH0 = densities[reaction['reactants'][0]]
                nH = densities['H'] + 2*densities['H2']
                alpha = reaction['coeffs'][0]
                beta = reaction['coeffs'][1]
                
                #rate[species] += alpha*temp**beta*nH*nH0
                rate[species] += H2_formation_HM79(Tn, Td, alpha, beta)*nH*nH0

            for reaction in reactions[species]['destr_DG']:
                # Do we need to care about the temperature range validity?
                if reaction['Tcheck']:
                    if (Tn < reaction['Trange'][0] and reaction['Trange'][0] != min(reaction['Trange'])): 
                        continue
                    elif (Tn > reaction['Trange'][1] and reaction['Trange'][1] != max(reaction['Trange'])): 
                        continue

                        
                nH0 = densities[reaction['reactants'][0]]
                nH = densities['H'] + 2*densities['H2']
                alpha = reaction['coeffs'][0]
                beta = reaction['coeffs'][1]
                
                #rate[species] -= alpha*temp**beta*nH*nH0
                rate[species] -= H2_formation_HM79(Tn, Td, alpha, beta)*nH*nH0
        ########################
            
        
    return rate
###################################################
