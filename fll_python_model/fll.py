from dco import dco
from cnt import cnt
from pid import pid


class fll:
    def __init__(self,
                 CW,
                 clk_ref_i,
                 clk_ref_en_i,
                 rst_ni,
                 clk_mult_i,
                 dco_pwr_sel_i,
                 dco_ctrl_man_i,
                 dco_ctrl_mode_i,
                 pid_kp_i,
                 pid_ki_i,
                 pid_kd_i,
                 lock_cnt_i,
                 k_dco,
                 init_dco_freq,
                 max_iter):
        """
        Frequency-locked loop (FLL) is a negative feedback control system that locks the output
        frequency signal to the target frequency. Principally, it continuously controls the
        oscillator frequency in an automated way until its output frequency matches the target
        value, after which that value is maintained at the output.

        Description of the FLL parameters:
        CW - control word width
        clk_ref_i - reference clock
        clk_ref_en_i - reference clock enable
        rst_ni - async reset
        clk_mult_i - reference frequency multiplier [20]
        dco_pwr_sel_i - DCO clock output power supply selection (1->VDD, 0->VDDL)
        dco_ctrl_man_i - manual DCO control word [200]
        dco_ctrl_mode_i - DCO control mode: FIXED/MANUAL/CNT/PID [3/2]
        pid_kp_i - PID controller proportional constant [0b01000000]
        pid_ki_i - PID controller integral constant [0b01000000]
        pid_kd_i - PID controller derivative constant [0]
        lock_cnt_i - FLL lock counter condition [0b1000]
        lock_o - output FLL lock signal
        """
        self.CW = CW
        self.clk_ref_i = clk_ref_i  # 32 MHz
        self.clk_ref_en_i = clk_ref_en_i
        self.rst_ni = rst_ni
        self.clk_mult_i = clk_mult_i
        self.dco_pwr_sel_i = dco_pwr_sel_i  # 1->VDD, 0->VDDL
        self.dco_ctrl_man_i = dco_ctrl_man_i
        self.dco_ctrl_mode_i = dco_ctrl_mode_i  # 2->CNT, 3->PID
        self.pid_kp_i = pid_kp_i
        self.pid_ki_i = pid_ki_i
        self.pid_kd_i = pid_kd_i
        self.lock_cnt_i = lock_cnt_i
        self.k_dco = k_dco
        self.init_dco_freq = init_dco_freq
        self.max_iter = max_iter

    def run(self):

        dco_inst = dco(k_dco=self.k_dco,
                       init_freq=self.init_dco_freq)

        cnt_inst = cnt(cnt_o=0)

        dco_freq = dco_inst.run(0)

        pid_inst = pid(rst_ni=self.rst_ni,
                       kp_i=self.pid_kp_i,
                       ki_i=self.pid_ki_i,
                       kd_i=self.pid_kd_i,
                       setpoint_i=self.clk_mult_i,
                       feedback_i=0,
                       lock_cnt_i=self.lock_cnt_i)

        dco_ctrl_pid = 0
        dco_ctrl_cnt = 0

        cnt_up_down = 1
        cnt_en_i = 1

        cnt_loop = 0
        num_steps_for_640 = 0
        reached_640 = 0
        freq_arr = []

        while (cnt_loop <= self.max_iter):
#        while (self.clk_ref_i * self.clk_mult_i != dco_freq):
            if (self.clk_mult_i == dco_freq//self.clk_ref_i):
                reached_640 = 1
            if (not reached_640):
                num_steps_for_640 += 1

            # PID logic
            dco_ctrl_pid = pid_inst.run()["ctrl_o"]

            # print("dco_ctrl_pid: " + str(dco_ctrl_pid))

            # cnt_en_i = 1 # if (self.clk_mult_i != dco_freq//self.clk_ref_i) else 0
            cnt_en_i = not pid_inst.lock_o if (self.clk_mult_i != dco_freq//self.clk_ref_i) else 0
            cnt_up_down = 1 if (self.clk_mult_i > dco_freq//self.clk_ref_i) else 0
            dco_ctrl_cnt = cnt_inst.run(self.clk_ref_en_i, cnt_en_i, cnt_up_down)

            # print("dco_ctrl_cnt: " + str(dco_ctrl_cnt))

            dco_ctrl_man = self.dco_ctrl_man_i if (self.dco_ctrl_mode_i in [1, 3]) else 203
            dco_ctrl_auto = dco_ctrl_pid if (self.dco_ctrl_mode_i in [1, 3]) else dco_ctrl_cnt
            dco_ctrl = dco_ctrl_auto if (self.dco_ctrl_mode_i in [2, 3]) else dco_ctrl_man

            # print("dco_ctrl: " + str(dco_ctrl))

            dco_freq = dco_inst.run(dco_ctrl)
            pid_inst.feedback_i = dco_freq//self.clk_ref_i   # current clock multiplier

            # print("dco_freq: " + str(dco_freq))

            # print("\n\n")

            freq_arr.append(dco_freq)
            cnt_loop += 1
        
        str_crtl_man = "Manual control: " + str(self.dco_ctrl_man_i) if (self.dco_ctrl_mode_i in [1, 3]) else "Manual control: " + str(203)
        str_ctrl_auto = "PID control"  if (self.dco_ctrl_mode_i in [1, 3]) else "Bang-bang control"
        str_ctrl = str_ctrl_auto if (self.dco_ctrl_mode_i in [2, 3]) else str_ctrl_man
        # print("Number of steps until reaching 640MHz (" + str_ctrl + "): " + str(num_steps_for_640) + "\n")
        print("Number of steps until reaching 640MHz (" + str_ctrl + "): " + str(num_steps_for_640) + ". Real frequency: " + str(round(dco_freq/1000000, 2)) + "MHz\n")

        return {"freq_arr": freq_arr,
                "cnt_loop": cnt_loop,
                "str_ctrl": str_ctrl}