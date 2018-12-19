class A:
    def __init__(self):
        self.name = "tom"
        self.age = 20

    def jineng(self):
        print("eat")

    def fangfa(self):
        print(23)

    def run(self):
        a = self.jineng()
        b = self.fangfa()


if __name__ == '__main__':
    s = A()
    s.run()