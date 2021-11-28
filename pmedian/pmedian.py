import pandas as pd
import folium
import math

from itertools import combinations
from pyproj import Proj, transform
from tqdm import tqdm
from typing import List


def preprocess_data(path: str) -> pd.DataFrame:
    """
    "Note": Modify and use according to your own data.
    Or you don't need to use this code, and you just insert some code about preprocess in "main"

    Explanation
    Data Path is received as inputs and data is purified in the order of "name"/"latitude"/"longitude".

    Arguments
        path: A path of a file in the form of 'xlsx' and 'csv' is input.

    Return
        Pandas Data Frame: Form of Pandas Data Frame with Column in the order of "Name", "Latitude", and "Longitude"
    """

    if "xlsx" in path:
        data = pd.read_excel(path)
        ############ Modify according to input/output ####################
        if "대구분명칭" in data.columns:
            data = data[["대구분명칭", "위도", "경도"]]
        elif "시장명" in data.columns:
            data = data[["시장명", "위도", "경도"]]
        data.columns = ["name", "latitude", "longitude"]
        ##########################################################
    elif "csv" in path:
        data = pd.read_csv(
            path, header=None
        )  # Header options are also modified according to your data.
        ############ Modify according to input/output ####################
        data.columns = ["longitude", "latitude", "name"]
        data = data[["name", "latitude", "longitude"]]
        ##########################################################
    return data


def coordinate_change(data: pd.DataFrame, c1: str, c2: str) -> pd.DataFrame:
    """
    Explanation
        The latitude and longitude existing in the data frame are converted from the coordinate c1 to the coordinate c2 to be converted.
    Arguments
        data: The columns are in the form of a Pandas Data Frame in the order of "name", "latitude", and "longitude".
        c1: The original latitude and longitude coordinate system.
        c2: The latitude and longitude coordinate system to convert.
            c1 & c2: something like 'epsg:5178', 'epsg:4326', etc..

    Return
        Pandas Data Frame: Data frame with converted latitude and longitude coordinates.
    """
    proj_c1 = Proj(init=c1)
    proj_c2 = Proj(init=c2)

    for i in tqdm(range(len(data))):
        change_long, change_lat = transform(
            proj_c1, proj_c2, data["longitude"][i], data["latitude"][i]
        )

        data["longitude"][i] = change_long
        data["latitude"][i] = change_lat

    return data


def shortest_distance(F: pd.DataFrame, L: pd.DataFrame):
    """
    Explanation
        Create the shortest matrix between public facilities and floating population.

    Arguments
        F: Coordinates of public facilities.
        L: Coordinates of the floating population.

    Return
        Pandas Data Frame: Shortest distance matrix between public facilities and floating population
    """
    F_list = []
    L_list = []
    for i in range(len(F)):
        name = f"F_{i}"
        F_list.append(name)

    for i in range(len(L)):
        name = f"L_{i}"
        L_list.append(name)

    distance = pd.DataFrame(columns=F_list, index=L_list)
    for i in range(len(distance)):
        for j, col in enumerate(distance.columns):
            square_sum = ((F["latitude"][j] - L["latitude"][i]) ** 2) + (
                (F["longitude"][j] - L["longitude"][i]) ** 2
            )
            dist = math.sqrt(square_sum)
            distance[col][i] = dist

    return distance


def p_list_set(distance_data: pd.DataFrame, p: int) -> List[List]:
    """
    Explanation
        Based on F(Public Facilities), '2p' public facilities with the shortest
         distance from the floating population coordinates are selected

    Args
        distance_data: The matrix of distances between F and L. (column = F, row = L)
        p: The number of public facilities to be finally selected.

    return
        p_list_set: A set of p lists tied up in p
        ex) candidate= [1,2,3,4,5,6,7,8,9,10] / p=3
            p_list_set = [
                [1,2,3],
                [2,3,4],
                [3,4,5]
            ]
    """
    # The sum of the distances between the coordinates of the floating population for public facilities.
    col_sum = list(distance_data.sum(axis=0))

    col_sum_tuple = []  # Tie col_sum with index.
    for i in range(len(col_sum)):
        tup = (i, col_sum[i])
        col_sum_tuple.append(tup)

    col_sum_tuple.sort(key=lambda x: x[1])
    col_sum_tuple = col_sum_tuple[: 2 * p]  # Choose the top 2p based on distance.

    p_list_set = [col_sum_tuple[i : i + p] for i in range(p)]

    return p_list_set


