"""QLearning():
  #initialization
  for each state s in AllNonTerminalStates:
     for each action a in Actions(s):
         Q(s,a) = random()
  for each s in TerminalStates:
      Q(s,_) = 0 #Q(s) = 0 for all actions in s
  Loop number_of_episodes:
    let s = start_state()
    # Play episode until the end
    Loop until game_over():
      # get action to perform on state s according
      # to the given policy 90% of the time, and a
      # random action 10% of the time.
      let a = get_epsilon_greedy_action(s, 0.1)
      # make move from s using a and get the new state s'
      # and the reward r
      let (s', r) = make_move(s, a)
      # choose the max Q-value (qmax) on state s'
      let qmax = get_max_qvalue_on_state(s')
      # incrementally compute the average at Q(s,a)
      let Q(s, a) = Q(s, a) + alpha*[r + gamma * qmax - Q(s, a)]"""

