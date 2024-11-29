import discord
from discord.ext import commands
import asyncio
import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('quiz_ci.db')
c = conn.cursor()

# Recriar a tabela de perguntas (removendo a antiga, se existir)
c.execute('''CREATE TABLE IF NOT EXISTS perguntas (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             pergunta TEXT,
             opcao_a TEXT,
             opcao_b TEXT,
             opcao_c TEXT,
             opcao_d TEXT,
             resposta TEXT,
             dificuldade TEXT
             )''')

# Criar a tabela de pontuações
c.execute('''CREATE TABLE IF NOT EXISTS pontuacoes (
             usuario_id TEXT PRIMARY KEY,
             pontos INTEGER
             )''')
conn.commit()

# Inserir as 50 questões sobre Ciência da Computação
questoes = [
    ("O que é um algoritmo?", "Conjunto de dados", "Conjunto de instruções", "Conjunto de variáveis", "Conjunto de funções", "B", "fácil"),
    ("Qual linguagem de programação é mais utilizada no desenvolvimento web?", "Python", "Java", "JavaScript", "C++", "C", "fácil"),
    ("O que é uma variável em programação?", "Uma função", "Um tipo de dado", "Uma estrutura de controle", "Uma referência para armazenar um valor", "D", "fácil"),
    ("O que significa a sigla 'HTTP'?", "HyperText Transfer Protocol", "HighText Transfer Protocol", "HyperText Test Protocol", "HighText Test Protocol", "A", "fácil"),
    ("Qual é a principal função de um sistema operacional?", "Controlar dispositivos de entrada", "Gerenciar recursos de hardware e software", "Executar programas em segundo plano", "Conectar redes de computadores", "B", "fácil"),
    ("O que é 'big data'?", "Armazenamento de grandes quantidades de dados", "Uma tecnologia de banco de dados", "Uma ferramenta de compressão de dados", "Uma linguagem de programação", "A", "médio"),
    ("O que é 'machine learning'?", "Processamento de textos", "Aprendizado automático de máquinas", "Gerenciamento de redes", "Desenvolvimento de jogos", "B", "médio"),
    ("Qual é o conceito de 'nuvem' em computação?", "Armazenamento de dados no computador local", "Armazenamento de dados na web", "Uma técnica de programação", "Uma tecnologia de segurança", "B", "médio"),
    ("O que é um banco de dados relacional?", "Um banco de dados que armazena dados em formato de texto", "Um banco de dados que armazena dados em tabelas com relações", "Um banco de dados que armazena dados de maneira hierárquica", "Um banco de dados semestral", "B", "médio"),
    ("O que é um sistema de gerenciamento de banco de dados (SGBD)?", "Um software para criptografar dados", "Um software para gerenciar redes", "Um software para gerenciar e organizar dados em bancos de dados", "Um software para programação de sites", "C", "médio"),
    ("O que é a computação em nuvem?", "Armazenamento de arquivos no disco rígido", "Processamento de dados em servidores remotos via internet", "Processamento de dados exclusivamente no local", "Armazenamento de dados no celular", "B", "médio"),
    ("O que é um servidor web?", "Um dispositivo de armazenamento de dados", "Um software que processa e entrega páginas da web", "Uma rede de computadores", "Uma linguagem de programação", "B", "médio"),
    ("O que significa a sigla 'SQL'?", "Structured Query Language", "Simple Query Language", "System Query Language", "Standard Query Language", "A", "médio"),
    ("O que é o protocolo TCP/IP?", "Protocolo de segurança", "Protocolo de controle de tráfego", "Protocolo de comunicação entre dispositivos", "Protocolo de busca de dados", "C", "médio"),
    ("O que é a arquitetura cliente-servidor?", "Uma arquitetura onde o cliente e o servidor são a mesma máquina", "Uma arquitetura de rede onde os clientes solicitam serviços a servidores", "Uma arquitetura que armazena dados localmente", "Uma arquitetura de redes de computadores sem clientes", "B", "médio"),
    ("O que é a virtualização?", "Técnica para criar várias instâncias de hardware em uma única máquina física", "Tecnologia para criptografar dados", "Tecnologia para conectar dispositivos", "Técnica para armazenar dados em várias nuvens", "A", "difícil"),
    ("O que é a linguagem Python?", "Uma linguagem de baixo nível", "Uma linguagem de alto nível", "Uma linguagem de machine learning", "Uma linguagem de banco de dados", "B", "fácil"),
    ("Qual é a função do compilador?", "Executar código em tempo de execução", "Converter código fonte em código de máquina", "Interpretar código linha por linha", "Gerenciar recursos de hardware", "B", "fácil"),
    ("O que é um código-fonte?", "Um código de criptografia", "O código de programação gerado por um compilador", "O código escrito pelo programador em uma linguagem de programação", "O código utilizado para otimizar a execução do programa", "C", "fácil"),
    ("O que significa a sigla 'RAM'?", "Read Access Memory", "Random Access Memory", "Rapid Access Memory", "Ready Access Memory", "B", "fácil"),
    ("Qual a função de um firewall?", "Proteger sistemas contra vírus", "Proteger a rede contra acessos não autorizados", "Garantir o bom funcionamento do servidor", "Gerenciar banco de dados", "B", "fácil"),
    ("O que é a 'engenharia de software'?", "A construção física de computadores", "A prática de projetar e criar software de alta qualidade", "A criação de algoritmos de inteligência artificial", "A manutenção de servidores de rede", "B", "médio"),
    ("O que é um sistema embarcado?", "Um sistema com software embarcado em hardware específico", "Um sistema de gerenciamento de banco de dados", "Um sistema de segurança", "Um sistema de rede", "A", "médio"),
    ("O que é 'cryptojacking'?", "Técnica de criptografar dados pessoais", "Ataque cibernético usando criptografia para roubo de dados", "Uso de recursos de computador para minerar criptomoedas sem permissão", "Uma tecnologia de compressão de dados", "C", "difícil"),
    ("O que é o sistema operacional Linux?", "Um sistema operacional baseado em código aberto", "Um sistema operacional proprietário", "Um sistema de gerenciamento de banco de dados", "Um sistema operacional exclusivo para servidores", "A", "fácil"),
    ("Qual linguagem de programação foi criada por Guido van Rossum?", "Java", "C#", "Python", "Ruby", "C", "fácil"),
    ("Qual é a principal característica da arquitetura de von Neumann?", "Uso de memória separada para dados e instruções", "Uso de uma única memória para dados e instruções", "Processamento paralelo de dados", "Armazenamento de dados de forma distribuída", "B", "médio"),
    ("O que é um protocolo de rede?", "Um conjunto de regras para transferência de dados", "Uma técnica de armazenamento de dados", "Um programa de segurança de rede", "Uma ferramenta para programação de servidores", "A", "médio"),
    ("O que é a programação orientada a objetos?", "Uma técnica para melhorar a velocidade do código", "Um paradigma de programação baseado em objetos e classes", "Uma técnica para criptografar dados", "Uma técnica de gerenciamento de redes", "B", "médio"),
    ("O que é um hash?", "Uma função de criptografia", "Uma função que mapeia dados de entrada para uma saída de tamanho fixo", "Uma técnica de compressão de dados", "Uma estrutura de dados", "B", "médio"),
    ("O que significa a sigla 'API'?", "Application Programming Interface", "Advanced Programming Interface", "Application Performance Interface", "Automated Programming Interface", "A", "fácil"),
    ("Qual é a principal diferença entre compilador e interpretador?", "O compilador executa o código linha por linha, o interpretador converte o código inteiro", "O compilador converte o código inteiro, o interpretador executa linha por linha", "Não há diferença", "O interpretador é mais rápido", "B", "fácil"),
    ("O que é 'Cloud Computing'?", "Armazenamento de dados em nuvem", "Computação baseada em servidores locais", "Computação sem a necessidade de internet", "Tecnologia para criar aplicativos móveis", "A", "fácil"),
    ("O que é a arquitetura 'RISC'?", "Uma arquitetura de processador com instruções complexas", "Uma arquitetura de processador com instruções simples e rápidas", "Uma arquitetura de rede", "Uma arquitetura de banco de dados", "B", "médio"),
    ("Qual é o conceito de 'agilidade' no desenvolvimento de software?", "Desenvolver software sem planejamento", "Desenvolver software sem documentação", "Desenvolver software de forma iterativa e incremental", "Desenvolver software sem testes", "C", "médio"),
    ("O que é um 'loop'?", "Uma função recursiva", "Uma estrutura que repete um conjunto de instruções", "Uma instrução condicional", "Uma estrutura de dados", "B", "fácil"),
    ("O que significa a sigla 'DNS'?", "Domain Name System", "Dynamic Network Service", "Data Name Server", "Domain Network Service", "A", "fácil"),
    ("O que é a 'criptografia simétrica'?", "Técnica de criptografar dados com uma chave secreta compartilhada", "Técnica de criptografar dados com chaves públicas", "Técnica de criptografar dados usando apenas números", "Técnica de criptografar dados sem chave", "A", "médio"),
    ("O que é o protocolo de segurança SSL?", "Protocolo de autenticação", "Protocolo para transferência de arquivos", "Protocolo de segurança para criptografar dados em transações na web", "Protocolo de comunicação de e-mails", "C", "médio"),
    ("O que significa a sigla 'URL'?", "Uniform Resource Locator", "Unified Resource Locator", "Universal Resource Locator", "Uniformal Resource Locator", "A", "fácil"),
    ("Qual é a principal função do 'Git'?", "Armazenamento de dados", "Controle de versões de código-fonte", "Programação de servidores", "Armazenamento de imagens", "B", "fácil"),
    ("O que é 'DevOps'?", "Uma metodologia para desenvolvimento de software e operações", "Uma metodologia para desenvolvimento de jogos", "Uma técnica de criptografia", "Uma linguagem de programação", "A", "médio"),
    ("O que significa 'IoT'?", "Internet of Things", "Interactive Online Tools", "Internet Open Tools", "Information of Things", "A", "médio"),
    ("Qual é o papel do 'GPU' em um computador?", "Processar dados de entrada", "Processar gráficos e imagens", "Armazenar dados", "Controlar o uso de memória", "B", "médio"),
    ("O que é o conceito de 'computação paralela'?", "Executar um programa em um único processador", "Executar várias tarefas simultaneamente em múltiplos processadores", "Executar programas sequenciais", "Executar programas em sistemas de rede", "B", "médio"),
    ("O que é o conceito de 'teste de unidade'?", "Testar o sistema como um todo", "Testar partes específicas do código para garantir que funcionem individualmente", "Testar o servidor", "Testar o banco de dados", "B", "médio"),
    ("O que é 'blockchain'?", "Uma tecnologia de redes de computadores", "Uma tecnologia de armazenamento de dados", "Uma tecnologia para criar aplicativos", "Uma tecnologia de registro de transações seguras", "D", "difícil"),
    ("O que é 'data mining'?", "Extração de dados valiosos de grandes conjuntos de dados", "Criação de bases de dados", "Compressão de dados", "Armazenamento de dados", "A", "difícil"),
]