def candidate_place(
    pb: pd.DataFrame, distance: pd.DataFrame, p_list_set: List[List]
) -> List:
    """
    Explanation
        Only names are extracted from DataFrame having a minimal distance within each set.

    Args:
        pb: DataFrame for public facilities.
        distance: DataFrame about the distance between F and L

        p_list_set: In distance, a set of p lists grouped by p based on distance

    Return:
        List: List of names of p public facilities.
    """
    min_sum_list = []  # take the minimum values in the pth list.
    for i in range(len(p_list_set)):
        tup_check = []
        for j in p_list_set[i]:
            tup_check.append(f"F_{j[0]}")
        check_df = distance[tup_check]

        check_df["min"] = 0  # generate 'min' column
        for k in range(len(check_df)):
            k_th_row = check_df.iloc[k][:-1]  # exclude 'min' column
            check_df["min"][k] = min(k_th_row)

        min_sum_value = sum(check_df["min"])
        min_sum_list.append(min_sum_value)

    final_index = min_sum_list.index(min(min_sum_list))
    final_set = p_list_set[final_index]
    final_set.sort(key=lambda x: x[0])

    final_idx = [idx for idx, dist in final_set]
    final_market_data = pb.iloc[final_idx, :]
    final_market_data.reset_index(drop=True, inplace=True)

    name_list = [name for name in final_market_data["name"]]
    return name_list


def top_value(char_list: List) -> int:
    """Heuristic Method with P-Median
    Explanation
        Get the top three to six. (If there is a duplicate value, bring up to six.)

    Args:
        char_list: A list of the names of the final candidates.

    Return:
        int: The number of final candidates to get
    """
    appearance_candidate = list(pd.Series(char_list).value_counts())

    num_of_candidate = 3
    for first, second in zip(appearance_candidate[2:], appearance_candidate[3:]):
        if first == second:
            num_of_candidate += 1
        else:
            break

    return num_of_candidate


def make_finalset(market_data: pd.DataFrame, char_list: List) -> pd.DataFrame:
    """Heuristic Method with P-Median
    Explanation
        After receiving the char_list, which is the list of the final candidates,
         The final candidates is mapped with public facility data
         to return a DataFrame containing only the final candidates.

    Args:
        market_data: Data containing market location information.
        char_list: The list with the names of the final candidates overlapped.

    Return:
        Pandas DataFrame: The final DataFrame containing the names, latitudes, and longitude of the final candidates.
    """

    num_of_candidate = top_value(char_list)
    final_name_list = pd.Series(char_list).value_counts().index[:num_of_candidate]

    market_index = [
        (market_data[market_data["name"] == name].index)[0] for name in final_name_list
    ]

    market_final = market_data.iloc[market_index, :]
    market_final.reset_index(drop=True, inplace=True)
    return market_final


if __name__ == "__main__":
    # Insert your own data
    pf_location_path = "../data/울진군예상좌표.xlsx"  # market: 지역_공공공장소/위도/경도
    population_location_path = "../data/울진_편의점.csv"  # population: 지역_유동인구/위도/경도

    # Dataset Upload
    pf_data = preprocess_data(pf_location_path)
    population_data = preprocess_data(population_location_path)

    # Chnage Coordinate
    pf_data = coordinate_change(pf_data, "epsg:4326", "epsg:5178")
    population_data = coordinate_change(population_data, "epsg:4326", "epsg:5178")

    # Calculate Distance between public facilities and  floating poplulation
    distance = shortest_distance(pf_data, population_data)

    # Using Heuristic P-Median
    char_list = []
    for p in range(3, 11):
        p_list = p_list_set(distance, p)
        name_list = candidate_place(pf_data, distance, p_list)

        char_list.extend(name_list)

    pf_final = make_finalset(pf_data, char_list)
    pf_final = coordinate_change(pf_final, "epsg:5178", "epsg:4326")
    print(pf_final)
