import threading
import time


class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.leader = None

    def __str__(self):
        return f"Node {self.node_id}"

    def election_thread(self, nodes):
        print(f"Node {self.node_id}: Election started")
        higher_nodes = []
        for node in nodes:
            if node.node_id > self.node_id:
                higher_nodes.append(node)
        
        for higher_node in higher_nodes:
            print(f"Node {self.node_id}: Election message sent to Node {higher_node.node_id}.")
            higher_node.receive_msg(self)

    def receive_msg(self, source_node):
        if self.leader is None or self.node_id > self.leader.node_id:
            print(f"Node {self.node_id}: Election message received from Node {source_node.node_id} --> ACK sent to Node {source_node.node_id}.")
            source_node.receive_ack(self)
        else:
            print(f"Node {self.node_id}: Ignored message from Node {source_node.node_id}.")

    def receive_ack(self, dest_node):
        print(
            f"Node {self.node_id}: ACK received from Node {dest_node.node_id}.")
        self.leader = dest_node
        print(
            f"Node {self.node_id}: Acknowledged Node {dest_node.node_id} as leader.")



if __name__ == "__main__":
    nodes = []
    for i in range(1, 6):
        nodes.append(Node(i))
    threads = []

    for node in nodes:
        t = threading.Thread(target=node.election_thread, args=(nodes,))
        t.start()
        threads.append(t)
        
    while any(t.is_alive() for t in threads):
        time.sleep(0.1)

    elected_leader = max(nodes, key=lambda node: node.node_id)

    print(f"\nLeader: {elected_leader}")
