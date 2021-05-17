import matplotlib.pyplot as plt
import numpy as np
import matplotlib
# matplotlib.use('Agg')
import seaborn as sns # 导入模块
from pylab import mpl
sns.set() # 设置美化参数，一般默认就好
mpl.rcParams['savefig.format'] = 'pdf'

with open(r"..\rewards\rewardshistory\0.txt", "r", encoding="utf-8") as f:
    data0 = [float(eve.strip("\n")) for eve in f]

# with open(r"..\rewards\1.txt", "r", encoding="utf-8") as f:
#     data1 = [float(eve.strip("\n")) for eve in f]
#
# with open(r"..\rewards\2.txt", "r", encoding="utf-8") as f:
#     data2 = [float(eve.strip("\n")) for eve in f]


def fenjie_data2five(all_data):
    result = [[],[],[],[],[]]
    for i, reward in enumerate(all_data):
        if i % 5 == 0:
            result[0].append(reward)
        elif i % 5 == 1:
            result[1].append(reward)
        elif i % 5 == 2:
            result[2].append(reward)
        elif i % 5 == 3:
            result[3].append(reward)
        else:
            result[4].append(reward)
    assert len(result[0]) == len(result[1]) == len(result[2]) == len(result[3]) == len(result[4])
    for j in range(len(result)):
        result[j] = np.array(result[j])
    xs = [np.array([j for j in range(len(result[0]))]) for i in range(5)]
    return np.concatenate((xs[0], xs[1], xs[2], xs[3], xs[4])), np.concatenate((result[0], result[1], result[2], result[3], result[4])), xs[0]



figurex0, figurey0, purex = fenjie_data2five(data0)
# figurex1, figurey1 = fenjie_data2five(data1)
# figurex2, figurey2 = fenjie_data2five(data2)

# plt.subplot(131)
sns.lineplot(x=figurex0,y=figurey0, color="g", label="agent predator")
# plt.subplot(132)
# sns.lineplot(x=figurex1,y=figurey1, color="b")
# plt.subplot(133)
# sns.lineplot(x=figurex2,y=figurey2, color="r")
plt.legend()
plt.xlim([0,850])
plt.ylim([0, 6])
temp_x = []
for i,eve in enumerate(purex):
    if i % 100 == 0:
        temp_x.append(i)
plt.xticks(temp_x, [str(eve*5) for eve in temp_x])

plt.xlabel("Time step")
plt.ylabel("Reward")
plt.savefig(r"D:\科研项目\paper4\初稿\ANNSIM初稿\manuscript\figure7.eps", format="eps")
plt.savefig(r"..\DrawFigures\train1.png", dpi=800)

plt.show()

# def remv(list_):
#     res = []
#     for eve in list_:
#         if eve != "qq":
#             res.append(eve)
#     return res
#
# rewards1 = remv([rewards[i] if i%5 == 0 else "qq" for i in range(len(rewards))])
# t = [rewards[i] if (i%5) == 1 else "qq" for i in range(len(rewards))]
# rewards2 = remv(t)
# rewards3 = remv([rewards[i] if (i%5) == 2 else "qq" for i in range(len(rewards))])
# rewards4 = remv([rewards[i] if (i%5) == 3 else "qq" for i in range(len(rewards))])
# rewards5 = remv([rewards[i] if (i%5) == 4 else "qq" for i in range(len(rewards))] + [99.0])
#
#
# print(len(rewards2), len(rewards3), len(rewards5))
#
# rewards1 = np.array(rewards1)
# rewards2 = np.array(rewards2)
# rewards3 = np.array(rewards3)
# rewards4 = np.array(rewards4)
# rewards5 = np.array(rewards5)
#
#
# rewards=np.concatenate((rewards1,rewards2, rewards3, rewards4, rewards5)) # 合并数组
# episode1=range(len(rewards1))
# episode1 = [eve*50 for eve in episode1]
# episode=np.concatenate((episode1,episode1, episode1,episode1,episode1))
# print(len(episode), len(rewards))
# sns.lineplot(x=episode, =rewards, color="g")
# plt.xlim([0,5001])
# plt.ylim([0, 100])
# plt.xlabel("Episode")
# plt.ylabel("Reward")
# plt.savefig("REINFORCE_reward2.pdf")
# plt.show()



