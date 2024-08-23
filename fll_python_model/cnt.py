class cnt:
    def __init__(self):
        self.cnt_o = 0
        self.default_val = 0

    def run(self,
            rst_ni,
            en_i,
            up_down_i):
        if (not rst_ni):
            self.cnt_o = self.default_val
        else:    
            if (en_i):
                if (up_down_i):
                    self.cnt_o += 1
                else:
                    self.cnt_o -= 1
        return self.cnt_o
