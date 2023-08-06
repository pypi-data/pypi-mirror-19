def rev(a):
   b = []
   a = list(a)
   for i in range(len(a)):
      x = a.pop()
      b.append(x)
   print(b)

