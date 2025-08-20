DIRTY = "Dirty"
CLEAN = "Clean"

def print_state(state):
    print(f"Room A: {state[0]}, Room B: {state[1]}, Agent at: {state[2]}")

def is_goal(state):
    return state[0] == CLEAN and state[1] == CLEAN

def vacuum_agent(state):
    roomA, roomB, position = state
    if position == "A":
        if roomA == DIRTY:
            print("Action: Suck (cleaning Room A)")
            state[0] = CLEAN
        else:
            print("Action: Move Right")
            state[2] = "B"
    elif position == "B":
        if roomB == DIRTY:
            print("Action: Suck (cleaning Room B)")
            state[1] = CLEAN
        else:
            print("Action: Move Left")
            state[2] = "A"
    return state

print("Vacuum Cleaner Problem Simulation")
roomA = input("Enter state of Room A (Clean/Dirty):").capitalize()
roomB = input("Enter state of Room B (Clean/Dirty):").capitalize()
agent_pos = input("Enter initial Agent Position (A/B)").upper()
if roomA not in [CLEAN, DIRTY] or roomB not in [CLEAN, DIRTY] or agent_pos not in ["A", "B"]:
    print("Invalid input! Please restart and enter values correctly.")
    exit()
state = [roomA, roomB, agent_pos]
print("\nInitial State:")
print_state(state)
print()
print("Vacuum Cleaner Starting!")
while not is_goal(state):
    state=vacuum_agent(state)
    print_state(state)
print("Task Completed! Both Room Are Clean")