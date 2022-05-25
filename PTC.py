import numpy as np

class PTC:
    def __init__(self, description, signal, noise):
        self.description = description
        self.signal = signal
        self.noise = noise

class camera(object):
    # PIX = 1000
    # DATA = 100                                # number of data points
    # edn = 2                                   # e−/DN
    # RN_e = 1.7                                # read noise (e−) \
    # RN = RN_e/edn                             # read noise (DN) \
    # FW_e = 10**5                              # full well (e−) \
    # FW = FW_e/edn                             # full well (DN) \
    # SCALE = DATA/np.log10(FW)                 # full well scale factor \
    # PN = 0.02                                 # FPN factor \
    # T = 270                                   # operating temperature (K) \
    # k1 = 8.62*10**-5                          # Boltzmann’s constant \
    # DFM = 0.5                                 # dark current figure of merit (nA/cmˆ2) \
    # DN = 0.30                                 # dark FPN factor \
    # PA = (8*10**-4)**2                        # pixel area (cmˆ2) \
    # t =.3                                     # integration time \
    # Eg = 1.1557-(7.021*10**-4*T**2)/(1108+T)  # silicon band gap energy (eV)
    # DARKe = t * 2.55 * 10**15 *PA *DFM * T**1.5 * np.exp(-Eg/(2*k1*T) ) # dark current (e−)
    # DARK = DARKe/edn                          # dark current (DN)

    def __init__(self, name, pixels=1000, data=100, edn=2, readNoise_e=1.7, PN=0.02, T=300, DFM=0.5, DN=0.3, PA=(8 * 10 ** -4) ** 2, t=0.01):
        self.SIG5 = None
        self.SIG4 = None
        self.SIG2 = None
        self.ptc4 = None
        self.ptc3 = None
        self.ptc2 = None
        self.ptc1 = None
        self.SIG3 = None
        self.SIG1 = None
        self.name = name
        self.pixels = pixels
        self.data = data
        self.edn = edn
        self.readNoise_e = readNoise_e
        self.PN = PN
        self.T = T
        self.DFM = DFM
        self.DN = DN
        self.PA = PA
        self.t = t

        self.k1 = 8.62*10**-5
        self.FW_e = 10 ** 5  # % full well (e−) \
        self.FW = self.FW_e / self.edn
        self.SCALE = self.data / np.log10(self.FW)
        self.Eg = 1.1557 - (7.021 * 10 ** -4 * self.T ** 2) / (1108 + self.T)
        self.RN = self.readNoise_e / self.edn
        self.DARKe = self.t * 2.55 * 10 ** 15 * self.PA * self.DFM * self.T ** 1.5 * np.exp(
            -self.Eg / (2 * self.k1 * self.T))
        self.DARK = self.DARKe / self.edn

    def buildPTC(self):
        C = np.random.randn(self.pixels)  # random number generator for FPN \
        F = np.random.randn(self.pixels)  # random number generator for dark FPN \

        self.RN = self.readNoise_e / self.edn
        self.DARKe = self.t * 2.55 * 10 ** 15 * self.PA * self.DFM * self.T ** 1.5 * np.exp(
            -self.Eg / (2 * self.k1 * self.T))
        self.DARK = self.DARKe / self.edn

        self.SIG1 = []
        self.SIG2 = []
        self.SIG3 = []
        self.SIG4 = []
        self.SIG5 = []
        for i in range(self.data):

            sig = 10 ** (i / self.SCALE)  # signal step (DN) \
            A = np.random.randn(self.pixels, self.data)  # random number generator \
            B = np.random.randn(self.pixels, self.data)  # random number generator \
            D = np.random.randn(self.pixels, self.data)  # random number generator
            read = self.RN * A[0:self.pixels, i]  # read noise (DN)
            shot = (sig / self.edn) ** 0.5 * B[0:self.pixels, i]  # % shot noise (DN)
            FPN = sig * self.PN * C
            Dshot = (self.DARK / self.edn) ** 0.5 * D[0:self.pixels, i]
            DFPN = self.DARK * self.DN * F
            self.SIG1.append(sig + read + shot + FPN + Dshot + DFPN)
            self.SIG2.append(sig + read + shot + FPN + Dshot)
            self.SIG3.append(sig + read + shot + Dshot)
            self.SIG4.append(sig + read + shot)
            self.SIG5.append(sig + read + shot + FPN)

        self.ptc1 = PTC('Read, Shot, FPN, Dshot, DFPN', np.mean(self.SIG1, axis=1), np.std(self.SIG1, axis=1))
        self.ptc2 = PTC('read + shot + FPN + Dshot', np.mean(self.SIG2, axis=1), np.std(self.SIG2, axis=1))
        self.ptc3 = PTC('read + shot + Dshot', np.mean(self.SIG3, axis=1), np.std(self.SIG3, axis=1))
        self.ptc4 = PTC('read + shot', np.mean(self.SIG4, axis=1), np.std(self.SIG4, axis=1))
        self.ptc5 = PTC('sig + read + shot + FPN', np.mean(self.SIG5, axis=1), np.std(self.SIG5, axis=1))


