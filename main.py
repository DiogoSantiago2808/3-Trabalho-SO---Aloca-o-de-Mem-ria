from memory import Memory
from algorithms import FitAlg

def parse_alg(s: str):
    s = s.strip().lower()
    if s == "first":
        return FitAlg.FIRST
    if s == "best":
        return FitAlg.BEST
    if s == "worst":
        return FitAlg.WORST
    if s == "next":
        return FitAlg.NEXT
    raise ValueError("Algoritmo desconhecido. Use first|best|worst|next")

def main():
    mem = None
    print("Simulador de Alocação de Memória (comandos: init, alloc, freeid, freeaddr, show, stats, exit)")
    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            break
        if not line:
            continue
        parts = line.split()
        cmd = parts[0]

        try:
            if cmd == "init":
                size = int(parts[1])
                mem = Memory(size)
                print(f"Memória inicializada com {size} bytes.")
            elif cmd == "alloc":
                if mem is None:
                    print("Erro: inicialize com init primeiro.")
                    continue
                size = int(parts[1])
                alg = parse_alg(parts[2])
                mem.alloc(size, alg)
            elif cmd == "freeid":
                if mem is None:
                    print("Erro: inicialize com init primeiro.")
                    continue
                mem.free_id(int(parts[1]))
            elif cmd == "freeaddr":
                if mem is None:
                    print("Erro: inicialize com init primeiro.")
                    continue
                mem.free_addr(int(parts[1]))
            elif cmd == "show":
                if mem is None:
                    print("Erro: inicialize com init primeiro.")
                    continue
                # opcional: permitir largura como segundo argumento
                if len(parts) >= 2:
                    w = int(parts[1])
                    mem.show(width=w)
                else:
                    mem.show()
            elif cmd == "stats":
                if mem is None:
                    print("Erro: inicialize com init primeiro.")
                    continue
                mem.stats()
            elif cmd == "exit":
                break
            else:
                print("Comando inválido.")
        except Exception as e:
            print("Erro ao processar comando:", e)

if __name__ == "__main__":
    main()
