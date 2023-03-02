import csv

num_zones_horizontal = 4
num_zones_vertical = 5
zone_width = 1280 // num_zones_horizontal
zone_height = 820 // num_zones_vertical

zone_times = {}
time_values = []

with open('output.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        x = int(row[0])
        y = int(row[1])
        time = int(row[2])
        zone_x = x // zone_width
        zone_y = y // zone_height
        zone_key = (zone_x, zone_y)
        if zone_key not in zone_times:
            zone_times[zone_key] = {
                'count': 0,
                'pixels': [(x, y)]
            }
        else:
            zone_times[zone_key]['pixels'].append((x, y))
        zone_times[zone_key]['count'] += 1
        time_values.append(time)

mean_time = time_values[-1] / len(time_values)

for y in range(num_zones_vertical):
    for x in range(num_zones_horizontal):
        zone_key = (x, y)
        time = zone_times.get(zone_key, {'count': 0, 'pixels': []})
        concentration_time = (time['count'] * mean_time) / 1000
        print(f"Зона {zone_key} ({zone_width},{zone_height}) - ({(x+1)*zone_width-1},{(y+1)*zone_height-1}): {time['count']} точек, Время концентрации на участке = {concentration_time:.2f} секунд") # округление до двух знаков после запятой



