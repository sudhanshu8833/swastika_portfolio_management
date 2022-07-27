import math

principal=int(input("write principal"))
amount=int(input("write amount"))

n=[]
r=[]

for i in range(1,1001):
    n.append(i)
    rate=100*((amount/principal-1)**1/i)
    r.append(rate)

print(n)
print(r)
