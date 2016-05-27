# Fundamentos de los Sistemas Inteligentes
Prácticas de Fundamentos de los Sistemas Inteligentes

Práctica 1: Búsqueda con oponente - Conecta 4

Hemos implementado una heurística que recorre por filas, columnas y diagonales buscando cada ocurrencia de piezas
adyacentes, dándole mayor importancia cuantas más piezas se hallen conjuntas. De esta forma, la acumulación de dos fichas
contiguas reporta a su jugador 10^3 puntos, de tres, 10^4 = 10000, y de 4 o más, 10^5 = 100000, indicando las combinaciones
más favorables para cada jugador.

Para ello, hemos desarrollado tres métodos que realizan cada uno de los tipos de recorrido, y que buscan para cada línea
el valor de las fichas contiguas de cada jugador. En el caso de las filas y las columnas, el recorrido se realiza de forma
natural, de izquierda a derecha y de abajo hacia arriba, respectivamente, mientras que para las diagonales se lleva a cabo
primero de forma ascendente y luego descendente, para poder así cuadricular el tablero.

Hemos realizado cambios en el código original, para modificar el jugador del turno inicial, y hemos reutilizado la función
"k_in_row", renombrándola a "mi_kinrow", que realiza las mismas operaciones, pero incluyendo la necesidad de dar un valor
al número de fichas encontradas, así como a obtener la posición en que se ha detenido el recorrido.

Además, el código permite la incorporación de nuevas heurísticas de juego, a través del array de modos de juego, y elegir
el jugador que ostenta el primer turno. Mediante la opción de heurística para el jugador oponente, se permite la incorporación
bien del mismo modo, o bien de un modo de juego distinto al que hemos nombrado "Modo Automático" para permitir así la
interacción máquina vs máquina.