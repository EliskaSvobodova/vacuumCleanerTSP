# Vysavač

Implementace vysavače, který se pomocí algoritmu A* s heuristikou velokosti minimální kostry (Kruskalův algoritmus) snaží vysát všechno smetí.

Vysavač začíná v počáteční poloze a postupně se přesouvá na políčka se smetím. Vždy když smetí najde a vysaje, restartuje algoritmus A* a začne políčka otevírat a prohledávat znovu.

Jako heuristiku jsem použila délku nejkratší kostry obsahující všechna políčka se smetím a aktuální polohu vysavače. 