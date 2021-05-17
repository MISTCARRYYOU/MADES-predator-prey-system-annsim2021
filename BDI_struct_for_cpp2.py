# 用于定义取代现在不同原子模型间字典格式的类（结构体），以方便与C++仿真器的融合过程。
# 这个部分在解释的时候可以根据上层文本中的变量类型进行初始化

# 两个被调用的结构体
# overall struct
# 由goal模块初始化并传递下去
class overallParameters2:
    # 一个计划对应一个专门的结构体，用于返回plan的结果，解决并行计划的问题
    def __init__(self,args):
        self.args = args

        # 与环境交互获得的变量
        self.s = None
        self.r = None


# 6个中间传参数的结构体
# goal2schedule
class goal2schedule:
    plans = [["plan1"], ["plan2", "plan3"]]  # 二维数组
    overall_parameters = None  # OverallParameters类型

# schedule2plan
class schedule2plan:
    planID = ["plan1"]  # 字符串
    overall_parameters = None  # OverallParameters类型

# plan2interaction
class plan2interaction:
    planID = "plan1"  # 字符串
    message = None  # Message类型

# interaction2plan
class interaction2plan:
    planID = "plan1"  # 字符串
    perception = None  # 未规定类型

# plan2schedule
class plan2schedule:
    planID = "plan1"  # 字符串
    plan_return = False  # bool值类型
    plan_struct = None  # plan1类型

# schedule2goal
class schedule2goal:
    plans_return = []  # bool list
    _overall_parameters = None  # OverallParameters类型


class Env_msg_content:
    def __init__(self, is_collect_over, s, transitions=None, policies=None, r=None):
        self.is_collect_over = is_collect_over
        self.s = s
        self.transitions = transitions
        self.policies = policies
        self.r = r


class Agent4env_content:
    def __init__(self, is_evaluate, action, is_reset, is_render, agent_id_num, policy):
        self.is_evaluate = is_evaluate
        self.action = action
        self.is_reset = is_reset
        self.is_render = is_render
        self.agent_id_num = agent_id_num
        self.policy = policy


