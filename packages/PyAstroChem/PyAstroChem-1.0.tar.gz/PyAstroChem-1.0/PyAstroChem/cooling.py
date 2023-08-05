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
def cooling_CII_K14(nH2, logT, T_CII=91.):
    '''
    CII line cooling (158 um) function from Krumholz (2014).
    This function assumes that the chemical composition is
    dominated by H2 (molecular hydrogen) and ignores the
    collisional excitation by He and free electrons.
    
    Parameters
    ----------
    nH2 : float
        number density of molecular hydrogen (cm^-3)
    
    logT : float
        base 10 logarithm of temperature (K)
        
    T_CII : float
        energy of the upper state measured in Kelvin
    
    Returns
    -------
    Lm_CII : float
        cooling rate (erg/s). multiply by the abundance of
        C+ to get cooling rate per H nuclei
    '''
    from numpy import exp

    kb_erg = 1.3806488e-16
    T=10.**logT
    
    k_CII = 6.6e-10*exp(-T_CII/T)
    
    Lm_CII = k_CII*kb_erg*T_CII*nH2
    
    return Lm_CII
###################################################






###################################################
def cooling_graingas_K14():

    return 1.e-50
###################################################







###################################################
def table_printout(L0, L_LTE, nhalf, alpha):
    
    print '----------------------------'
    print '   -log10(L0/(erg cm^3 s^-1))'
    print L0
    print '----------------------------'
    print
    print '----------------------------'
    print '   -log10(L_LTE/(erg s^-1))'
    print L_LTE
    print '----------------------------'
    print
    print '----------------------------'
    print '   log10(n_half/(cm^-3))'
    print nhalf
    print '----------------------------'
    print
    print '----------------------------'
    print '   alpha'
    print alpha
    print '----------------------------'
###################################################



    
    

###################################################
def table_printout_H2_93(L0, L_LTE, nhalf, alpha):
    from astropy.table import Table, Column
        
    
    logT = L0.keys()
    
    table_H2 = Table( [L0.keys()], names=['logT'])
    table_H2.add_column(Column(name='-log10(L_0)', data=list(L0[0])))
    table_H2.add_column(Column(name='-log10(L_LTE)', data=list(L_LTE[0])))
    table_H2.add_column(Column(name='log10(n_half)', data=list(nhalf[0])))
    table_H2.add_column(Column(name='alpha', data=list(alpha[0])))
    
    print table_H2
###################################################





    
    
###################################################
def table_printout_H2_95(L0, L_LTE, nhalf, alpha):
    from astropy.table import Table, Column     
    
    logT = L0.keys()
    
    table_H2 = Table( [L0.keys()], names=['logT'])
    table_H2.add_column(Column(name='-log10(L_0 exp[509/T])', data=list(L0[0])))
    table_H2.add_column(Column(name='-log10(L_LTE exp[509/T])', data=list(L_LTE[0])))
    table_H2.add_column(Column(name='log10(n_half)', data=list(nhalf[0])))
    table_H2.add_column(Column(name='alpha', data=(['...','...','...']+list(alpha[0]))))
    
    print table_H2
###################################################
    
    
    
    

###################################################
def table_combine(low, high):
    '''
    NK93 and N95 tables are inconsistent at T=100K.
    We simply average the two values at 100K to get
    the full table from 10K up to 2000K (or 4000K).
    
    
    '''
    from astropy.table import Column
    
    combined_table = low.copy()
    
    try:
        average_column = Column((low['100']+high['100'])/2.)
        combined_table.replace_column('100', average_column)
        high.remove_column('100')
    except KeyError:
        average_column = Column((low['2']+high['2'])/2.)
        combined_table.replace_column('2', average_column)
        high.remove_column('2')
    
    try:
        high.remove_column('N')
    except:
        pass
    
    for col in high.itercols():
        combined_table.add_column(col)
    
    return combined_table
###################################################







###################################################
def get_row(table, Ntilde, k0, s0):
    from scipy.interpolate import UnivariateSpline
    from numpy import where
    
    if Ntilde in table['N']:
        # Create spline interpolation of the appropriate row.
        row = list(table[where(table['N'] == Ntilde)[0][0]])
    else:
        # Create spline interpolation down the columns (for each temperature)
        # so that we can "create a row" between rows.
        
        logNtilde = list(table['N'])
        row = []
        
        for key in table.keys():
            row.append(UnivariateSpline(logNtilde, list(table[key]), k=k0, s=s0)(Ntilde))
    
    return row
###################################################

    

###################################################
def NK_params_functions(mol, L0, L_LTE, n_half, alpha, Ntilde, k0, s0):
    '''
    Return interpolated functions of the parameters for the cooling
    functions in NK93 and N95.
    
    Parameters
    ----------
    mol: str
        name of molecule, e.g. 'CO', 'H2O', 'H2'
    L0 : astropy table
    
    L_LTE : astropy table
    
    n_half : astropy table
    
    alpha : astropy table
    
    Ntilde : float
        (log10 of) optical depth parameter
    
    k0 : int
        order of spline interpolation
    
    s0 : float
        I don't know
    
    Returns
    -------
    L0_func, L_LTE_func, n_half_func, alpha_func
    '''
    from scipy.interpolate import UnivariateSpline
    from numpy import log10, where
    
    if (mol=='CO') or (mol=='H2O') or (mol=='OH'):
        temps = [float(x) for x in L0.keys()]
        
        # Get the parameters as a function of temperature for this Ntilde
        L0_pts = list(L0[0])
        
        if Ntilde in alpha['N']:
            # Create spline interpolation of the appropriate row.
            
            L_LTE_pts = list(L_LTE[where(L_LTE['N'] == Ntilde)[0][0]])[1:]
            n_half_pts = list(n_half[where(n_half['N'] == Ntilde)[0][0]])[1:]
            alpha_pts = list(alpha[where(alpha['N'] == Ntilde)[0][0]])[1:]
        else:
            # Create spline interpolation down the columns (for each temperature)
            # so that we can "create a row" between rows.
            
            logNtilde = list(L_LTE['N'])
            L_LTE_pts = []
            n_half_pts = []
            alpha_pts = []
            
            for key in L0.keys():
                L_LTE_pts.append(UnivariateSpline(logNtilde, list(L_LTE[key]), k=k0, s=s0)(Ntilde))
                n_half_pts.append(UnivariateSpline(logNtilde, list(n_half[key]), k=k0, s=s0)(Ntilde))
                alpha_pts.append(UnivariateSpline(logNtilde, list(alpha[key]), k=k0, s=s0)(Ntilde))
            
        # Interpolate in logspace because that reduces instability
        L0_func = UnivariateSpline(log10(temps), L0_pts, k=k0, s=s0)
        L_LTE_func = UnivariateSpline(log10(temps), L_LTE_pts, k=k0, s=s0)
        n_half_func = UnivariateSpline(log10(temps), n_half_pts, k=k0, s=s0)
        alpha_func = UnivariateSpline(log10(temps), alpha_pts, k=k0, s=s0)
        
        return L0_func, L_LTE_func, n_half_func, alpha_func
    
    if mol == 'H2':
        logT = [float(x) for x in L0.keys()]
        logT2 = [float(x) for x in alpha.keys()] # alpha has less temperatures in NLM95 
        
        L0_func = UnivariateSpline(logT, list(L0[0]), k=k0, s=s0)
        L_LTE_func = UnivariateSpline(logT, list(L_LTE[0]), k=k0, s=s0)
        n_half_func = UnivariateSpline(logT, list(n_half[0]), k=k0, s=s0)
        alpha_func = UnivariateSpline(logT2, list(alpha[0]), k=k0, s=s0)
        
        return L0_func, L_LTE_func, n_half_func, alpha_func
###################################################
    
    
    

    
    
    
    
    
###################################################
def NK_CO_cooling(paths, Ntilde, k0, s0):
    '''
    CO cooling function of Neufeld and Kauffman (1993) and
    Neufeld et al. (1995).
    
    Parameters
    ----------
    paths : dicts
        dictionary of paths to tabulated data. has keys:
        
        'L0_low'
        'L_LTE_low'
        'n_half_low'
        'alpha_low'
        'L0_high'
        'L_LTE_high'
        'n_half_high'
        'alpha_high'

    Ntilde : float
        (log10 of) optical depth parameter
    k0 : int
        order of spline interpolation
    s0 : float
        I don't know
    
    Returns
    -------
    CO_cool : function
        Cooling function L(nH2,logT) (erg/s). Multiply this by the
        number density of CO to get cooling per volume.
        
    '''
    from numpy import where
    from astropy.table import Table
    
    # Open tables: CO
    CO_L0_low = Table.read(paths['L0_low'])
    CO_L_LTE_low = Table.read(paths['L_LTE_low'])
    CO_n_half_low = Table.read(paths['n_half_low'])
    CO_alpha_low = Table.read(paths['alpha_low'])
    
    CO_L0_high = Table.read(paths['L0_high'])
    CO_L_LTE_high = Table.read(paths['L_LTE_high'])
    CO_n_half_high = Table.read(paths['n_half_high'])
    CO_alpha_high = Table.read(paths['alpha_high'])
    
    # Remove logNtilde=14 from high temperature tables, as this case
    # doesn't exist in the low temperature tables
    CO_L_LTE_high.remove_row(where(CO_L_LTE_high['N'] == 14.0)[0][0])
    CO_n_half_high.remove_row(where(CO_n_half_high['N'] == 14.0)[0][0])
    CO_alpha_high.remove_row(where(CO_alpha_high['N'] == 14.0)[0][0])
    
    # Combine low and high temperature tables by averaging the 
    # 100K column
    CO_L0_table = table_combine(CO_L0_low.copy(), CO_L0_high.copy())
    CO_L_LTE_table = table_combine(CO_L_LTE_low.copy(), CO_L_LTE_high.copy())
    CO_n_half_table = table_combine(CO_n_half_low.copy(), CO_n_half_high.copy())
    CO_alpha_table = table_combine(CO_alpha_low.copy(), CO_alpha_high.copy())
    
    # Spline interpolate params at the appropriate Ntilde, the
    # arguments of these functions are log10(temperature)
    neglogL0, neglogL_LTE, lognhalf, alpha = NK_params_functions('CO', CO_L0_table, CO_L_LTE_table, CO_n_half_table, CO_alpha_table, Ntilde, k0=k0, s0=s0)

    def CO_cool(nH2, logT):
        cool = nH2/(10.**neglogL0(logT) + 
            nH2*10.**neglogL_LTE(logT) + 
            ((nH2*10.**(-lognhalf(logT)))**alpha(logT))*(1.0 - 10.**lognhalf(logT)*10.**(-neglogL0(logT))*10.**neglogL_LTE(logT))*10.**neglogL0(logT))
        return cool
    
    return CO_cool
