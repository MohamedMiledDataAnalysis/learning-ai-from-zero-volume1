"""Chapter 19 — reinforcement learning: Q-learning on a collections problem.

TEACHING SIMULATION. The probabilities and rewards below are invented for this
chapter; they are not taken from the deal pack or from any real servicer.

A loan is 1, 2 or 3 instalments in arrears. Each month the collections team
chooses an action. The loan then cures (pays everything: +100), stays where it
is, or rolls one bucket further. Rolling from 3 instalments means default (-300).
Actions cost money: nothing 0, reminder letter -2, phone call -10.
"""

import numpy as np

STATES = ["1 in arrears", "2 in arrears", "3 in arrears"]
ACTIONS = ["nothing", "reminder", "call"]
COST = {"nothing": 0, "reminder": -2, "call": -10}
CURE, DEFAULT = 100, -300
# P[state][action] = (probability of cure, of staying, of rolling one bucket further)
P = {
    0: {"nothing": (0.30, 0.40, 0.30), "reminder": (0.45, 0.35, 0.20), "call": (0.60, 0.25, 0.15)},
    1: {"nothing": (0.15, 0.45, 0.40), "reminder": (0.25, 0.45, 0.30), "call": (0.45, 0.35, 0.20)},
    2: {"nothing": (0.05, 0.45, 0.50), "reminder": (0.10, 0.45, 0.45), "call": (0.30, 0.40, 0.30)},
}
GAMMA = 0.95       # a reward next month is worth 95% of the same reward now


def step(state, action, rng):
    """Play one month: return (reward, next state or None when the episode ends)."""
    cure, stay, roll = P[state][action]
    u = rng.random()
    if u < cure:
        return COST[action] + CURE, None
    if u < cure + stay:
        return COST[action], state
    if state == 2:
        return COST[action] + DEFAULT, None
    return COST[action], state + 1


def q_learning(episodes=20000, alpha=0.05, epsilon=0.2, seed=0):
    rng = np.random.default_rng(seed)
    Q = np.zeros((3, 3))                                  # Q[state, action]: the agent's estimate of the value
    for _ in range(episodes):
        state = 0                                         # every episode starts at 1 instalment in arrears
        while state is not None:
            if rng.random() < epsilon:                    # explore: try a random action
                a = int(rng.integers(3))
            else:                                         # exploit: take the best action so far
                a = int(Q[state].argmax())
            reward, nxt = step(state, ACTIONS[a], rng)
            target = reward + (GAMMA * Q[nxt].max() if nxt is not None else 0.0)
            Q[state, a] += alpha * (target - Q[state, a])    # move the estimate a little towards the target
            state = nxt
    return Q


def exact_values():
    """Value iteration: the exact answer, computable here because we know P (a real agent does not)."""
    Q = np.zeros((3, 3))
    for _ in range(500):
        V = Q.max(axis=1)
        for s in range(3):
            for a, name in enumerate(ACTIONS):
                cure, stay, roll = P[s][name]
                roll_value = DEFAULT if s == 2 else GAMMA * V[s + 1]
                Q[s, a] = COST[name] + cure * CURE + stay * GAMMA * V[s] + roll * roll_value
    return Q


def show(title, Q):
    print(title)
    print("  state          | " + " | ".join(f"{a:>8}" for a in ACTIONS) + " | best action")
    for s, name in enumerate(STATES):
        print(f"  {name:<14} | " + " | ".join(f"{v:8.1f}" for v in Q[s]) + f" | {ACTIONS[int(Q[s].argmax())]}")


if __name__ == "__main__":
    show("Learnt by Q-learning (20,000 simulated loans):", q_learning())
    print()
    show("Exact values (value iteration):", exact_values())
