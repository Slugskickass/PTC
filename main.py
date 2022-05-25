import PTC as PTC
import matplotlib.pyplot as plt

PIX = 1000
DATA = 100                                # % number of data points
edn = 2                                   # e−/DN
RN_e = 1.7                                # read noise (e−) \
PN = 0.02                                 # FPN factor \
T = 270                                   # operating temperature (K) \
DFM = 0.5                                 # dark current figure of merit (nA/cmˆ2) \
DN = 0.30                                 # dark FPN factor \
PA = (8*10**-4)**2                        # pixel area (cmˆ2) \
t = .3                                    # % integration time \



#PIX, DATA, edn, RN_e, PN, T, DFM, DN, PA, t

if __name__ == '__main__':
#    myCamera = PTC.camera("Ham", PIX, DATA, edn, RN_e, PN, T, DFM, DN, PA, t)

    myCamera = PTC.camera("Ham", PIX, DATA, edn, RN_e, PN, T, DFM, DN, PA, t)

    # RN_e done
    # PN done
    # T done
    # DFM not done
    # DN not done
    # PA done
    # t done

    for current in range(1, 10, 1):
        myCamera.buildPTC()
        plt.loglog(myCamera.ptc1.signal, myCamera.ptc1.noise, label=current)
    plt.legend()
    plt.title(myCamera.ptc1.description)
    plt.show()