###################################################








###################################################
def n_eff(coolant, nH2, nHI, ne, T):
    '''
    This is an effective number density that replaces nH2 in the
    NK cooling functions. This takes into account collisional
    excitation by atomic hydrogen and electrons whereas the original
    NK function assumed a fully molecular hydrogen medium. The
    expression for n_eff(CO) is taken from Gong et al (2016), though 
    it's details are expanded on in Meijerink and Spaans (2005) and 
    Glover et al (2010). For example, in Meijerink and Spaans (2005) 
    it is made clear that nH refers to n(H) (atomic hydrogen, not
    total hydrogen).
    
    Parameters
    ----------
    coolant : str
        name of coolant, accepts 'CO'
    nH2 : float
        number density of molecular hydrogen (cm^-3)
    nHI : float
        number density of atomic hydrogen (cm^-3)
    ne : float
        number density of free electrons (cm^-3)
    T : float
        gas temperature (K)
    
    
    Returns
    -------
    n_eff : float
        effective number density (cm^-3)
    '''
    from math import sqrt, exp
    
    
    if coolant == 'COr':
        sigma_HI = 2.3e-15
        sigma_H2 = 3.3e-16*(T/1000.)**-0.25
        ve=1.03e4*T**0.5

        n_eff = nH2 + sqrt(2.)*(sigma_HI/sigma_H2)*nHI + (1.3e-8/sigma_H2/ve)*ne

    if coolant == 'COv':
        L_CO_e = 1.03e-10*(T/300.)**0.938*exp(-3080./T)
        L_CO_0 = 1.14e-14*exp(-68./T**(1./3.))*exp(-3080./T)
        
        n_eff = nH2 + 50.0*nHI + (L_CO_e/L_CO_0)*ne
        

    elif coolant == 'H2Or':
        kH2 = 7.4e12*T**0.5
        log10_ke=-8.020+15.749/T**(1./6.)-47.137/T**(1./3.)+76.648/T**0.5-60.191/T**(2./3.)
        ke=10.**log10_ke
        
        n_eff = nH2 + 10.*nHI + (ke/kH2)*ne

    if coolant == 'H2Ov':
        L_H2O_e = 2.6e-6*T**(-0.5)*exp(-2325./T)
        L_H2O_0 = 0.64e-14*exp(-47.5/T**(1./3.))*exp(-2325./T)
        
        n_eff = nH2 + 50.0*nHI + (L_H2O_e/L_H2O_0)*ne

    elif (coolant == 'H2r') or (coolant == 'H2v'):
        n_eff = nH2 + 7.*nHI + 16.*ne
    
    return n_eff
###################################################




###################################################
def NK_COv_cooling(path, Ntilde, k0, s0):
    '''
    CO vibrational cooling function of Neufeld and Kauffman (1993). 
    This is only valid for logT => 2.0.
    
    Parameters
    ----------
    path : str
        path to table of fitting parameters for L_LTE
    Ntilde : float
        
    k0 : int
        order of spline interpolation
    s0 : float
        spline knots 
    
    Returns
    -------
    COv_cool : function
        Cooling function L(nH2,logT) (erg/s). Multiply this by the
        number density of CO to get cooling per volume.
        
    '''
    from numpy import exp, log10
    from astropy.table import Table
    from scipy.interpolate import UnivariateSpline
    import matplotlib.pyplot as plt
    
    
    
    L_LTE_table = Table.read(path)
    
    temps = [float(x) for x in L_LTE_table.keys()[1:]]
    L_LTE_row = get_row(L_LTE_table, Ntilde, k0=k0, s0=s0)[1:]
            
    L_LTE_pts = []
    for i,T in enumerate(L_LTE_table.keys()[1:]):
        L_LTE_pts.append(exp(float(T)/3080.)*10**(-L_LTE_row[i]))
        
    # Interpolate in logspace because that reduces instability
    L_LTE_func = UnivariateSpline(log10(temps), L_LTE_pts, k=k0, s=s0)
    vib_L0   = lambda T: 1.83e-26*T*exp(-68./T**(1./3.)-3080./T)
    

    def COv_cool(nH2, logT):
        cool = nH2/(1.0/vib_L0(10.**logT) + nH2/L_LTE_func(logT))
        return cool
    
    return COv_cool
###################################################





###################################################
def NK_H2r_cooling(paths, k0, s0):
    '''
    H2 rotational line cooling function of Neufeld and Kauffman (1993)
    and Neufeld et al. (1995).
    
    Parameters
    ----------
    paths : dicts
        dictionary of paths to tabulated data. has keys:
        
        'L0_low'
        'L_LTE_low'
        'n_half_low'
        'alpha_low'
        'L0_high'
        'L_LTE_high'
        'n_half_high'
        'alpha_high'

    Ntilde : float
        (log10 of) optical depth parameter
    k0 : int
        order of spline interpolation
    s0 : float
        I don't know
    
    Returns
    -------
    H2_cool : function
        Cooling function L(nH2,logT) (erg/s). Multiply this by the
        number density of H2 to get cooling per volume.
        
    '''
    from numpy import array, exp, log10, sqrt
    from astropy.table import Table
    
    # Open tables
    L0_low = Table.read(paths['L0_low'])
    L_LTE_low = Table.read(paths['L_LTE_low'])
    n_half_low = Table.read(paths['n_half_low'])
    alpha_low = Table.read(paths['alpha_low'])
    
    L0_high = Table.read(paths['L0_high'])
    L_LTE_high = Table.read(paths['L_LTE_high'])
    n_half_high = Table.read(paths['n_half_high'])
    alpha_high = Table.read(paths['alpha_high'])
    
    # Convert low temperature parameters to be consistent with high temperature parameters
    temps_low = 10**array([float(x) for x in L0_low.keys()])
    factor = [exp(509./T) for T in temps_low]
        
    L0_low = Table(rows=[[L0+log10(k) for k,L0 in zip(factor,L0_low[0])]], names=L0_low.keys())
    L_LTE_low = Table(rows=[[L+log10(k) for k,L in zip(factor,L_LTE_low[0])]], names=L_LTE_low.keys())    
    
    
    # Combine low and high temperature tables by averaging the 
    # 100K column
    L0_table = table_combine(L0_low.copy(), L0_high.copy())
    L_LTE_table = table_combine(L_LTE_low.copy(), L_LTE_high.copy())
    n_half_table = table_combine(n_half_low.copy(), n_half_high.copy())
    alpha_table = table_combine(alpha_low.copy(), alpha_high.copy())
    
    # Spline interpolate params, the arguments of these functions are log10(temperature)    
    neglogL0, neglogL_LTE, lognhalf, alpha = NK_params_functions('H2', L0_table, L_LTE_table, n_half_table, alpha_table, 0, k0=k0, s0=s0)


    def H2r_cool(nH2, logT):
        cool = nH2/(10.**neglogL0(logT) + 
            nH2*10.**neglogL_LTE(logT) + 
            ((nH2*10.**(-lognhalf(logT)))**alpha(logT))*(1.0 - 10.**lognhalf(logT)*10.**(-neglogL0(logT))*10.**neglogL_LTE(logT))*10.**neglogL0(logT))
        return cool
    
    return H2r_cool
###################################################







###################################################
def NK_H2v_cooling(k0, s0):
    '''
    H2 vibrational cooling function of Neufeld and Kauffman (1993) 
    and Neufeld et al. (1995). This is only valid for logT => 1.9
    
    Parameters
    ----------
    k0 : int
        order of spline interpolation
    s0 : float
        spline knots 
    
    Returns
    -------
    H2_cool : function
        Cooling function L(nH2,logT) (erg/s). Multiply this by the
        number density of H2 to get cooling per volume.
        
    '''
    from numpy import exp
    
    # Vibrational cooling
    vib_L0   = lambda T: 1.19e-24*T**0.5*exp(-18100./(T + 1190.) - 5987./T)
    vib_LTE  = lambda T: 1.10e-18*exp(-6744./T )

    def H2v_cool(nH2, logT):
        cool = nH2/(1.0/vib_L0(10.**logT) + nH2/vib_LTE(10.**logT))
        return cool
    
    return H2v_cool
###################################################





