from pypdevs.DEVS import *
from pypdevs.infinity import INFINITY
from Message import Message

class Controller2(AtomicDEVS):
    def __init__(self, mas_list):
        AtomicDEVS.__init__(self, "prey-controller")
        self.outport = self.addOutPort("outport")  # 增加端口
        self.inport = self.addInPort("inport")  # 增加端口
        self.name = "prey-controller"
        self.needed_agent_names = []
        self.isbegin = False
        # 来自外部的参数
        self.agent_names = mas_list  # ["prey"]
        self.agent_nums = len(self.agent_names)

        self.count = 0

    def timeAdvance(self):  # ta要的是返回值
        if self.isbegin == False:  # mas_names不为空要继续output
            return INFINITY
        else:
            return 0

    # 输出
    def outputFnc(self):
        temp_msg = Message(self.name, self.agent_names, "signal from center", None)
        self.count = 0
        return {self.outport:[temp_msg]}

    def intTransition(self):
        self.isbegin = False
        return self.state

    # 外部事件转移函数
    # 消息可能同步到达，也可能一个个地异步到达
    # 这部分由agent单独的端口控制，因此不需要判断是不是给controller的
    # 收齐完所有的signal之后再统一输出
    def extTransition(self, inputs):
        content = inputs[self.inport]  # 是一个list
        for eve in content:
            self.count += 1
        if self.count == self.agent_nums:
            self.isbegin = True
        else:
            self.isbegin = False
        return self.state

