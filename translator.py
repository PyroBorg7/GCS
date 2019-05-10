import shapefile
"""
data = [
    [38.8781548838115,-77.3764300346375],
    [38.8795413373583,-77.3796486854553],
    [38.877570226617,-77.3796057701111],
    [38.8764343074595,-77.3767948150635],
    [38.8769521552097,-77.3733186721802],
    [38.8783720409729,-77.3724174499512],
    [38.8798420104618,-77.3733830451965],
    [38.8809945789057,-77.3758506774902],
    [38.8809611713878,-77.3782968521118],
    [38.8795413373583,-77.3796486854553]
]
"""
data = [
    [38.861164455523, -77.4728393554688],
    [38.8619998713995, -77.4670457839966],
    [38.8574550904945, -77.4666166305542],
    [38.8579229489991, -77.4706506729126],
    [38.8593265060448, -77.4732685089111],
    [38.861164455523, -77.4728393554688]
]
new_data = [
    [38.8609639542521, -77.4471759796143],
    [38.8588252388515, -77.4385070800781],
    [38.8502697340142, -77.4397945404053],
    [38.8502697340142, -77.4397945404053],
    [38.8519408119263, -77.4490642547607],
    [38.8609639542521, -77.4471759796143]
]
"""
for i in data:
    first = i[0] + 0.00001
    second = i[1] + 0.00001
    new_data.append([first, second])
"""
print(new_data)
w = shapefile.Writer('./test')
w.field('name', 'C')
w.poly([
    data,  # poly 1
    new_data  # poly 2
])
w.record('polygon1')
w.close()
