#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pprint
from baseconv import BaseConverter
import operator
import pygraphviz as pgv


class arizona(object):
    def __init__(self, make_graph=False):
        self.nodes = {}
        self.edges = {}
        self.marks = {}
        self.pesos = {}
        self.longest_path = []
        self.make_graph = make_graph
        if self.make_graph:
            self.graph = pgv.AGraph(directed=True)

    def clear_marks(self):
        for mark in self.marks:
            mark = False

    def compara(self, u, v):
        """Retorna True se v é maior que u e se entre u e v somente um dígito
        em base 6 é alterado"""
        if int(v) < int(u):
            return False
        bsu = self.base6(u)
        bsv = self.base6(v)

        if len(bsu) != len(bsv):
            # Não posso adicionar nem remover dígitos
            return False

        digitos_diferentes = 0

        for i in range(0, len(bsv)):
            if bsu[i] != bsv[i]:
                digitos_diferentes += 1
            if digitos_diferentes > 1:
                return False

        return True

    def pad(self, n, size):
        while len(n) < size:
            n = [0] + n

        return n

    def base6(self, num):
        """Retorna uma representação em base 6 do número em um array"""
        n = int(num)
        base6 = BaseConverter('012345')
        return base6.encode(n)

    def create_nodes(self, file):
        """Lê um arquivo e cria um nodo para cada linha diferente"""
        with open(file) as f:
            for line in f:
                l = line.rstrip()
                self.nodes[l] = self.base6(l)
                self.pesos[l] = 0
                if self.make_graph:
                    self.graph.add_node(l)

    def create_edges(self):
        """A partir dos nodos, cria vértices que respeitem as regras"""
        for u in self.nodes:
            gen = [v for v in self.nodes if int(v) > int(u)]
            for v in gen:
                if self.compara(u, v):
                    # print "Aresta: %r(%r) -> %r(%r)" %(u, self.nodes[u], v, self.nodes[v])
                    self.edges[u + "," + v] = True
                    if self.make_graph:
                        self.graph.add_edge(u, v)


    def vizinhos(self, u):
        """Retorna uma lista de vizinhos de um nodo"""
        viz = []
        if self.nodes[u]:
            for v in self.nodes:
                if self.existe_aresta(u, v):
                    viz.append(v)
        return viz


    def caminha(self, u):
        """Caminha no grafo a partir de um nodo u
        IMPORTANTE: Retorna todo mundo, não só um caminho
        ANTA"""
        path = []
        self.clear_marks()
        self.marks[u] = True
        l = [u]

        while len(l) > 0:
            u = l.pop(0)
            path.append((u, self.nodes[u]))
            for v in self.vizinhos(u):
                if not self.marked(v):
                    self.marks[v] = True
                    l = [v] + l

        return path


    def existe_aresta(self, u, v):
        return self.edges.get(u + "," + v, False) != False

    def marked(self, u):
        return self.marks.get(u, False)


    def vizinhos_que_chegam(self, u):
        """Retorna uma lista de todos os nodos que chegam em u"""
        return {k: v for k, v in self.nodes.iteritems() if self.existe_aresta(k, u)}

    def popula_tamanho_paths(self, u):
        """Popula o tamanho do maior caminho que liga a u"""
        # Olha os vizinhos que chegam em u
        # o tamanho de u é o maior tamanho deles, mais um
        for v in self.vizinhos_que_chegam(u):
            if self.pesos.get(v) == 0:
                self.pesos[v] = self.popula_tamanho_paths(v) + 1
            if self.pesos[v] > self.pesos[u]:
                self.pesos[u] = self.pesos[v] + 1

        return self.pesos[u]


    def encontra_maior_peso(self, pesos):
        return max(pesos.iteritems(), key=operator.itemgetter(1))[0]


    def calcula_longest_path(self):
        """Retorna o maior caminho do grafo"""
        for u in self.nodes:
            self.popula_tamanho_paths(u)

        maior_peso = self.encontra_maior_peso(self.pesos)
        # print "(%r,%r)" % (maior_peso, self.pesos[maior_peso])
        #self.longest_path = [(maior_peso, self.nodes[maior_peso])]
        self.longest_path = [maior_peso]

        vizinhos = self.vizinhos_que_chegam(maior_peso)
        while len(vizinhos) > 0:
            maior_peso = self.encontra_maior_peso(vizinhos)
            # print "(%r,%r)" % (maior_peso, self.pesos[maior_peso])
            #self.longest_path = [(maior_peso, self.nodes[maior_peso])] + self.longest_path
            self.longest_path = [maior_peso] + self.longest_path
            vizinhos = self.vizinhos_que_chegam(maior_peso)

        return self.longest_path


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print "Uso: %s [arquivo]" % sys.argv[0]
        exit()
    pp = pprint.PrettyPrinter(indent=4)

    print "Arizona Jones entrou no templo"
    print "Lendo o arquivo %s" % sys.argv[1]
    a = arizona(make_graph=True)
    #a = arizona()
    a.create_nodes(sys.argv[1])

    # Force conversion of all nodes
    # for n in a.nodes:
    #    a.base6(n)

    print "Lidos os nodos"
    # pp.pprint(a.nodes)
    # pp.pprint(a.pesos)

    a.create_edges()
    print "Criadas as arestas"
    # pp.pprint(a.edges)

    # for u in a.nodes:
    #     print "Os vizinhos de %s são:" % u
    #     pp.pprint(a.vizinhos(u))

    # for u in a.nodes:
    #     print "Caminhando a partir de %s:" % u
    #     pp.pprint(a.caminha(u))


    print "O maior caminho é:"
    pp.pprint(a.calcula_longest_path())
    print "E seu tamanho é: %d" % len(a.longest_path)

    # print "Arestas: "
    # pp.pprint(a.edges)

    # print "Populado:"
    # pp.pprint(a.pesos)
    #print "Imprimindo grafo"
    #a.graph.write("docs/" + sys.argv[1] + ".dot")
