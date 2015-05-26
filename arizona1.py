#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pprint
from baseconv import BaseConverter
import operator


class arizona(object):
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.marks = {}
        self.pesos = {}
        self.longest_path = []

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

        digitos_diferentes = 0

        bsu = self.pad(bsu, len(bsv))

        for i in range(0, len(bsv) - 1):
            if bsu[-i] != bsv[-i]:
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
        if self.nodes[num] == []:
            base6 = BaseConverter('012345')
            num6 = base6.encode(n)
            self.nodes[num] = map(int, num6)
        return self.nodes[num]

    def create_nodes(self, file):
        """Lê um arquivo e cria um nodo para cada linha diferente"""
        with open(file) as f:
            for line in f:
                self.nodes[line.rstrip()] = []

    def create_edges(self):
        """A partir dos nodos, cria vértices que respeitem as regras"""
        for u in self.nodes:
            gen = [v for v in self.nodes if int(v) > int(u)]
            for v in gen:
                if self.compara(u, v):
                    # print "Aresta: %r(%r) -> %r(%r)" %(u, self.nodes[u], v, self.nodes[v])
                    self.edges[u + "," + v] = True


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
        lista = []
        if self.nodes.get(u, False):
            for v in self.nodes:
                # inverso de self.vizinhos!
                if self.existe_aresta(v, u):
                    lista.append(v)
        return lista


    def popula_tamanho_paths(self, u):
        """Popula o tamanho do maior caminho que liga a u"""
        # Olha os vizinhos que chegam em u
        # o tamanho de u é o maior tamanho deles, mais um
        v = self.pesos.get(u, 0)
        max = 0
        for viz in self.vizinhos_que_chegam(u):
            peso = self.pesos.get(viz, False)
            if not peso:
                self.pesos[viz] = self.popula_tamanho_paths(viz) + 1
            if peso > max:
                max = peso
        self.pesos[v] = max
        return max


    def encontra_maior_peso(self, pesos):
        print "pesos", pesos
        nodes = [self.nodes[str(p)] for p in pesos]
        return max(nodes.iteritems(), key=operator.itemgetter(1))[0]


    def calcula_longest_path(self):
        """Retorna o maior caminho do grafo"""
        for u in self.nodes:
            self.popula_tamanho_paths(u)

        maior_peso = self.encontra_maior_peso(self.pesos)
        print "(%r,%r)" % (maior_peso, self.pesos[maior_peso])
        self.longest_path = [self.nodes[maior_peso]]

        vizinhos = self.vizinhos_que_chegam(maior_peso)
        while len(vizinhos) > 0:
            maior_peso = self.encontra_maior_peso(vizinhos)
            print "(%r,%r)" % (maior_peso, self.pesos[maior_peso])
            self.longest_path = [self.nodes[maior_peso]] + self.longest_path
            vizinhos = self.vizinhos_que_chegam(maior_peso)

        return self.longest_path


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print "Uso: %s [arquivo]" % sys.argv[0]
        exit()
    pp = pprint.PrettyPrinter(indent=4)

    print "Arizona Jones entrou no templo"
    print "Lendo o arquivo %s" % sys.argv[1]
    a = arizona()
    a.create_nodes(sys.argv[1])

    # Force conversion of all nodes
    # for n in a.nodes:
    #    a.base6(n)

    print "Lidos os nodos"
    pp.pprint(a.nodes)

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

    #print "Arestas: "
    #pp.pprint(a.edges)

    #print "Populado:"
    #pp.pprint(a.pesos)