# Inserir as perguntas no banco de dados
for pergunta, opcao_a, opcao_b, opcao_c, opcao_d, resposta, dificuldade in questoes:
    c.execute('''INSERT INTO perguntas (pergunta, opcao_a, opcao_b, opcao_c, opcao_d, resposta, dificuldade)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', (pergunta, opcao_a, opcao_b, opcao_c, opcao_d, resposta, dificuldade))

conn.commit()

# Configuração do bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Bot está online como {bot.user}')


# Comando para iniciar o quiz
@bot.command()
async def quiz(ctx):
    c.execute("SELECT * FROM perguntas ORDER BY RANDOM() LIMIT 1")
    pergunta = c.fetchone()
    texto_pergunta = (
        f"**Pergunta:** {pergunta[1]}\n"
        f"A: {pergunta[2]}\n"
        f"B: {pergunta[3]}\n"
        f"C: {pergunta[4]}\n"
        f"D: {pergunta[5]}\n"
        f"(Dificuldade: {pergunta[7]})\n"
        f"Digite a letra correspondente à sua resposta (A, B, C ou D)."
    )
    await ctx.send(texto_pergunta)

    def check(m):
        return (
                m.author == ctx.author
                and m.channel == ctx.channel
                and m.content.upper() in ["A", "B", "C", "D"]
        )

    try:
        msg = await bot.wait_for('message', check=check, timeout=30.0)
        resposta_usuario = msg.content.upper()
        resposta_correta = pergunta[6].upper()

        if resposta_usuario == resposta_correta:
            await ctx.send("🎉 Parabéns, você acertou!")
            c.execute("INSERT OR IGNORE INTO pontuacoes (usuario_id, pontos) VALUES (?, ?)", (str(ctx.author.id), 0))
            c.execute("UPDATE pontuacoes SET pontos = pontos + 1 WHERE usuario_id = ?", (str(ctx.author.id),))
            conn.commit()
        else:
            await ctx.send(f"😞 Que pena, a resposta correta era: {resposta_correta}")
    except asyncio.TimeoutError:
        await ctx.send("⏰ Tempo esgotado! Tente novamente.")


# Comando para adicionar perguntas (somente administradores)
@bot.command()
@commands.has_permissions(administrator=True)
async def adicionar(ctx):
    await ctx.send("Por favor, envie a pergunta.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        pergunta_msg = await bot.wait_for('message', check=check, timeout=60.0)
        pergunta = pergunta_msg.content

        await ctx.send("Agora envie a opção A.")
        opcao_a_msg = await bot.wait_for('message', check=check, timeout=30.0)
        opcao_a = opcao_a_msg.content

        await ctx.send("Agora envie a opção B.")
        opcao_b_msg = await bot.wait_for('message', check=check, timeout=30.0)
        opcao_b = opcao_b_msg.content

        await ctx.send("Agora envie a opção C.")
        opcao_c_msg = await bot.wait_for('message', check=check, timeout=30.0)
        opcao_c = opcao_c_msg.content

        await ctx.send("Agora envie a opção D.")
        opcao_d_msg = await bot.wait_for('message', check=check, timeout=30.0)
        opcao_d = opcao_d_msg.content

        await ctx.send("Agora envie a letra da resposta correta (A, B, C ou D).")
        resposta_msg = await bot.wait_for('message', check=check, timeout=30.0)
        resposta = resposta_msg.content.upper()

        if resposta not in ["A", "B", "C", "D"]:
            await ctx.send("❌ Resposta inválida! Operação cancelada.")
            return

        await ctx.send("Por fim, envie o nível de dificuldade (fácil, médio ou difícil).")
        dificuldade_msg = await bot.wait_for('message', check=check, timeout=30.0)
        dificuldade = dificuldade_msg.content.lower()

        c.execute(
            '''INSERT INTO perguntas (pergunta, opcao_a, opcao_b, opcao_c, opcao_d, resposta, dificuldade)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (pergunta, opcao_a, opcao_b, opcao_c, opcao_d, resposta, dificuldade)
        )
        conn.commit()
        await ctx.send("✅ Pergunta adicionada com sucesso!")
    except asyncio.TimeoutError:
        await ctx.send("⏰ Tempo esgotado! Operação cancelada.")


# Comando para listar todas as perguntas (somente administradores)
@bot.command()
@commands.has_permissions(administrator=True)
async def listar(ctx):
    c.execute("SELECT * FROM perguntas")
    perguntas = c.fetchall()

    if not perguntas:
        await ctx.send("❌ Nenhuma pergunta encontrada.")
        return

    texto = "**Perguntas cadastradas:**\n"
    for pergunta in perguntas:
        texto += f"ID: {pergunta[0]}, Pergunta: {pergunta[1]}, Resposta: {pergunta[6]}\n"
    await ctx.send(texto)


# Comando para exibir pontuação de um usuário
@bot.command()
async def pontuacao(ctx):
    c.execute("SELECT pontos FROM pontuacoes WHERE usuario_id = ?", (str(ctx.author.id),))
    resultado = c.fetchone()

    if resultado:
        await ctx.send(f"🏆 Você acertou {resultado[0]} perguntas até agora!")
    else:
        await ctx.send("❌ Você ainda não acertou nenhuma pergunta. Tente participar do quiz!")


bot.run('MTMwODgzMzc4OTE5OTM4NDY1Nw.GUFdSV.pF_ptu_D0zw4DVvShzjIhS-M2ipXpKQW2IGokg')
