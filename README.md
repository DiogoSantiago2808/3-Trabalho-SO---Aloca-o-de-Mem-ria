# 🧠 Simulador de Alocação de Memória

## 📚 Disciplina

**Sistemas Operacionais**

---

O desenvolvimento do projeto foi realizado de forma colaborativa, com divisão de responsabilidades entre os membros do grupo, conforme descrito abaixo:

Diego Rabelo de Sá
Responsável pelo estudo teórico dos algoritmos de alocação de memória e pelo apoio na definição da arquitetura geral do simulador.

Diogo Santiago Oliveira
Responsável pela implementação dos algoritmos de escolha de blocos (First Fit, Best Fit, Worst Fit e Next Fit) no módulo algorithms.py.

Ernesto Dalva de Medeiros
Responsável pela implementação da lógica principal de gerenciamento de memória, incluindo a estrutura de blocos e a aplicação da técnica do Buddy Allocator no módulo memory.py.

July Santiago Coelho
Responsável pelo desenvolvimento da interface interativa em linha de comando (main.py) e pela validação dos comandos do usuário.

Ramon Nicolas Gomes Luna
Responsável pela criação dos cenários automáticos de teste (demo.py), pela validação dos resultados e pelo apoio na documentação do projeto.

Essa divisão permitiu melhor organização do desenvolvimento, facilitando testes, manutenção do código e integração das funcionalidades.

## 🎯 Objetivo do Projeto

Este projeto implementa um simulador de gerência de memória que representa, de forma didática, o funcionamento interno de um sistema operacional no processo de alocação e liberação de memória.

O simulador permite analisar o comportamento de diferentes algoritmos clássicos de escolha de blocos:

- First Fit
- Best Fit
- Worst Fit
- Next Fit (extensão adicional)

A gerência da memória é realizada utilizando a técnica do **Buddy Allocator**, na qual os blocos de memória possuem tamanhos em potências de dois, permitindo uma coalescência eficiente e a visualização clara da fragmentação interna e externa.

Além disso, o sistema exibe mapas visuais da memória, identificadores de blocos alocados e estatísticas detalhadas, conforme solicitado na atividade prática.

---

## 📁 Estrutura do Projeto

```
.
├── algorithms.py   # Algoritmos de escolha de blocos (First, Best, Worst, Next)
├── memory.py       # Gerência de memória com Buddy Allocator
├── main.py         # Interface interativa (CLI)
├── demo.py         # Cenários automáticos de teste
├── utils.py        # Funções utilitárias
├── README.md       # Documentação do projeto
```

---

## 🧩 Descrição dos Módulos

### 🔹 `algorithms.py`

Responsável exclusivamente pela escolha do bloco livre conforme o algoritmo selecionado.

- Enum `FitAlg` define os algoritmos disponíveis:

  - `FIRST`
  - `BEST`
  - `WORST`
  - `NEXT`

- Função `choose_block(...)`:

  - Recebe a lista de blocos livres
  - Seleciona um bloco que comporte o tamanho solicitado
  - Não modifica a memória
  - Funciona de forma independente da técnica de alocação interna

Implementações:

- **First Fit**: seleciona o primeiro bloco livre que comporta o pedido
- **Best Fit**: seleciona o menor bloco livre possível
- **Worst Fit**: seleciona o maior bloco livre disponível
- **Next Fit**: continua a busca a partir da última posição alocada (com wrap-around)

---

### 🔹 `memory.py`

Contém a lógica principal da simulação, incluindo a implementação do Buddy Allocator.

#### 📦 Classe `Block`

Representa um bloco de memória, contendo:

- Endereço inicial (`start`)
- Tamanho físico do bloco (`size`) — sempre potência de 2
- Identificador do bloco (`id`)
- Estado (`used`)
- Tamanho solicitado pelo usuário (`requested_size`)

Essa separação permite o cálculo correto da fragmentação interna.

---

#### 🧠 Classe `Memory`

Responsável por:

- Inicializar a memória total (ajustada para potência de dois)
- Alocar blocos utilizando **Buddy Allocator**
- Liberar blocos e realizar **coalescência entre buddies**
- Exibir mapas visuais da memória
- Calcular estatísticas detalhadas

Principais métodos:

- `alloc(size, alg)`
- `free_id(id)`
- `free_addr(addr)`
- `show()`
- `stats()`

##### 🧩 Buddy Allocator

A técnica do Buddy Allocator funciona da seguinte forma:

- O tamanho solicitado é arredondado para a próxima potência de dois
- Blocos livres são divididos recursivamente até atingir o menor tamanho possível
- Apenas blocos irmãos (buddies) podem ser unidos durante a coalescência
- Essa abordagem reduz a fragmentação externa, ao custo de fragmentação interna controlada

---

### 🔹 `main.py` — Interface Interativa (CLI)

Permite o uso do simulador via linha de comando.

#### Comandos disponíveis:

```
init <tamanho>
alloc <tamanho> <first|best|worst|next>
freeid <id>
freeaddr <endereco>
show [largura]
stats
exit
```

#### Exemplo de uso:

```
> init 64
> alloc 10 first
> alloc 8 first
> freeid 2
> alloc 6 best
> show
> stats
```

---

### 🔹 `demo.py` — Cenários Automáticos

Executa cenários pré-definidos para demonstrar o comportamento dos algoritmos de escolha de blocos em conjunto com o Buddy Allocator:

1. First Fit com fragmentação interna
2. Best Fit com divisão e coalescência de buddies
3. Worst Fit explorando o maior bloco disponível
4. Comportamento do Next Fit
5. Stress test com alocações e liberações aleatórias

Ideal para avaliação e demonstração rápida do funcionamento do simulador.

---

### 🔹 `utils.py`

Arquivo de apoio com funções utilitárias simples, como cálculo de potência de dois e controle de valores.

---

## ▶️ Como Executar o Projeto

### 🔸 Execução Interativa (CLI)

```bash
python main.py
```

### 🔸 Execução dos Cenários de Teste

```bash
python demo.py
```

---

## 📊 Visualização e Estatísticas

O método `show()` exibe:

- Mapa de memória com:

  - `#` → bloco ocupado
  - `.` → bloco livre

- Identificadores dos blocos
- Lista detalhada dos blocos ativos

O método `stats()` exibe:

- Memória total
- Memória ocupada e livre
- Fragmentação externa (número de buracos)
- Fragmentação interna (desperdício devido ao Buddy Allocator)
- Uso efetivo da memória (%)

---

## ⚠️ Desafios Encontrados na Implementação

### 🔹 Implementação do Buddy Allocator

Foi necessário garantir que todos os blocos possuíssem tamanhos em potência de dois, além de implementar corretamente a divisão recursiva e a coalescência apenas entre blocos irmãos.

### 🔹 Coalescência de Blocos

A junção de blocos livres exigiu o uso de regras específicas do Buddy Allocator para evitar fusões inválidas.

### 🔹 Fragmentação Interna

A distinção entre tamanho físico do bloco e tamanho solicitado pelo usuário foi essencial para calcular corretamente o desperdício de memória.

---

## ✅ Conclusão

O simulador atende aos requisitos da atividade prática, permitindo:

- Comparação entre algoritmos clássicos de escolha de blocos
- Demonstração prática do funcionamento do Buddy Allocator
- Visualização clara da fragmentação interna e externa
- Análise didática do uso da memória em sistemas operacionais
