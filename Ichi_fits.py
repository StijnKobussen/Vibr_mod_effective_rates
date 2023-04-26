import numpy as np
import matplotlib

Tev = np.linspace(0.2,10,100)
Tiv = Tev # Assume Ti=Te


def ichihara_rates(iso_mass = 2):

    #calculate effective molecular CX rate using Ichihara rates
    import mat73, os
    ichi_tables = os.path.join(os.path.dirname(__file__), 'MolCX_Ichi.mat')

    ichi_tab = mat73.loadmat(ichi_tables)
    from scipy.interpolate import interp1d

    #make interpolation object
    f_ichi = interp1d(ichi_tab['T'], 1e-6*ichi_tab['MolCX_Ichi_01'], bounds_error=False,
                        fill_value=(1e-6*ichi_tab['MolCX_Ichi_01'][:, 0], 1e-6*ichi_tab['MolCX_Ichi_01'][:, -1])) #interpolate Ichihara tables at EH2=0.1 eV. Nearest neighbour extrapolation

    return f_ichi(Tiv/iso_mass)

def ichi_fit(input_rates):
    fit = np.zeros((15,9))
    for i in range(15):
        fit[i,:] = np.flip(np.polyfit(np.log(Tev),np.log(input_rates[i,:]/1e-6),8))
    return fit

def eval_1D(coeff,T):
    o = np.zeros(np.shape(T))
    for i in range(0,len(coeff)):
        o = o + coeff[i]*(np.log(T)**i)
    return 1e-6*np.exp(o)


def output_string(A):
    exponent = str(f"{A:E}").split('E')[1]
    output = f"{A / 10**int(exponent):.12f}E{exponent}"
    if A>0:
        output = ' ' + output
    return output

def block_string(X):
    block = '  b0 ' + output_string(X[0]) + '  b1 ' + output_string(X[1]) + '  b2 ' + output_string(X[2])+'\n'+\
            '  b3 ' + output_string(X[3]) + '  b4 ' + output_string(X[4]) + '  b5 ' + output_string(X[5])+'\n'+\
            '  b6 ' + output_string(X[6]) + '  b7 ' + output_string(X[7]) + '  b8 ' + output_string(X[8])+'\n'
    return block


def numpy_to_string(i): 
    part_1 = "\subsection{\n" +\
                f"Reaction 2.{i}q6\n"+\
                f"$ p + H_2(v={i}) \\rightarrow H + H_2^+$ (ion conversion)\n" +\
                "}\n"+\
                "Rate coeff. for H2 at rest, derived from HYDHEL rate coeff. data.\n"+\
                "Taken at $E(H_2) = 0.1 \\approx 0.0$ eV,  and fit is for temperature $T_p=T$ with $H_2$ at rest.\n"+\
                "\n"+\
                "\\begin{small}\\begin{verbatim}\n"+\
                "\n"
                
    part_2 =   "\n"+\
                "\\end{verbatim}\end{small}\n"+\
                "\n"+\
                "\\newpage\n"
    return part_1, part_2


full_string = ''
coeffs = np.random.rand(15,9)

def gen_full_string():
    full_string = ''
    for i in range(15):
        str1, str2 = numpy_to_string(i)
        full_string += str1+block_string(coeffs[i,:])+str2
    return full_string



rates = ichihara_rates()
coeffs = ichi_fit(rates)
full_string = gen_full_string()

# print(numpy_to_string(coeff))

dat_file = open("rates/custom_ichi.tex", 'w')
dat_file.write(full_string)
dat_file.close()

# import matplotlib.pyplot as plt
# plt.figure()
# plt.loglog(Tev,rates[0,:],label='Effective rate (NEW)')
# fit = eval_1D(coeff[:,0],Tev)
# plt.plot(Tev, fit,  '--', label='Fit')
# plt.xlabel('Temperature (eV)')
# plt.legend()
# plt.show()