###################################################
def NK_H2O_cooling(paths, Ntilde, k0, s0):
    '''
    H2O cooling function of Neufeld and Kauffman (1993) and
    Neufeld et al. (1995). This function assumes ortho-para
    ratio of 3:1 at all temperatures.
    
    Parameters
    ----------
    paths : dicts
        dictionary of paths to tabulated data. has keys:
        
        'o_L0_low'
        'o_L_LTE_low'
        'o_n_half_low'
        'o_alpha_low'
        'p_L0_low'
        'p_L_LTE_low'
        'p_n_half_low'
        'p_alpha_low'
        'L0_high'
        'L_LTE_high'
        'n_half_high'
        'alpha_high'

    Ntilde : float
        (log10 of) optical depth parameter
    k0 : list
        orders of spline interpolation: 
            k0[0] for oH2O (low temp)
            k0[1] for pH2O (low temp)
            k0[2] for H2O (high temp)
    s0 : list
        spline knots 
            s0[0] for oH2O (low temp)
            s0[1] for pH2O (low temp)
            s0[2] for H2O (high temp)
    
    Returns
    -------
    H2O_cool : function
        Cooling function L(nH2,logT) (erg/s). Multiply this by the
        number density of H2O to get cooling per volume.
        
    '''
    from scipy.interpolate import UnivariateSpline
    from numpy import log10, array
    from astropy.table import Table
    
    
    # Open tables
    o_L0_low = Table.read(paths['o_L0_low'])
    o_L_LTE_low = Table.read(paths['o_L_LTE_low'])
    o_n_half_low = Table.read(paths['o_n_half_low'])
    o_alpha_low = Table.read(paths['o_alpha_low'])
    
    p_L0_low = Table.read(paths['p_L0_low'])
    p_L_LTE_low = Table.read(paths['p_L_LTE_low'])
    p_n_half_low = Table.read(paths['p_n_half_low'])
    p_alpha_low = Table.read(paths['p_alpha_low'])
    
    L0_high = Table.read(paths['L0_high'])
    L_LTE_high = Table.read(paths['L_LTE_high'])
    n_half_high = Table.read(paths['n_half_high'])
    alpha_high = Table.read(paths['alpha_high'])
    
    # Get the parameters as a function of temperature for this Ntilde
    # I.e., extract(/combine) appropriate row from the tables.
    o_L_LTE_low1 = get_row(o_L_LTE_low, Ntilde-1, k0[0], s0[0])
    o_L_LTE_low2 = get_row(o_L_LTE_low, Ntilde, k0[0], s0[0])
    
    o_n_half_low1 = get_row(o_n_half_low, Ntilde-1, k0[0], s0[0])
    o_n_half_low2 = get_row(o_n_half_low, Ntilde, k0[0], s0[0])
    
    o_alpha_low1 = get_row(o_alpha_low, Ntilde-1, k0[0], s0[0])
    o_alpha_low2 = get_row(o_alpha_low, Ntilde, k0[0], s0[0])
    
    p_L_LTE_low1 = get_row(p_L_LTE_low, Ntilde-1, k0[1], s0[1])
    p_L_LTE_low2 = get_row(p_L_LTE_low, Ntilde, k0[1], s0[1])
    
    p_n_half_low1 = get_row(p_n_half_low, Ntilde-1, k0[1], s0[1])
    p_n_half_low2 = get_row(p_n_half_low, Ntilde, k0[1], s0[1])
    
    p_alpha_low1 = get_row(p_alpha_low, Ntilde-1, k0[1], s0[1])
    p_alpha_low2 = get_row(p_alpha_low, Ntilde, k0[1], s0[1])
    
    
    # Combine adjacent rows by magical Wardle method
    wo = log10(7.5)
    wp = log10(2.5)
    
    o_L_LTE_low3 = (1.-wo)*array(o_L_LTE_low1)[1:] + wo*array(o_L_LTE_low2)[1:]
    o_n_half_low3 = (1.-wo)*array(o_n_half_low1)[1:] + wo*array(o_n_half_low2)[1:]
    o_alpha_low3 = (1.-wo)*array(o_alpha_low1)[1:] + wo*array(o_alpha_low2)[1:]
    
    p_L_LTE_low3 = (1.-wp)*array(p_L_LTE_low1)[1:] + wp*array(p_L_LTE_low2)[1:]
    p_n_half_low3 = (1.-wp)*array(p_n_half_low1)[1:] + wp*array(p_n_half_low2)[1:]
    p_alpha_low3 = (1.-wp)*array(p_alpha_low1)[1:] + wp*array(p_alpha_low2)[1:]
    
    # Interpolation
    logT = log10([float(x) for x in o_L0_low.keys()])
    
    o_L0 = UnivariateSpline(logT, list(o_L0_low[0]), k=k0[0], s=s0[0])
    o_L_LTE = UnivariateSpline(logT, o_L_LTE_low3, k=k0[0], s=s0[0])
    o_n_half = UnivariateSpline(logT, o_n_half_low3, k=k0[0], s=s0[0])
    o_alpha = UnivariateSpline(logT, o_alpha_low3, k=k0[0], s=s0[0])
    
    p_L0 = UnivariateSpline(logT, list(p_L0_low[0]), k=k0[1], s=s0[1])
    p_L_LTE = UnivariateSpline(logT, p_L_LTE_low3, k=k0[1], s=s0[1])
    p_n_half = UnivariateSpline(logT, p_n_half_low3, k=k0[1], s=s0[1])
    p_alpha = UnivariateSpline(logT, p_alpha_low3, k=k0[1], s=s0[1])
    
    # Get the splines at the appropriate Ntilde of the high temperature parameters    
    neglogL0, neglogL_LTE, lognhalf, alpha = NK_params_functions('H2O', L0_high, L_LTE_high, n_half_high, alpha_high, Ntilde, k0[2], s0[2])
    
    
    def H2O_cool(nH2, logT):
        if logT >= 2.0:
            cool = nH2/(10.**neglogL0(logT) + 
                nH2*10.**neglogL_LTE(logT) + 
                ((nH2*10.**(-lognhalf(logT)))**alpha(logT))*(1.0 - 10.**lognhalf(logT)*10.**(-neglogL0(logT))*10.**neglogL_LTE(logT))*10.**neglogL0(logT))
        else:
            o_cool = nH2/(10.**o_L0(logT) + 
                nH2*10.**o_L_LTE(logT) + 
                ((nH2*10.**(-o_n_half(logT)))**o_alpha(logT))*(1.0 - 10.**o_n_half(logT)*10.**(-o_L0(logT))*10.**o_L_LTE(logT))*10.**o_L0(logT))
            p_cool = nH2/(10.**o_L0(logT) + 
                nH2*10.**o_L_LTE(logT) + 
                ((nH2*10.**(-o_n_half(logT)))**o_alpha(logT))*(1.0 - 10.**o_n_half(logT)*10.**(-o_L0(logT))*10.**o_L_LTE(logT))*10.**o_L0(logT))
                
            cool = 0.75*o_cool + 0.25*p_cool
            
        return cool
    
    return H2O_cool
###################################################


    
    
    
    
    
###################################################
def NK_H2Ov_cooling(path, Ntilde, k0, s0):
    '''
    H2O vibrational cooling function of Neufeld and Kauffman (1993). 
    This is only valid for logT => 2.0.
    
    Parameters
    ----------
    path : str
        path to table of fitting parameters for L_LTE
    Ntilde : float
        
    k0 : int
        order of spline interpolation
    s0 : float
        spline knots 
    
    Returns
    -------
    H2Ov_cool : function
        Cooling function L(nH2,logT) (erg/s). Multiply this by the
        number density of H2O to get cooling per volume.
        
    '''
    from numpy import exp, log10, where, linspace
    from astropy.table import Table
    from scipy.interpolate import UnivariateSpline
    import matplotlib.pyplot as plt
    
    L_LTE_table = Table.read(path)
    
    temps = [float(x) for x in L_LTE_table.keys()[1:]]
    L_LTE_row = get_row(L_LTE_table, Ntilde, k0=k0, s0=s0)[1:]
            
    L_LTE_pts = []
    for i,T in enumerate(L_LTE_table.keys()[1:]):
        L_LTE_pts.append(exp(float(T)/2325.)*10**(-L_LTE_row[i]))
        
    # Interpolate in logspace because that reduces instability
    L_LTE_func = UnivariateSpline(log10(temps), L_LTE_pts, k=k0, s=s0)
    vib_L0   = lambda T: 1.03e-26*T*exp(-47.5/T**(1./3.)-2325./T)

    def H2Ov_cool(nH2, logT):
        cool = nH2/(1.0/vib_L0(10.**logT) + nH2/L_LTE_func(logT))
        return cool
    
    return H2Ov_cool
###################################################




        
        
        
        
        
           
###################################################
def O10_OH_cooling(paths, Ntilde, k0, s0):
    '''
    OH cooling function of based on formulism of Neufeld and 
    Kauffman (1993) but with parameters computed by
    Omukai et al. 2010.
    
    Parameters
    ----------
    paths : dicts
        dictionary of paths to tabulated data. has keys:
        
        'L0_low'
        'L_LTE_low'
        'n_half_low'
        'alpha_low'
        'L0_high'
        'L_LTE_high'
        'n_half_high'
        'alpha_high'

    Ntilde : float
        (log10 of) optical depth parameter
    k0 : int
        order of spline interpolation
    s0 : float
        I don't know
    
    Returns
    -------
    OH_cool : function
        Cooling function L(nH2,logT) (erg/s). Multiply this by the
        number density of OH to get cooling per volume, or by the
        abundance of OH (with respect to H nuclei) to get the cooling
        rate per H nuclei.
        
    '''
    from astropy.table import Table
    
    # Open tables: OH
    OH_L0 = Table.read(paths['L0'])
    OH_L_LTE = Table.read(paths['L_LTE'])
    OH_n_half = Table.read(paths['n_half'])
    OH_alpha = Table.read(paths['alpha'])
    
    # Spline interpolate params at the appropriate Ntilde, the
    # arguments of these functions are log10(temperature)
    neglogL0, neglogL_LTE, lognhalf, alpha = NK_params_functions('OH', OH_L0, OH_L_LTE, OH_n_half, OH_alpha, Ntilde, k0=k0, s0=s0)

    def OH_cool(nH2, logT):
        cool = nH2/(10.**neglogL0(logT) + 
            nH2*10.**neglogL_LTE(logT) + 
            ((nH2*10.**(-lognhalf(logT)))**alpha(logT))*(1.0 - 10.**lognhalf(logT)*10.**(-neglogL0(logT))*10.**neglogL_LTE(logT))*10.**neglogL0(logT))
        return cool
    
    return OH_cool
###################################################





        
        
    
    

