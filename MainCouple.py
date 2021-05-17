from pypdevs.DEVS import *
from pypdevs.simulator import Simulator

from BDIAGENT.BDI_Plan1 import Plan1
from BDIAGENT.BDI_Plan2 import Plan2
from BDIAGENT.BDI_Plan3 import Plan3
from BDIAGENT.BDI_Plan4 import Plan4
from BDIAGENT.BDI_Plan5 import Plan5
from BDIAGENT.BDI_Goal import Goal
from BDIAGENT.BDI_Interaction import Interaction
from BDIAGENT.BDI_Schedule import Schedule
from CENTER.Controller1 import Controller1

from BDIAGENT2.BDI_Goal import Goal2
from BDIAGENT2.BDI_Interaction import Interaction2
from BDIAGENT2.BDI_Plan1 import Plan1_2
from BDIAGENT2.BDI_Plan2 import Plan2_2
from BDIAGENT2.BDI_Schedule import Schedule2
from CENTER.Controller2 import Controller2

from ENVIRONMENT.StepScheduler import StepScheduler

from Common.com import *


# 大的仿真耦合模型
class Simulation(CoupledDEVS):
    def __init__(self):
        CoupledDEVS.__init__(self, "Simulation")
        # 参数定义区
        args = get_args()
        env, args = make_env(args)

        # 定义区
        # predator的内部端口连接---------------------------------------------------
        # agent 1
        predator1_goal = Goal(args, 0)
        self.predator1_goal = self.addSubModel(predator1_goal)
        self.predator1_schedule = self.addSubModel(Schedule())
        self.predator1_plan1 = self.addSubModel(Plan1("predator1"))
        self.predator1_plan2 = self.addSubModel(Plan2("predator1"))
        self.predator1_plan3 = self.addSubModel(Plan3("predator1"))
        self.predator1_plan4 = self.addSubModel(Plan4("predator1"))
        self.predator1_plan5 = self.addSubModel(Plan5("predator1"))


        self.predator1_interaction = self.addSubModel(Interaction("predator1"))

        # 连接goal与schedule
        self.connectPorts(self.predator1_goal.outport_schedule, self.predator1_schedule.inport_goal)
        self.connectPorts(self.predator1_schedule.outport_goal, self.predator1_goal.inport_schedule)

        # 连接schedule与plan
        self.connectPorts(self.predator1_schedule.outport_plan, self.predator1_plan1.inport_schedule)
        self.connectPorts(self.predator1_plan1.outport_schedule, self.predator1_schedule.inport_plan)

        self.connectPorts(self.predator1_schedule.outport_plan, self.predator1_plan2.inport_schedule)
        self.connectPorts(self.predator1_plan2.outport_schedule, self.predator1_schedule.inport_plan)

        self.connectPorts(self.predator1_schedule.outport_plan, self.predator1_plan3.inport_schedule)
        self.connectPorts(self.predator1_plan3.outport_schedule, self.predator1_schedule.inport_plan)

        self.connectPorts(self.predator1_schedule.outport_plan, self.predator1_plan4.inport_schedule)
        self.connectPorts(self.predator1_plan4.outport_schedule, self.predator1_schedule.inport_plan)

        self.connectPorts(self.predator1_schedule.outport_plan, self.predator1_plan5.inport_schedule)
        self.connectPorts(self.predator1_plan5.outport_schedule, self.predator1_schedule.inport_plan)

        # 连接plan与interaction
        self.connectPorts(self.predator1_plan1.outport_interaction, self.predator1_interaction.inport_plan)
        self.connectPorts(self.predator1_interaction.outport_plan, self.predator1_plan1.inport_interaction)

        self.connectPorts(self.predator1_plan2.outport_interaction, self.predator1_interaction.inport_plan)
        self.connectPorts(self.predator1_interaction.outport_plan, self.predator1_plan2.inport_interaction)

        self.connectPorts(self.predator1_plan3.outport_interaction, self.predator1_interaction.inport_plan)
        self.connectPorts(self.predator1_interaction.outport_plan, self.predator1_plan3.inport_interaction)

        self.connectPorts(self.predator1_plan4.outport_interaction, self.predator1_interaction.inport_plan)
        self.connectPorts(self.predator1_interaction.outport_plan, self.predator1_plan4.inport_interaction)

        self.connectPorts(self.predator1_plan5.outport_interaction, self.predator1_interaction.inport_plan)
        self.connectPorts(self.predator1_interaction.outport_plan, self.predator1_plan5.inport_interaction)



        # agent3
        predator3_goal = Goal(args, 2)
        self.predator3_goal = self.addSubModel(predator3_goal)
        self.predator3_schedule = self.addSubModel(Schedule())
        self.predator3_plan1 = self.addSubModel(Plan1("predator3"))
        self.predator3_plan2 = self.addSubModel(Plan2("predator3"))
        self.predator3_plan3 = self.addSubModel(Plan3("predator3"))
        self.predator3_plan4 = self.addSubModel(Plan4("predator3"))
        self.predator3_plan5 = self.addSubModel(Plan5("predator3"))


        self.predator3_interaction = self.addSubModel(Interaction("predator3"))

        # 连接goal与schedule
        self.connectPorts(self.predator3_goal.outport_schedule, self.predator3_schedule.inport_goal)
        self.connectPorts(self.predator3_schedule.outport_goal, self.predator3_goal.inport_schedule)

        # 连接schedule与plan
        self.connectPorts(self.predator3_schedule.outport_plan, self.predator3_plan1.inport_schedule)
        self.connectPorts(self.predator3_plan1.outport_schedule, self.predator3_schedule.inport_plan)

        self.connectPorts(self.predator3_schedule.outport_plan, self.predator3_plan2.inport_schedule)
        self.connectPorts(self.predator3_plan2.outport_schedule, self.predator3_schedule.inport_plan)

        self.connectPorts(self.predator3_schedule.outport_plan, self.predator3_plan3.inport_schedule)
        self.connectPorts(self.predator3_plan3.outport_schedule, self.predator3_schedule.inport_plan)

        self.connectPorts(self.predator3_schedule.outport_plan, self.predator3_plan4.inport_schedule)
        self.connectPorts(self.predator3_plan4.outport_schedule, self.predator3_schedule.inport_plan)

        self.connectPorts(self.predator3_schedule.outport_plan, self.predator3_plan5.inport_schedule)
        self.connectPorts(self.predator3_plan5.outport_schedule, self.predator3_schedule.inport_plan)

        # 连接plan与interaction
        self.connectPorts(self.predator3_plan1.outport_interaction, self.predator3_interaction.inport_plan)
        self.connectPorts(self.predator3_interaction.outport_plan, self.predator3_plan1.inport_interaction)

        self.connectPorts(self.predator3_plan2.outport_interaction, self.predator3_interaction.inport_plan)
        self.connectPorts(self.predator3_interaction.outport_plan, self.predator3_plan2.inport_interaction)

        self.connectPorts(self.predator3_plan3.outport_interaction, self.predator3_interaction.inport_plan)
        self.connectPorts(self.predator3_interaction.outport_plan, self.predator3_plan3.inport_interaction)

        self.connectPorts(self.predator3_plan4.outport_interaction, self.predator3_interaction.inport_plan)
        self.connectPorts(self.predator3_interaction.outport_plan, self.predator3_plan4.inport_interaction)

        self.connectPorts(self.predator3_plan5.outport_interaction, self.predator3_interaction.inport_plan)
        self.connectPorts(self.predator3_interaction.outport_plan, self.predator3_plan5.inport_interaction)

        # agent 2
        predator2_goal = Goal(args, 1)
        self.predator2_goal = self.addSubModel(predator2_goal)
        self.predator2_schedule = self.addSubModel(Schedule())
        self.predator2_plan1 = self.addSubModel(Plan1("predator2"))
        self.predator2_plan2 = self.addSubModel(Plan2("predator2"))
        self.predator2_plan3 = self.addSubModel(Plan3("predator2"))
        self.predator2_plan4 = self.addSubModel(Plan4("predator2"))
        self.predator2_plan5 = self.addSubModel(Plan5("predator2"))

        self.predator2_interaction = self.addSubModel(Interaction("predator2"))

        # 连接goal与schedule
        self.connectPorts(self.predator2_goal.outport_schedule, self.predator2_schedule.inport_goal)
        self.connectPorts(self.predator2_schedule.outport_goal, self.predator2_goal.inport_schedule)

        # 连接schedule与plan
        self.connectPorts(self.predator2_schedule.outport_plan, self.predator2_plan1.inport_schedule)
        self.connectPorts(self.predator2_plan1.outport_schedule, self.predator2_schedule.inport_plan)

        self.connectPorts(self.predator2_schedule.outport_plan, self.predator2_plan2.inport_schedule)
        self.connectPorts(self.predator2_plan2.outport_schedule, self.predator2_schedule.inport_plan)

        self.connectPorts(self.predator2_schedule.outport_plan, self.predator2_plan3.inport_schedule)
        self.connectPorts(self.predator2_plan3.outport_schedule, self.predator2_schedule.inport_plan)

        self.connectPorts(self.predator2_schedule.outport_plan, self.predator2_plan4.inport_schedule)
        self.connectPorts(self.predator2_plan4.outport_schedule, self.predator2_schedule.inport_plan)

        self.connectPorts(self.predator2_schedule.outport_plan, self.predator2_plan5.inport_schedule)
        self.connectPorts(self.predator2_plan5.outport_schedule, self.predator2_schedule.inport_plan)

        # 连接plan与interaction
        self.connectPorts(self.predator2_plan1.outport_interaction, self.predator2_interaction.inport_plan)
        self.connectPorts(self.predator2_interaction.outport_plan, self.predator2_plan1.inport_interaction)

        self.connectPorts(self.predator2_plan2.outport_interaction, self.predator2_interaction.inport_plan)
        self.connectPorts(self.predator2_interaction.outport_plan, self.predator2_plan2.inport_interaction)

        self.connectPorts(self.predator2_plan3.outport_interaction, self.predator2_interaction.inport_plan)
        self.connectPorts(self.predator2_interaction.outport_plan, self.predator2_plan3.inport_interaction)

        self.connectPorts(self.predator2_plan4.outport_interaction, self.predator2_interaction.inport_plan)
        self.connectPorts(self.predator2_interaction.outport_plan, self.predator2_plan4.inport_interaction)

        self.connectPorts(self.predator2_plan5.outport_interaction, self.predator2_interaction.inport_plan)
        self.connectPorts(self.predator2_interaction.outport_plan, self.predator2_plan5.inport_interaction)

        # predator mas 的定义和端口连接 上端口--------------------------
        self.predators_center = self.addSubModel(Controller1(["predator1", "predator2", "predator3"]))

        self.connectPorts(self.predators_center.outport, self.predator1_goal.inport_center)
        self.connectPorts(self.predator1_goal.outport_center, self.predators_center.inport)

        self.connectPorts(self.predators_center.outport, self.predator2_goal.inport_center)
        self.connectPorts(self.predator2_goal.outport_center, self.predators_center.inport)

        self.connectPorts(self.predators_center.outport, self.predator3_goal.inport_center)
        self.connectPorts(self.predator3_goal.outport_center, self.predators_center.inport)

        # prey的内部端口连接---------------------------------------------------
        self.prey_goal = self.addSubModel(Goal2(args))
        self.prey_schedule = self.addSubModel(Schedule2())
        self.prey_plan1 = self.addSubModel(Plan1_2("prey"))
        self.prey_plan2 = self.addSubModel(Plan2_2("prey"))

        self.prey_interaction = self.addSubModel(Interaction2("prey"))

        # 连接goal与schedule
        self.connectPorts(self.prey_goal.outport_schedule, self.prey_schedule.inport_goal)
        self.connectPorts(self.prey_schedule.outport_goal, self.prey_goal.inport_schedule)

        # 连接schedule与plan
        self.connectPorts(self.prey_schedule.outport_plan, self.prey_plan1.inport_schedule)
        self.connectPorts(self.prey_plan1.outport_schedule, self.prey_schedule.inport_plan)

        self.connectPorts(self.prey_schedule.outport_plan, self.prey_plan2.inport_schedule)
        self.connectPorts(self.prey_plan2.outport_schedule, self.prey_schedule.inport_plan)

        # 连接plan与interaction
        self.connectPorts(self.prey_plan1.outport_interaction, self.prey_interaction.inport_plan)
        self.connectPorts(self.prey_interaction.outport_plan, self.prey_plan1.inport_interaction)

        self.connectPorts(self.prey_plan2.outport_interaction, self.prey_interaction.inport_plan)
        self.connectPorts(self.prey_interaction.outport_plan, self.prey_plan2.inport_interaction)

        # 连接center与prey
        self.prey_center = self.addSubModel(Controller2(["prey2"]))

        self.connectPorts(self.prey_center.outport, self.prey_goal.inport_center)
        self.connectPorts(self.prey_goal.outport_center, self.prey_center.inport)


        # 环境原子模型的连接过程 ------下端口----------------------------------------------
        # 定义环境原子模型，并将智能体与环境模型的端口进行连接------------------------------

        self.Env = self.addSubModel(StepScheduler(env, args))

        self.connectPorts(self.predator1_interaction.outport_agent, self.Env.inport)
        self.connectPorts(self.Env.outport, self.predator1_interaction.inport_agent)

        self.connectPorts(self.predator2_interaction.outport_agent, self.Env.inport)
        self.connectPorts(self.Env.outport, self.predator2_interaction.inport_agent)

        self.connectPorts(self.predator3_interaction.outport_agent, self.Env.inport)
        self.connectPorts(self.Env.outport, self.predator3_interaction.inport_agent)

        self.connectPorts(self.prey_interaction.outport_agent, self.Env.inport)
        self.connectPorts(self.Env.outport, self.prey_interaction.inport_agent)

        # 注意，理论上所有agent的端口都需要两两连接


if __name__ == "__main__":

    # 3-进行仿真


    model = Simulation()
    sim = Simulator(model)
    sim.setVerbose("log.txt")
    sim.setTerminationTime(500000)
    sim.simulate()

