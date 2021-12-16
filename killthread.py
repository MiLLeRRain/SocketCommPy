import os
with os.popen('netstat -aon|findstr "9999"') as res:
    res = res.read().split('\n')
result = []
for line in res:
    temp = [i for i in line.split(' ') if i != '']
    if len(temp) > 4:
        result.append({'pid': temp[4], 'address': temp[1], 'state': temp[3]})
    print(result)