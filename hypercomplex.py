class HyperComplex:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def get_real(self):
        return self.real
    def get_imag(self):
        return self.imag


class CoSystem:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_a(self):
        return self.a
    def get_b(self):
        return self.b