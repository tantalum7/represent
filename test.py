
from represent.represent import Represent



if __name__ == "__main__":

    represent = Represent()

    mp = represent.get_representative(10020)

    div = represent.get_division(31595)
    print(div.votes)

    results = represent.search_divisions("education")

    for division in results:
        print(division.division_id, division.name)

    print("done")
