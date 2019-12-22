from queue import Queue, PriorityQueue
import json
from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


def get_file_contents(path):
    with open(path, 'r') as content_file:
        content = content_file.read()
        return content


def write_file_contents(path, contents):
    f = open(path, "w")
    f.write(contents)
    f.close()


lava_map1_string = get_file_contents("cave300x300")
lava_map2_string = get_file_contents("cave600x600")
lava_map3_string = get_file_contents("cave900x900")


def get_processed_map(string_map):
    proccessable_map = get_proccessable_map(string_map)
    start = get_start(proccessable_map)
    goal = get_goal(proccessable_map)

    frontier = PriorityQueue()
    frontier.put(PrioritizedItem(priority=0, item=start))

    came_from = {}
    came_from[json.dumps(start)] = None

    cost_so_far = {}
    cost_so_far[json.dumps(start)] = 0

    took_steps_count = 0

    while not frontier.empty():
        took_steps_count = took_steps_count + 1
        item = frontier.get()
        current_node = item.item

        neighbor_nodes = get_neighbors(proccessable_map, current_node)

        for neighbor_node in neighbor_nodes:

            if get_node_is_in_bounds(proccessable_map, neighbor_node):

                already_visited = json.dumps(neighbor_node) in came_from
                if not already_visited:

                    can_travel_to_neighbor_node = get_can_travel_to_neighbor_node(
                        proccessable_map,
                        neighbor_node
                    )
                    if can_travel_to_neighbor_node:

                        new_cost = cost_so_far[json.dumps(current_node)] + 1
                        if json.dumps(neighbor_node) not in cost_so_far or new_cost < cost_so_far[json.dumps(neighbor_node)]:
                            cost_so_far[json.dumps(neighbor_node)] = new_cost
                            heuristic_priority = get_heuristic_priority(
                                neighbor_node,
                                goal
                            )
                            frontier.put(
                                PrioritizedItem(
                                    priority=new_cost + heuristic_priority,
                                    item=neighbor_node
                                )
                            )
                            came_from[json.dumps(neighbor_node)] = current_node

                    is_diamond = get_is_diamond(
                        proccessable_map,
                        neighbor_node
                    )
                    if is_diamond:
                        processed_map = {
                            "proccessable_map": proccessable_map,
                            "came_from": came_from,
                            "diamond": neighbor_node,
                            "start": start
                        }
                        print("Took iterations to process:", took_steps_count)
                        print("Path has steps:", len(get_path(processed_map)))
                        return processed_map

    return {
        "proccessable_map": proccessable_map,
        "came_from": came_from}


def get_heuristic_priority(neighbor_node, goal):
    return max(abs(neighbor_node["column_index"]-goal["column_index"]), abs(neighbor_node["row_index"]-goal["row_index"]))


def get_is_diamond(proccessable_map, position):
    return proccessable_map[position["row_index"]][position["column_index"]] == "D"


def get_can_travel_to_neighbor_node(proccessable_map, position):
    return proccessable_map[position["row_index"]][position["column_index"]] != "*"


def get_neighbors(proccessable_map, position):
    left_position = {
        "column_index": position["column_index"]-1, "row_index": position["row_index"]}
    right_position = {
        "column_index": position["column_index"]+1, "row_index": position["row_index"]}
    top_position = {
        "column_index": position["column_index"], "row_index": position["row_index"]-1}
    bottom_position = {
        "column_index": position["column_index"], "row_index": position["row_index"]+1}

    neighbors = [
        left_position,
        right_position,
        top_position,
        bottom_position
    ]
    return list(filter(lambda x: x, neighbors))


def get_node_at(proccessable_map, position):
    if get_node_is_in_bounds(proccessable_map, position):
        return proccessable_map[position["row_index"]][position["column_index"]]


def get_node_is_in_bounds(proccessable_map, position):
    rows_count = len(proccessable_map)
    columns_count = len(proccessable_map[0])

    row_index = position["row_index"]
    column_index = position["column_index"]

    return row_index > -1 and row_index < rows_count and column_index > -1 and column_index < columns_count


def get_start(proccessable_map):
    for row_index in range(0, len(proccessable_map)):
        for column_index in range(0, len(proccessable_map[0])):
            if proccessable_map[row_index][column_index] == "s":
                return {"column_index": column_index, "row_index": row_index}


def get_goal(proccessable_map):
    for row_index in range(0, len(proccessable_map)):
        for column_index in range(0, len(proccessable_map[0])):
            if proccessable_map[row_index][column_index] == "D":
                return {"column_index": column_index, "row_index": row_index}


def get_proccessable_map(string_map):
    rows = string_map.split("\n")
    return list(map(lambda row: list(row), rows))


def process_and_store_result(filename, map_string):
    processed_map = get_processed_map(map_string)

    map_with_path = get_map_with_path(processed_map)
    print("Wrote result to file: ", filename)
    write_file_contents(filename, map_to_string(map_with_path))


def get_path(processed_map):
    diamond = processed_map["diamond"]
    path = []

    previous_node = diamond
    while(previous_node):
        path.append(previous_node)
        previous_node = processed_map["came_from"][json.dumps(previous_node)]

    return path


def get_map_with_path(processed_map):
    proccessable_map = processed_map["proccessable_map"]
    start = processed_map["start"]
    diamond = processed_map["diamond"]
    path = get_path(processed_map)

    new_map = list(proccessable_map)

    for node in path:
        new_map[node["row_index"]][node["column_index"]] = "."

    new_map[start["row_index"]][start["column_index"]] = "s"
    new_map[diamond["row_index"]][diamond["column_index"]] = "D"

    return new_map


def map_to_string(proccessable_map):
    return "\n".join(list(map(lambda x: "".join(x), proccessable_map)))


def main():
    process_and_store_result("cave300x300-result-astar-lisa1", lava_map1_string)
    process_and_store_result("cave600x600-result-astar-lisa1", lava_map2_string)
    process_and_store_result("cave900x900-result-astar-lisa1", lava_map3_string)


main()