###################################################
def NK_cooling_functions(
        path, 
        molecules = ['COr', 'H2Or', 'H2r'], 
        Ntilde = {'CO': 18.0, 'H2O': 18.0},
        spline_order = {'COr': 1.0, 'COv': 3.0, 'H2Or': 3.0, 'H2Ov': 3.0, 'oH2O': 3.0, 'pH2O': 3.0, 'H2r': 1.0, 'H2v': 1.0, 'OHr': 1.0}, 
        spline_knots = {'COr': 0.0, 'COv': None, 'H2Or': None, 'H2Ov': None, 'oH2O': None, 'pH2O': None, 'H2r': 0.0, 'H2v': 0.0, 'OHr': 0.0}
    ):
    '''
    Cooling function as defined in Neufeld & Kaufman (1993)
    and Neufeld et al. (1995).
    
    Parameters
    ----------
    path : str
        absolute path of folder containing tables of NK fitting params
    molecules : list
        list of molecule names to choose what cooling functions
        you want. currently supported are 'CO', 'H2r', 'H2v', 'H2O'
    Ntilde : dict
        dictionary of log10(Ntilde) values for the molecules in
        molecules list. E.g. Ntilde={'CO':17.3}. Unecessary for H2
    spline_order : dict
        order of the splining 
    spline_knots : dict
    
    Returns
    -------
    cool_func : dict
        dictionary of interpolation functions for the chosen molecules
        with entries identical with strings in 'molecule' parameter. The
        cooling functions are the cooling rate coefficient L (from
        Neufeld & Kaufman (1993)) multiplied by the molecular hydrogen
        number density. Multiply these functions by the number density
        of the coolant molecule to obtain the cooling per volume in
        units of erg/s/cm^-3 (if your number densities are in cubic cm).
    
    '''
    from os.path import join
    
    cool_func = {}
    
    ### Carbon Monoxide ###
    # Rotational cooling #
    if 'COr' in molecules:
        if 'CO' not in Ntilde:
            print 'ERROR: \'CO\' key in molecule dict but not in Ntilde dict'
            quit()
            
        paths = {
            'L0_low' : join(path, 'L0_CO_95.csv'),
            'L_LTE_low' : join(path, 'L_LTE_CO_95.csv'),
            'n_half_low' : join(path, 'n_half_CO_95.csv'),
            'alpha_low' : join(path, 'alpha_CO_95.csv'),
            'L0_high' : join(path, 'L0_CO_93.csv'),
            'L_LTE_high' : join(path, 'L_LTE_CO_93.csv'),
            'n_half_high' : join(path, 'n_half_CO_93.csv'),
            'alpha_high' : join(path, 'alpha_CO_93.csv')
        }
        cool_func['COr'] = NK_CO_cooling(paths, Ntilde['CO'], k0=spline_order['COr'], s0=spline_knots['COr'])
    
    # Vibrational Cooling #
    if 'COv' in molecules:
        if 'CO' not in Ntilde:
            print 'ERROR: \'COv\' key in molecule dict but \'CO\' not in Ntilde dict'
            quit()
        path_COv = join(path, 'L_LTE_COv_93.csv')
        cool_func['COv'] = NK_COv_cooling(path=path_COv, Ntilde=Ntilde['CO'], k0=spline_order['COv'], s0=spline_knots['COv'])
    #######################
    
    
    ### Molecular Hydrogen ###
    # Rotational cooling #
    if 'H2r' in molecules:
        paths = {
            'L0_low' : join(path, 'L0_H2_95.csv'),
            'L_LTE_low' : join(path, 'L_LTE_H2_95.csv'),
            'n_half_low' : join(path, 'n_half_H2_95.csv'),
            'alpha_low' : join(path, 'alpha_H2_95.csv'),
            'L0_high' : join(path, 'L0_H2_93.csv'),
            'L_LTE_high' : join(path, 'L_LTE_H2_93.csv'),
            'n_half_high' : join(path, 'n_half_H2_93.csv'),
            'alpha_high' : join(path, 'alpha_H2_93.csv')
        }
        cool_func['H2r'] = NK_H2r_cooling(paths, k0=spline_order['H2r'], s0=spline_knots['H2r'])
    
    # Vibrational Cooling #
    if 'H2v' in molecules:
        cool_func['H2v'] = NK_H2v_cooling(k0=spline_order['H2v'], s0=spline_knots['H2v'])
    #######################
  
  
    ### Water ###
    # Rotational cooling #
    if 'H2Or' in molecules:
        if 'H2O' not in Ntilde:
            print 'ERROR: \'H2Or\' key in molecule dict but not in Ntilde dict'
            quit()
            
        paths = {
            'o_L0_low' : join(path, 'L0_oH2O_95.csv'),
            'o_L_LTE_low' : join(path, 'L_LTE_oH2O_95.csv'),
            'o_n_half_low' : join(path, 'n_half_oH2O_95.csv'),
            'o_alpha_low' : join(path, 'alpha_oH2O_95.csv'),
            'p_L0_low' : join(path, 'L0_pH2O_95.csv'),
            'p_L_LTE_low' : join(path, 'L_LTE_pH2O_95.csv'),
            'p_n_half_low' : join(path, 'n_half_pH2O_95.csv'),
            'p_alpha_low' : join(path, 'alpha_pH2O_95.csv'),
            'L0_high' : join(path, 'L0_H2O_93.csv'),
            'L_LTE_high' : join(path, 'L_LTE_H2O_93.csv'),
            'n_half_high' : join(path, 'n_half_H2O_93.csv'),
            'alpha_high' : join(path, 'alpha_H2O_93.csv')
        }
        k_spline = [spline_order['oH2O'],spline_order['pH2O'],spline_order['H2Or']]
        kn_spline = [spline_knots['oH2O'],spline_knots['pH2O'],spline_knots['H2Or']]
        cool_func['H2Or'] = NK_H2O_cooling(paths, Ntilde['H2O'], k0=k_spline, s0=kn_spline)
    
    # Vibrational Cooling #
    if 'H2Ov' in molecules:
        if 'H2O' not in Ntilde:
            print 'ERROR: \'H2Ov\' key in molecule dict but not in Ntilde dict'
            quit()
        path_H2Ov = join(path, 'L_LTE_H2Ov_93.csv')
        cool_func['H2Ov'] = NK_H2Ov_cooling(path=path_H2Ov, Ntilde=Ntilde['H2O'], k0=spline_order['H2Ov'], s0=spline_knots['H2Ov'])
    #######################
    
    
    
    
    
    
    ### Hydroxyl (OH) ###
    # Rotational cooling #
    if 'OHr' in molecules:
        if 'OH' not in Ntilde:
            print 'ERROR: \'OH\' key in molecule dict but not in Ntilde dict'
            quit()
        if 'OHr' not in spline_order:
            print 'ERROR: \'OH\' key in molecule dict but not in spline_order dict'
            quit()
        if 'OHr' not in spline_knots:
            print 'ERROR: \'OH\' key in molecule dict but not in spline_knots dict'
            quit()
            
        paths = {
            'L0' : join(path, 'L0_OH_O10.csv'),
            'L_LTE' : join(path, 'L_LTE_OH_O10.csv'),
            'n_half' : join(path, 'n_half_OH_O10.csv'),
            'alpha' : join(path, 'alpha_OH_O10.csv')
        }
        cool_func['OHr'] = O10_OH_cooling(paths, Ntilde['OH'], k0=spline_order['OHr'], s0=spline_knots['OHr'])
    #######################
    
    
    
    return cool_func
###################################################
        
        
        







###################################################
def dust_gas_cooling_HM89(nH, Tgas, Tdust, s_min):
    '''
    Cooling rate of gas via collisions with dust from Hollenbach
    and Mckee (1989).
    
    Parameters
    ----------
    nH : float
        number density of Hydrogen nuclei (cm^-3)
    Tgas : float
        gas temperature (K)
    Tdust : float
        dust temperature (K)
    s_min : float
        minimum radius of grain size distribution (cm)
    
    Returns
    -------
    cool_rate : float
        cooling rate per volume (erg/s/cm^3)    
    '''
    from numpy import exp
    
    cool_rate = 1.2e-31*nH**2.*(Tgas/1000.)**0.5*(1.e-6/s_min)**0.5*(1.-0.8*exp(-75./Tgas))*(Tgas-Tdust)
    
    return cool_rate
    
