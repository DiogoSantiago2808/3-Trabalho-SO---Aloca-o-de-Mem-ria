from memory import Memory
from algorithms import FitAlg


def separator(name):
    print("\n" + "=" * 60)
    print(f" DEMO: {name}")
    print("=" * 60)


def scenario_basic_first_fit():
    separator("Cenário 1 — First Fit com Buddy (fragmentação interna)")
    mem = Memory(64)

    mem.alloc(10, FitAlg.FIRST)   # pedido=10 → bloco=16
    mem.alloc(8, FitAlg.FIRST)    # pedido=8  → bloco=8
    mem.free_id(2)
    mem.alloc(6, FitAlg.FIRST)    # pedido=6  → bloco=8

    mem.show()
    mem.stats()


def scenario_best_fit_fragmentation():
    separator("Cenário 2 — Best Fit + Buddy")
    mem = Memory(80)  # será arredondado para 128 internamente

    mem.alloc(20, FitAlg.BEST)  # → 32
    mem.alloc(10, FitAlg.BEST)  # → 16
    mem.alloc(15, FitAlg.BEST)  # → 16
    mem.free_id(2)
    mem.free_id(1)

    mem.alloc(8, FitAlg.BEST)   # → 8
    mem.alloc(5, FitAlg.BEST)   # → 8

    mem.show()
    mem.stats()


def scenario_worst_fit_expansion():
    separator("Cenário 3 — Worst Fit com Buddy")
    mem = Memory(100)  # → 128

    mem.alloc(10, FitAlg.WORST)  # 16
    mem.alloc(12, FitAlg.WORST)  # 16
    mem.alloc(7, FitAlg.WORST)   # 8
    mem.free_id(2)
    mem.alloc(8, FitAlg.WORST)   # 8 (do maior bloco disponível)

    mem.show()
    mem.stats()


def scenario_next_fit_behavior():
    separator("Cenário 4 — Next Fit com Buddy")
    mem = Memory(64)

    mem.alloc(10, FitAlg.FIRST)   # id1 → 16 @0
    mem.alloc(12, FitAlg.FIRST)   # id2 → 16 @16
    mem.free_id(1)                # libera bloco @0

    # next-fit começa após last_alloc_pos (=16)
    mem.alloc(8, FitAlg.NEXT)     # deve ir após o último bloco alocado

    mem.show()
    mem.stats()


def scenario_stress():
    separator("Cenário 5 — Stress test (Buddy + Fits)")
    mem = Memory(200)  # → 256

    import random
    random.seed(42)

    for _ in range(25):
        if random.random() < 0.6:
            size = random.randint(5, 30)
            alg = random.choice([
                FitAlg.FIRST,
                FitAlg.BEST,
                FitAlg.WORST,
                FitAlg.NEXT
            ])
            mem.alloc(size, alg)
        else:
            used = [b for b in mem.blocks if b.used]
            if used:
                mem.free_id(random.choice(used).id)

    mem.show()
    mem.stats()


if __name__ == "__main__":
    scenario_basic_first_fit()
    scenario_best_fit_fragmentation()
    scenario_worst_fit_expansion()
    scenario_next_fit_behavior()
    scenario_stress()
