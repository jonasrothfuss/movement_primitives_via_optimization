import matplotlib.pyplot as plt
import pandas as pd
from movement_primitives_optimization.trajectory_adaptation import *
from movement_primitives_optimization.record import record_trajectory


def simple_trajectory_example():
  """ generate a 2d example trajectory with function 0.1*x^2 + 0.2*x^3"""
  time_steps = 20
  x = np.linspace(start=0, stop=5, num=time_steps)
  old_traj = 0.1* x ** 2 + 0.2 * x ** 3
  traj_d = np.asarray([x, old_traj]).T

  start = np.asarray([0,0])
  goal = np.asarray([5,25])

  adapted_trajectories = adapt_all_dimensions(traj_d, start, goal)

  new_traj_x = adapted_trajectories[0]
  new_traj_y = adapted_trajectories[1]


  plt.plot(x, old_traj)
  plt.plot(new_traj_x, new_traj_y)
  plt.plot([start[0], goal[0]], [start[1], goal[1]])
  plt.show()


def record_trajectories_and_adapt(number_trajectories):
  recorded_trajectories = record_trajectory.record_n_trajectories(n=number_trajectories)
  adapt_recorded_trajectories(recorded_trajectories)


def adapt_recorded_trajectories(trajectories, plot=True):
  """ adapts all the given trajectories and plots them to different figure windows """
  assert trajectories is not None, "no trajectory given"

  was_df = False
  if isinstance(trajectories, pd.DataFrame):
    # flatten required to convert 2d array to 1d
    trajectories = trajectories.values.flatten()
    was_df = True


  number_of_recordings = trajectories.shape[0]
  trajectories_adapted = list()
  for i_traj in range(number_of_recordings):
    traj_d = trajectories[i_traj]

    start = [traj_d[0,0]+0.2, traj_d[0,1]+0.2]
    goal = [traj_d[-1,0]+0.2, traj_d[-1,1]+0.2]

    adapted_trajectories = adapt_all_dimensions(traj_d, start, goal)

    new_traj_x = adapted_trajectories[0]
    new_traj_y = adapted_trajectories[1]
    new_traj_xy = np.asarray([new_traj_x, new_traj_y]).T
    trajectories_adapted.append(new_traj_xy)

    if plot:
      plt.figure()
      plt.plot(traj_d[:,0], traj_d[:,1])
      plt.plot(new_traj_x, new_traj_y)
      plt.plot([start[0], goal[0]], [start[1], goal[1]])
      plt.show()

  if was_df:
    return pd.DataFrame(np.asarray(trajectories_adapted))
  else:
    return np.asarray(trajectories_adapted)

