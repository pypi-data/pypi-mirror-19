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
def cr_heating_coefficient_K14(nH):
    '''
    Krumholz (2014) fit to data of Glassgold et al. (2012) giving
    the heating coefficient from cosmic ray ionization in regions
    dominated by molecular hydrogen.
    
    Parameters
    ----------
    
    Returns
    -------
    qCR : float
        heating coefficient (erg), such that the heating rate, G
        (in erg/s/H), is
        G = zeta qCR
        where zeta is the CR ionization rate (per H?)
    '''
    from numpy import log10
    
    ev2erg = 1.60217646e-12
    
    if log10(nH) < 2:
        return 10.*ev2erg
    elif log10(nH) < 4:
        return (10.+ 3./2.*(log10(nH)-2.))*ev2erg
    elif log10(nH) < 7:
        return (13.+ 4./3.*(log10(nH)-4.))*ev2erg
    elif log10(nH) < 10:
        return (17.+ 1./3.*(log10(nH)-7.))*ev2erg
    else:
        return 18.*ev2erg
###################################################





###################################################
def cr_HI_heating_coefficient_D11(xe):
    '''
    Draine (2011) fit to data of Dalgarno & McCray (1972) giving
    the heating coefficient from cosmic ray ionization in atomic
    regions.
    
    Parameters
    ----------
    xe : float
        electron abundance ne/nH (wrt to total hydrogen)

    Returns
    -------
    qCR_HI : float
        heating coefficient (erg), such that the heating rate, G
        (in erg/s/H), is
        G = zeta qCR_HI
        where zeta is the CR ionization rate per H
    '''
    
    ev2erg = 1.60217646e-12

    q_eV = 6.5 + 26.4*(xe/(xe+0.07))**0.5

    return q_eV*ev2erg
###################################################








###################################################
def cr_heating_function_K14(zeta, nH):
    '''
    Cosmic-ray heating function from Krumholz (2014).

    Parameters
    ----------
    zeta : float
        cosmic-ray ionization rate (1/s/H)

    Returns
    -------
    G_cr : float
        heating rate (erg/s/cm^3)

    '''
    
    qCR=cr_heating_coefficient_K14(nH)

    G_cr=zeta*qCR*nH

    return G_cr
###################################################




###################################################
def cr_total_heating_function_K14(zeta, nH, xHI, xH2, xe):
    '''
    Cosmic-ray heating function from Krumholz (2014).
    This assumes atomic and molecular regions are distinct,
    so it probably breaks down when nH2 ~ nHI.

    Parameters
    ----------
    zeta : float
        cosmic-ray ionization rate (1/s/H)

    nH : float
        total hydrogen number density (cm^-3)

    xHI : float
        abundance of atomic hydrogen n(H)/nH

    xH2 : float
        abundance of molecular hydrogen n(H2)/nH

    xe : float
        abundance of electron ne/nH        

    Returns
    -------
    G_cr : float
        heating rate (erg/s/cm^3)

    '''
    
    qCR_HI=cr_HI_heating_coefficient_D11(xe)
    qCR_H2=cr_heating_coefficient_K14(nH)

    G_cr=zeta*(xHI*qCR_HI + 2.*xH2*qCR_H2)*nH

    return G_cr
###################################################





###################################################
def pe_heating_function_K14(NH, chi=1.0, Zd=1.0, sigma_d=1.e-21):
    '''
    Photoelectric heating function from Krumholz (2014).

    Parameters
    ----------
    NH : float
        column density that the UV field has passed through
    chi: float
        UV field relative to Milky Way field; the energy density
        of the interstellar radiation field is
            u_isrf = chi u_MW
    Zd : float
        dust abundance relative to solar
    sigma_d : float
        dust cross section

    Returns
    -------
    G_pe : float
        heating rate (erg/s/cm^3)

    '''
    from numpy import exp
    
    attenuation = exp(-0.5*NH*sigma_d)

    G_pe = 4.e-26 * chi * Zd * attenuation

    return G_pe
###################################################




###################################################
def pe_heating_function_W03(nH, ne, Tgas, Av, gamma=3.02, G0=1.0, phi=1.0):
    '''
    Photoelectric heating function from Wolfire (2013).

    Parameters
    ----------
    nH : float
        total H number density (cm^-3)
    ne: float
        electron number density (cm^-3)
    Tgas :  float
        gas temperature (K)
    Av :  float
        magnitudes of extinction
    gamma :  float
        optical depth per magnitude of extinction (default 3.02)
    G0 :  float
        UV radiation field (Habing, G0=chi/1.7)
    phi :  float
        some parameter about PAHs. just use 1.0
    

    Returns
    -------
    G_pe : float
        volume heating rate (erg/s/cm^3)

    '''
    
    from numpy import exp
    
    attenuation=exp(-gamma*Av)
    G0_eff=attenuation*G0
    
    psi = G0_eff*Tgas**0.5/ne/phi
    
    epsilon = 4.87e-2/(1. + 4.e-3*psi**0.73) + 3.65e-2*(Tgas/1.e4)**0.7/(1.+2.e-4*psi)
    
    G_pe = 1.3e-24*nH*epsilon*G0_eff
    
    return G_pe

###################################################





