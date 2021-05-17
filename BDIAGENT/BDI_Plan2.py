from pypdevs.DEVS import *
from pypdevs.infinity import INFINITY
import numpy as np
import torch
from BDI_struct_for_cpp import plan2interaction, plan2schedule


# select actions
class Plan2(AtomicDEVS):
    def __init__(self, agentID):
        AtomicDEVS.__init__(self, "predator-plan2")
        self.outport_schedule = self.addOutPort("outport_schedule")  # 增加端口
        self.inport_schedule = self.addInPort("inport_schedule")  # 增加端口

        self.outport_interaction = self.addOutPort("outport_interaction")  # 增加端口
        self.inport_interaction = self.addInPort("inport_interaction")  # 增加端口

        self.isbegin = False
        self.choose_output = "interaction"  # interaction或者schedule
        self.name = "predator-plan2"
        self.agentID = agentID  # string类

        # 通讯协议
        self.msg = None  # messsage类
        self.message = None  # messsage类

        self.default_sender = ["any"]  # string array

        # # 初始化结构体参数
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
        if self.overallparameters.is_evaluate == False:
            actions = self.select_action(False, self.overallparameters.s[self.overallparameters.agent_id_num],
                                         self.overallparameters.args, self.overallparameters.agent_id_num, self.overallparameters.agent_policy)
        else:
            actions = self.select_action(True, self.overallparameters.s[self.overallparameters.agent_id_num],
                                         self.overallparameters.args, self.overallparameters.agent_id_num, self.overallparameters.agent_policy)
        self.overallparameters.chosen_actions = actions
        # 执行到最后，一定会反馈给调度模块相应的内容
        self.choose_output = "schedule"
        self.plan2schedule.planID = self.name  # string
        self.plan2schedule.overallparameters = self.overallparameters
        return self.state

    def select_action(self, is_evaluate, o, args, agent_id, policy):
        with torch.no_grad():
            if is_evaluate == True:
                noise_rate = 0
                epsilon = 0
            else:
                noise_rate = args.noise_rate
                epsilon = args.epsilon
            if np.random.uniform() < epsilon:
                u = np.random.uniform(-args.high_action, args.high_action, args.action_shape[agent_id])
            else:
                inputs = torch.tensor(o, dtype=torch.float32).unsqueeze(0)
                pi = policy.actor_network(inputs).squeeze(0)
                # print('{} : {}'.format(self.name, pi))
                u = pi.cpu().numpy()
                noise = noise_rate * args.high_action * np.random.randn(*u.shape)  # gaussian noise
                u += noise
                u = np.clip(u, -args.high_action, args.high_action)
            return u.copy()
