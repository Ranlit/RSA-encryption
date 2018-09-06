def quotient(a,d):
    r=a%d
    q=int(a/d)
    return (q,r)

def mod(a,d):
    return a%d

def quot(a,d):
    return int(a/d)
    
def euclidean(a,b):
    (q,r)=quotient(a,b)
    if r==0:
        return (b,0,1)
    else:
        (d,s1,t1)=euclidean(b,r)
        return (d,t1, s1-t1*q)

def relatively_prime(a,b):
    (d,s,t)=euclidean(a,b)
    if (d==1):
        return True
    return False

def inverse(a,n):
    if relatively_prime(a,n):
        (d,x,y)=euclidean(a,n)
        while (x<0):
            x=x+n
        while (x>n):
            x=x-n
        return x
    else:
        return False

def prime(a):
    k=2
    while(k<=(a)**(1/2)):
        (q,r)=quotient(a,k)
        if r==0:
            return False
        k=k+1
    return True

def list_primes(small,big):
    a=max(small,2)
    P=[]
    while (a<=big):
        if prime(a):
            P.append(a)
        a=a+1
    return P



Letter = {0:' ',1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I',10:'J',11:'K',12:'L',13:'M',14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',20:'T',21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z'}
Number = { Letter[x]:x for x in Letter}
for x in Letter:
    Number[Letter[x].lower()]=x