###################################################
def sticking_coefficient(Tgas, Tdust):
    '''
    Sticking coefficient given by Hollenbach and Mckee (1979).
    
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
    S = 1./(1. + 0.4*(Tgas + Tdust)**0.5 + 2.e-3*Tgas + 8e-6*Tgas**2.)
    
    return S
###################################################


###################################################
def recombination_efficiency(mu, F, beta_H2, beta_Hp, alpha_pc):
    '''
    Recombination efficiency given by Cazaux and Tielens (2002, 2004).
    
    Parameters
    ----------
    mu : float
        fraction of H2 that remains on surface after formation
    F : float
        flux of hydrogen atoms
    beta_H2 : float
        desorption rate of molecular hydrogen
    beta_Hp : float
        desorption rate of physisorbed hydrogen
    alpha_pc : float
        evaporation rate from physisorbed to chemisorbed sites
    
    Returns
    -------
    epsilon : float
        recombination efficiency
    '''
    
    epsilon = 1./(1. + mu*F/2./beta_H2 + beta_Hp/alpha_pc)
    
    return epsilon
###################################################





###################################################
def rate_H2_formation_TH85(Tgas, Tdust, nH, nD, alpha=5.20E-17, beta=0.50):
    '''
    H2 formation rate in the form of Tielens and Hollenbach (1985)
    
    
    Parameters
    ----------
    Tgas, Tdust, nH, nD, alpha, beta
    
    Returns
    -------
    R : float
        formation rate (cm^-3 s^-1)s
    '''
    
    R = alpha*(Tgas/300.)**beta*nH*nD*sticking_coefficient(Tgas, Tdust)
    
    return R
###################################################



###################################################
def H2_formation_heating_HM79(nH, xH, xH2, Tgas, Tdust, alpha=5.20E-17, beta=0.50):
    '''
    Heating rate due to formation of H2 on dust grains. We use the
    formulae of Hollenbach and Mckee (1979).
    
    Parameters
    ----------
    nH : float
        total hydrogen number density (cm^-3)
    xH : float
        atomic hydrogen abundance n(H)/nH
    xH2 : float
        molecular hydrogen abundance n(H2)/nH
    T : float
        gas temperature (K)
    
    Returns
    -------
    G_form : float
        heating rate due to H2 formation on grains (erg/s/cm^3). 
        to get the heating rate per H divide this by nH
    '''
    from numpy import exp

    ev2erg = 1.60217646e-12
    
    n_cr = 1.e6*Tgas**(-0.5)/(1.6*xH*exp(-(400./Tgas)**2.)+1.4*xH2*exp(-12000./(Tgas+1200.)))
    
    # fraction of atoms which form molecules before evaporating off grain
    f = 1./(1. + 1.e-4*exp(-600./Tdust))
    # sticking factor
    S = 1./(1.+0.4*(Tgas/100.+Tdust/100.)**0.5 + 0.2*(Tgas/100.) + 0.08+(Tgas/100.)**2.)
    Rf = alpha*(Tgas/300.)**beta*f*S
    
    G_form=Rf*xH*(0.2 + 4.2/(1.+n_cr/nH))
    
    return G_form*ev2erg*nH**2.
    
###################################################




###################################################
def ncrit_LS83(T, gas_composition):
    '''
    Critical number density for some process.
    Taken from Lepp and Shull 1983. The atomic
    n_crit has been reduced by an order of magnitude
    following the suggestion of Martin et al 1996.
    
    Parameters
    ----------
    T : float
        temperature in kelvin
        
    gas_composition : str
        'atomic' or 'molecular'
    
    Returns
    -------
    n_cr : float
        critical density (cm^-3)
    '''
    x = T/1.e4
    
    if gas_composition == 'atomic':
        logncr= 3. - 0.416*x - 0.327*x**2.
    elif gas_composition == 'molecular':
        logncr= 4.13 - 0.968*x + 0.119*x**2.
    
    return 10.**logncr
###################################################




###################################################
def ncrit_SK87(T, gas_composition):
    '''
    Critical number density for some process.
    Taken from Shapiro and Kang 1987. The atomic
    n_crit has been reduced by an order of magnitude
    following the suggestion of Martin et al 1996.
    
    Parameters
    ----------
    T : float
        temperature in kelvin
        
    gas_composition : str
        'atomic' or 'molecular'
    
    Returns
    -------
    n_cr : float
        critical density (cm^-3)
    '''
    x = T/1.e4
    
    if gas_composition == 'atomic':
        logncr= 3. - 0.416*x - 0.327*x**2.
    elif gas_composition == 'molecular':
        logncr= 4.845 - 1.3*x + 1.62*x**2.
    
    return 10.**logncr
###################################################



###################################################
def H2_diss_MS04(G0, extinction, NH2, b=1.0, gamma=3.02):
    '''
    H2 dissociation heating taken from Meijerink and Spaans (2004).
    
    Returns
    -------
    G_diss : float
        dissociation volume heating rate (erg/s/cm^3)
    '''
    from lehmann_astrochemistry.chemistry import self_shielding_H2
    from numpy import exp
    
    f_s = self_shielding_H2(NH2, b=1.0) # H2 self shielding
    attenuation = exp(-gamma*extinction) # dust attenuation
    
    G_diss = 2.2e-23*G0*f_s*attenuation
    
    return G_diss
###################################################



###################################################
def specific_heat(xM):
    '''
    Specific heat at constant volume from Gong et al. (2016).
    
    Parameters
    ----------
    xM : dict
        abundances n(M)/nH
    
    Returns
    -------
    c_v : float
        specific heat (erg/K)
    '''
    kb_erg = 1.3806488e-16
    
    species=['H','H2','H+','He','He+','e-']
    # degrees of freedom
    f={
        'H': 3,
        'H2': 5,
        'H+': 3,
        'He': 3,
        'He+': 3,
        'e-': 3,
    }
    c_v=0
    for key in species:
        if key in xM.keys():
            c_v+=0.5*kb_erg*f[key]*xM[key]
    
    return c_v
    
###################################################



