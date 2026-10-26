# Syntax-only stand-in showing LEAN's event-driven strategy surface.
# No LEAN execution, live data, orders, or brokerage.
class MyStrategy(QCAlgorithm):
    def initialize(self):
        self.set_start_date(2020, 1, 1)
        self.asset = self.add_equity("AAPL").symbol
    def on_data(self, data):
        if self.asset in data:
            self.observe(data[self.asset].close)
