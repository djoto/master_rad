class dco:
    def __init__(self,
                 # num_rows,
                 # num_columns,
                 # num_always_on_inv,
                 k_dco,
                 init_freq):
        self.num_rows = 18
        self.num_columns = 15
        self.num_always_on_inv = 15
        self.k_dco = k_dco  # MHz
        self.init_freq = init_freq  # MHz

    def run(self,
            dco_ctrl):
        freq_out = self.init_freq + self.k_dco * dco_ctrl
        return int(freq_out)
