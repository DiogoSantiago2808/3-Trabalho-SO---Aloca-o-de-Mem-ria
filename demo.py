from memory import Memory
from algorithms import FitAlg

def separator(name):
    print("\n" + "="*60)
    print(f" DEMO: {name}")
    print("="*60)

def scenario_basic_first_fit():
    separator("Cenário 1 — First Fit básico")
    mem = Memory(64)
    mem.alloc(10, FitAlg.FIRST)   # id 1
    mem.alloc(8, FitAlg.FIRST)    # id 2
    mem.free_id(2)
    mem.alloc(6, FitAlg.FIRST)    # id 3
    mem.show()
    mem.stats()

def scenario_best_fit_fragmentation():
    separator("Cenário 2 — Best Fit com fragmentação")
    mem = Memory(80)
    mem.alloc(20, FitAlg.BEST)  # 1
    mem.alloc(10, FitAlg.BEST)  # 2
    mem.alloc(15, FitAlg.BEST)  # 3
    mem.free_id(2)
    mem.free_id(1)
    mem.alloc(8, FitAlg.BEST)   # should fit in best spot
    mem.alloc(5, FitAlg.BEST)
    mem.show()
    mem.stats()

def scenario_worst_fit_expansion():
    separator("Cenário 3 — Worst Fit explorando maior buraco")
    mem = Memory(100)
    mem.alloc(10, FitAlg.WORST)
    mem.alloc(12, FitAlg.WORST)
    mem.alloc(7, FitAlg.WORST)
    mem.free_id(2)
    mem.alloc(8, FitAlg.WORST)
    mem.show()
    mem.stats()

def scenario_next_fit_behavior():
    separator("Cenário 4 — Next Fit comportamento")
    mem = Memory(60)
    mem.alloc(10, FitAlg.FIRST)   # id1 @0
    mem.alloc(12, FitAlg.FIRST)   # id2 @10
    mem.free_id(1)                # free @0
    mem.alloc(8, FitAlg.NEXT)     # next-fit should start from last_alloc_pos (12) -> allocate in the next available spot
    mem.show()
    mem.stats()

def scenario_stress():
    separator("Cenário 5 — Stress test automático")
    mem = Memory(200)
    import random
    random.seed(42)
    for _ in range(25):
        if random.random() < 0.6:
            size = random.randint(5, 30)
            alg = random.choice([FitAlg.FIRST, FitAlg.BEST, FitAlg.WORST, FitAlg.NEXT])
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
