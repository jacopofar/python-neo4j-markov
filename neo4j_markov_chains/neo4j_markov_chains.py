# -*- coding: utf-8 -*-

from neo4j.v1 import GraphDatabase, basic_auth
import random


class Neo4jMarkovChain():

    def __init__(self, credentials=('neo4j', 'neo4j'), host='localhost', ngram_size=1):
        auth_token = basic_auth(credentials[0], credentials[1])
        self.session = GraphDatabase.driver("bolt://" + host, auth=auth_token).session()
        self.window_size = ngram_size
        self.transitions_queue = []

    def list_transitions(self, array, weight=1):
        for i in range(len(array)):
            yield (array[i:i + self.window_size],
                   array[i + 1:i + 1 + self.window_size], weight)

    def add_transitions(self, transitions):
        for (from_key, to_key, count) in transitions:
            # upsert for the starting and ending nodes and the corresponding relationship
            self.session.run('''MERGE (a:ngram {array:{startsubseq}})
            MERGE (b:ngram {array:{endsubseq}})
            MERGE (a)-[r:PRECEDES]->(b)
            ON CREATE SET r.count = {increment}
            ON MATCH SET r.count = r.count + {increment} RETURN r.count''', {"startsubseq": from_key, "endsubseq": to_key, "increment": count})

    def add_array(self, array):
        for (from_key, to_key, w) in self.list_transitions(array):
            # upsert for the starting and ending nodes and the corresponding relationship
            self.session.run('''MERGE (a:ngram {array:{startsubseq}})
            MERGE (b:ngram {array:{endsubseq}})
            MERGE (a)-[r:PRECEDES]->(b)
            ON CREATE SET r.count = {increment}
            ON MATCH SET r.count = r.count + {increment} RETURN r.count''', {"startsubseq": from_key, "endsubseq": to_key, "increment": w})

    def count_followers(self, elements):
        return self.session.run('MATCH (s:ngram {array:{fromsubseq}})-[r:PRECEDES]->(e:ngram) RETURN sum(r.count) as count',
                         {"fromsubseq": elements}).single()['count']

    def get_specific_follower(self, elements, index):
        return self.session.run('''MATCH (s:ngram {array:{fromsubseq}})-[r:PRECEDES]->(e:ngram)
RETURN reduce(partial={slack:{counter},found:''}, v IN collect({count:r.count,value:e.array})|
{slack:partial.slack - v.count,
found: CASE WHEN
(partial.slack>=0 AND v.count>partial.slack)
THEN v.value
ELSE partial.found
END
})''', {"fromsubseq": elements, "counter": index}).single()

    def continuation(self, elements):
        continuation_count = self.count_followers(elements)
        if continuation_count == 0:
            return None
        continue_index = continuation_count * random.random()
        return self.get_specific_follower(elements, continue_index).values()[0]['found']

    def enqueue_transition(self, transition):
        for (i,t) in enumerate(self.transitions_queue):
            if t[0:2] == transition[0:2]:
                self.transitions_queue[i] = (self.transitions_queue[i][0],
                                             self.transitions_queue[i][1],
                                             self.transitions_queue[i][2] + transition[2])
                return True
        self.transitions_queue.append(transition)
        return False

    def flush_queue(self):
        self.add_transitions(self.transitions_queue)
        self.transitions_queue = []

