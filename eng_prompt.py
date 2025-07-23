#Fabio Leandro Lapuinka 23/07/2025

def construir_prompt():
    # Dicionário para armazenar as respostas
    respostas = {
        'tema': '',
        'modelo': '',
        'tempo': '',
        'personas': [],
        'dominio': '',
        'ajustes': '',
        'iteracoes': [],
        'checklist': {}
    }

    print("\n=== FASE 1 - COLETA INICIAL ===")
    
    # Passo 1/4
    respostas['tema'] = input("Qual é o tema/objetivo principal do prompt que você deseja criar?\n> ")
    
    # Passo 2/4
    print("\nEm qual plano/modelo pretende rodar?")
    modelos = [
        "1. GPT‑4o Plus",
        "2. GPT‑4 Enterprise",
        "3. o3 (ChatGPT Plus)",
        "4. Outro – especifique",
        "5. Não sei"
    ]
    for modelo in modelos:
        print(modelo)
    escolha = input("> ")
    if escolha == "4":
        respostas['modelo'] = input("Especifique o modelo: ")
    else:
        respostas['modelo'] = modelos[int(escolha)-1][3:]
    
    # Passo 3/4
    print("\nExiste restrição de tempo para gerar a resposta?")
    print("1. Sim – detalhe")
    print("2. Não")
    escolha = input("> ")
    if escolha == "1":
        respostas['tempo'] = input("Detalhe a restrição de tempo: ")
    else:
        respostas['tempo'] = "Sem restrição de tempo"
    
    # Passo 4/4
    print("\nSelecione as personas (digite os números separados por vírgula):")
    personas = [
        "1. Estudante",
        "2. Profissional",
        "3. Gerente",
        "4. Técnico",
        "5. Executivo",
        "6. Outra – especifique"
    ]
    for persona in personas:
        print(persona)
    escolhas = input("> ").split(',')
    for esc in escolhas:
        if esc.strip() == "6":
            respostas['personas'].append(input("Especifique a persona: "))
        else:
            respostas['personas'].append(personas[int(esc.strip())-1][3:])
    
    # Fase 2 - Validação de Domínio
    print("\n=== FASE 2 - VALIDAÇÃO DE DOMÍNIO ===")
    print(f"Detectei que o domínio é: {respostas['tema']}")
    print("1. Sim")
    print("2. Não – corrija, por favor")
    escolha = input("> ")
    if escolha == "2":
        respostas['dominio'] = input("Corrija o domínio: ")
    else:
        respostas['dominio'] = respostas['tema']
    
    # Fase 3 - Primeira Síntese
    print("\n=== FASE 3 - PRIMEIRA SÍNTESE ===")
    print("\n=== PROMPT REVISADO v1 ===")
    print(f"Tema: {respostas['tema']}")
    print(f"Modelo: {respostas['modelo']}")
    print(f"Tempo: {respostas['tempo']}")
    print(f"Personas: {', '.join(respostas['personas'])}")
    print(f"Domínio: {respostas['dominio']}")
    
    print("\nDeseja ajustar algo ou posso seguir para as próximas perguntas de refinamento?")
    print("1. Seguir para refinamento")
    print("2. Ajustar")
    escolha = input("> ")
    if escolha == "2":
        respostas['ajustes'] = input("Quais ajustes deseja fazer? ")
    
    # Fase 4 - Iteração Contínua
    print("\n=== FASE 4 - ITERAÇÃO CONTÍNUA ===")
    iteracao = 1
    while True:
        print(f"\n=== ITERAÇÃO {iteracao} ===")
        print("Resumo das decisões:")
        print(f"- Tema: {respostas['tema']}")
        print(f"- Modelo: {respostas['modelo']}")
        print(f"- Personas: {', '.join(respostas['personas'])}")
        
        # Passo 1/n - Mostrar prompt revisado
        print("\n=== PROMPT REVISADO v{iteracao} ===")
        print(construir_texto_prompt(respostas))
        
        # Passo 2/n - Pergunta de refinamento
        print("\nSelecione uma opção para refinamento:")
        opcoes = [
            "1. Contexto de uso",
            "2. Público-alvo",
            "3. Tom/Estilo",
            "4. Formato de saída",
            "5. Restrições",
            "6. Finalizar"
        ]
        for op in opcoes:
            print(op)
        escolha = input("> ")
        
        if escolha == "6":
            break
            
        if escolha == "1":
            print("\nContexto de uso:")
            contextos = [
                "1. Blog Post",
                "2. Documento Técnico",
                "3. Chat de Suporte",
                "4. Apresentação Executiva",
                "5. Social Media",
                "6. Outra"
            ]
            for ctx in contextos:
                print(ctx)
            esc = input("> ")
            if esc == "6":
                respostas['iteracoes'].append(("Contexto", input("Especifique o contexto: ")))
            else:
                respostas['iteracoes'].append(("Contexto", contextos[int(esc)-1][3:]))
        
        # Adicione aqui os outros casos (2-5) de forma similar
        
        iteracao += 1
    
    # Fase 5 - Checklist Final
    print("\n=== FASE 5 - CHECKLIST FINAL ===")
    print("\n=== CHECKLIST ===")
    print(f"1. Tema: {respostas['tema']}")
    print(f"2. Domínio: {respostas['dominio']}")
    print(f"3. Persona(s): {', '.join(respostas['personas'])}")
    print(f"4. Modelo/Tokens: {respostas['modelo']}")
    # Adicione os outros itens do checklist
    
    print("\nTudo correto? Posso gerar a versão final?")
    print("1. Sim")
    print("2. Não – o que ajustar?")
    escolha = input("> ")
    if escolha == "2":
        ajuste = input("O que precisa ser ajustado? ")
        # Implemente a lógica de ajuste conforme necessário
    
    # Fase 6 - Entrega Final
    print("\n=== FASE 6 - ENTREGA FINAL ===")
    print("\n=== PROMPT DEFINITIVO ===\n")
    print(construir_texto_prompt(respostas))

def construir_texto_prompt(respostas):
    prompt = f"""
# Função
Você atuará como Engenheiro(a) de Prompts especializado em {respostas['dominio']}.

# Contexto
Tema principal: {respostas['tema']}
Personas: {', '.join(respostas['personas']}
Modelo: {respostas['modelo']}
Restrição de tempo: {respostas['tempo']}

# Diretrizes"""
    
    # Adiciona iterações
    for iteracao in respostas['iteracoes']:
        prompt += f"\n{iteracao[0]}: {iteracao[1]}"
    
    prompt += "\n\n# Formato de Resposta\nTexto claro e objetivo em português (PT-BR)"
    return prompt

# Iniciar o processo
if __name__ == "__main__":
    print("=== SISTEMA DE CONSTRUÇÃO DE PROMPTS ===")
    construir_prompt()
