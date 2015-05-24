#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pprint
from baseconv import BaseConverter


class arizona(object):
    def __init__(self):
        self.nodes = {}
        self.vertices = {}
        self.marks = {}

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
        for i, d in enumerate(bsu):
            if d != bsv[i]:
                digitos_diferentes += 1
            if digitos_diferentes > 1:
                break

        if digitos_diferentes > 1:
            return False
        return True

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

    def create_vertices(self):
        """A partir dos nodos, cria vértices que respeitem as regras"""
        for u in self.nodes:
            gen = [v for v in self.nodes if v > u]
            for v in gen:
                if self.compara(u, v):
                    self.vertices[u + "," + v] = True

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

    print "Lidos os nodos:"
    pp.pprint(a.nodes)

    a.create_vertices()
    print "Criados os vértices:"
    pp.pprint(a.vertices)
