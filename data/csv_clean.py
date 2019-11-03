import csv
data = []

f = open('data\\flights.csv', 'r')
csvreader = csv.reader(f)

for row in csvreader: 
    data.append(row) 

city_list = data[0]

print(city_list)
for i in range(1, len(data)):
    data[i][i] = 0

for i in range(len(data)):  
    for j in range(i + 1, len(data)):  
        data[i][j] = data[j][i]

f2 = open('data\\flights.csv', 'w')
for i in data:
    for j in i:
        f2.write(str(j))
        f2.write(',')
    f2.write('\n') 