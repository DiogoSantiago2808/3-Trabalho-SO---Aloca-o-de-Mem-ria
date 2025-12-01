from algorithms import choose_block, FitAlg
import math

class Block:
    def __init__(self, start, size, bid=None, used=False, requested_size=None):
        self.start = start            # posição inicial
        self.size = size              # tamanho do bloco físico
        self.id = bid                 # id se alocado
        self.used = used              # bool
        self.requested_size = requested_size  # tamanho pedido pelo usuário (se usado)

    def __repr__(self):
        return (f"<Block start={self.start} size={self.size} used={self.used} "
                f"id={self.id} req={self.requested_size}>")

class Memory:
    def __init__(self, size):
        if size <= 0:
            raise ValueError("size deve ser > 0")
        self.size = size
        # inicialmente um bloco livre que ocupa toda a memória
        self.blocks = [Block(0, size, None, False, None)]
        self.next_id = 1
        self.last_alloc_pos = 0  # usado por next-fit (start da última alocação)

    # ----------------- ALOCAÇÃO -----------------
    def alloc(self, req_size, alg: FitAlg):
        if req_size <= 0:
            print("Erro: tamanho de alocação deve ser > 0.")
            return None

        block = choose_block(self.blocks, req_size, alg, self.last_alloc_pos)
        if not block:
            print("Erro: memória insuficiente para alocar", req_size)
            return None

        # vamos substituir/inserir mantendo ordem por start
        self.blocks.sort(key=lambda b: b.start)
        idx = self.blocks.index(block)

        bid = self.next_id
        self.next_id += 1

        # se bloco é maior que pedido, dividir
        if block.size > req_size:
            allocated = Block(block.start, req_size, bid, True, req_size)
            remainder = Block(block.start + req_size, block.size - req_size, None, False, None)
            # substituir o bloco original por allocated + remainder
            self.blocks[idx:idx+1] = [allocated, remainder]
        else:
            # size == req_size
            block.used = True
            block.id = bid
            block.requested_size = req_size
            allocated = block

        # atualizar posição last_alloc_pos (para next-fit)
        self.last_alloc_pos = allocated.start

        print(f"Alocado: id={allocated.id} @ {allocated.start} +{allocated.size}B (pedido={allocated.requested_size}B) via {alg.name}")
        return allocated.id

    # ----------------- LIBERAÇÃO -----------------
    def free_id(self, bid):
        target = next((b for b in self.blocks if b.used and b.id == bid), None)
        if not target:
            print(f"Erro: bloco ID {bid} não encontrado.")
            return False
        target.used = False
        target.id = None
        target.requested_size = None
        self._coalesce()
        print(f"Bloco ID {bid} liberado.")
        return True

    def free_addr(self, addr):
        target = next((b for b in self.blocks if b.start == addr), None)
        if not target:
            print(f"Erro: não existe bloco com start={addr}.")
            return False
        if not target.used:
            print(f"Erro: bloco em {addr} já está livre.")
            return False
        bid = target.id
        target.used = False
        target.id = None
        target.requested_size = None
        self._coalesce()
        print(f"Bloco @ {addr} (id={bid}) liberado.")
        return True

    # ----------------- AUX -----------------
    def _normalize(self):
        self.blocks.sort(key=lambda b: b.start)

    def _coalesce(self):
        """Une blocos livres adjacentes"""
        self._normalize()
        i = 0
        while i < len(self.blocks) - 1:
            a = self.blocks[i]
            b = self.blocks[i+1]
            if (not a.used) and (not b.used) and (a.start + a.size == b.start):
                # funde
                a.size += b.size
                del self.blocks[i+1]
            else:
                i += 1

    # ----------------- SHOW (mapa visual compacto) -----------------
    def show(self, width: int = 80):
        """
        Exibe mapa visual compacto. Se self.size <= width, desenha 1 caractere por byte.
        Se self.size > width, compacta em 'width' segmentos.
        Linha 1: '#' para ocupado, '.' para livre (por segmento)
        Linha 2: ids (inteiros) ou '.' (por segmento)
        Depois, imprime a lista completa de blocos alocados com IDs completos.
        """
        if self.size <= width:
            # mapa por byte
            line1 = ["." for _ in range(self.size)]
            line2 = ["." for _ in range(self.size)]
            for b in self.blocks:
                if b.used:
                    for i in range(b.start, b.start + b.size):
                        line1[i] = "#"
                        line2[i] = str(b.id)
            print("Mapa de Memória (1 char = 1 byte)")
            print("-" * self.size)
            print("".join(line1))
            # segunda linha: mostrar ids; se id multi-dígito, fica largo - mas é preciso
            # vamos juntar com separador para que seja legível
            # em memórias pequenas isso é aceitável
            # para manter alinhamento visual simples, mostramos ids com espaço
            print(" ".join(line2))
            print("-" * self.size)
        else:
            # compacta em 'width' segmentos
            seg_count = width
            seg_size = math.ceil(self.size / seg_count)
            segs_occupied = []
            segs_id = []
            for s in range(seg_count):
                seg_start = s * seg_size
                seg_end = min(self.size, seg_start + seg_size)
                # verificar se existe algum byte ocupado no segmento
                occupied = False
                id_counts = {}
                for b in self.blocks:
                    # interseção entre [seg_start, seg_end) e [b.start, b.start+b.size)
                    if b.used and not (b.start + b.size <= seg_start or b.start >= seg_end):
                        occupied = True
                        id_counts[b.id] = id_counts.get(b.id, 0) + 1
                segs_occupied.append('#' if occupied else '.')
                if occupied:
                    # pegar id com maior presença no segmento
                    main_id = max(id_counts.items(), key=lambda t: t[1])[0]
                    segs_id.append(str(main_id))
                else:
                    segs_id.append('.')
            print(f"Mapa de Memória compacto (cada segmento ≈ {seg_size} bytes)")
            print("-" * seg_count)
            print("".join(segs_occupied))
            # para ids, imprimimos como sequência separada por espaço para legibilidade
            print(" ".join(segs_id))
            print("-" * seg_count)

        # Lista de blocos alocados (detalhada)
        ativos = [b for b in self.blocks if b.used]
        if ativos:
            print("\nBlocos ativos:")
            for b in ativos:
                print(f"[id={b.id}] @{b.start} +{b.size}B (pedido={b.requested_size}B)")
        else:
            print("\nNenhum bloco alocado.")

    # ----------------- STATS -----------------
    def stats(self):
        total_used = sum(b.size for b in self.blocks if b.used)
        total_free = sum(b.size for b in self.blocks if not b.used)
        holes = [b.size for b in self.blocks if not b.used]

        # fragmentacao externa = número de buracos
        frag_externa = len(holes)

        # fragmentacao interna = soma dos desperdicios por bloco alocado (size - requested_size)
        frag_interna = sum((b.size - (b.requested_size or 0)) for b in self.blocks if b.used)

        print("== Estatísticas ==")
        print(f"Tamanho total: {self.size} bytes")
        print(f"Ocupado (blocos físicos): {total_used} bytes | Livre: {total_free} bytes")
        print(f"Buracos (fragmentação externa): {frag_externa}")
        print(f"Fragmentação interna (desperdício): {frag_interna} bytes")
        uso_efetivo = (sum((b.requested_size or 0) for b in self.blocks if b.used) / self.size * 100) if self.size>0 else 0
        print(f"Uso efetivo (somatório pedidos / total): {uso_efetivo:.2f}%")
        return {
            "total": self.size,
            "used": total_used,
            "free": total_free,
            "holes": frag_externa,
            "internal_frag": frag_interna,
            "effective_usage_pct": uso_efetivo
        }
