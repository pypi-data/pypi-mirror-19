def add(*a):
    s=0
    for i in a:
        s=s+i
    print("sum is",s)
def sub(a,*b):
    s=a
    for i in b:
      s=s-i
    print("sub is",s)
