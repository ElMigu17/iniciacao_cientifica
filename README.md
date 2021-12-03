# Iniciacao cientifica
Repositorio para colocar tudo relacionado a iniciação cientifica sobre "Problema de coleta e entrega dinamico com janela de tempo".

## Como usar?:
Vá até o diretorio "codigos/insertions" <br>
coloque o comando: <br>
	`python3.9 run_and_test s` <br>
**Importante**: O **s** quer dizer que a heuristica de incerção dinamica vai ser a inserção simples, pode rodar com l (com locais-fixos), r (com pedidos-fixos) ou m (randomico)

## Como alterar o input?
A algumas possibilidades de inputs com diferentes tamanho e caracteristica. Caso queira usar um input existente nesse repositorio diferente do atual, as possibilidades de tamanho são: 10, 200, 300 ou 400. A caracteristica que pode alterar é a existencia de pontos de coleta e entrega fazendo par com o deposito, em que 30% dos pedidos são randomicamente selecionados para fazerem par com o deposito. Para gerar essas instancias, basta rodar no arquivo "codigos/insertions/instancias":<br>
  `python3.9 adapt_json.py <quantidade escolhida> <T para ter os pedidos fazendo par com o deposito e F para não ter>`


