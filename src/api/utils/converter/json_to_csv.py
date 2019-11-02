import csv


def flattenjson(b, delim):
    val = {}
    for i in b.keys():
        if isinstance(b[i], dict):
            get = flattenjson(b[i], delim)
            for j in get.keys():
                val[i + delim + j] = get[j]
        else:
            val[i] = b[i]

    return val


def export_json_to_csv(json_data, response):
    flatten_json_data = flattenjson(json_data, delim='__')

    header = flatten_json_data.keys()

    writer = csv.DictWriter(response, fieldnames=header)
    writer.writeheader()
    writer.writerow(flatten_json_data)

    return response
