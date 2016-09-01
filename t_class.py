
class Person(object):
    def __init__(self, name):
        self.name = name


class Doctor(Person):
    def __init__(self, name):
        super(Doctor, self).__init__(name)
        print("my name is {}".format(name))


d = Doctor("Tom")
print(d.name)

'''
Model

Form / ModelForm

Field -> Form Field -> Form Widget
'''