###################################################
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
###################################################
def debug_tables(path):
    from os.path import join
    from astropy.table import Table

    ########## CO ##########
    CO_L0_low = Table.read(join(path, 'L0_CO_95.csv'))
    CO_L0_high = Table.read(join(path, 'L0_CO_93.csv'))
    
    CO_L_LTE_low = Table.read(join(path, 'L_LTE_CO_95.csv'))
    CO_L_LTE_high = Table.read(join(path, 'L_LTE_CO_93.csv'))
    CO_L_LTE_vib = Table.read(join(path, 'L_LTE_COv_93.csv'))
    
    CO_n_half_low = Table.read(join(path, 'n_half_CO_95.csv'))
    CO_n_half_high = Table.read(join(path, 'n_half_CO_93.csv'))
    
    CO_alpha_low = Table.read(join(path, 'alpha_CO_95.csv'))
    CO_alpha_high = Table.read(join(path, 'alpha_CO_93.csv'))



    ######### H2 ###########
    H2_L0_low = Table.read(join(path, 'L0_H2_95.csv'))
    H2_L0_high = Table.read(join(path, 'L0_H2_93.csv'))
    
    H2_L_LTE_low = Table.read(join(path, 'L_LTE_H2_95.csv'))
    H2_L_LTE_high = Table.read(join(path, 'L_LTE_H2_93.csv'))
    
    H2_n_half_low = Table.read(join(path, 'n_half_H2_95.csv'))
    H2_n_half_high = Table.read(join(path, 'n_half_H2_93.csv'))
    
    H2_alpha_low = Table.read(join(path, 'alpha_H2_95.csv'))
    H2_alpha_high = Table.read(join(path, 'alpha_H2_93.csv'))
    

    ########## H2O #########
    oH2O_L0_low = Table.read(join(path, 'L0_oH2O_95.csv'))
    pH2O_L0_low = Table.read(join(path, 'L0_pH2O_95.csv'))
    H2O_L0_high = Table.read(join(path, 'L0_H2O_93.csv'))
    
    oH2O_L_LTE_low = Table.read(join(path, 'L_LTE_oH2O_95.csv'))
    pH2O_L_LTE_low = Table.read(join(path, 'L_LTE_pH2O_95.csv'))
    H2O_L_LTE_high = Table.read(join(path, 'L_LTE_H2O_93.csv'))
    H2O_L_LTE_vib = Table.read(join(path, 'L_LTE_H2Ov_93.csv'))
    
    oH2O_n_half_low = Table.read(join(path, 'n_half_oH2O_95.csv'))
    pH2O_n_half_low = Table.read(join(path, 'n_half_pH2O_95.csv'))
    H2O_n_half_high = Table.read(join(path, 'n_half_H2O_93.csv'))
    
    oH2O_alpha_low = Table.read(join(path, 'alpha_oH2O_95.csv'))
    pH2O_alpha_low = Table.read(join(path, 'alpha_pH2O_95.csv'))
    H2O_alpha_high = Table.read(join(path, 'alpha_H2O_93.csv'))
    

    print '======================================='
    print
    print ' CO (rotational) COOLING TABLE FROM N93'
    table_printout(CO_L0_low, CO_L_LTE_low, CO_n_half_low, CO_alpha_low)
    print
    print ' CO (vibrational) COOLING TABLE FROM N93'
    print
    print '----------------------------'
    print '   -log10(exp(3080/T)L_LTE/(erg s^-1))'
    print CO_L_LTE_vib
    print '----------------------------'
    
    print
    print ' CO COOLING TABLE FROM N95'
    table_printout(CO_L0_high, CO_L_LTE_high, CO_n_half_high, CO_alpha_high)
    
    print
    print ' H2O (rotational) COOLING TABLE FROM N93'
    table_printout(H2O_L0_high, H2O_L_LTE_high, H2O_n_half_high, H2O_alpha_high)
    print
    print ' H2O (vibrational) COOLING TABLE FROM N93'
    print
    print '----------------------------'
    print '   -log10(exp(2325/T)L_LTE/(erg s^-1))'
    print H2O_L_LTE_vib
    print '----------------------------'
    
    print
    print ' oH2O COOLING TABLE FROM N95'
    table_printout(oH2O_L0_low, oH2O_L_LTE_low, oH2O_n_half_low, oH2O_alpha_low)
    
    print
    print ' pH2O COOLING TABLE FROM N95'
    table_printout(pH2O_L0_low, pH2O_L_LTE_low, pH2O_n_half_low, pH2O_alpha_low)
    
    print
    print ' H2 COOLING TABLE FROM N93'
    table_printout_H2_93(H2_L0_high, H2_L_LTE_high, H2_n_half_high, H2_alpha_high)
    
    print
    print ' H2 COOLING TABLE FROM N95'
    table_printout_H2_95(H2_L0_low, H2_L_LTE_low, H2_n_half_low, H2_alpha_low)
    
    print
    print '======================================='
###################################################









        
        
        


