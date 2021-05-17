from pypdevs.DEVS import *
from pypdevs.infinity import INFINITY

from BDI_struct_for_cpp import *
from Message import Message
from ENVIRONMENT.EnvInfo import Buffer

class StepScheduler(AtomicDEVS):
    def __init__(self, env, args):
        AtomicDEVS.__init__(self, "env")
        self.outport = self.addOutPort("outport")  # 增加端口
        self.inport = self.addInPort("inport")  # 增加端口
        self.name = "env"
        self.agent_queue = []
        self.isbegin = False
        self.env_store = {}  # 以字典的方式存储每一个agent传给环境的值

        # 来自外部的参数
        self.env = env
        self.args = args
        self.buffer = Buffer(args)
        self.agents_actions = ["ini" for eve in range(self.env.n)]
        self.agents_policies = ["ini" for eve in range(self.env.n-1)]
        self.agents_is_reset = []
        self.agents_is_render = []
        self.agents_is_evaluate = []
        self.count_agents = 0
        self.s = None

        self.prey_action = None

        self.agents_is_first = []

    def timeAdvance(self):  # ta要的是返回值
        if self.isbegin == False:  # mas_names不为空要继续output
            return INFINITY
        else:
            return 0.1

    # 输出
    # 因为环境是通过interaction端口来进行传递的，所以需要以message的方式进行传递，每次pop一个agent的输出，ta==0
    def outputFnc(self):
        is_all_agree2first = self.judge_resetrender(self.agents_is_first)
        if is_all_agree2first:  # 如果是第一次发送就返回初始化环境状态
            self.s = self.env.reset()
            temp_msg_content = Env_msg_content(False, self.s, r=0)
            message2agent = Message("env", ["predator1", "predator2", "predator3", "prey"], temp_msg_content, None)
            return {self.outport: [message2agent]}

        is_all_agree2reset = self.judge_resetrender(self.agents_is_reset)
        is_all_agree2render = self.judge_resetrender(self.agents_is_render)
        is_all_agree2evaluate = self.judge_resetrender(self.agents_is_evaluate)

        # 清空is列表
        self.clear_is_list()

        if is_all_agree2render:
            self.env.render()
        if is_all_agree2reset:
            self.s = self.env.reset()
        assert self.prey_action is not None
        self.agents_actions[-1] = self.prey_action
        s_next, r, done, info = self.env.step(self.agents_actions)
        assert self.s is not None

        if is_all_agree2evaluate:  # 测试部分
            temp_msg_content = Env_msg_content(False, self.s, r=r)
        else:
            self.buffer.store_episode(self.s[:self.args.n_agents], self.agents_actions[:self.args.n_agents], r[:self.args.n_agents], s_next[:self.args.n_agents])
            if self.buffer.current_size > self.args.batch_size:
                transitions = self.buffer.sample(self.args.batch_size)
                temp_msg_content = Env_msg_content(True, self.s, transitions, self.agents_policies)
            else:
                temp_msg_content = Env_msg_content(False, self.s)
        message2agent = Message("env", ["predator1", "predator2", "predator3", "prey"], temp_msg_content, None)
        self.isbegin = False
        self.s = s_next

        return {self.outport: [message2agent]}

    def intTransition(self):
        self.isbegin = False
        return self.state

    # 外部事件转移函数
    # 消息可能同步到达，也可能一个个地异步到达
    def extTransition(self, inputs):
        content = inputs[self.inport]  # 是一个list
        for each_mes in content:
            if self.name in each_mes.to:
                self.count_agents += 1
                if each_mes.from_ in ["predator1", "predator2", "predator3"]:
                    if each_mes.content == "initialize":
                        self.agents_is_first.append(True)
                    else:
                        self.agents_is_first.append(False)
                        self.agent_queue.append(each_mes.from_)
                        self.env_store[each_mes.from_] = each_mes.content  # 这句话在目前的案例中没什么作用
                        self.agents_actions[each_mes.content.agent_id_num] = each_mes.content.action  # 注意prey放在最后num= 3(从0开始计数)
                        self.agents_policies[each_mes.content.agent_id_num] = each_mes.content.policy  # 把各自的策略也传了出来
                        self.agents_is_reset.append(each_mes.content.is_reset)
                        self.agents_is_render.append(each_mes.content.is_render)
                        self.agents_is_evaluate.append(each_mes.content.is_evaluate)

                elif each_mes.from_ == "prey":
                    if each_mes.content == "initialize":
                        self.agents_is_first.append(True)
                    else:
                        self.agents_is_first.append(False)
                        self.prey_action = each_mes.content  # 来自prey的message只有一个代表其随机动作的content
                else:
                    raise EOFError

        if self.count_agents == self.env.n:
            self.isbegin = True
            self.count_agents = 0
        else:
            self.isbegin = False

        return self.state

    # 有一个不同意环境就不会改变
    def judge_resetrender(self, alist):
        res = True
        for eve in alist:
            if eve == False:
                res = False
        return res

    def clear_is_list(self):
        self.agents_is_first = []
        self.agents_is_reset = []
        self.agents_is_render = []
        self.agents_is_evaluate = []



