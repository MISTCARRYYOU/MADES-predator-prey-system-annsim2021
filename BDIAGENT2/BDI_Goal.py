from pypdevs.DEVS import *
from pypdevs.infinity import INFINITY
from BDI_struct_for_cpp2 import goal2schedule, overallParameters2
from Message import Message


# Goal部分
class Goal2(AtomicDEVS):
    def __init__(self, args):
        AtomicDEVS.__init__(self, "prey-goal")

        # goal的端口只与intention进行交互
        self.outport_schedule = self.addOutPort("outport")  # 增加端口
        self.inport_schedule = self.addInPort("inport")  # 增加端口

        self.outport_center = self.addOutPort("outport")  # 增加端口
        self.inport_center = self.addInPort("inport")  # 增加端口

        self.isbegin = True
        self.goal4center_signal = None


        # 初始化结构体参数
        self.goal2schedule = goal2schedule()  # goal2schedule类
        self.overallparameters = overallParameters2(args)  # overallParameters类

        self.is_first = True

    def timeAdvance(self):  # ta 要的是返回值
        if self.isbegin:
            return 1.0
        else:
            return INFINITY

    # 输出
    def outputFnc(self):  # ta 要的是返回值

        self.goal2schedule.plans = self._decide_plan()  # 二维数组，最里面存放字符串格式
        self.isbegin = False
        if self.goal2schedule.plans == "over":
            print("仿真已经结束了！！")
            return {}  # 将程序锁死
        self.goal2schedule.overall_parameters = self.overallparameters  # overallParameters类
        return {self.outport_schedule: [self.goal2schedule], self.outport_center: [self.goal4center_signal]}

        # 外部事件转移函数
    def extTransition(self, inputs):
        # 获取intention的输出，从一时刻起，而不是零时刻
        port_list = list(inputs.keys())
        for every_port in port_list:
            if every_port == self.inport_schedule:  # 收到来自调度端口的输入
                self.inputs = inputs[self.inport_schedule][0]  # 因为schedule不可能产生并行事件
                self.overallparameters = self.inputs.overall_parameters  # overallParameters类
                self.isbegin = True
            elif every_port == self.inport_center:  # 收到来自中心端口的输入
                self.goal4center_signal = "signal"
            else:
                raise EOFError
        return self.state

    # 返回一个列表
    def _decide_plan(self):
        # 判断智能体是否已经完成了自己的目标

        # 训练部分
        # if self.overallparameters.is_collect_over == False:
        #     self.deal_plan_list = [["plan2"], ["plan3"]]
        # else:
        #     self.deal_plan_list = [["plan2"], ["plan3"], ["plan1"]]

        # 测试部分
        if self.is_first:
            self.deal_plan_list = [["prey-plan2"]]
            self.is_first = False
        else:
            self.deal_plan_list = [["prey-plan1"]]
        return self.deal_plan_list


