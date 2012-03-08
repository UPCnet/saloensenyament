SALO ENSENYAMENT 2012
=======================

Versió 2012 SaloEnsenyament *(inclou salofutura)*

Usuari i password encriptat amb MD5 a fitxer */src/saloensenyament/passwd*

Format::

	usuari:encriptedpass


**La url principal http://SITE/ mostra el saloensenyament del 2012**

**El salo futura es mostra a http://SITE/salofutura**

NOTA:
Es fan servir dos fitxers

saloensenyament: Titulacions-2012-saloensenyament.csv

salo futura: Titulacions-2012-salofutura.csv

+---------------------------------------------------------------------------------------------+
|BUG: Problema amb dades que porten '    Ex: d'Edificació                                     |
+---------------------------------------------------------------------------------------------+
|SOLUCIÓ: Al csv original canviem ' per doble espai, i al enviar al mail, el tornem a '       |
+---------------------------------------------------------------------------------------------+

També es guarda un log (saloensenyament.log) amb::

   Dia / Hora / Warning level / Thread / Nom applicació / email / Graus seleccionats






