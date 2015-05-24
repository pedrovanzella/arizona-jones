#!/usr/bin/env python


def compara(u, v):
    """Retorna True se v é maior que u e se entre u e v somente um dígito
    em base 6 é alterado"""
    if v < u:
        return False
    bsu = base6(u)
    bsv = base6(v)
    digitos_diferentes = 0
    for i, d in enumerate(bsu):
        if d != bsv[i]:
            digitos_diferentes += 1
        if digitos_diferentes > 1:
            break

    if digitos_diferentes > 1:
        return False
    return True


def base6(num):
    """Retorna uma representação em base 6 do número em um array"""
    n = int(num)
    return [0, 0, 0]  # TODO: actually make this work


if __name__ == "__main__":
    print "Arizona Jones entrou no templo"