from algorithms import choose_block, FitAlg
import math

class Block:
    def __init__(self, start, size, bid=None, used=False, requested_size=None):
        self.start = start            # posição inicial
        self.size = size              # tamanho do bloco físico
        self.id = bid                 # id se alocado
        self.used = used              # bool
        self.requested_size = requested_size  # tamanho pedido pelo usuário (se usado)

    def __repr__(self):
        return (f"<Block start={self.start} size={self.size} used={self.used} "
                f"id={self.id} req={self.requested_size}>")

class Memory:
    def __init__(self, size):
        if size <= 0:
            raise ValueError("size deve ser > 0")
        self.size = size
        # inicialmente um bloco livre que ocupa toda a memória
        self.blocks = [Block(0, size, None, False, None)]
        self.next_id = 1
        self.last_alloc_pos = 0  # usado por next-fit (start da última alocação)

    # ----------------- ALOCAÇÃO -----------------
    def alloc(self, req_size, alg: FitAlg):
        if req_size <= 0:
            print("Erro: tamanho de alocação deve ser > 0.")
            return None

        block = choose_block(self.blocks, req_size, alg, self.last_alloc_pos)
        if not block:
            print("Erro: memória insuficiente para alocar", req_size)
            return None

        # vamos substituir/inserir mantendo ordem por start
        self.blocks.sort(key=lambda b: b.start)
        idx = self.blocks.index(block)

        bid = self.next_id
        self.next_id += 1

        # se bloco é maior que pedido, dividir
        if block.size > req_size:
            allocated = Block(block.start, req_size, bid, True, req_size)
            remainder = Block(block.start + req_size, block.size - req_size, None, False, None)
            # substituir o bloco original por allocated + remainder
            self.blocks[idx:idx+1] = [allocated, remainder]
        else:
            # size == req_size
            block.used = True
            block.id = bid
            block.requested_size = req_size
            allocated = block

        # atualizar posição last_alloc_pos (para next-fit)
        self.last_alloc_pos = allocated.start

        print(f"Alocado: id={allocated.id} @ {allocated.start} +{allocated.size}B (pedido={allocated.requested_size}B) via {alg.name}")
        return allocated.id

    # ----------------- LIBERAÇÃO -----------------
    def free_id(self, bid):
        target = next((b for b in self.blocks if b.used and b.id == bid), None)
        if not target:
            print(f"Erro: bloco ID {bid} não encontrado.")
            return False
        target.used = False
        target.id = None
        target.requested_size = None
        self._coalesce()
        print(f"Bloco ID {bid} liberado.")
        return True

    def free_addr(self, addr):
        target = next((b for b in self.blocks if b.start == addr), None)
        if not target:
            print(f"Erro: não existe bloco com start={addr}.")
            return False
        if not target.used:
            print(f"Erro: bloco em {addr} já está livre.")
            return False
        bid = target.id
        target.used = False
        target.id = None
        target.requested_size = None
        self._coalesce()
        print(f"Bloco @ {addr} (id={bid}) liberado.")
        return True

    # ----------------- AUX -----------------
    def _normalize(self):
        self.blocks.sort(key=lambda b: b.start)

    def _coalesce(self):
        """Une blocos livres adjacentes"""
        self._normalize()
        i = 0
        while i < len(self.blocks) - 1:
            a = self.blocks[i]
            b = self.blocks[i+1]
            if (not a.used) and (not b.used) and (a.start + a.size == b.start):
                # funde
                a.size += b.size
                del self.blocks[i+1]
            else:
                i += 1

    # ----------------- SHOW (mapa visual compacto) -----------------
    def show(self, width: int = 80):
        """
        Exibe mapa visual compacto. Se self.size <= width, desenha 1 caractere por byte.
        Se self.size > width, compacta em 'width' segmentos.
        Linha 1: '#' para ocupado, '.' para livre (por segmento)
        Linha 2: ids (inteiros) ou '.' (por segmento)
        Depois, imprime a lista completa de blocos alocados com IDs completos.
        """
        if self.size <= width:
            # mapa por byte
            line1 = ["." for _ in range(self.size)]
            line2 = ["." for _ in range(self.size)]
            for b in self.blocks:
                if b.used:
                    for i in range(b.start, b.start + b.size):
                        line1[i] = "#"
                        line2[i] = str(b.id)
            print("Mapa de Memória (1 char = 1 byte)")
            print("-" * self.size)
            print("".join(line1))
            # segunda linha: mostrar ids; se id multi-dígito, fica largo - mas é preciso
            # vamos juntar com separador para que seja legível
            # em memórias pequenas isso é aceitável
            # para manter alinhamento visual simples, mostramos ids com espaço
            print(" ".join(line2))
            print("-" * self.size)
        else:
            # compacta em 'width' segmentos
            seg_count = width
            seg_size = math.ceil(self.size / seg_count)
            segs_occupied = []
            segs_id = []
            for s in range(seg_count):
                seg_start = s * seg_size
                seg_end = min(self.size, seg_start + seg_size)
                # verificar se existe algum byte ocupado no segmento
                occupied = False
                id_counts = {}
                for b in self.blocks:
                    # interseção entre [seg_start, seg_end) e [b.start, b.start+b.size)
                    if b.used and not (b.start + b.size <= seg_start or b.start >= seg_end):
                        occupied = True
                        id_counts[b.id] = id_counts.get(b.id, 0) + 1
                segs_occupied.append('#' if occupied else '.')
                if occupied:
                    # pegar id com maior presença no segmento
                    main_id = max(id_counts.items(), key=lambda t: t[1])[0]
                    segs_id.append(str(main_id))
                else:
                    segs_id.append('.')
            print(f"Mapa de Memória compacto (cada segmento ≈ {seg_size} bytes)")
            print("-" * seg_count)
            print("".join(segs_occupied))
            # para ids, imprimimos como sequência separada por espaço para legibilidade
            print(" ".join(segs_id))
            print("-" * seg_count)

        # Lista de blocos alocados (detalhada)
        ativos = [b for b in self.blocks if b.used]
        if ativos:
            print("\nBlocos ativos:")
            for b in ativos:
                print(f"[id={b.id}] @{b.start} +{b.size}B (pedido={b.requested_size}B)")
        else:
            print("\nNenhum bloco alocado.")

    # ----------------- STATS -----------------
    def stats(self):
        total_used = sum(b.size for b in self.blocks if b.used)
        total_free = sum(b.size for b in self.blocks if not b.used)
        holes = [b.size for b in self.blocks if not b.used]

        # fragmentacao externa = número de buracos
        frag_externa = len(holes)

        # fragmentacao interna = soma dos desperdicios por bloco alocado (size - requested_size)
        frag_interna = sum((b.size - (b.requested_size or 0)) for b in self.blocks if b.used)

        print("== Estatísticas ==")
        print(f"Tamanho total: {self.size} bytes")
        print(f"Ocupado (blocos físicos): {total_used} bytes | Livre: {total_free} bytes")
        print(f"Buracos (fragmentação externa): {frag_externa}")
        print(f"Fragmentação interna (desperdício): {frag_interna} bytes")
        uso_efetivo = (sum((b.requested_size or 0) for b in self.blocks if b.used) / self.size * 100) if self.size>0 else 0
        print(f"Uso efetivo (somatório pedidos / total): {uso_efetivo:.2f}%")
        return {
            "total": self.size,
            "used": total_used,
            "free": total_free,
            "holes": frag_externa,
            "internal_frag": frag_interna,
            "effective_usage_pct": uso_efetivo
        }
