"""
这个文件用于处理pypdevs产生的log为wave图的形式，以观测底层devs仿真器各个原子模型的状态转移情况

"""
import matplotlib.pyplot as plt


# 预处理log文件
def read_log(file_path):
    with open(file_path, "r") as file:
        content = [eve.strip("\n").strip("\t") for eve in file]
    res = []
    # 去除无用信息
    for eve in content:
        if eve != "":
            if ("Current Time" in eve) or ("EXTERNAL TRANSITION" in eve) or ("INTERNAL TRANSITION" in eve) or ("transition at time" in eve):
                # print(eve)
                res.append(eve)
    # 将信息进行组合成[模型名称，是否是外部，当前发生时间，下一时刻的内部转移时间]，并存入processed_list
    processed_list = []
    for i in range(len(res)):

        if "TRANSITION in model" in res[i]: # 代表开始新的存储了
            temp = []
            temp.append(res[i].split(".")[-1].split(">")[0])
            if "EXTERNAL TRANSITION" in res[i]:
                temp.append(True)
            elif "INTERNAL TRANSITION" in res[i]:
                temp.append(False)
            else:
                raise EOFError
            # 开始遍历之前最近的current time
            is_find_time = False
            for j in range(i, -1, -1):
                if "Current Time" in res[j]:
                    is_find_time =True
                    current_time = float(res[j].split(":")[-1].strip().split(" ")[0])
                    temp.append(current_time)
                    break  # 只找最近的
            if is_find_time == False:
                print("当前原子模型未找到其current time的位置")
                raise EOFError
            # 下面开始计算原子模型的状态持续时间
            assert "transition at time" in res[i+1]
            if res[i+1].split("time")[-1].strip() != "inf":
                next_time = float(res[i+1].split("time")[-1].strip())
            else:
                next_time = "infinity"
            temp.append(next_time)
            assert len(temp) == 4
            processed_list.append(temp)
    return processed_list


# 绘制一个原子模型的内部或者外部事件转移的方波图
def plot_one_wave(atomic_name, processed_list, y_position, x_lim, time_base=0.0):
    # 颜色和线条
    color1 = "blue"
    linestyle1 = "-"
    color2 = "green"
    linestyle2 = "-"

    # 首先收集相关atomic_name的相关信息
    related_info = []
    for eve in processed_list:
        if atomic_name == eve[0]:
            related_info.append(eve)
    # 开始针对一个related_info内的点进行绘制
    y_inte = y_position
    y_exte = y_position - 0.5

    for eve in related_info:
        tmp_crt = eve[2]-time_base
        if eve[1] == True:  # 绘制外部事件

            plt.arrow(tmp_crt, y_exte + 0.3, 0, 0.1, color=color1, linestyle=linestyle1, head_width=0.1, lw=0.8,
                      # 箭头⻓度，箭尾线宽
                      length_includes_head=True)
        else:  # 绘制内部事件

            plt.arrow(tmp_crt, y_inte + 0.1, 0, -0.1, color=color2, linestyle=linestyle2, head_width=0.1, lw=0.8,
                      # 箭头⻓度，箭尾线宽
                      length_includes_head=True)
            if eve[3] == "infinity": # 此时绘制一条直线 infinity
                pass
            else:  # 此时绘制一条横线
                plt.plot([tmp_crt, eve[3]-time_base], [y_inte + 0.4, y_inte + 0.4], color=color2, linestyle=linestyle2)
            # plt.plot([tmp_crt, tmp_crt], [y_position, y_position + 0.4], color=color2, linestyle=linestyle2)
            # plt.plot([tmp_net, tmp_net], [y_position, y_position + 0.4], color=color2, linestyle=linestyle2)
    # 绘制直线
    plt.plot(x_lim, [y_position - 0.05, y_position - 0.05], color="black", linestyle=":")

# 绘制多个原子模型的图
def plot_wave_curves(name_list, y_min, processed_list, xlim, ytriks = None):
    y_position = y_min
    y_tracks = [y_position]
    for name in name_list:
        plot_one_wave(name, processed_list, y_position, xlim, 860.9)
        y_position += 1.3
        y_tracks.append(y_position)
    if ytriks is None:
        plt.yticks(y_tracks, [eve.split("-")[-1] for eve in name_list])
    else:
        plt.yticks(y_tracks, ytriks)



if __name__ == "__main__":
    # [['predator-controller', True, 860.9, 860.9], ['predator-schedule', True,...
    # para
    from pylab import mpl

    mpl.rcParams['font.size'] = 21
    xlim = [-0.05, 10.3]

    processed_list = read_log("..\\DrawFigures\\one)step_train_devs_log.txt")

    plt.figure(figsize=(20, 6))
    # plot_wave_curves(["predator-interaction", "predator-plan5", "predator-plan4",
    #                   "predator-plan3", "predator-plan2", "predator-plan1","predator-schedule", "predator-goal","predator-controller"],
    #                  1.5,
    #                  processed_list, xlim)
    plot_wave_curves(["env", "predator-interaction", "prey-interaction"],1.5,processed_list, xlim, ["stepbuffer", "predator\ninteraction", "prey\ninteraction"])
    # 图画的有问题，还得继续改进
    # plt.legend()
    plt.xticks([i for i in range(11)], [str(i) for i in range(11)])
    plt.xlim(xlim)
    plt.ylim([0.5, 5])
    plt.xlabel("Simulation time(s)")
    plt.text(2.2, 4.1, "Internal event transition occurs", fontsize=15)
    plt.text(2.2, 3.8, "External event transition occurs", fontsize=15)
    plt.text(0 - 0.4, 5.1, "training step i", fontsize=15)
    plt.text(5.1 - 0.4, 5.1, "training step i+1", fontsize=15)
    plt.text(10.2 - 0.4, 5.1, "training step i+2", fontsize=15)
    plt.plot([5.1, 5.1], [0, 5.1], color="r", linestyle=":")
    plt.plot([0, 0], [0, 5.1], color="r", linestyle=":")
    plt.plot([10.2, 10.2], [0, 5.1], color="r", linestyle=":")




    # plt.ylim()
    plt.savefig(r"G:\paper4\初稿\ANNSIM初稿_within12pages\manuscript\figure10.eps", format="eps")
    plt.show()

