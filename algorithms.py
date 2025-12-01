from enum import Enum

class FitAlg(Enum):
    FIRST = 1
    BEST = 2
    WORST = 3
    NEXT = 4

def choose_block(blocks, size, alg: FitAlg, last_pos: int = 0):
    """
    Escolhe um bloco conforme o algoritmo, sem modificá-lo.
    - blocks: lista de Block (assume que podem estar desordenados)
    - size: tamanho pedido
    - alg: FitAlg
    - last_pos: para NEXT-fit, posição (start) a partir da qual procurar
    Retorna o bloco escolhido (objeto) ou None.
    """
    # Considera apenas blocos livres e suficientes
    candidates = [b for b in blocks if not b.used and b.size >= size]
    if not candidates:
        return None

    if alg == FitAlg.FIRST:
        # ordenar por start e pegar primeiro que cabe
        candidates.sort(key=lambda b: b.start)
        return candidates[0]

    if alg == FitAlg.BEST:
        return min(candidates, key=lambda b: b.size)

    if alg == FitAlg.WORST:
        return max(candidates, key=lambda b: b.size)

    if alg == FitAlg.NEXT:
        # NEXT-FIT: procurar a partir de last_pos (por start), dar wrap-around
        ordered = sorted(candidates, key=lambda b: b.start)
        # find first with start > last_pos
        for b in ordered:
            if b.start >= last_pos:
                return b
        # wrap-around: return first in ordered
        return ordered[0]

    return None
