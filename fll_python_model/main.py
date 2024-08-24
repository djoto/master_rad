from fll import fll
import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib

FLL_MAX_ITER = 250
SUBPLOTS = 0

def run_fll(fll_inst, fll_max_iter):
    freq_arr = []
    cnt_loop = 0
    num_steps_for_640 = 0
    reached_640 = 0
    dco_ctrl_mode_bin_arr = list(map(int, list(bin(fll_inst.dco_ctrl_mode_i)[2:][::-1])))
    while (cnt_loop <= fll_max_iter):
        if (fll_inst.clk_mult_i == fll_inst.clk_dco_o//fll_inst.clk_ref_i):
            reached_640 = 1
        if (not reached_640):
            num_steps_for_640 += 1
        fll_inst.run(rst_ni=fll_inst.rst_ni)
        freq_arr.append(fll_inst.clk_dco_o)
        cnt_loop += 1
    str_ctrl_man = "Manual control: " + str(fll_inst.dco_ctrl_man_i) if (dco_ctrl_mode_bin_arr[0]) else "Manual control: " + str(203)
    str_ctrl_auto = "PID control"  if (dco_ctrl_mode_bin_arr[0]) else "Bang-bang control"
    str_ctrl = str_ctrl_auto if (dco_ctrl_mode_bin_arr[1]) else str_ctrl_man
    print("Number of steps until reaching 640MHz (" + str_ctrl + "): " + str(num_steps_for_640) + ". Reached frequency: " + str(round(fll_inst.clk_dco_o/1000000, 2)) + "MHz\n")
    fll_data = {"freq_arr": freq_arr,
                "cnt_loop": cnt_loop,
                "str_ctrl": str_ctrl}
    return fll_data


if __name__ == "__main__":

    fll_inst_1 = fll(
        CW=8,
        clk_ref_i=16*10**6,  # 32 MHz
        clk_ref_en_i=1,
        rst_ni=1,
        clk_mult_i=40,
        dco_pwr_sel_i=0,  # 1->VDD, 0->VDDL
        dco_ctrl_man_i=200,
        dco_ctrl_mode_i=2,  # 2->CNT, 3->PID
        pid_kp_i=16,
        pid_ki_i=16,
        pid_kd_i=0,
        lock_cnt_i=8,
        k_dco=2.8*10**6,
        clk_dco_init=42*10**6)  # output in MHz

    fll_data_1 = run_fll(fll_inst_1, FLL_MAX_ITER)


    fll_inst_2 = fll(
        CW=8,
        clk_ref_i=16*10**6,  # 32 MHz
        clk_ref_en_i=1,
        rst_ni=1,
        clk_mult_i=40,
        dco_pwr_sel_i=0,  # 1->VDD, 0->VDDL
        dco_ctrl_man_i=200,
        dco_ctrl_mode_i=3,  # 2->CNT, 3->PID
        pid_kp_i=16,
        pid_ki_i=16,
        pid_kd_i=0,
        lock_cnt_i=8,
        k_dco=2.8*10**6,
        clk_dco_init=42*10**6)  # output in MHz

    fll_data_2 = run_fll(fll_inst_2, FLL_MAX_ITER)


    fll_inst_3 = fll(
        CW=8,
        clk_ref_i=16*10**6,  # 32 MHz
        clk_ref_en_i=1,
        rst_ni=1,
        clk_mult_i=40,
        dco_pwr_sel_i=0,  # 1->VDD, 0->VDDL
        dco_ctrl_man_i=200,
        dco_ctrl_mode_i=3,  # 2->CNT, 3->PID
        pid_kp_i=1,
        pid_ki_i=16,
        pid_kd_i=0,
        lock_cnt_i=8,
        k_dco=2.8*10**6,
        clk_dco_init=42*10**6)  # output in MHz

    fll_data_3 = run_fll(fll_inst_3, FLL_MAX_ITER)


    fll_inst_4 = fll(
        CW=8,
        clk_ref_i=16*10**6,  # 32 MHz
        clk_ref_en_i=1,
        rst_ni=1,
        clk_mult_i=40,
        dco_pwr_sel_i=0,  # 1->VDD, 0->VDDL
        dco_ctrl_man_i=200,
        dco_ctrl_mode_i=3,  # 2->CNT, 3->PID
        pid_kp_i=64,
        pid_ki_i=16,
        pid_kd_i=0,
        lock_cnt_i=8,
        k_dco=2.8*10**6,
        clk_dco_init=42*10**6)  # output in MHz

    fll_data_4 = run_fll(fll_inst_4, FLL_MAX_ITER)


    freq_arr_1 = fll_data_1["freq_arr"]
    freq_arr_1[:] = [x / 1000000 for x in freq_arr_1] # to get frequency in MHz
    cnt_loop_1 = fll_data_1["cnt_loop"]
    str_ctrl_1 = fll_data_1["str_ctrl"]

    freq_arr_2 = fll_data_2["freq_arr"]
    freq_arr_2[:] = [x / 1000000 for x in freq_arr_2] # to get frequency in MHz
    cnt_loop_2 = fll_data_2["cnt_loop"]
    str_ctrl_2 = fll_data_2["str_ctrl"]

    freq_arr_3 = fll_data_3["freq_arr"]
    freq_arr_3[:] = [x / 1000000 for x in freq_arr_3] # to get frequency in MHz
    cnt_loop_3 = fll_data_3["cnt_loop"]
    str_ctrl_3 = fll_data_3["str_ctrl"]

    freq_arr_4 = fll_data_4["freq_arr"]
    freq_arr_4[:] = [x / 1000000 for x in freq_arr_4] # to get frequency in MHz
    cnt_loop_4 = fll_data_4["cnt_loop"]
    str_ctrl_4 = fll_data_4["str_ctrl"]

    if (not SUBPLOTS):
        plt.step(list(range(cnt_loop_1)), freq_arr_1, where='pre', label=str_ctrl_1)
        plt.step(list(range(cnt_loop_2)), freq_arr_2, where='pre', label=str_ctrl_2)
        #plt.step(list(range(cnt_loop_3)), freq_arr_3, where='pre', label=str_ctrl_3 + ". Kp = " + str(fll_inst_3.pid_kp_i))
        #plt.step(list(range(cnt_loop_4)), freq_arr_4, where='pre', label=str_ctrl_4 + ". Kp = " + str(fll_inst_4.pid_kp_i))
        #plt.step(list(range(cnt_loop_2)), freq_arr_2, where='pre', label="Kp = " + str(fll_inst_2.pid_kp_i) + ", Ki = " + str(fll_inst_2.pid_ki_i) + ", Kd = " + str(fll_inst_2.pid_kd_i))
        #plt.step(list(range(cnt_loop_3)), freq_arr_3, where='pre', label="Kp = " + str(fll_inst_3.pid_kp_i) + ", Ki = " + str(fll_inst_3.pid_ki_i) + ", Kd = " + str(fll_inst_3.pid_kd_i))
        #plt.step(list(range(cnt_loop_4)), freq_arr_4, where='pre', label="Kp = " + str(fll_inst_4.pid_kp_i) + ", Ki = " + str(fll_inst_4.pid_ki_i) + ", Kd = " + str(fll_inst_4.pid_kd_i))
        #plt.plot(list(range(cnt_loop_1)), freq_arr_1, label=str_ctrl_1)
        #plt.plot(list(range(cnt_loop_2)), freq_arr_2, label=str_ctrl_2)
        plt.xlabel("Број итерација")
        plt.ylabel("Фреквенција осциловања [MHz]")
        plt.xticks(np.arange(0, FLL_MAX_ITER + 10, 10))
        plt.yticks(np.arange(0.0, 700.0, 50.0))
        plt.grid()
    #    plt.tight_layout()
        plt.tick_params(labelsize=10)
       # plt.legend()
    else:
        plt.subplot(211)
        plt.step(list(range(cnt_loop_1)), freq_arr_1, where='pre', label=str_ctrl_1)
        plt.xlabel("Број итерација")
        plt.ylabel("Фреквенција осциловања [MHz]")
        plt.xticks(np.arange(0, FLL_MAX_ITER + 10, 10))
        plt.yticks(np.arange(0.0, 700.0, 50.0))
        plt.grid()
   #     plt.tight_layout()
        plt.tick_params(labelsize=10)
        plt.legend()

        plt.subplot(212)
        plt.step(list(range(cnt_loop_2)), freq_arr_2, where='pre', label=str_ctrl_2)
        plt.xlabel("Број итерација")
        plt.ylabel("Фреквенција осциловања [MHz]")
        plt.xticks(np.arange(0, fll_max_iter + 10, 10))
        plt.yticks(np.arange(0.0, 700.0, 50.0))
        plt.grid()
    #    plt.tight_layout()
        plt.tick_params(labelsize=10)
        plt.legend()

    plt.tight_layout()
    #$figure = plt.gcf()  # get current figure
    #figure.set_size_inches(32, 18)   # set figure's size manually to your full screen (32x18)
    #plt.savefig("results/pid_vs_cnt.png", bbox_inches='tight', dpi=300)  # bbox_inches removes extra white spaces
    #plt.savefig("results/bang_bang_vs_pid.png", bbox_inches='tight')  # bbox_inches removes extra white spaces
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    #plt.show()
    tikzplotlib.save("results/sim_py_pid_vs_cnt.tex", dpi=300) 
    plt.close()