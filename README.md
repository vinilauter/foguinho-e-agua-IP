# Fireboy and Watergirl: python version

Projeto final da disciplina de introdução à programação: reprodução do jogo Fireboy and Watergirl em Python

Integrantes:
* Bruno Melo (bslm))
* Caique Machado (cmso)
* Joyce Gomes (jogg)
* Ricardo Lira (rcl4)
* Robson (rlcj)
* Vinicius Oliveira (vlfo)

### Dia 1 - lançamento do projeto (01/08/2025)

Considerando o prazo para o projeto e as opções disponíveis, os membros presentes na aula (Caíque, Ricardo e Vinicius) fizeram uma rápida troca de ideias e decidiram por fazer uma reprodução do jogo Fireboy and Watergirl, jogo muito presente na infância dos integrantes da equipe.

Mais tarde nesse dia, foi repassado ao restante da equipe um panorama geral do que foi decidido e as ferramentas a serem utilizadas para a execução do projeto

Foi estabelecido que as seguinte ferramentas serão empregadas:

* Canal de comunicação do time: WhatsApp e Discord
* Gerenciamento do conhecimento: README
* Gerenciamento das tarefas: Trello
* Repositório do código: GitHub
* Bibliotecas adicionais: Os, Sys, Pygame

### Dia 2 - primeira reunião e alinhamento de tarefas (02/08/2025)

Foi marcada e feita uma reunião às 14 horas pelo Discord, nela foram repassados os detalhes do que ocorreu no dia do lançamento do projeto. Também foi decidido que para melhor execução do projeto, foram criadas 5 grandes tarefas e cada membro vai se ocupar em fazer uma delas

Lista das tarefas:
* Criação dos personagens no código, membro responsável
* Arquitetura do nível, membro responsável
* Regras de vitória/derrota, a coleta de itens e a interface do usuário (HUD), membro responsável
* Mecânicas do jogo e física, membro responsável
* Loop principal do jogo e jogabilidade, membro responsável

Por fim, foi definido que até segunda feira (04/08), o responsável por cada tarefa irá subdividi-la em pequenas tarefas a fim de organizar melhor e manter prazos. 

### Dia 4 - primeiro checkpoint (04/08/2025)

No dia 4 de agosto foi incluído e devidamente integrado um novo membro à equipe, Bruno, este ficando responsável também pela parte de mecânicas do jogo e física.
Também houve o primeiro commit do arquivo Main, pouco antes do primeiro checkpoint com os monitores, no qual foram sanadas algumas dúvidas e feito o alinhamento geral com eles.

### Dia 5 - primeiras features e arquivo main (05/08/2025)

No dia 5 de agosto o membro Vinicius fez o commit das primeiras features parcialmente prontas, as alavancas com modularidade de cor e a gravidade aplicada aos personagens, o membro Robson também criou e fez várias otimizações no esqueleto do arquivo main, com a criação de diversos esboços de classes importantes para o jogo.

### Dia 6 - segundo checkpoint (06/08/2025)

No dia 6 de agosto foi feito um checkpoint presencial com a professora Fernanda Madeiral, foram alinhadas as expectativas e apresentado o projeto, com tudo correndo bem e a sinalização de que estamos no caminho certo.

### Dia 8 - terceiro checkpoint (08/08/2025)

No dia 8 de agosto foi feito um checkpoint com os monitores designados, atualizando-os das novas features em estágio de implementação e a explicação de como está sendo a estruturação do repositório em arquivos separados, no mais a maioria das features já foi esboçada e a equipe logo iniciará uma fase de integração e alinhamento para a inclusão correta de cada funcionalidade na main.

### Dia 11 - quarto checkpoint (11/08/2025) 

No dia 11 de agosto foi feito um checkpoint presencial com a professora Fernanda Madeiral, sendo dado um feedback muito positivo sobre o estado do jogo e seu funcionamento, com o jogo estando quase finalizado, faltando apenas alguns ajustes finos estéticos e de hitbox.

### Dia 13 - quinto checkpoint (13/08/2025)

No dia 13 de agosto pela manhã foi implementado um novo coletável de PowerUp de velocidade, sendo testado e aprovado. Também foram texturizadas as paredes do nível elevando o padrão estético do nível, foi marcado para 16h o checkpoint presencial para os monitores. No checkpoint tudo correu bem, sendo o projeto bastante elogiado e foram repassadas orientações para a finalização do relatório e confecção da apresentação.

### Divisão de tarefas
| Membro  | Tarefa |
| ------------- | ------------- |
| Bruno Melo | Botões, plataformas que movem com o acionamento dos botões, revisão de código |
| Caíque Machado | Personagens, gravidade e ajustes na main |
| Joyce Gomes  | Arquitetura do nível e texturas |
| Ricardo Lira  | HUD, contadores de coletáveis, gerenciamento de estados |
| Robson | Criação e integração do código à main e revisão de código |
| Vinicius Oliveira | Gerenciamento de equipe, alavancas, porta final, plataformas acionadas por alavancas e PowerUp |

