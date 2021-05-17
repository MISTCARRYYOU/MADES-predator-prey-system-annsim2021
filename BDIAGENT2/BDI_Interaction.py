from pypdevs.DEVS import *
from pypdevs.infinity import INFINITY
from Message import Message
from BDI_struct_for_cpp2 import interaction2plan


# 交互部分
# 注意，agent代表的是整个智能体的，其端口应该与环境进行连接
class Interaction2(AtomicDEVS):
    def __init__(self, agentID):
        AtomicDEVS.__init__(self, "prey-interaction")

        self.outport_plan = self.addOutPort("outport_plan")  # 增加端口
        self.inport_plan = self.addInPort("inport_plan")  # 增加端口
        self.outport_agent = self.addOutPort("outport_agent")  # 增加端口
        self.inport_agent = self.addInPort("inport_agent")  # 增加端口

        # 变量
        self.state = None
        self.isbegin = False
        self.choose_output = "agent"  # agent和plan两个接口

        self.agentID = agentID
        self.message = None
        self.isreceive_trigger = False

        self.mail_box = []  # 邮箱 里面装有message对象
        self.message_null_in_mail = Message("interaction", ["plan"], "null in mail", "inform")
        self.sender_list = None

        # 结构体参数初始化
        self.interaction2plan = interaction2plan()

    def timeAdvance(self):  # ta 要的是返回值
        if self.isbegin:
            return 0
        else:
            return INFINITY

    # 输出
    def outputFnc(self):  # ta 要的是返回值
        if self.choose_output == "agent":
            # print(self.message.content)
            # print(self.message.content,666)
            self.interaction2plan.perception = "for send"
            return {self.outport_agent: [self.message], self.outport_plan: [self.interaction2plan]}  # self.state 为当前选择的位置
        elif self.choose_output == "plan":
            return {self.outport_plan: [self.interaction2plan]}

    def intTransition(self):  # ta 要的是返回值
        self.isbegin = False
        return self.state

    # 外部事件转移函数
    # 默认为inform协议什么也不需要做
    def extTransition(self, inputs):
        current_port = list(inputs.keys())[0]
        # 处理两个端口
        if current_port == self.inport_plan:  # 来自plan的输入
            self.inputs_plan = inputs[self.inport_plan][0]
            self.message = self.inputs_plan.message
            self.interaction2plan.planID = self.inputs_plan.planID
            # 使用消息的协议来控制这种固定字段的选择问题
            if self.message.protocol == "receive-1":  # 此时不发送，只等待接收
                self.sender_list = self.message.content
                self.isbegin = False
                self.choose_output = "plan"
                self.isreturn = False
                self.isreceive_trigger = True
                # print(self.current_plan, self.message,self.isreceive_trigger)
            elif self.message.protocol == "receive-2":  # 此时只是判断一圈是否有消息
                self.sender_list = self.message.content
                self.isbegin = True
                self.choose_output = "plan"
                self.isreturn = False
                if self.mail_box != []:
                    # 在此检查receive-2消息中指定的发送对象
                    self.interaction2plan.perception = self.mail_box.pop(0)  # 理论上所有消息都是消息格式
                    self.interaction2plan.perception = self.check_sender_forreceive2(self.sender_list,
                                                                                     self.interaction2plan.perception)
                    if self.interaction2plan.perception == []:  # 代表没有针对它的信息
                        self.interaction2plan.perception = ["for receive-2"]
                else:
                    self.interaction2plan.perception = ["for receive-2"]
            elif self.message.protocol == "send":
                self.isbegin = True
                self.choose_output = "agent"
            else:
                raise EOFError
            return self.state

        elif current_port == self.inport_agent:  # 收到agent的输入
            self.inputs_agent_ = inputs[self.inport_agent]  # [{},{},{},...]
            self.isbegin = True
            self.choose_output = "plan"
            # print(666, self.isreceive_trigger, self.inputs_agent_[0].from_)
            # 将发送给它的消息放在列表中
            self.inputs_agent = []
            # 判断消息是不是发给这个智能体的
            for msg in self.inputs_agent_:
                # print(555, msg.to, msg.content)
                if self.agentID in msg.to:
                    self.inputs_agent.append(msg)  # 接收方在这里把消息提取出来

            # 为receive-1准备的判断
            if self.inputs_agent == [] or self.isreceive_trigger == False:  # 证明发送不是针对它的
                self.isbegin = False  # 继续锁住
                # 先加入到邮箱中-只要是发送给这个智能体的内容就会增加到邮箱中
                if self.inputs_agent != []:
                    self.mail_box.append(self.inputs_agent)
            else:
                # 在此检查receive-1消息中指定的发送对象
                # print(6666, self.inputs_agent)
                # 从发送给它的消息中留下它想要接受的消息，可能一个也留不下
                self.isreceive_trigger = False
                self.inputs_agent = self.check_sender(self.sender_list, self.inputs_agent)
                if self.inputs_agent == []:  # 代表没有想要接受的消息
                    self.isbegin = False  # 继续锁住
                else:
                    self.isbegin = True
                    # 给结构体赋值
                    self.interaction2plan.perception = []
                    for eve in self.inputs_agent:  # self.inputs_agent为message array
                        self.interaction2plan.perception.append(eve.content)
            return self.state
        else:
            raise EOFError

    # 检查发送方是否为要求的发送方
    def check_sender(self, sender_list, checked_list):
        assert isinstance(sender_list, list)
        assert isinstance(checked_list, list)
        if sender_list == ["any"]:
            return checked_list
        res = []
        for eve_sender in sender_list:
            for eve_message in checked_list:
                if eve_sender == eve_message.from_:
                    res.append(eve_message)
        return res

    # 检查发送方是否为要求的发送方
    def check_sender_forreceive2(self, sender_list, checked_list):
        assert isinstance(sender_list, list)
        assert isinstance(checked_list, list)
        if sender_list == ["any"]:
            return checked_list
        res = []
        for eve_sender in sender_list:
            for eve_message in checked_list:
                if eve_sender == eve_message.from_:
                    res.append(eve_message.content)
        return res