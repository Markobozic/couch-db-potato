import json

with open('query6.json', 'r') as file:
    data = json.load(file)

data = data['rows']
unique_freeway_values = {}

for each in data:
    if each['key'] in unique_freeway_values:
        continue
    else:
        unique_freeway_values[str(each['key'])] = each['value']

johnson_creek_id = '1046'
columbia_id = '1140'
path = []

while(1):
    path.append(unique_freeway_values[johnson_creek_id]['name'])
    curr = johnson_creek_id
    while curr != columbia_id:
        curr = unique_freeway_values[str(curr)]['downstream']
        print(path)
        path.append(unique_freeway_values[str(curr)]['name'])
    break

