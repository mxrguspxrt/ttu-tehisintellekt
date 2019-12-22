from queue import Queue
import json

lava_map1_string = "\n".join([
    "      **               **      ",
    "     ***     D        ***      ",
    "     ***                       ",
    "                      *****    ",
    "           ****      ********  ",
    "           ***          *******",
    " **                      ******",
    "*****             ****     *** ",
    "*****              **          ",
    "***                            ",
    "              **         ******",
    "**            ***       *******",
    "***                      ***** ",
    "                               ",
    "                s              ",
])

lava_map2_string = "\n".join([
    "     **********************    ",
    "   *******   D    **********   ",
    "   *******                     ",
    " ****************    **********",
    "***********          ********  ",
    "            *******************",
    " ********    ******************",
    "********                   ****",
    "*****       ************       ",
    "***               *********    ",
    "*      ******      ************",
    "*****************       *******",
    "***      ****            ***** ",
    "                               ",
    "                s              ",
])


def get_processed_map(string_map):
    proccessable_map = get_proccessable_map(string_map)
    start = get_start(proccessable_map)

    frontier = Queue()
    frontier.put(start)

    came_from = {}
    came_from[json.dumps(start)] = None

    while not frontier.empty():
        current_node = frontier.get()

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
                        frontier.put(neighbor_node)
                        came_from[json.dumps(neighbor_node)] = current_node

                    is_diamond = get_is_diamond(
                        proccessable_map, neighbor_node)
                    if is_diamond:
                        return {
                            "proccessable_map": proccessable_map,
                            "came_from": came_from,
                            "diamond": neighbor_node,
                            "start": start
                        }

    return {
        "proccessable_map": proccessable_map,
        "came_from": came_from}


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


def get_proccessable_map(string_map):
    rows = string_map.split("\n")
    return list(map(lambda row: list(row), rows))


def print_path(map_string):
    processed_map = get_processed_map(map_string)

    path = get_path(processed_map)

    map_with_path = get_map_with_path(processed_map)
    print("\n\nMap with path is:")
    print(map_to_string(map_with_path))


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
    print_path(lava_map1_string)
    print_path(lava_map2_string)


main()
