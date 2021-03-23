#!/usr/bin/env python
# coding: utf-8

# # Fuctions _Supersaturation 

# ## equilibrium

# In[1]:


def equilibrium(time_s, elements, errors):
    results = []
    for i, j in zip(elements, errors):
    # assigne x and y values
        x = time_s
        y = df[i].to_numpy()*0.01
        y_err = df[j].to_numpy()*0.01
        #print ("\nelement", i)

        # Equilibrium concentration with 1/3 
        # A : rate_constant, to: onset of the time Ceq:eqilibrium concentraion
        # r =1/3
        r=1/3

        # define power function
        def power(x, A, Ceq):
            return A*(x)**(-r)+Ceq

        # fitting power plot with 2sigma
        popt, pcov = curve_fit(power, x, y, bounds=([-10, 0], [100000, 100]), sigma=y_err) 
        #print("Popt:", popt)
        #print("pcov: ", pcov)
        #print("A =", popt[0], "+/-", pcov[0,0]**0.5)
        #print("Ceq =", popt[1], "+/-", pcov[1,1]**0.5)
        results.append((i, "A =", round(popt[0],4), "+/-", round(pcov[0,0]**0.5,4), "Ceq =", round(popt[1],4),"+/-", round(pcov[1,1]**0.5,4)))

    print("\nEquilibrium Concentrations")
    # print stored data of equiilbrium concentration 
    print("Ceq_Al:", results[0][6], "+/-", results[0][8])
    print("Ceq_Cr:", results[1][6], "+/-", results[1][8])
    print("Ceq_Re:", results[2][6], "+/-", results[2][8])
    Ni = 1- results[0][6] - results[1][6] -results[2][6]
    Ni_err = ((results[0][8])**2 + (results[1][8])**2 + (results[2][8])**2)**0.5
    print("Ceq_Ni:", Ni,"+/-", round(Ni_err, 4))

    print("\nList(Al, Cr, Re)")
    eq_conc = [results[0][6], results[1][6], results[2][6]]
    eq_concerr = [results[0][8], results[1][8], results[2][8]]
    print(eq_conc)
    print(eq_concerr)
    return {'eq_conc':eq_conc,'eq_concerr':eq_concerr}


# ## fitting_value

# In[2]:


def fitting_value(x, y, y_err, Ceq):
    
    def power(x, A, r):
        return A*(x)**(-r)+Ceq

    # fitting power plot with 2sigma
    popt, pcov = curve_fit(power, x, y, bounds=([-1, 0], [1, 1]), sigma=y_err) 
    print("\nA =", round(popt[0], 4), "+/-", pcov[0,0]**0.5)
    print("r =", round(popt[1], 4), "+/-", pcov[1,1]**0.5)
    A = round(popt[0], 4)
    r = round(popt[1], 4)

    # Calcualte the R_squared value
    best_fit = A*(x)**(-r)+Ceq
    Rsquared = round(r2_score(best_fit, y), 4)
    print(f"R_2: {Rsquared}")

    # model_fit with fine scale
    xfine = np.linspace(900, max(x), 10000) 
    f2 = A*(xfine)**(-r)+Ceq

    return {'A':A,'r':r, 'Rsquared':Rsquared, 'xfine':xfine, 'f2':f2 }


# ## fitting_with_r values

# In[3]:


def fitting_withr(x, y, y_err, r, Ceq):
    
    def power(x, A):
        return A*(x)**(-r)+Ceq

    # fitting power plot with 2sigma
    popt, pcov = curve_fit(power, x, y, bounds=([-1], [1]), sigma=y_err) 
    print("A =", round(popt[0], 4), "+/-", pcov[0,0]**0.5)

    A = round(popt[0], 4)

    # Calcualte the R_squared value
    best_fit = A*(x)**(-r)+Ceq
    Rsquared = round(r2_score(best_fit, y), 4)
    print(f"R_2: {Rsquared}")

    # model_fit with fine scale
    xfine = np.linspace(900, max(x), 10000) 
    f2 = A*(xfine)**(-r)+Ceq

    return {'A':A, 'Rsquared':Rsquared, 'xfine':xfine, 'f2':f2}

