a = int(input( ))
d = 0
while a > 0:
    d*=10
    d+= a % 10
    a//=10
print(d)