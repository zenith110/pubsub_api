import csv


class FinalData:
    def __init__(self) -> None:
        self.data = []


class Data:
    def __init__(self, zipcode, city, state) -> None:
        self.zipcode = zipcode
        self.city = city
        self.state = state


def parse_data():
    filename = "zipcodes.csv"
    final_data = FinalData()
    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            zipcode = row[0].split()[0]
            city = row[0].split()[1]
            state = row[0].split()[2]
            zipcode_data = Data(zipcode, city, state)
            final_data.data.append(zipcode_data)
    return final_data.data
