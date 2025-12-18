from algorithms import choose_block, FitAlg
import math

# --------- FUNÇÕES AUXILIARES DO BUDDY ---------

# Calcula a próxima potência de dois maior ou igual a n
# Usada para ajustar o tamanho solicitado pelo usuário
def next_power_of_two(n):
    return 1 if n == 0 else 2 ** (n - 1).bit_length()


# Calcula o endereço inicial do bloco "buddy"
# No Buddy Allocator, o buddy é obtido com XOR entre
# o endereço inicial do bloco e o tamanho do bloco
def buddy_start(block):
    return block.start ^ block.size


# --------- BLOCO ---------

# Representa um bloco de memória
class Block:
    def __init__(self, start, size, bid=None, used=False, requested_size=None):
        self.start = start              # Endereço inicial do bloco
        self.size = size                # Tamanho físico (sempre potência de 2)
        self.id = bid                   # Identificador do bloco
        self.used = used                # Indica se o bloco está ocupado
        self.requested_size = requested_size  # Tamanho solicitado pelo usuário

    # Representação textual do bloco (útil para debug)
    def __repr__(self):
        return (f"<Block start={self.start} size={self.size} "
                f"used={self.used} id={self.id} req={self.requested_size}>")


# --------- MEMÓRIA ---------

# Classe responsável pelo gerenciamento da memória
class Memory:
    def __init__(self, size):
        if size <= 0:
            raise ValueError("size deve ser > 0")

        # Ajusta o tamanho total da memória para potência de 2
        self.size = next_power_of_two(size)

        # Lista de blocos de memória (inicia com um único bloco livre)
        self.blocks = [Block(0, self.size)]

        # Próximo ID a ser atribuído a um bloco alocado
        self.next_id = 1

        # Guarda a posição da última alocação (usado no Next Fit)
        self.last_alloc_pos = 0

    # ----------------- ALOCAÇÃO (BUDDY) -----------------

    # Aloca memória utilizando o Buddy Allocator
    # req_size: tamanho solicitado pelo usuário
    # alg: algoritmo de escolha de bloco (First, Best, Worst, Next)
    def alloc(self, req_size, alg: FitAlg):
        if req_size <= 0:
            print("Erro: tamanho inválido.")
            return None

        # Ajusta o tamanho solicitado para potência de dois
        real_size = next_power_of_two(req_size)

        # Escolhe um bloco livre conforme o algoritmo selecionado
        block = choose_block(self.blocks, real_size, alg, self.last_alloc_pos)
        if not block:
            print("Erro: memória insuficiente para alocar", req_size)
            return None

        # Divide recursivamente o bloco até atingir o tamanho necessário
        while block.size > real_size:
            half = block.size // 2
            left = Block(block.start, half)
            right = Block(block.start + half, half)

            self.blocks.remove(block)
            self.blocks.extend([left, right])

            # Continua a divisão sempre pelo bloco da esquerda
            block = left

        # Marca o bloco como ocupado
        block.used = True
        block.id = self.next_id
        block.requested_size = req_size

        # Atualiza o próximo ID e a posição da última alocação
        self.next_id += 1
        self.last_alloc_pos = block.start

        print(f"Alocado: id={block.id} @ {block.start} "
              f"+{block.size}B (pedido={req_size}B) via {alg.name}")

        return block.id

    # ----------------- LIBERAÇÃO -----------------

    # Libera um bloco a partir do seu identificador
    def free_id(self, bid):
        block = next((b for b in self.blocks if b.used and b.id == bid), None)
        if not block:
            print(f"Erro: bloco ID {bid} não encontrado.")
            return False

        # Marca o bloco como livre
        block.used = False
        block.id = None
        block.requested_size = None

        # Tenta unir blocos buddies livres
        self._coalesce()

        print(f"Bloco ID {bid} liberado.")
        return True

    # Libera um bloco a partir do endereço inicial
    def free_addr(self, addr):
        block = next((b for b in self.blocks if b.start == addr), None)
        if not block or not block.used:
            print("Erro: endereço inválido ou bloco já livre.")
            return False

        bid = block.id

        # Marca o bloco como livre
        block.used = False
        block.id = None
        block.requested_size = None

        # Realiza a coalescência
        self._coalesce()

        print(f"Bloco @ {addr} (id={bid}) liberado.")
        return True

    # ----------------- COALESCÊNCIA (BUDDY) -----------------

    # Une recursivamente blocos livres que sejam buddies
    def _coalesce(self):
        merged = True
        while merged:
            merged = False

            # Ordena os blocos por tamanho e endereço
            self.blocks.sort(key=lambda b: (b.size, b.start))

            for b in list(self.blocks):
                if b.used:
                    continue

                # Calcula o endereço do buddy
                buddy_addr = buddy_start(b)

                # Procura o bloco buddy correspondente
                buddy = next(
                    (x for x in self.blocks
                     if not x.used and x.size == b.size and x.start == buddy_addr),
                    None
                )

                # Se encontrar, une os dois blocos
                if buddy:
                    new_start = min(b.start, buddy.start)
                    self.blocks.remove(b)
                    self.blocks.remove(buddy)
                    self.blocks.append(Block(new_start, b.size * 2))
                    merged = True
                    break

    # ----------------- SHOW -----------------

    # Exibe o mapa visual da memória
    def show(self, width: int = 80):
        # Exibição detalhada (1 caractere por byte)
        if self.size <= width:
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
            print(" ".join(line2))
            print("-" * self.size)

        # Exibição compacta para memórias grandes
        else:
            seg_size = math.ceil(self.size / width)
            occ = []
            ids = []

            for i in range(width):
                start = i * seg_size
                end = min(self.size, start + seg_size)
                seg = [b for b in self.blocks if b.used and not
                       (b.start + b.size <= start or b.start >= end)]
                occ.append('#' if seg else '.')
                ids.append(str(seg[0].id) if seg else '.')

            print("Mapa de Memória compacto")
            print("-" * width)
            print("".join(occ))
            print(" ".join(ids))
            print("-" * width)

        # Lista os blocos atualmente alocados
        ativos = [b for b in self.blocks if b.used]
        if ativos:
            print("\nBlocos ativos:")
            for b in ativos:
                print(f"[id={b.id}] @{b.start} +{b.size}B (pedido={b.requested_size}B)")
        else:
            print("\nNenhum bloco alocado.")

    # ----------------- STATS -----------------

    # Exibe estatísticas detalhadas da memória
    def stats(self):
        used = sum(b.size for b in self.blocks if b.used)
        free = sum(b.size for b in self.blocks if not b.used)
        holes = len([b for b in self.blocks if not b.used])
        internal = sum(b.size - b.requested_size
                       for b in self.blocks if b.used)

        print("== Estatísticas ==")
        print(f"Tamanho total: {self.size} bytes")
        print(f"Ocupado: {used} | Livre: {free}")
        print(f"Buracos (fragmentação externa): {holes}")
        print(f"Fragmentação interna: {internal} bytes")

        uso = sum(b.requested_size for b in self.blocks if b.used) / self.size * 100
        print(f"Uso efetivo: {uso:.2f}%")