### Bibliotecas utilizadas

* Pygame: Pygame foi a biblioteca escolhida por ser uma framework de código aberto para Python, projetada especificamente para o desenvolvimento de jogos 2D, o que simplificou a prototipagem rápida. Ela oferece um conjunto robusto de módulos para renderização de gráficos, gestão de sprites e deteção de colisões, que são essenciais para um jogo de plataforma. Adicionalmente, o Pygame permite um controle básico sobre o loop principal, a gestão de eventos e o tempo, garantindo a funcionalidade do projeto.
* Sys: A função sys.exit() foi utilizada para garantir o encerramento seguro e imediato da aplicação. No contexto do jogo, ela é chamada especificamente em resposta ao evento pygame.QUIT, que é acionado quando o utilizador clica no botão de fechar da janela. A sua utilização assegura que o loop principal do jogo é interrompido de forma limpa, prevenindo que o programa continue a rodar em segundo plano e liberando todos os recursos de sistema que estavam a ser utilizados.
* os: A biblioteca os foi empregada para interagir com o sistema operacional de maneira portátil, garantindo que o jogo funcione em diferentes plataformas como Windows, macOS e Linux. A sua função primária foi a manipulação de caminhos de arquivo, utilizando os.path.join() para construir de forma segura os caminhos para os recursos do jogo, como imagens.

# Organização do Código

O código é modularizado e dividido em vários arquivos separados que são importados de acordo com sua utilização na main ou em arquivos complementares

### Métodos

* **`__init__(self, x, y, cor, controles)`**
    * Construtor da classe. Inicializa o sprite do jogador em uma posição `(x, y)` específica, define sua `cor`, seus `controles` de teclado e configura todas as variáveis de física (gravidade, pulo) e de estado (velocidade, power-ups).

* **`update(self, teclas)`**
    * Chamado a cada frame. Verifica se o efeito do power-up de velocidade expirou. Lê o estado atual das `teclas` pressionadas para definir a velocidade horizontal do jogador e para iniciar a ação de pular.

* **`ativar_powerup_velocidade(self, duracao_ms)`**
    * Ativa o bônus de velocidade. Aumenta a `velocidade_atual` do jogador e define um temporizador para a `duração` do efeito.

* **`desativar_powerup_velocidade(self)`**
    * Restaura a velocidade normal. Chamado quando o tempo do power-up acaba, revertendo a `velocidade_atual` do jogador para o seu valor padrão.

* **`aplicar_gravidade(self)`**
    * Simula a gravidade. Aumenta a velocidade vertical (`vel_y`) do jogador a cada frame, criando o efeito de aceleração para baixo.

* **`checar_colisao(self, plataformas)`**
    * Método para a física e colisão. Move o jogador nos eixos X e Y separadamente, verificando colisões com a lista de `plataformas` a cada passo. Ajusta a posição do jogador para evitar que ele atravesse objetos e define a flag `pode_pular` como `True` quando ele está sobre uma superfície.

* **`desenhar(self, tela)`**
    * Renderiza o jogador. Método simples para desenhar a imagem (`self.image`) do jogador na `tela` na sua posição atual (`self.rect`).

# Conceitos utilizados

## 1. Programação Orientada a Objetos (POO)

> A POO é um paradigma de programação que organiza o código em "objetos". Cada objeto é criado a partir de uma "classe" (um molde) e possui seus próprios dados (atributos) e comportamentos (métodos). Isso torna o código mais organizado, reutilizável e fácil de manter.

### Aplicação no Projeto

Todo o projeto foi estruturado em torno da POO, onde cada elemento do jogo é uma classe.

* **Classes e Objetos**: Cada elemento interativo é uma classe. Por exemplo, a classe `Alavanca` define o que é uma alavanca (com seus atributos de estado, cooldown e hitboxes), e a classe `Jogador` define o comportamento de um personagem. No arquivo `nivel.py`, são criados os objetos (instâncias) específicos que aparecem na fase.

* **Herança**: Para evitar a repetição de código, foi usada a herança. As classes `Foguinho` e `Agua` são "filhas" da classe `Jogador`, herdando todos os seus métodos de física e movimento e adicionando apenas suas características únicas (imagem e tipo). O mesmo padrão é visto em `diamante.py`.

* **Encapsulamento**: Cada classe é responsável por gerenciar seu próprio estado interno. A classe `Cronometro`, por exemplo, controla o seu `tempo_inicial` e `tempo_decorrido` internamente. O loop principal do jogo só precisa chamar `cronometro.update()` e `cronometro.desenhar()`, sem se preocupar com os detalhes de como o tempo é calculado.

## 2. Funções

> Funções são blocos de código nomeados que realizam uma tarefa específica e podem ser chamados (executados) de várias partes do programa. Elas são a base para a reutilização de código e a organização lógica.