###################################################
def debug_interpolation(
        path, 
        Ntilde = {'CO':18.1, 'H2O':14.4}, 
        spline_order = {'COr': 1.0, 'COv': 3.0, 'H2Or': 3.0, 'H2Ov': 3.0, 'oH2O': 3.0, 'pH2O': 3.0, 'H2r': 1.0, 'H2v': 1.0}, 
        spline_knots = {'COr': 0.0, 'COv': None, 'H2Or': None, 'H2Ov': None, 'oH2O': None, 'pH2O': None, 'H2r': 0.0, 'H2v': 0.0}
    ):
    '''
    One of the debugging functions. This plots the parameters 
    from the NK93 and NLM95 papers to see how the interpolation
    is working.
    
    Parameters
    ----------
    path : str
        absolute path of folder containing tables of NK fitting params
    Ntilde : dict
        logNtilde for CO and H2O. Needs keys 'CO' and 'H2O'
    spline_order : dict
        
    spline_knots : dict
        
    Result
    ------
    Plots the fitting parameters from NK93 at the chosen logNtilde
    over interpolations of those parameters.
    '''
    from matplotlib import pyplot as plt
    from os.path import abspath, join
    from astropy.table import Table
    from numpy import where, array, exp, log10, linspace, logspace
    from scipy.interpolate import UnivariateSpline
    import seaborn
    
    ########## CO ##########
    CO_L0_low = Table.read(join(path, 'L0_CO_95.csv'))
    CO_L0_high = Table.read(join(path, 'L0_CO_93.csv'))
    
    CO_L_LTE_low = Table.read(join(path, 'L_LTE_CO_95.csv'))
    CO_L_LTE_high = Table.read(join(path, 'L_LTE_CO_93.csv'))
    CO_L_LTE_vib = Table.read(join(path, 'L_LTE_COv_93.csv'))
    
    CO_n_half_low = Table.read(join(path, 'n_half_CO_95.csv'))
    CO_n_half_high = Table.read(join(path, 'n_half_CO_93.csv'))
    
    CO_alpha_low = Table.read(join(path, 'alpha_CO_95.csv'))
    CO_alpha_high = Table.read(join(path, 'alpha_CO_93.csv'))

    # Remove logNtilde=14 from high temperature tables, as this case
    # doesn't exist in the low temperature tables
    CO_L_LTE_high.remove_row(where(CO_L_LTE_high['N'] == 14.0)[0][0])
    CO_n_half_high.remove_row(where(CO_n_half_high['N'] == 14.0)[0][0])
    CO_alpha_high.remove_row(where(CO_alpha_high['N'] == 14.0)[0][0])
    
    # Combine low and high temperature tables by averaging the 
    # 100K column
    CO_L0_table = table_combine(CO_L0_low.copy(), CO_L0_high.copy())
    CO_L_LTE_table = table_combine(CO_L_LTE_low.copy(), CO_L_LTE_high.copy())
    CO_n_half_table = table_combine(CO_n_half_low.copy(), CO_n_half_high.copy())
    CO_alpha_table = table_combine(CO_alpha_low.copy(), CO_alpha_high.copy())
    
    # Spline interpolate params at the appropriate Ntilde, the
    # arguments of these functions are log10(temperature)
    CO_neglogL0, CO_neglogL_LTE, CO_lognhalf, CO_alpha = NK_params_functions('CO', CO_L0_table, CO_L_LTE_table, CO_n_half_table, CO_alpha_table, Ntilde['CO'], k0=spline_order['COr'], s0=spline_knots['COr'])
    
    
    CO_L_LTE_low_pts = get_row(CO_L_LTE_low, Ntilde['CO'], k0=spline_order['COr'], s0=spline_knots['COr'])[1:]
    CO_L_LTE_high_pts = get_row(CO_L_LTE_high, Ntilde['CO'], k0=spline_order['COr'], s0=spline_knots['COr'])[1:]
    CO_n_half_low_pts = get_row(CO_n_half_low, Ntilde['CO'], k0=spline_order['COr'], s0=spline_knots['COr'])[1:]
    CO_n_half_high_pts = get_row(CO_n_half_high, Ntilde['CO'], k0=spline_order['COr'], s0=spline_knots['COr'])[1:]
    CO_alpha_low_pts = get_row(CO_alpha_low, Ntilde['CO'], k0=spline_order['COr'], s0=spline_knots['COr'])[1:]
    CO_alpha_high_pts = get_row(CO_alpha_high, Ntilde['CO'], k0=spline_order['COr'], s0=spline_knots['COr'])[1:]
    
    # CO vibrational
    temps = [float(x) for x in CO_L_LTE_vib.keys()[1:]]
    COv_L_LTE_pts = get_row(CO_L_LTE_vib, Ntilde['CO'], k0=spline_order['COv'], s0=spline_knots['COv'])[1:]
    COv_L_LTE_func = UnivariateSpline(log10(temps), COv_L_LTE_pts, k=spline_order['COv'], s=spline_knots['COv'])
    ########################






    ######### H2 ###########
    H2_L0_low = Table.read(join(path, 'L0_H2_95.csv'))
    H2_L0_high = Table.read(join(path, 'L0_H2_93.csv'))
    
    H2_L_LTE_low = Table.read(join(path, 'L_LTE_H2_95.csv'))
    H2_L_LTE_high = Table.read(join(path, 'L_LTE_H2_93.csv'))
    
    H2_n_half_low = Table.read(join(path, 'n_half_H2_95.csv'))
    H2_n_half_high = Table.read(join(path, 'n_half_H2_93.csv'))
    
    H2_alpha_low = Table.read(join(path, 'alpha_H2_95.csv'))
    H2_alpha_high = Table.read(join(path, 'alpha_H2_93.csv'))
    
    # Convert low temperature parameters to be consistent with high temperature parameters
    temps_low = 10**array([float(x) for x in H2_L0_low.keys()])
    factor = [exp(509./T) for T in temps_low]
        
    L0_low = Table(rows=[[L0+log10(k) for k,L0 in zip(factor,H2_L0_low[0])]], names=H2_L0_low.keys())
    L_LTE_low = Table(rows=[[L+log10(k) for k,L in zip(factor,H2_L_LTE_low[0])]], names=H2_L_LTE_low.keys())    
    
    
    # Combine low and high temperature tables by averaging the 
    # 100K column
    H2_L0_table = table_combine(H2_L0_low.copy(), H2_L0_high.copy())
    H2_L_LTE_table = table_combine(H2_L_LTE_low.copy(), H2_L_LTE_high.copy())
    H2_n_half_table = table_combine(H2_n_half_low.copy(), H2_n_half_high.copy())
    H2_alpha_table = table_combine(H2_alpha_low.copy(), H2_alpha_high.copy())
    
    # Spline interpolate params, the arguments of these functions are log10(temperature)    
    H2_neglogL0, H2_neglogL_LTE, H2_lognhalf, H2_alpha = NK_params_functions('H2', H2_L0_table, H2_L_LTE_table, H2_n_half_table, H2_alpha_table, 0, k0=spline_order['H2r'], s0=spline_knots['H2r'])
    ########################
    
    
    
    
    

    ########## H2O #########
    k0, s0 = 3., None
    oH2O_L0_low = Table.read(join(path, 'L0_oH2O_95.csv'))
    pH2O_L0_low = Table.read(join(path, 'L0_pH2O_95.csv'))
    H2O_L0_high = Table.read(join(path, 'L0_H2O_93.csv'))
    
    oH2O_L_LTE_low = Table.read(join(path, 'L_LTE_oH2O_95.csv'))
    pH2O_L_LTE_low = Table.read(join(path, 'L_LTE_pH2O_95.csv'))
    H2O_L_LTE_high = Table.read(join(path, 'L_LTE_H2O_93.csv'))
    H2O_L_LTE_vib = Table.read(join(path, 'L_LTE_H2Ov_93.csv'))
    
    oH2O_n_half_low = Table.read(join(path, 'n_half_oH2O_95.csv'))
    pH2O_n_half_low = Table.read(join(path, 'n_half_pH2O_95.csv'))
    H2O_n_half_high = Table.read(join(path, 'n_half_H2O_93.csv'))
    
    oH2O_alpha_low = Table.read(join(path, 'alpha_oH2O_95.csv'))
    pH2O_alpha_low = Table.read(join(path, 'alpha_pH2O_95.csv'))
    H2O_alpha_high = Table.read(join(path, 'alpha_H2O_93.csv'))
    
    # Get the parameters as a function of temperature for this Ntilde
    # I.e., extract(/combine) appropriate row from the tables.
    o_L_LTE_low1 = get_row(oH2O_L_LTE_low, Ntilde['H2O']-1, k0, s0)
    o_L_LTE_low2 = get_row(oH2O_L_LTE_low, Ntilde['H2O'], k0, s0)
    
    o_n_half_low1 = get_row(oH2O_n_half_low, Ntilde['H2O']-1, k0, s0)
    o_n_half_low2 = get_row(oH2O_n_half_low, Ntilde['H2O'], k0, s0)
    
    o_alpha_low1 = get_row(oH2O_alpha_low, Ntilde['H2O']-1, k0, s0)
    o_alpha_low2 = get_row(oH2O_alpha_low, Ntilde['H2O'], k0, s0)
    
    p_L_LTE_low1 = get_row(pH2O_L_LTE_low, Ntilde['H2O']-1, k0, s0)
    p_L_LTE_low2 = get_row(pH2O_L_LTE_low, Ntilde['H2O'], k0, s0)
    
    p_n_half_low1 = get_row(pH2O_n_half_low, Ntilde['H2O']-1, k0, s0)
    p_n_half_low2 = get_row(pH2O_n_half_low, Ntilde['H2O'], k0, s0)
    
    p_alpha_low1 = get_row(pH2O_alpha_low, Ntilde['H2O']-1, k0, s0)
    p_alpha_low2 = get_row(pH2O_alpha_low, Ntilde['H2O'], k0, s0)
    
    
    # Combine adjacent rows by magical Wardle method
    wo = log10(7.5)
    wp = log10(2.5)
    
    o_L_LTE_low3 = (1.-wo)*array(o_L_LTE_low1)[1:] + wo*array(o_L_LTE_low2)[1:]
    o_n_half_low3 = (1.-wo)*array(o_n_half_low1)[1:] + wo*array(o_n_half_low2)[1:]
    o_alpha_low3 = (1.-wo)*array(o_alpha_low1)[1:] + wo*array(o_alpha_low2)[1:]
    
    p_L_LTE_low3 = (1.-wp)*array(p_L_LTE_low1)[1:] + wp*array(p_L_LTE_low2)[1:]
    p_n_half_low3 = (1.-wp)*array(p_n_half_low1)[1:] + wp*array(p_n_half_low2)[1:]
    p_alpha_low3 = (1.-wp)*array(p_alpha_low1)[1:] + wp*array(p_alpha_low2)[1:]
    
    # Interpolation
    logT = log10([float(x) for x in oH2O_L0_low.keys()])
    
    o_L0 = UnivariateSpline(logT, list(oH2O_L0_low[0]), k=spline_order['oH2O'], s=spline_knots['oH2O'])
    o_L_LTE = UnivariateSpline(logT, o_L_LTE_low3, k=spline_order['oH2O'], s=spline_knots['oH2O'])
    o_n_half = UnivariateSpline(logT, o_n_half_low3, k=spline_order['oH2O'], s=spline_knots['oH2O'])
    o_alpha = UnivariateSpline(logT, o_alpha_low3, k=spline_order['oH2O'], s=spline_knots['oH2O'])
    
    p_L0 = UnivariateSpline(logT, list(pH2O_L0_low[0]), k=spline_order['pH2O'], s=spline_knots['pH2O'])
    p_L_LTE = UnivariateSpline(logT, p_L_LTE_low3, k=spline_order['pH2O'], s=spline_knots['pH2O'])
    p_n_half = UnivariateSpline(logT, p_n_half_low3, k=spline_order['pH2O'], s=spline_knots['pH2O'])
    p_alpha = UnivariateSpline(logT, p_alpha_low3, k=spline_order['pH2O'], s=spline_knots['pH2O'])
    
    # Get the splines at the appropriate Ntilde of the high temperature parameters    
    H2O_neglogL0, H2O_neglogL_LTE, H2O_lognhalf, H2O_alpha = NK_params_functions('H2O', H2O_L0_high, H2O_L_LTE_high, H2O_n_half_high, H2O_alpha_high, Ntilde['H2O'], k0=spline_order['H2Or'], s0=spline_knots['H2Or'])
    
    H2O_L_LTE_pts = get_row(H2O_L_LTE_high, Ntilde['H2O'], k0=spline_order['H2Or'], s0=spline_knots['H2Or'])[1:]
    H2O_n_half_pts = get_row(H2O_n_half_high, Ntilde['H2O'], k0=spline_order['H2Or'], s0=spline_knots['H2Or'])[1:]
    H2O_alpha_pts = get_row(H2O_alpha_high, Ntilde['H2O'], k0=spline_order['H2Or'], s0=spline_knots['H2Or'])[1:]
    
    
    # CO vibrational H2O_L_LTE_vib
    temps = [float(x) for x in H2O_L_LTE_vib.keys()[1:]]
    H2Ov_L_LTE_pts = get_row(H2O_L_LTE_vib, Ntilde['H2O'], k0=spline_order['H2Ov'], s0=spline_knots['H2Ov'])[1:]
    H2Ov_L_LTE_func = UnivariateSpline(log10(temps), H2Ov_L_LTE_pts, k=spline_order['H2Ov'], s=spline_knots['H2Ov'])
    ########################
    
    
    
    
    
    
    
    
    fig=plt.figure(figsize=(17,10))
    T1, T2 = 1.e1, 1.e4
    N_pts = 100
    
    # CO plots
    ax1=fig.add_subplot(4,4,1)
    ax2=fig.add_subplot(4,4,5)
    ax3=fig.add_subplot(4,4,9)
    ax4=fig.add_subplot(4,4,13)
    ax1.set_title(r'$\rm{CO}; \, \log_{10}\tilde{N}=$'+str(Ntilde['CO']), fontsize=22)
    
    logT = log10([float(x) for x in CO_L0_table.keys()])
    logT0 = linspace(log10(T1), log10(T2), N_pts)
    
    ax1.plot([float(x) for x in CO_L0_low.keys()], list(CO_L0_low[0]), marker='o', ls='')
    ax1.plot([float(x) for x in CO_L0_high.keys()], list(CO_L0_high[0]), marker='o', ls='')
    ax1.plot(10**logT0, CO_neglogL0(logT0))
    ax1.set_xscale('log')
    ax1.set_ylabel(r'$-log_{10}(L_0)$')
    ax1.set_xlim([T1, T2])
    
    ax2.plot([float(x) for x in CO_L_LTE_low.keys()[1:]], CO_L_LTE_low_pts, marker='o', ls='')
    ax2.plot([float(x) for x in CO_L_LTE_high.keys()[1:]], CO_L_LTE_high_pts, marker='o', ls='')
    ax2.plot(10**logT0, CO_neglogL_LTE(logT0))
    ax2.set_xscale('log')
    ax2.set_ylabel(r'$-log_{10}(\mathcal{L}_\mathrm{LTE})$')
    ax2.set_xlim([T1, T2])
    
    ax3.plot([float(x) for x in CO_n_half_low.keys()[1:]], CO_n_half_low_pts, marker='o', ls='')
    ax3.plot([float(x) for x in CO_n_half_high.keys()[1:]], CO_n_half_high_pts, marker='o', ls='')
    ax3.plot(10**logT0, CO_lognhalf(logT0))
    ax3.set_xscale('log')
    ax3.set_ylabel(r'$log_{10}(n_{1/2})$')
    ax3.set_xlim([T1, T2])
    
    ax4.plot([float(x) for x in CO_alpha_low.keys()[1:]], CO_alpha_low_pts, marker='o', ls='')
    ax4.plot([float(x) for x in CO_alpha_high.keys()[1:]], CO_alpha_high_pts, marker='o', ls='')
    ax4.plot(10**logT0, CO_alpha(logT0))
    ax4.set_xscale('log')
    ax4.set_ylabel(r'$\alpha$')
    ax4.set_xlabel(r'$T \, (K)$')
    ax4.set_xlim([T1, T2])
    
    
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.setp(ax3.get_xticklabels(), visible=False)
    #################
    
    
    # H2 Plots
    ax5=fig.add_subplot(4,4,2)
    ax6=fig.add_subplot(4,4,6)
    ax7=fig.add_subplot(4,4,10)
    ax8=fig.add_subplot(4,4,14)
    ax5.set_title(r'$\rm{H}_2$', fontsize=22)
    
    logT = [float(x) for x in H2_L0_table.keys()]
    logT2 = [float(x) for x in H2_alpha_table.keys()]   
    
    ax5.plot(10**array([float(x) for x in H2_L0_low.keys()]), list(H2_L0_low[0]), marker='o', ls='')
    ax5.plot(10**array([float(x) for x in H2_L0_high.keys()]), list(H2_L0_high[0]), marker='o', ls='')
    ax5.plot(logspace(0,4,100), H2_neglogL0(log10(logspace(0,4,100))))
    ax5.set_xscale('log')
    ax5.set_ylabel(r'$-log_{10}(L_0)$')
    ax5.set_xlim([T1, T2])
    
    ax6.plot(10**array([float(x) for x in H2_L_LTE_low.keys()]), list(H2_L_LTE_low[0]), marker='o', ls='')
    ax6.plot(10**array([float(x) for x in H2_L_LTE_high.keys()]), list(H2_L_LTE_high[0]), marker='o', ls='')
    ax6.plot(logspace(0,4,100), H2_neglogL_LTE(log10(logspace(0,4,100))))
    ax6.set_xscale('log')
    ax6.set_ylabel(r'$-log_{10}(\mathcal{L}_\mathrm{LTE})$')
    ax6.set_xlim([T1, T2])
    
    ax7.plot(10**array([float(x) for x in H2_n_half_low.keys()]), list(H2_n_half_low[0]), marker='o', ls='')
    ax7.plot(10**array([float(x) for x in H2_n_half_high.keys()]), list(H2_n_half_high[0]), marker='o', ls='')
    ax7.plot(logspace(0,4,100), H2_lognhalf(log10(logspace(0,4,100))))
    ax7.set_xscale('log')
    ax7.set_ylabel(r'$log_{10}(n_{1/2})$')
    ax7.set_xlim([T1, T2])
    
    ax8.plot(10**array([float(x) for x in H2_alpha_low.keys()]), list(H2_alpha_low[0]), marker='o', ls='')
    ax8.plot(10**array([float(x) for x in H2_alpha_high.keys()]), list(H2_alpha_high[0]), marker='o', ls='')
    ax8.plot(logspace(0,4,100), H2_alpha(log10(logspace(0,4,100))))
    ax8.set_xscale('log')
    ax8.set_ylabel(r'$\alpha$')
    ax8.set_xlabel(r'$T \, (K)$')
    ax8.set_xlim([T1, T2])
    
    plt.setp(ax5.get_xticklabels(), visible=False)
    plt.setp(ax6.get_xticklabels(), visible=False)
    plt.setp(ax7.get_xticklabels(), visible=False)
    #################
    
    
    
    
    
    # H2O plots
    ax9=fig.add_subplot(4,4,3)
    ax10=fig.add_subplot(4,4,7)
    ax11=fig.add_subplot(4,4,11)
    ax12=fig.add_subplot(4,4,15)
    ax9.set_title(r'$\rm{H}_2\rm{O}; \, \log_{10}\tilde{N}=$'+str(Ntilde['H2O']), fontsize=22)
    
    logT = log10([float(x) for x in H2O_L0_high.keys()])
    logT0 = linspace(logT[0], log10(T2), N_pts)
    logTlow = log10([float(x) for x in oH2O_L0_low.keys()])
    logTlow0 = linspace(logTlow[0], logT[0], N_pts)
    
    ax9.plot(10**array(logT), list(H2O_L0_high[0]), marker='o', ls='')
    ax9.plot(10**logT0, H2O_neglogL0(logT0))
    ax9.plot(10**array(logTlow), list(oH2O_L0_low[0]), marker='o', ls='')
    ax9.plot(10**array(logTlow), list(pH2O_L0_low[0]), marker='o', ls='')
    ax9.plot(10**logTlow0, o_L0(logTlow0))
    ax9.plot(10**logTlow0, p_L0(logTlow0))
    ax9.set_xscale('log')
    ax9.set_ylabel(r'$-log_{10}(L_0)$')
    ax9.set_xlim([T1, T2])
    
    ax10.plot([float(x) for x in H2O_L_LTE_high.keys()[1:]], H2O_L_LTE_pts, marker='o', ls='')
    ax10.plot(10**logT0, H2O_neglogL_LTE(logT0))
    ax10.plot(10**array(logTlow), o_L_LTE_low3, marker='o', ls='')
    ax10.plot(10**array(logTlow), p_L_LTE_low3, marker='o', ls='')
    ax10.plot(10**logTlow0, o_L_LTE(logTlow0))
    ax10.plot(10**logTlow0, p_L_LTE(logTlow0))
    ax10.set_xscale('log')
    ax10.set_ylabel(r'$-log_{10}(\mathcal{L}_\mathrm{LTE})$')
    ax10.set_xlim([T1, T2])
    
    ax11.plot([float(x) for x in H2O_n_half_high.keys()[1:]], H2O_n_half_pts, marker='o', ls='')
    ax11.plot(10**logT0, H2O_lognhalf(logT0))
    ax11.plot(10**array(logTlow), o_n_half_low3, marker='o', ls='')
    ax11.plot(10**array(logTlow), p_n_half_low3, marker='o', ls='')
    ax11.plot(10**logTlow0, o_n_half(logTlow0))
    ax11.plot(10**logTlow0, p_n_half(logTlow0))
    ax11.set_xscale('log')
    ax11.set_ylabel(r'$log_{10}(n_{1/2})$')
    ax11.set_xlim([T1, T2])
    
    ax12.plot([float(x) for x in H2O_alpha_high.keys()[1:]], H2O_alpha_pts, marker='o', ls='')
    ax12.plot(10**logT0, H2O_alpha(logT0))
    ax12.plot(10**array(logTlow), o_alpha_low3, marker='o', ls='')
    ax12.plot(10**array(logTlow), p_alpha_low3, marker='o', ls='')
    ax12.plot(10**logTlow0, o_alpha(logTlow0))
    ax12.plot(10**logTlow0, p_alpha(logTlow0))
    ax12.set_xscale('log')
    ax12.set_ylabel(r'$\alpha$')
    ax12.set_xlabel(r'$T \, (K)$')
    ax12.set_xlim([T1, T2])
    
    plt.setp(ax9.get_xticklabels(), visible=False)
    plt.setp(ax10.get_xticklabels(), visible=False)
    plt.setp(ax11.get_xticklabels(), visible=False)
    #################
    
    
    
    
    
    
    # Vibrational plot
    ax13=fig.add_subplot(4,4,4)
    ax14=fig.add_subplot(4,4,12)
    ax13.set_title(r'$\rm{CO(vib)}; \, \log_{10}\tilde{N}=$'+str(Ntilde['CO']), fontsize=22)
    
    logT0 = linspace(log10(T1), log10(T2), N_pts)
    
    ax13.plot([float(x) for x in CO_L_LTE_vib.keys()[1:]], COv_L_LTE_pts, marker='o', ls='')
    ax13.plot(10**logT0, COv_L_LTE_func(logT0))
    ax13.set_xscale('log')
    ax13.set_ylabel(r'$-log_{10}(\exp \left(3080/T\right)\mathcal{L}_\mathrm{LTE}/(\mathrm{erg/s}))$')
    ax13.set_xlabel(r'$T \, (K)$')
    ax13.set_xlim([T1, T2])
    
    
    ax14.set_title(r'$\rm{H}_2\mathrm{O(vib)}; \, \log_{10}\tilde{N}=$'+str(Ntilde['H2O']), fontsize=22)
    
    
    ax14.plot([float(x) for x in H2O_L_LTE_vib.keys()[1:]], H2Ov_L_LTE_pts, marker='o', ls='')
    ax14.plot(10**logT0, H2Ov_L_LTE_func(logT0))
    ax14.set_xscale('log')
    ax14.set_ylabel(r'$-log_{10}(\exp \left(2325/T\right)\mathcal{L}_\mathrm{LTE}/(\mathrm{erg/s}))$')
    ax14.set_xlabel(r'$T \, (K)$')
    ax14.set_xlim([T1, T2])
    
    
    
    
    
    
    fig.subplots_adjust(hspace=0.02, top=0.95, bottom=0.07, left=0.07, right=0.95, wspace=0.25)
    
    plt.show(block=False)
    #plt.show()

    savename = abspath('coolingtest_params.png')
    fig.savefig(savename, type = "png", transparent = False)
    raw_input(' Params plots output to: ' + savename)
    plt.close('all')
