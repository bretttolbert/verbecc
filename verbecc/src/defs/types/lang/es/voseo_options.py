import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum


class VoseoOptions(StrEnum):
    """
    Enumeración de diferentes tipos de conjugación verbal en voseo en español

    NoVoseo: Indica que no se utiliza el voseo en la conjugación verbal.

    TIPO 1 Voseo ortodoxo, corresponde con la conjugación del voseo reverencial
    antiguo, aunque sin sus formas pronominales.
    Se escucha en Venezuela (Zulia), Colombia (occidente de Norte de Santander,
    sur de La Guajira y norte del Cesar, limítrofes con el Zulia venezolano),
    en el noroeste de Bolivia, en el centro de Panamá (Península de Azuero),
    y en una pequeña franja al oriente de Cuba.

    TIPO 2 Se escucha en la sierra de Ecuador, la zona meridional del Perú,
    noroeste de Argentina y el suroeste de Bolivia.

    TIPO 3 Ocurre en el sureste de México, en Centroamérica (excepto Panamá),
    la costa pacífica y zona andina centrooccidental de Colombia, parte de la
    zona andina de Venezuela, la costa de Ecuador, el sur y el este de Bolivia,
    Paraguay, Argentina y Uruguay. Es aceptado como parte de la norma culta en
    Argentina, Paraguay y Uruguay.

    TIPO 4 Ocurre en Argentina (Santiago del Estero).

    * En Chile nunca se pronuncia ni se escribe la «s» en las formas terminadas
    en «-áis», por ejemplo: «estái», «comái», «hablabai», etc. Existe la
    tendencia a utilizar la terminación en «-ay» para evitar la acentuación
    gráfica correspondiente a la terminación «-ái»; sin embargo, y pese a que
    la grafía con «-ay» se adapta mejor a la ortografía del español, no se
    recomienda para las formas diptongadas propias del voseo chileno.

    Desinencias en Indicativo Presente
    Tipo (nombres alternativos) 	-ar 	-er 	-ir
    --------------------------------------------------------
    Voseo tipo 1 (Voseo clásico) 	-áis 	-éis 	-ís
    Voseo tipo 2 	                -áis 	-ís 	-ís
    Voseo tipo 3 (Voseo típico) 	-ás 	-és 	-ís
    Voseo tipo 4 	                -ás 	-és 	-és
    Voseo chileno 	                -ái* 	-ís 	-ís

    Fuente: https://es.wikipedia.org/wiki/Voseo
    """

    NoVoseo = "no-voseo"  # default (tú)
    VoseoTipo1 = "voseo-tipo-1"  # Voseo Clásico
    VoseoTipo2 = "voseo-tipo-2"
    VoseoTipo3 = "voseo-tipo-3"  # Voseo típico aka Rioplatense
    VoseoTipo4 = "voseo-tipo-4"
    VoseoChileno = "voseo-chileno"
