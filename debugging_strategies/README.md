# Estratégias de Debugging em Python

Este diretório contém exemplos práticos de diferentes estratégias de debugging em Python, com foco em aplicações para segurança da informação e desenvolvimento de software.

## Arquivos de Exemplo

1. **01_print_debugging.py** - Demonstra a técnica mais básica de debugging:
   - Uso de prints estratégicos para rastrear o fluxo de execução
   - Visualização de valores de variáveis em pontos críticos
   - Técnicas para formatar a saída de debug

2. **02_logging_debug.py** - Demonstra o uso do módulo logging:
   - Configuração básica e avançada de logging
   - Diferentes níveis de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
   - Formatação de mensagens de log
   - Redirecionamento de logs para arquivos

3. **03_pdb_debugger.py** - Demonstra o uso do debugger integrado do Python:
   - Uso do módulo pdb para debugging interativo
   - Definição de breakpoints
   - Navegação pelo código durante a execução
   - Inspeção de variáveis em tempo de execução

4. **04_excecoes_debug.py** - Demonstra técnicas de debugging com exceções:
   - Captura e análise de exceções para debugging
   - Criação de exceções personalizadas para facilitar o debugging
   - Uso de try/except/finally para rastreamento de erros

5. **05_testes_unitarios.py** - Demonstra o uso de testes para debugging:
   - Criação de testes unitários com unittest/pytest
   - Uso de assertions para verificar comportamentos esperados
   - Identificação de bugs através de testes

6. **06_profiling_debug.py** - Demonstra técnicas de profiling para debugging:
   - Identificação de gargalos de performance
   - Uso do módulo cProfile
   - Análise de tempo de execução

## Como Executar

Cada arquivo pode ser executado individualmente usando o interpretador Python:

```
python 01_print_debugging.py
python 02_logging_debug.py
python 03_pdb_debugger.py
# etc.
```

## Observações

Estes exemplos são destinados a fins educacionais e demonstram diferentes abordagens para debugging em Python. Em um ambiente de produção, é recomendável combinar várias dessas técnicas para uma estratégia de debugging eficaz.