###################################################
        


        
        
        
        
        
        
def cooltest_NLM95(path):
    '''
    SINGLE ISOTHERMAL SPHERE FROM NEUFELD, LEPP and MELNICK 1995 (hereafter NLM95)
    
    NLM95 say they chose initial depleted abundances from Millar 91.
    In Millar 91, C starts at 7.3e-5 and O starts at 1.76e-4. NLM95 don't
    show how CO evolves in their chemical model, so I've assumed an
    abundance of CO from the end of Millar's work (Table 5): xCO = 1.452e-4 
    '''
    from matplotlib import pyplot as plt
    from os.path import abspath
    from numpy import linspace, log10
    
    xCO = 1.452e-4 
    xHI = 2.5e-3
    xH2 = 0.5*(1.-xHI)
    
    
    ### Approximating the H2O abundance as a straight line in logspace up to 100 K
    # from Figure 1 in NLM95
    def xH2O_idx(T, f10=-5.75, f100=-6.4):
        b = (10*f10-f100)/9.
        m = (f100-f10)/90.
    
        return m*T+b
        
    
    
    fig2 = plt.figure(figsize=(9,16))
    dens = linspace(3, 10, 30)
    for temp in [10.0, 20.0, 40.0, 100.0]:
        xH2O = 10.**xH2O_idx(temp)
        xO2 = 10.**(-4.2)
    
        LmH2, LmCO, LmH2O = [], [], []
        LmO2 = []
        
        for n in 10**dens:
            Ntilde_H2 = 5.1e19*n**0.5
            logNCO = log10(xCO*Ntilde_H2)
            #logNO2 = log10(7.*xO2*Ntilde_H2)
            logNH2O = log10(xH2O*Ntilde_H2)
            
            cool_func = NK_cooling_functions(path, molecules=['CO', 'H2O'], Ntilde={'CO': logNCO, 'H2O': logNH2O})
            #cool_func_O2 = NK_cooling_functions(path, molecules=['CO'], Ntilde={'CO': logNO2}, debug=False)
            
            #LmH2.append(xH2*cool_func['H2r'](n, log10(temp)))
            LmCO.append(xCO*cool_func['CO'](n, log10(temp)))
            LmH2O.append(xH2O*cool_func['H2O'](n, log10(temp)))
            #LmO2.append(xO2*cool_func['CO'](0.008*n, log10(temp)))
        
        #LmH2 = array(LmH2)
        LmCO = log10(LmCO)
        LmH2O = log10(LmH2O)
        #LmO2 = log10(LmO2)
        
        
        
        if temp == 10.0:
            ax = fig2.add_subplot(221)
        elif temp == 20.0:
            ax = fig2.add_subplot(222)
        elif temp == 40.0:
            ax = fig2.add_subplot(223)
        elif temp == 100.0:
            ax = fig2.add_subplot(224)
        
        #ax.plot(dens, LmH2, lw = 2, label = r'$\mathrm{H}_2$')
        ax.plot(dens, LmH2O, ls='-', lw=2, label = r'$\mathrm{H}_2\mathrm{O}$', color='blue')
        ax.plot(dens, LmCO, ls=':', lw=2, label = r'$\mathrm{CO}$', color='black')
        #ax.plot(dens, LmO2, ls='--', lw=2, label = r'$\mathrm{O2}$', color='red')
        #ax.plot(dens, LmH2O+LmCO+LmO2, lw=3, ls='-', label = r'$\mathrm{Total}$')
        
        #ax.set_yscale('log')
        #ax.set_xscale('log')
        
        ax.set_xlabel(r'$n \, (\mathrm{cm}^{-3})$', fontsize=24)
        
        #ax.set_xlim([1.0e3, 1.0e10])
        ax.set_xlim([3, 10])
        
        if temp == 10.0:
            ax.set_ylabel(r'$\mathrm{Cooling \, Rate \, (erg/s/H}_2)$',fontsize=24)
            ax.text(6., -25.5, 'T = %.0f K' %temp, fontsize=24)
            ax.set_ylim([-31, -25])
        elif temp == 20.0:
            ax.text(6., -25.5, 'T = %.0f K' %temp, fontsize=24)
            ax.set_ylim([-31, -25])
            plt.setp(ax.get_yticklabels(), visible=False)
        elif temp == 40.0:
            ax.set_ylabel(r'$\mathrm{Cooling \, Rate \, (erg/s/H}_2$',fontsize=24)
            ax.text(6., -23.5, 'T = %.0f K' %temp, fontsize=24)
            ax.set_ylim([-29, -23])
        elif temp == 100.0:
            ax.text(6., -23.5, 'T = %.0f K' %temp, fontsize=24)
            ax.set_ylim([-29, -23])
            plt.setp(ax.get_yticklabels(), visible=False)
            
        legend = ax.legend(loc=3, frameon=False)
        for label in legend.get_texts():
            label.set_fontsize(22)
        
        
        ax.tick_params(which = 'major', length=10, width = 2, labelsize=22)
        ax.tick_params(which = 'minor', length=5, width = 2)
        [i.set_linewidth(2) for i in ax.spines.itervalues()]
        
        
    plt.show(block=False)
    fig2.subplots_adjust(left=0.15, bottom=0.10, right=0.95, top=0.95, wspace=0.12)
    
    savename = abspath('cooling_NLM95.png')
    fig2.savefig(savename, type = "png", transparent = False)
    raw_input(' NLM95 figure output to: ' + savename)
    plt.close('all')
    
