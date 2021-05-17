from pypdevs.DEVS import *
from pypdevs.infinity import INFINITY
from Message import Message
from BDI_struct_for_cpp2 import plan2interaction, plan2schedule
import numpy as np


# initilize
class Plan2_2(AtomicDEVS):
    def __init__(self, agentID):
        AtomicDEVS.__init__(self, "prey-plan2")
        self.outport_schedule = self.addOutPort("outport_schedule")  # 增加端口
        self.inport_schedule = self.addInPort("inport_schedule")  # 增加端口

        self.outport_interaction = self.addOutPort("outport_interaction")  # 增加端口
        self.inport_interaction = self.addInPort("inport_interaction")  # 增加端口

        self.isbegin = False
        self.choose_output = "interaction"  # interaction或者schedule
        self.name = "prey-plan2"
        self.agentID = agentID  # string类

        # 初始化结构体参数
        self.plan2interaction = plan2interaction()  #plan2interaction类
        self.plan2schedule = plan2schedule()  # plan2schedule类


    def timeAdvance(self):  # ta 要的是返回值
        if self.isbegin:
            return 0
        else:
            return INFINITY

    # 输出
    def outputFnc(self):  # ta 要的是返回值
        if self.choose_output == "interaction":
            return {self.outport_interaction: [self.plan2interaction]}  # plan2interaction类
        elif self.choose_output == "schedule":
            return {self.outport_schedule: [self.plan2schedule]}  # plan2schedule类

    def intTransition(self):  # ta 要的是返回值
        self.isbegin = False
        return self.state

    # 外部事件转移函数
    def extTransition(self, inputs):
        current_port = list(inputs.keys())[0]  # 不会有两个端口同时产生事件的时候

        if current_port == self.inport_schedule:  # 收到调度模块的输入
            self.inputs_schedule = inputs[self.inport_schedule][0]  # schedule2plan类
            assert isinstance(self.inputs_schedule.planID, list) is True

            if self.name in self.inputs_schedule.planID:  # 证明这次发送针对它
                self.isbegin = True
                self.overallparameters = self.inputs_schedule.overall_parameters  # overallparameters类

                # ---------------------------------------------------------------------------------------alter
                self.is_need_send = True
                self.is_need_receive = True
                # ---------------------------------------------------------------------------------------over


            else:
                self.isbegin = False
                return self.state

        elif current_port == self.inport_interaction:  # 收到interaction的输入
            # 接受来自交互模块的内容
            self.inputs_interaction = inputs[self.inport_interaction][0]  # interaction2plan类
            # print(self.name ,self.inputs_interaction.planID)
            if self.name == self.inputs_interaction.planID:  # 证明这次发送针对它
                self.isbegin = True
            else:
                self.isbegin = False
                return self.state
            # 只是直接对调度模块进行反馈的步骤

            if self.inputs_interaction.perception not in ["for send"]:
                # 切片取0是为了给处理并行事件留出接口，在此不需要，所以将列表中元素取出来
                self.perception = self.inputs_interaction.perception[0]  # 结构体env2car
        else:
            raise EOFError

        # 定义部分-------------------------------------------------------

        if self.is_need_send:
            self.is_need_send = False
            # 控制time_step
            msg = Message(self.agentID, ["env"], "initialize", "send")
            self.choose_output = "interaction"
            self.plan2interaction.planID = self.name  # string
            self.plan2interaction.message = msg  # message 类
            return self.state

        # receive-1方法
        if self.is_need_receive:
            self.is_need_receive = False
            msg = Message(self.agentID, [None], ["env"], "receive-1")  # 这个地方是用来作区分的地方
            self.choose_output = "interaction"
            self.plan2interaction.planID = self.name  # string
            self.plan2interaction.message = msg
            # 消息内容存储到了self.perception里
            return self.state

        # 执行到最后，一定会反馈给调度模块相应的内容
        self.choose_output = "schedule"
        self.plan2schedule.planID = self.name  # string
        self.plan2schedule.overallparameters = self.overallparameters
        return self.state


