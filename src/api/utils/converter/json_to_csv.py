import csv


def export_json_to_csv(json_data, response):
    header = json_data.keys()
    writer = csv.DictWriter(response, fieldnames=header)
    writer.writeheader()
    writer.writerow(json_data)

    return response