### Aplicação no Projeto

* **Função de Fabricação**: O melhor exemplo é a função `criar_primeiro_nivel()` no arquivo `nivel.py`. Sua única responsabilidade é criar todos os objetos e configurações de uma fase e retorná-los de forma organizada. Isso desacopla a definição do nível do motor principal do jogo.

* **Função de Inicialização**: Em `diamante.py`, a função `carregar_sprites_diamantes()` é usada para carregar as imagens dos diamantes uma única vez no início do jogo, uma tarefa de configuração importante.

* **Métodos como Funções**: Todos os métodos dentro das classes (como `update`, `toggle`, `checar_colisao`, etc.) são funções associadas a um objeto.

## 3. Estruturas Condicionais (`if`, `elif`, `else`)

> As estruturas condicionais permitem que o programa tome decisões e execute diferentes ações com base em certas condições serem verdadeiras ou falsas. Elas são o cérebro do programa.

### Aplicação no Projeto

* **Gerenciamento de Estado do Jogo**: Em `main.py`, a lógica principal dos métodos `atualizar()` e `desenhar()` é controlada por condicionais que verificam o estado atual do jogo (`if self.estado == JOGANDO:`).

* **Lógica de Gameplay**: A classe `Alavanca` usa uma condicional complexa em `check_colisao` para decidir se deve ativar ou desativar, baseando-se no estado atual (`if not self.ativada...`) e em qual lado o jogador colidiu (`...and jogador.rect.colliderect(self.rect_ativar)`).

* **Entrada do Jogador**: Em `jogador.py`, o método `update` usa `if teclas[...]` para verificar quais teclas de controle estão pressionadas e mover o personagem.

* **Interação entre Objetos**: Em `plataforma_vertical_alavanca.py`, o movimento da plataforma depende diretamente do estado da alavanca associada a ela (`if self.alavanca_designada.ativada:`).

## 4. Laços de Repetição (`for`)

> Laços de repetição são usados para executar o mesmo bloco de código várias vezes, geralmente para processar cada item de uma lista ou outra sequência.

### Aplicação no Projeto

* **Loop de Jogo e Eventos**: O coração do `main.py` é o loop de eventos (`for evento in pygame.event.get():`), que processa todas as ações do usuário, como fechar a janela ou pressionar teclas.

* **Atualização e Renderização**: Em `main.py`, laços `for` são usados extensivamente para passar por listas de objetos e chamar seus métodos de atualização e desenho (ex: `for jogador in [self.jogador1, self.jogador2]:`, `for diamante in self.diamantes:`).

* **Lógica de Colisão**: O método `checar_colisao` na classe `Jogador` usa um laço `for` para verificar a colisão contra cada plataforma na lista `plataformas`.

* **Animação**: A classe `Botao` em `nova_plataforma_movel.py` usa um laço `for i in range(5):` para carregar as diferentes imagens que compõem sua animação de pressionamento.

## 5. Dicionários

> Dicionários são estruturas de dados que armazenam informações no formato `chave: valor`. Eles são extremamente eficientes para recuperar um valor quando você conhece sua chave única.

### Aplicação no Projeto

* **Estrutura de Nível**: O uso de dicionários está em `nivel.py`. A função `criar_primeiro_nivel` retorna um grande dicionário onde as chaves são strings (`"jogador1"`, `"plataformas"`, `"powerups"`) e os valores são os objetos ou listas de objetos do jogo. Em `main.py`, o `__init__` da classe `Jogo` acessa esses valores para configurar a fase (ex: `self.jogador1 = nivel["jogador1"]`).

* **Configuração de Controles**: A classe `Jogador` recebe um dicionário de `controles` no `__init__`. Isso permite mapear ações (como `"esquerda"`) a teclas específicas (`pygame.K_a`), tornando a configuração dos controles flexível e fácil de entender.

# Desafios e aprendizados

* Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele?
  
  A divisão de tarefas foi um pouco mal formulada, principalmente porque não foi incluída a função de revisor de código, deixando tudo um pouco confuso e com as funções ao longo do projeto se misturando, isso foi contornado com a mescla de funções entre cada membro do grupo e alguns membros naturalmente revisando o código ao mesmo tempo em que faziam tarefas menores

* Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele?

  O uso do Git para versionamento de código em pouco tempo hábil para aprendizado. O desafio foi parcialmente contornado com os membros se adaptando à ferramenta, porém sem tanto emprego de boas práticas de código, como commit semântico e gitflow, porém a forte comunicação entre os membros do grupo favoreceu um desfecho favorável ante as adversidades.

* Quais as lições aprendidas durante o projeto?

  A importância de ter uma ideia clara de como fazer um projeto antes de começar a dividir tarefas e a prática de git foram grandes aprendizados do projeto que serão levados ao longo de toda a carreira profissional.
