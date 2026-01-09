r=int(input("Enter the number of prime numbers you want in series: "))
number=1
prev=[]
div=[]
prime=[]

while len(prime)<r:
    number+=1
    prev.append(number)
    div=[]
    if prev:
        for p in prev:
            if p!=1 and p!=number and number%p==0:
                div.append(p)
        if div:
            continue
        else:
            prime.append(number)
print(prime)