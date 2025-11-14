# GS2-Alexandre
integrantes: 

André Ayello de Nobrega: RM561754
André Gouveia de Lima: RM564219
Mirella Mascarenhas: RM562092

Career Advisor - Orientador de Carreiras (CLI)

Descrição do projeto e propósito:

Este projeto é uma aplicação em Python orientada a objetos que analisa perfis profissionais com base em competências técnicas e comportamentais (ex.: lógica, programação, colaboração, adaptabilidade). A partir dos dados informados pelo usuário, a ferramenta calcula a aderência a diferentes carreiras do futuro, destaca lacunas (gaps) e sugere trilhas de aprendizado para evolução.

Recursos principais
- Cadastro rápido de perfil com pontuação de competências (0–100).
- Modelo OOP com classes: Competency, Profile, Career.
- Recomendador que ranqueia carreiras e aponta lacunas (gaps) e trilhas sugeridas.
- Interface de linha de comando (CLI) simples.

Execução:
Fluxo básico:
1) Escolha “1 - Criar/editar meu perfil”.
2) Informe seu nome e pontue competências de 0 a 100.
3) Escolha “2 - Ver recomendações de carreira”.
4) Veja o ranking de carreiras, as lacunas (quantos pontos faltam em cada competência) e sugestões de trilhas de aprendizado.
5) Escolha "3 - Lista de carreiras disponíveis". 
6) Mostra as carreiras disponiveis e quando é necessário em cada competência para conseguir o emprego.
Carreiras que são mostradas: Cientista de Dados, Engenheiro de Software, Especialista em Segurança, Designer de Produto Digital, Analista de Negócios.


Classes principais (em cli.py)
- Competency: representa uma competência com nome e tipo (technical/behavioral).
- Profile: armazena o nome da pessoa e um dicionário de pontuações por competência (0–100).
- Career: define uma carreira com descrição e requisitos mínimos por competência.
- Recommender: calcula a aderência do perfil às carreiras, lista lacunas e sugere trilhas de aprendizado.

Dados incluídos (em cli.py)
- Catálogo de competências: lógica, programação, dados, IA/ML, segurança, criatividade, colaboração, comunicação, adaptabilidade, resolução de problemas.
- Carreiras modelo: Cientista de Dados, Engenheiro de Software, Especialista em Segurança, Designer de Produto Digital, Analista de Negócios.
- Trilhas de aprendizado (links de referência) por competência.
