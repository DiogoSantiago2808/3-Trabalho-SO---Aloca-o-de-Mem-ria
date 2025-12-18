from memory import Memory
from algorithms import FitAlg

# Converte a string informada pelo usuário no algoritmo de alocação correspondente
# Retorna um valor do enum FitAlg
def parse_alg(s: str):
    # Remove espaços extras e converte para minúsculo
    s = s.strip().lower()
    
    # Mapeia o texto digitado para o algoritmo correto
    if s == "first":
        return FitAlg.FIRST
    if s == "best":
        return FitAlg.BEST
    if s == "worst":
        return FitAlg.WORST
    if s == "next":
        return FitAlg.NEXT
    
    # Caso o algoritmo não seja reconhecido
    raise ValueError("Algoritmo desconhecido. Use first|best|worst|next")


# Função principal do programa
# Responsável por controlar o loop de interação com o usuário
def main():
    # Referência para o objeto de memória (inicialmente inexistente)
    mem = None

    # Mensagem inicial com os comandos disponíveis
    print("Simulador de Alocação de Memória (comandos: init, alloc, freeid, freeaddr, show, stats, exit)")
    
    # Loop principal da interface em linha de comando
    while True:
        try:
            # Lê o comando digitado pelo usuário
            line = input("> ").strip()
        except EOFError:
            # Encerra o programa caso não haja mais entrada
            break
        
        # Ignora linhas vazias
        if not line:
            continue
        
        # Divide o comando em partes (comando + argumentos)
        parts = line.split()
        cmd = parts[0]

        try:
            # Inicializa a memória com o tamanho informado
            if cmd == "init":
                size = int(parts[1])
                mem = Memory(size)
                print(f"Memória inicializada com {size} bytes.")

            # Aloca um bloco de memória usando o algoritmo escolhido
            elif cmd == "alloc":
                if mem is None:
                    print("Erro: inicialize com init primeiro.")
                    continue
                size = int(parts[1])
                alg = parse_alg(parts[2])
                mem.alloc(size, alg)

            # Libera um bloco de memória a partir do identificador
            elif cmd == "freeid":
                if mem is None:
                    print("Erro: inicialize com init primeiro.")
                    continue
                mem.free_id(int(parts[1]))

            # Libera um bloco de memória a partir do endereço inicial
            elif cmd == "freeaddr":
                if mem is None:
                    print("Erro: inicialize com init primeiro.")
                    continue
                mem.free_addr(int(parts[1]))

            # Exibe o mapa visual da memória
            elif cmd == "show":
                if mem is None:
                    print("Erro: inicialize com init primeiro.")
                    continue
                # Permite definir a largura do mapa, se informada
                if len(parts) >= 2:
                    w = int(parts[1])
                    mem.show(width=w)
                else:
                    mem.show()

            # Exibe estatísticas detalhadas de uso da memória
            elif cmd == "stats":
                if mem is None:
                    print("Erro: inicialize com init primeiro.")
                    continue
                mem.stats()

            # Encerra o programa
            elif cmd == "exit":
                break

            # Trata comandos inválidos
            else:
                print("Comando inválido.")

        # Captura erros de execução e exibe mensagem amigável
        except Exception as e:
            print("Erro ao processar comando:", e)


# Ponto de entrada do programa
# Garante que o main() só seja executado quando o arquivo for executado diretamente
if __name__ == "__main__":
    main()
