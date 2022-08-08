# 1 Objetivo

Neste projeto será implementado um relógio GMT (Greenwich Mean Time) idêntico à face correspondente do Apple Watch 1 . O relógio GMT foi criado pela Rolex em 1954 a pedido da Pan American Airlines, como uma solução para pilotos que viajam por diversas zonas de tempo, mas mantendo o tempo natal (da cidade original do viajante).<br>

Basicamente, há um segundo ponteiro vermelho de horas para um segundo fuso horário. Entretanto, ele completa uma rotação de 360◦ em 24 horas, ao invés de 12 horas4 . Se o segundo fuso for igual ao fuso natal, o ponteiro aponta para cima à meia noite, e para baixo ao meio dia. Pode-se contar as horas usando-se as marcas da coroa (bezel), e há 24, incluindo a seta localizada no topo. Assim, o mostrador externo permite saber se a hora é AM ou PM, por exemplo, 8h ou 20h.<br>

Se for escolhido um segundo fuso horário5 (por ex., tocando no centro do relógio), será lido no mostrador externo (coroa), no ponto onde ponteiro vermelho aponta, a hora correspondente ao fuso horário alternativo (figura 1b). Isto será 1-12, se o relógio estiver no modo de 12 horas, ou 1-24 se o relógio estiver no modo de 24 horas (o modo de tempo é escolhido no iPhone pareado).

A cor da coroa muda para a hora do nascer / por do sol6 7 do fuso escolhido. Se não for escolhido um segundo fuso horário, ainda é possı́vel tocar e escolher a hora natal (fuso corrente ou natal). Isto fará com que as cores da coroa mudem para a hora do nascer / por do sol8 9 e que seja exibida a hora completa (AM/PM) mais recente do fuso natal. Tocando no centro e escolhendo ’NONE’, como na figura 1a, fará com que a coroa mude para aquilo que se vê, por ex., 06:00 até 18:00, se for lida a hora do mostrador externo de 24 horas.
