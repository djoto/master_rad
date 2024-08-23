import copy


class pid:
    def __init__(self,
                 rst_ni,
                 kp_i,
                 ki_i,
                 kd_i,
                 setpoint_i,
                 feedback_i,
                 lock_cnt_i):
        self.rst_ni = rst_ni
        self.kp_i = kp_i
        self.ki_i = ki_i
        self.kd_i = kd_i
        self.setpoint_i = setpoint_i
        self.feedback_i = feedback_i
        self.lock_cnt_i = lock_cnt_i
        self.ctrl_o = 0
        self.lock_o = 0
        self.err_eq0_cnt = 0
        self.integ = 0
        self.err = setpoint_i - feedback_i
        self.err_prev = 0
        self.ctrl_pid = 0

    def run(self,
            rst_ni):
        self.rst_ni = rst_ni

        if (not self.rst_ni):
            self.err_eq0_cnt = 0
        else:
            if ((self.err == 0) and (self.err_eq0_cnt < self.lock_cnt_i)):
                self.err_eq0_cnt += 1

        prop = 0
        # integ = 0
        deriv = 0
        self.err = self.setpoint_i - self.feedback_i
        err_diff = self.err - self.err_prev

        if (not self.rst_ni):
            prop = 0
            self.integ = 0
            deriv = 0
            self.err_prev = 0
            self.ctrl_pid = 0
            self.lock_o = 0
        else:
            prop = self.kp_i * self.err
            self.integ += self.ki_i * self.err
            deriv = self.kd_i * err_diff
            self.err_prev = copy.deepcopy(self.err)
            if ((self.err == 0) and (self.err_eq0_cnt == self.lock_cnt_i) and (self.lock_cnt_i != 0)):
                self.lock_o = 1
            if (not self.lock_o):
                self.ctrl_pid = prop + self.integ + deriv

        self.ctrl_o = int(format(int(self.ctrl_pid), '018b')[4:12], 2)

