class dco:
    def __init__(self,
                 k_dco,
                 init_freq):
        self.k_dco = k_dco
        self.init_freq = init_freq
        self.freq_out = init_freq

    def run(self,
            ctrl):
        self.freq_out = self.init_freq + self.k_dco * ctrl
