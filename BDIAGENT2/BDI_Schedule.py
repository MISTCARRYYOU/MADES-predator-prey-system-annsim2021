from pypdevs.DEVS import *
from pypdevs.infinity import INFINITY
from BDI_struct_for_cpp2 import schedule2goal, schedule2plan


# 交互部分
class Schedule2(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "prey-schedule")
        self.outport_goal = self.addOutPort("outport_goal")  # 增加端口
        self.inport_goal = self.addInPort("inport_goal")  # 增加端口
        self.outport_plan = self.addOutPort("outport_plan")  # 增加端口
        self.inport_plan = self.addInPort("inport_plan")  # 增加端口
        self.isbegin = False  # 初始为静止
        self.choose_output = "plan"  # 两个值，plan和goal

        self.plans_return = []
        # 初始化结构体参数
        self.schedule2plan = schedule2plan()  # schedule2plan类
        self.schedule2goal = schedule2goal()  # schedule2goal类


    def timeAdvance(self):  # ta要的是返回值
        if self.isbegin:  # bool
            return 1.0
        else:
            return INFINITY

    # 输出
    def outputFnc(self):  # ta 要的是返回值
        if self.choose_output == "plan":
            return {self.outport_plan: [self.schedule2plan]}  # schedule2plan类
        elif self.choose_output == "goal":
            return {self.outport_goal: [self.schedule2goal]}  # schedule2goal类
        else:
            raise EOFError

    def intTransition(self):  # ta 要的是返回值
        self.isbegin = False
        return self.state

        # 外部事件转移函数
        # 接受来自goal的信息：self.outport:{"plans":plans, "parameters":parameters, "state": self.state}

    def extTransition(self, inputs):
        self.isbegin = True  # 无论谁给调度模块来消息，都是开始
        current_port = list(inputs.keys())[0]  # 不会有两个端口同时产生事件的时候
        # 下面分别对两种外部转移函数的模式进行处理
        # 1-goal  2-plan
        if current_port == self.inport_goal:  # goal
            self.inputs_goal = inputs[self.inport_goal][0]  # goal2schedule类
            self.choose_output = "plan"
            # 下面对于plans里面的每一个计划都进行一个调度过程
            self.choose_plan = 0
            self.plans_return = []
            self.overallparameters = self.inputs_goal.overall_parameters  # overallParameters类

        elif current_port == self.inport_plan:  # plan
            plans_list = inputs[self.inport_plan]  # 最外层是一个数组（列表），存储并行事件，里面元素均为plan2schedule类
            if len(plans_list) != 1:
                # 只有在设置了并行plan，并且凑巧的情况下，才有可能发生这件事情，只要不设置并行事件一定不会发生这件事情
                print("产生了同一个agent的并行plan!!!!!!!!!!!!!!!!!!!!!!!!!")

            # 将最后一个计划的overallparameter进行赋值操作
            self.overallparameters = plans_list[-1].overallparameters

            # 判断下一步的内容 self.inputs_goal.plans 为[["plan1"],["plan2", "plan3"],...]这样的二维数组
            if self.choose_plan == self.get_deal_plan_list_len(self.inputs_goal.plans) - len(plans_list):  # 代表上一个已经完成了最后的plan调度
                self.choose_output = "goal"
                self.schedule2goal.overall_parameters = self.overallparameters  # overallparameters
                return self.state
            else:
                self.choose_output = "plan"
            self.choose_plan += len(plans_list)  #开始执行下一个计划
        else:
            raise EOFError
        # 这个部分是公共的部分，意义是指定下一次输出的plan的类型和内容

        # 下面这句话在出现并行plan时是不正确的
        self.schedule2plan.planID = self.inputs_goal.plans[self.choose_plan]  # string
        self.schedule2plan.overall_parameters = self.overallparameters  # overallparameter
        return self.state

        # input as [["plan1"],["plan2", "plan3"],...]
        # return one int variable
        # count the plans in deal_plan_list

    def get_deal_plan_list_len(self, deal_plan_list):
        res = 0
        for eve in deal_plan_list:
            for ev in eve:
                res += 1
        return res
