from enum import Enum

class FitAlg(Enum):
    FIRST = 1
    BEST = 2
    WORST = 3
    NEXT = 4


def choose_block(blocks, size, alg: FitAlg, last_pos: int = 0):
    """
    Escolhe um bloco livre conforme o algoritmo de alocação.
    
    - blocks: lista de Block
    - size: tamanho mínimo do bloco (já ajustado pelo Buddy, potência de 2)
    - alg: FitAlg
    - last_pos: usado apenas no NEXT-FIT
    Retorna o bloco escolhido ou None.
    """

    # apenas blocos livres e suficientemente grandes
    candidates = [b for b in blocks if not b.used and b.size >= size]
    if not candidates:
        return None

    if alg == FitAlg.FIRST:
        candidates.sort(key=lambda b: b.start)
        return candidates[0]

    if alg == FitAlg.BEST:
        return min(candidates, key=lambda b: b.size)

    if alg == FitAlg.WORST:
        return max(candidates, key=lambda b: b.size)

    if alg == FitAlg.NEXT:
        ordered = sorted(candidates, key=lambda b: b.start)
        for b in ordered:
            if b.start >= last_pos:
                return b
        return ordered[0]  # wrap-around

    return None
