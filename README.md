Código do fibonacci retirado no link: https://github.com/meskatjahan/Fibonacci-Code-using-cool-language/blob/master/fibonacci.cl

Outros exemplos de código foram retirados de: http://openclassroom.stanford.edu/MainFolder/DocumentPage.php?course=Compilers&doc=docs/pa.html

para executar o analisador léxico e sintático basta executar o comando na raiz do projeto:
- python3 main.py

##Análise léxica

O programa irá executar a análise léxica de todo o código no Testes.cl e irá printar o resultado
no terminal no formato valor, tipo.

Todos os tipos estão listados na classe TokenType.py e são separados em conjuntos no vars.py.

Cada conjunto não é sobre similaridade de tipo, mas sim sobre os caracteres que o compõem, pra facilitar
a verificação do tipo.

Para não precisar ficar voltando em caracteres anteriores, foi criada uma função "peek_next_char" que 
não avança a linha para a próxima posição, então caso o próximo caracter não faça parte do token atual,
não há necessidade de avançar a linha para a próxima posição nesse momento.

## Análise sintática

Após ter o retorno da análise léxica, é feito um filtro nos tokens retornados para ignorar os de comentário,
apóis isso é chamado o analisador sintático. Ele itera sobre cada token recursivamente, verificando qual o próximo
estado é o válido baseado em qual é o token atual e em qual é o próximo token. Se não houver token válido, é adicionado
a posição desse token na lista de erros e segue até depois o próximo ponto de parada da iteração atual, definido na 
chamada do token.

Todos os tipos BNF estão listados em BNFType.py.

No fim, é retornado e printado no terminal uma árvore sintática em que cada nó interno é não-terminal e cada nó folha é 
terminal.