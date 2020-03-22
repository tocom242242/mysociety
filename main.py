from simulator import *

TEST_CONFIG = {
    "nb_episode": 10,
    "nb_agents": 3,
    "save_interval": 2,
    "result_dir": "./result/",
    "agent": {"epsilon": 1.,
              "epsilon_decay_rate": .99,
              }
}

CONFIG = {
    "nb_episode": 1,
    "nb_agents": 3,
    "save_interval": 1,
    "result_dir": "./result/",
    "agent": {"epsilon": 1.,
              "epsilon_decay_rate": .99,
              }
}

main(cfg=TEST_CONFIG)
# main(cfg=CONFIG)
