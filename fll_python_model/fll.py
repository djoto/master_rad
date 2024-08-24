from dco import dco
from cnt import cnt
from pid import pid


class fll:
    def __init__(self,
                 # Inputs from design
                 CW,               # control word width
                 clk_ref_i,        # reference clock
                 clk_ref_en_i,     # reference clock enable
                 rst_ni,           # async reset
                 clk_mult_i,       # reference frequency multiplier [40]
                 dco_pwr_sel_i,    # DCO clock output power supply selection: VDDL/VDD [0/1]
                 dco_ctrl_man_i,   # manual DCO control word [200]
                 dco_ctrl_mode_i,  # DCO control mode: FIXED/MANUAL/CNT/PID [3/2]
                 pid_kp_i,         # PID controller proportional constant [0b01000000]
                 pid_ki_i,         # PID controller integral constant [0b01000000]
                 pid_kd_i,         # PID controller derivative constant [0]
                 lock_cnt_i,       # FLL lock counter condition [0b1000]
                 # Additional input parameters
                 k_dco,            # DCO frequency resolution
                 clk_dco_init):    # DCO initial frequency (dco_ctrl=0) 
        """
        Frequency-locked loop (FLL) is a negative feedback control system that locks the output
        frequency signal to the target frequency. Principally, it continuously controls the
        oscillator frequency in an automated way until its output frequency matches the target
        value, after which that value is maintained at the output.
        """
        # Inputs from design
        self.CW = CW
        self.clk_ref_i = clk_ref_i 
        self.clk_ref_en_i = clk_ref_en_i
        self.rst_ni = rst_ni
        self.clk_mult_i = clk_mult_i
        self.dco_pwr_sel_i = dco_pwr_sel_i  
        self.dco_ctrl_man_i = dco_ctrl_man_i
        self.dco_ctrl_mode_i = dco_ctrl_mode_i 
        self.pid_kp_i = pid_kp_i
        self.pid_ki_i = pid_ki_i
        self.pid_kd_i = pid_kd_i
        self.lock_cnt_i = lock_cnt_i
        # Additional input parameters
        self.k_dco = k_dco
        self.clk_dco_init = clk_dco_init
        # Component instantiation
        self.dco_inst = dco(k_dco=self.k_dco,
                            init_freq=self.clk_dco_init)
        self.cnt_inst = cnt()
        self.pid_inst = pid(rst_ni=self.rst_ni,
                            kp_i=self.pid_kp_i,
                            ki_i=self.pid_ki_i,
                            kd_i=self.pid_kd_i,
                            setpoint_i=self.clk_mult_i,
                            feedback_i=self.clk_dco_init//self.clk_ref_i,
                            lock_cnt_i=self.lock_cnt_i)
        # Outputs from design
        self.lock_o = self.clk_dco_init//self.clk_ref_i == self.clk_mult_i
        self.clk_dco_o = self.clk_dco_init

    def run(self,
            rst_ni):
        self.rst_ni = rst_ni

        # Convert control mode integer to binary array (1/0 integers) 
        dco_ctrl_mode_bin_arr = list(map(int, list(bin(self.dco_ctrl_mode_i)[2:][::-1])))

        # PID logic
        self.pid_inst.feedback_i = self.clk_dco_o//self.clk_ref_i
        self.pid_inst.run(rst_ni=self.rst_ni)
        dco_ctrl_pid = self.pid_inst.ctrl_o

        # Bang-bang logic
        #cnt_en_i = 1  # used if you want frequency oscillation in the stable state
        cnt_en_i = not self.pid_inst.lock_o if (self.clk_mult_i != self.clk_dco_o//self.clk_ref_i) else 0
        cnt_up_down = 1 if (self.clk_mult_i > self.clk_dco_o//self.clk_ref_i) else 0
        self.cnt_inst.run(rst_ni=self.rst_ni,
                          en_i=cnt_en_i and dco_ctrl_mode_bin_arr[1],
                          up_down_i=cnt_up_down)
        dco_ctrl_cnt = self.cnt_inst.cnt_o

        # Control preprocessing
        dco_ctrl_man = self.dco_ctrl_man_i if (dco_ctrl_mode_bin_arr[0]) else 203
        dco_ctrl_auto = dco_ctrl_pid if (dco_ctrl_mode_bin_arr[0]) else dco_ctrl_cnt
        dco_ctrl = dco_ctrl_auto if (dco_ctrl_mode_bin_arr[1]) else dco_ctrl_man

        # DCO logic
        self.dco_inst.run(ctrl=dco_ctrl)

        # FLL outputs setup
        self.clk_dco_o = int(self.dco_inst.freq_out)
        self.lock_o = self.pid_inst.lock_o
