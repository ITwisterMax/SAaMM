from services.exponential_distribution import exponential_number


class Generator:
    def __init__(self, intensity):
        self.intensity = intensity
        self.ticks_for_generate = 0

    def start_generate(self):
        self.ticks_for_generate = exponential_number(self.intensity)

    def is_generated(self):
        return self.ticks_for_generate <= 0

    def tick(self):
        if self.ticks_for_generate > 0:
            self.ticks_for_generate -= 1
