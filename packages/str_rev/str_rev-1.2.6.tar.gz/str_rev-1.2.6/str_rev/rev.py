class A:
    def __init__(self,a):
        self.a=a

    def reverse(self):
        l = []
        c = 1
        for i in range(0, len(self.a)):
            l.append(self.a[len(self.a) - c])
            c += 1
        l = ''.join(l)
        return l


