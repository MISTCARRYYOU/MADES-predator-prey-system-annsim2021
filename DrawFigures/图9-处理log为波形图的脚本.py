import matplotlib.pyplot as plt
import numpy as np
from pylab import mpl
mpl.rcParams['font.size'] = 18


# 1 in plot list, the lefts are 0
# dot_list is [1,2,3,4,6,7], even number
def plot_square_wave(dots_list, y_track, name, color, aix_begin, aix_end, linestyle):
    if dots_list == []:
        plt.plot([aix_begin,aix_end], [y_track, y_track], color= color, linestyle=linestyle)
        return

    assert len(dots_list) % 2 == 0
    starts = []
    ends = []
    temp_dots_list = []
    for i, dot in enumerate(dots_list):
        if i % 2 == 0:
            starts.append(dot)
            temp_dots_list.append(dot)
        else:
            ends.append(dot+0.1)
            temp_dots_list.append(dot+0.1)
    # draw the |--| mountain
    for i in range(len(starts)):
        plt.plot([starts[i], ends[i]], [y_track+1, y_track+1], color=color, linestyle=linestyle)
        plt.plot([starts[i], starts[i]], [y_track, y_track+1], color=color, linestyle=linestyle)
        plt.plot([ends[i], ends[i]], [y_track, y_track+1], color=color, linestyle=linestyle)

    # draw the - - - -
    all_dots = [aix_begin]
    all_dots += sorted(list(set(temp_dots_list)))
    all_dots.append(aix_end)
    starts = []
    ends = []
    for i, dot in enumerate(all_dots):
        if i % 2 == 0:
            starts.append(dot)
        else:
            ends.append(dot)
    for i in range(len(starts)):
        plt.plot([starts[i], ends[i]], [y_track, y_track], color=color, linestyle=linestyle)

# 将log str 中的某个原子模型的内部或者外部事件的起始点提取出来，返回其起始点与终止点
def extract_dots(is_external, extract_name, time_sequence_str, timeadvance, is_divide3):
    if is_external:
        extract_str = "EXTERNAL"
    else:
        extract_str = "INTERNAL"
    time_record = []
    y_dots = []
    for i, eve in enumerate(time_sequence_str):
        if type(eve) == float:
            time_record.append(i)
    part_4_time = [[] for eve in time_record]

    for index, i in enumerate(time_record):
        if index != len(time_record)-1:
            part_4_time[index] += (time_sequence_str[i+1:time_record[index+1]])
        else:
            part_4_time[index] += (time_sequence_str[i + 1:])

    assert len(part_4_time) == len(time_record)
    time = []
    for eve in time_record:
        time.append(time_sequence_str[eve])

    for i in range(len(time)):
        for eve in part_4_time[i]:
            if extract_str in eve and extract_name in eve:
                y_dots.append(time[i])

    start_end_dots = []
    for i,eve in enumerate(y_dots):
        if is_divide3:  # 代表需要除三，因为三个agent
            if i % 3 == 0:
                start_end_dots.append(eve)
                start_end_dots.append(eve + 0.2 + timeadvance)
        else:
            start_end_dots.append(eve)
            start_end_dots.append(eve + 0.2 + timeadvance)

    return start_end_dots


if __name__ == "__main__":
    # 直接统计每个时刻发生的事件列表先
    plt.figure(figsize=(20, 3))
    with open(r"../DrawFigures/one)step_train_devs_log.txt", "r") as file:
        content = [eve.strip("\n").strip("\t") for eve in file]
    res = []
    for eve in content:
        if eve != "":
            if "Current Time" in eve or "EXTERNAL TRANSITION" in eve or "INTERNAL TRANSITION" in eve:
                res.append(eve)
    pure_time = []

    for eve in res:
        if "Current Time" in eve:
            temp = eve.split(":")[-1].strip().split(" ")[0]
            pure_time.append(float(temp))
        else:
            pure_time.append(eve)
    # 此时 pure_time 为[860.9, 'EXTERNAL TRANSITION in model <Simulation.predator-controller>', 'EXTERNAL TRANSITION in model <Simulation.predator-schedule>'。。。
    buffer_ex_dots = [round(eve-860.9, 2) for eve in extract_dots(True, "env", pure_time, 0.1, False)]
    buffer_in_dots = [round(eve-860.9, 2) for eve in extract_dots(False, "env", pure_time, 0.1, False)]


    plt.figure(1)
    plt.xlim([0,5.1])
    plot_square_wave(buffer_ex_dots, 1, "env-EXTERNAL", "red", 0, 10, ":")
    plot_square_wave(buffer_in_dots, 3.5, "env-INTERNAL", "green", 0, 10, "-")

    plt.xlabel("Simulation time(s)")

    plt.yticks([1, 3.5], ["Stepbuffer-Ext", "Stepbuffer-Int"])
    # plt.legend()
    plt.savefig(r"D:\科研项目\paper4\初稿\ANNSIM初稿\manuscript\figure10.eps", format="eps")

    plt.show()
    # times = []
    # for eve_str in res:

