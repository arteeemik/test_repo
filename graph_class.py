"""The file describes the graph class."""
import typing

import osmnx as ox
from osmnx import distance as osmnx_distance
from osmnx import utils_graph
import networkx as nx


class Graph:
    """
    Класс графа некоторой области и функции, необходимые для работы с ним.

    Attributes
    --------
    graph : networkx.MultiDiGraph
    """

    def __init__(self, place_full_name: str, movement_type: str = "walk"):
        """
        Определяет объект graph в классе.

        Parameters
        ---------
        place_full_name : str
            Полное имя области, для которой хотим создать граф.
            example: "San Francisco, California, United States"
        movement_type : str {"all_private", "all", "bike", "drive", "drive_service", "walk"}
            Тип передвижения.
        """
        ox.config(log_console=True, use_cache=True)
        self.graph = ox.graph_from_place(
            place_full_name, network_type=movement_type
        )

    def get_nearest_nodes(
        self, points: typing.List[typing.Tuple[float, float]]
    ) -> typing.List[int]:
        """
        Возвращает ids ближайших вершин к координатам в points в графе.

        Parameters
        ---------
        points : typing.List[typing.Tuple[float, float]]
            Список координат точек.
        Returns
        ---------
        ids : typing.List[int]
           IDs ближайших вершины к координатам из points в графе.
        """
        latitude_coordinates = [point[0] for point in points]
        longitude_coordinates = [point[1] for point in points]
        return list(
            osmnx_distance.nearest_nodes(
                self.graph, longitude_coordinates, latitude_coordinates
            )
        )

    def get_shortest_path_between_two_points(
        self,
        first_point: typing.Tuple[float, float],
        second_point: typing.Tuple[float, float],
        optimizer: str = "length",
    ) -> (int, typing.List[int]):
        # pylint: disable=unbalanced-tuple-unpacking
        """
        Возвращает кратчайший путь между двумя координатами в области графа.

        Для точек first_point и second_point возьмется ближайший объект из графа.

        Parameters
        ---------
        first_point : typing.Tuple[float, float]
            Координаты точки.
        second_point : typing.Tuple[float, float]
            Координаты точки.
        optimizer : str {"length", "time"}
            Метрика, по которой ищем минимальный путь между двумя координатами.

        Returns
        ---------
        (distance, shortest_route) : (int, typing.List[int])
            distance -
                Если optimizer == "length": длина в метрах округленная до целых чисел.
                Если optimizer == "time": время в часах, которое будет затрачено на маршрут.
            shortest_route - путь от first_point до second_point в виде списка айдишников
                             объектов из графа.
        """
        first_node, second_node = self.get_nearest_nodes(
            [first_point, second_point]
        )

        shortest_route = nx.shortest_path(
            self.graph, first_node, second_node, weight=optimizer
        )
        edge_lengths = utils_graph.get_route_edge_attributes(
            self.graph, shortest_route, optimizer
        )
        distance = round(sum(edge_lengths))

        return distance, shortest_route
