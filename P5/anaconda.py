# Michael Gunning (mhgunnin)
# Nick Junius (njunius)
import json
import sys
from collections import namedtuple
from heapq import heappush, heappop


with open('Crafting.json') as f:
    Crafting = json.load(f)

Items = Crafting['Items']
initial_inventory = Crafting['Initial']
goal_inventory = Crafting['Goal']
item_index = {name: i for i,name in enumerate(Items)}
inverse_item_index = {}
for i in item_index:
    inverse_item_index[item_index[i]] = i

def make_state(inventory):
    state_list = []
    for i in Items:
        if i in inventory:
            state_list.append(inventory[i])
        else:
            state_list.append(0)
    return tuple(state_list)

initial = make_state(initial_inventory)
goal = make_state(goal_inventory)

def make_checker(rule):
    consumes, requires = rule.get('Consumes',{}), rule.get('Requires',{})
    consumption_pairs = [(item_index[item],consumes[item]) for item in consumes]
    requirement_pairs = [(item_index[item],1) for item in requires]
    both_pairs = consumption_pairs + requirement_pairs
    def check(state):
        return all([state[i] >= v for i,v in both_pairs])

    return check

def make_effector(rule):
    # use rule to build a list of pairs:
    #    (index of item, how much to shift that item count) that covers all items
    delta_pairs = []
    consumes, produces = rule.get('Consumes',{}), rule.get('Produces',{})

    consumption_pairs = [(item_index[item],consumes[item]*-1) for item in consumes]
    for item in Items:

        if item in consumes:
            delta_pairs.append((item_index[item],consumes[item]*-1))
        elif item in produces:
            delta_pairs.append((item_index[item],produces[item]))
        else:
            delta_pairs.append((item_index[item],0))

    def effect(state):
        return tuple([state[i] + delta for i, delta in delta_pairs])
    return effect

Recipe = namedtuple('Recipe',['name','check','effect','cost'])
all_recipes = []
for name, rule in Crafting['Recipes'].items():
    checker = make_checker(rule)
    effector = make_effector(rule)
    recipe = Recipe(name, checker, effector, rule['Time'])
    all_recipes.append(recipe)


def graph(state):
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)

def heuristic(state):
    if state[0] > 1 or state[1] > 1 or state[2] > 1 or state[3] > 14 or state[4] > 1  or state[5] > 6 or state[8] > 1 or state[9] > 7 or state[14] > 1 \
            or state[6] > 1 or state[7] > 1 or state[11] > 8 or state[12] > 1 or state[13] > 1 or state[15] > 1 or state[16] > 1: return sys.maxint
    count_of_state_to_goal = 0
    for i in range(len(goal)):
        if goal[i] > 0 and state[i] >= goal[i]:
            count_of_state_to_goal += state[i]
    nonzero_in_goal = 0
    for i in goal:
        if i > 0:
            nonzero_in_goal += i
    return nonzero_in_goal - count_of_state_to_goal

def is_goal(state):
    count_of_state_to_goal = 0
    for i in range(len(goal)):
        if goal[i] > 0 and state[i] >= goal[i]:
            count_of_state_to_goal += 1
    nonzero_in_goal = 0
    for i in goal:
        if i > 0:
            nonzero_in_goal += 1
    return nonzero_in_goal <= count_of_state_to_goal

def search(graph, initial, is_goal, limit, heuristic):
    queue = []
    prev = {}
    cost_so_far = {}
    plan = []
    name_of_action = {}
    action_cost = {}
    iterations_made = 0
    total_cost = 0

    heappush(queue, (0, initial))
    prev[initial] = None
    cost_so_far[initial] = 0
    while queue:
        current_state = heappop(queue)[1];
        if iterations_made == limit:
            print "Limit hit!"
            print current_state
            break

        if is_goal(current_state):
            total_cost = cost_so_far[current_state]
            while current_state != initial:
                plan.append((action_cost[current_state], current_state, name_of_action[current_state]))
                current_state = prev[current_state]
            plan.reverse()
            break
        for next_state_tuple in graph(current_state):
            next_state = next_state_tuple[1]
            new_cost = next_state_tuple[2] + cost_so_far[current_state];
            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost;
                action_cost[next_state] = next_state_tuple[2];
                heappush(queue, (heuristic(next_state) + new_cost, next_state))
                prev[next_state] = current_state
                name_of_action[next_state] = next_state_tuple[0]
        iterations_made += 1;


    return total_cost, plan
limit = 1000000

total_cost, plan = search(graph, initial, is_goal, limit, heuristic)

def state_to_result(state):
    out = {}
    index = 0
    for i in state:
        if i != 0:
            out[inverse_item_index[index]] = i
        index += 1
    return out
for i in plan:
    print i[0], i[2], state_to_result(i[1])

print "Total Cost: " + str(total_cost) + " Length: " + str(len(plan))










