import os
import sys
import webbrowser
from pyvis.network import Network


class InternalGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = list()

    def add_node(self, name, hashrate):
        self.nodes[name] = hashrate

    def add_edge(self, miner_identifier, to_miner_id, relay_latency):
        self.edges.append((miner_identifier, to_miner_id, relay_latency)) # add as tuple

    def generate_pyvis_network(self):
        net = Network(notebook=True, directed =True)
        # add notebook=True, from: https://www.cnblogs.com/chucklu/p/17326394.html
        # add notebook=True, from: https://stackoverflow.com/a/70198398/2006674
        net.repulsion(node_distance=200, spring_length=300)

        for miner_identifier, miner_hashrate in self.nodes.items():
            net.add_node(n_id = miner_identifier, 
                         value = miner_hashrate, 
                         title = f'Hashrate is {miner_hashrate}')
            
        for (from_node, to_node, relay_latency) in self.edges:
            net.add_edge(from_node, 
                         to_node, 
                         arrowStrikethrough = False,
                         title = f'Latency is: {relay_latency}', 
                         value = 1.0/float(relay_latency))

        return net


def main():
    ig = InternalGraph()

    with open(sys.argv[1]) as file:
        for line in file:
            line = line.strip()
            
            # skip empty lines
            if line == '':
                continue

            # skip comments
            if line[0] == '#':
                continue

            # print(line) # DEBUG

            tokens = line.split()
            len_tokens = len(tokens)

            if len_tokens < 2:
                print(f'minimum is 2 tokens per line {len_tokens=} {tokens=}')
                exit()
            elif len_tokens % 2 != 0:
                print(f'number of tokens must be even {len_tokens=} {tokens=}')
                exit()

            # miner identifier (string)
            # its hashrate (floating point)
            # a list of peers, each is a pair of:
            # miner id (string)
            # relay latency (floating point)
                # format explanation from: https://github.com/LarryRuane/minesim#configuration-file

            miner_identifier = tokens[0]
            miner_hashrate = tokens[1]
            # print(f'  {miner_identifier=} {miner_hashrate=}') # DEBUG

            ig.add_node(miner_identifier, miner_hashrate)

            # iterate over 2 element in same time
            it = iter(tokens[2:])
            while True:
                try:
                    to_miner_id = next(it) 
                    relay_latency = next(it)
                    # print(f'    {to_miner_id=} {relay_latency=}') # DEBUG

                    ig.add_edge(miner_identifier, to_miner_id, relay_latency)

                except StopIteration:
                    # no more elements in the iterator
                    break
                
    # show visualization
    net = ig.generate_pyvis_network()
    filename = 'nodes.html'
    net.show(filename)
    webbrowser.open('file://' + os.path.realpath(filename))


if __name__ == "__main__":
    main()
