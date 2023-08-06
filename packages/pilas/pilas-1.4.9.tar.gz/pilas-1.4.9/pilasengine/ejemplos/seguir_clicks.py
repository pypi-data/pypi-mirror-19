# -*- encoding: utf-8 -*-
import pilasengine
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas = pilasengine.iniciar()
mono = pilas.actores.Mono()
mono.aprender(pilas.habilidades.SeguirClicks)
mono.aprender(pilas.habilidades.AumentarConRueda)

pilas.avisar(u"El mono sigue los clicks, y cambia de tamaño si mueves la\nrueda del mouse.")
pilas.ejecutar()
