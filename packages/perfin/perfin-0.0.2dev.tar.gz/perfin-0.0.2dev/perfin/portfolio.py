class Stock:
    """ The stock object represents a specific stock symbol"""

    def __init__(self, symbol, amount):
        """ Creates a stock object.

        Args:



        Returns:

        """
        self.symbol = symbol
        self.amount = amount


class Portfolio:
    """ A portfolio represents

    """
    def __init__(self, stocks=None):
        """  """
        self.stocks = stocks

    def get_current_value(self):
        """ Returns the current value of the portfolio. """
        pass