
class Edge(object):
    """Base class for graph edges , a simple class that holds the connection values of plugs,
    """

    def __init__(self, name, input=None, output=None, arbitraryData=None):
        """
        :param name: str, the name for the edge
        :param input: InputPlug instance, the input plug instance
        :param output: OutputPlug instance, the output plug instance
        :param arbitraryData: any extra edge data, should be serializable eg dict,list
        """
        self.name = name
        self.input = input,
        self.output = output
        self.arbitraryData = arbitraryData

    def __repr__(self):
        return "{0}{1}".format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, Edge) and other.input == self.input and other.output == self.output

    def serialize(self):
        """Returns a dict of the input, output and the arbitraryData
        :return: dict
        """
        data = {"name": self.name,
                "input": self.input,
                "output": self.output,
                "arbitraryData": self.arbitraryData
                }
        return data