###############################################









       

###############################################
def cooltest_YZ13(path):
    '''
    We'll try to reproduce the cooling plot (Figure 7b)
    from Yusef-Zadeh et al. 2013 (hereafter YZ13)

    These values of Ntilde are assumptions. I can't find what was used in the paper.
    '''
    import matplotlib.pyplot as plt
    from os.path import abspath
    from numpy import log10, array, logspace
    import seaborn
    
    fig = plt.figure(figsize=(9,6))    
    ax = plt.subplot(111)
    
    for n0 in [1.e3, 1.e4, 1.e5]:
        # Assume logNtilde for CO and H2O, based on Mark only using these values in his mathpad scripts
        logNCO = 18.0
        logNH2O = 18.0
        
        xHI = 1.e-4 # Assumption
        xCO = 2.8e-4 # This was given in the paper
        xH2= 0.5*(1.0-xHI)
        xH2O = lambda x: 10.**(-6.222 + 2.831/(1.0+(245./x)**14.)) # Given in paper (possibly an abundance with respect to H2)
        

        #### Initialise cooling functions ####
        cool_func = NK_cooling_functions(path, molecules=['CO', 'H2r', 'H2v', 'H2O'], Ntilde={'CO': logNCO, 'H2O': logNH2O})
        
        
        T = logspace(0,3,100)
        
        # Get cooling per H2
        LmH2 = []
        for t in T:
            if log10(t) < 1.9:
                LmH2.append(xH2*cool_func['H2r'](n0, log10(t)))
            else:
                LmH2.append(xH2*(cool_func['H2r'](n0, log10(t)) + cool_func['H2v'](n0, log10(t))))
        #LmH2  = xH2*array([cool_func['H2r'](n0, log10(t)) for t in T])
        LmCO  = xCO*array([cool_func['CO'](n0, log10(t)) for t in T])
        LmH2O  = array([xH2O(t)*cool_func['H2O'](n0, log10(t)) for t in T])


        if n0 == 1.e3:
            ax.plot(T, LmH2, linewidth = 2, label = r'$\mathrm{H}_2$', ls='--', dashes=(20,10))
            ax.plot(T, LmH2O, linewidth = 2, label = r'$\mathrm{H}_2\mathrm{O}$', ls='--', dashes=(10,10))
            ax.plot(T, LmCO, linewidth = 2, label = r'$\mathrm{CO}$', ls='--', dashes=(15,10))
        #ax.plot(T, LmH2, linewidth=2, ls='-')
        #ax.plot(T, LmH2O, linewidth=2, ls=':')
        #ax.plot(T, LmCO, linewidth=2, ls='--', label='CO, n(H2)=%.0e' %n0)
        ax.plot(T, LmH2+LmH2O+LmCO, linewidth = 2, label='n(H2)=%.0e' %n0)
    
    ax.set_yscale('log')
    ax.set_xscale('log')
    
    ax.set_ylabel(r'$\mathrm{Cooling \, Rate \, (erg/s/H}_2)$',fontsize=22)
    ax.set_xlabel(r'$T \, \mathrm{(K)}$', fontsize=22)
    
    #ax.text( 100.0, 1.0e-4, 'xHI = ' + str( '%.1e' % xHI ), fontsize = 20 )
    #ax.text( 100.0, 1.0*10**(-4.5), 'xCO = ' + str( '%.1e' % xCO ), fontsize = 20 )
    #ax.text( 100.0, 1.0*10**(-5.5), 'n0 = ' + str( '%.1e' % n0 ), fontsize = 20 )
    
    legend = ax.legend(loc='best',frameon=False)
    #
    #for label in legend.get_texts():
    #    label.set_fontsize(22)
        
    ax.axis([1.0e1, 1.0e3, 1.0e-27, 1.0e-22])
    fig.subplots_adjust(left=0.15, bottom=0.15, right=0.90, top=0.90)
    
    #ax.tick_params(which = 'major', length=10, width = 2, labelsize=20)
    #ax.tick_params(which = 'minor', length=5, width = 2)
    [i.set_linewidth(2) for i in ax.spines.itervalues()]
    plt.show(block=False)
    #plt.show()
    
    savename = abspath('coolingtest_YZ13.png')
    fig.savefig(savename, type = "png", transparent = False)
    raw_input(' YZ13 figure output to: ' + savename)
    plt.close('all')
###################################################





###############################################
def cooltest(
        path, 
        nH=1.e3, 
        temps=[10.,1000.],
        x={'H':1.e-4, 'CO':1.4e-4, 'H2O':1.e-7},
        mol=['CO', 'H2r', 'H2v', 'H2O'],
        Ntilde={'CO': 18.0, 'H2O': 18.0}
    ):
    '''
    We'll try to reproduce the cooling plot (Figure 7b)
    from Yusef-Zadeh et al. 2013 (hereafter YZ13)

    These values of Ntilde are assumptions. I can't find what was used in the paper.
    '''
    import matplotlib.pyplot as plt
    from os.path import abspath
    from numpy import log10, array, logspace
    import seaborn
    
    fig = plt.figure(figsize=(9,6))    
    ax = plt.subplot(111)
    
    xH2= 0.5*(1.0-x['H'])
    nH2=nH*xH2

    #### Initialise cooling functions ####
    cool_func = NK_cooling_functions(path, molecules=mol, Ntilde=Ntilde)
    
    
    T = logspace(log10(temps[0]),log10(temps[1]),50)
    
    # Get cooling per H2
    
    LmH2r = xH2*array([cool_func['H2r'](nH2, log10(t)) for t in T])
    LmH2v = xH2*array([cool_func['H2v'](nH2, log10(t)) for t in T])
            
    LmCO = x['CO']*array([cool_func['CO'](nH2, log10(t)) for t in T])
    LmH2O = x['H2O']*array([cool_func['H2O'](nH2, log10(t)) for t in T])


    ax.plot(T, LmH2r, lw=2, label=r'$\mathrm{H}_2(r)$', ls='--', dashes=(15,5))
    ax.plot(T, LmH2v, lw=2, label=r'$\mathrm{H}_2(v)$', ls='--', dashes=(20,10))
    ax.plot(T, LmH2O, lw=2, label=r'$\mathrm{H}_2\mathrm{O}$', ls='--', dashes=(10,10))
    ax.plot(T, LmCO, lw=2, label=r'$\mathrm{CO}$', ls='--', dashes=(15,10))
    
    ax.set_yscale('log')
    ax.set_xscale('log')
    
    ax.set_ylabel(r'$\mathrm{Cooling \, Rate \, (erg/s/H}_2)$',fontsize=22)
    ax.set_xlabel(r'$T \, \mathrm{(K)}$', fontsize=22)
    
    legend = ax.legend(loc='best',frameon=False)
        
    #ax.axis([1.0e1, 1.0e3, 1.0e-27, 1.0e-22])
    fig.subplots_adjust(left=0.15, bottom=0.15, right=0.90, top=0.90)
    [i.set_linewidth(2) for i in ax.spines.itervalues()]
    plt.show(block=False)
    raw_input('Cool!')
    plt.close('all')
###################################################

        
        
        
        
        
        
        
        


