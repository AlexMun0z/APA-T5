# Sonido estéreo y ficheros WAVE

## Nom i cognoms

> [!Important]
> Introduzca a continuación su nombre y apellidos:
>
> Alex Muñoz Paton

## Aviso Importante

> [!Caution]
> 
> El objetivo de esta tarea es manejar la lectura y escritura de ficheros binarios. Para ello, sólo se
> permite el uso de las funciones de la biblioteca `struct`. Aunque existen distintas bibliotecas que
> permiten manejar los ficheros WAVE de una manera más eficiente y sencilla, su uso está prohibido.
>
> ¿Quiere saber más?, consulte con el profesorado.

## Fecha de entrega: 24 de mayo a medianoche

## El formato WAVE

El formato WAVE es uno de los más extendidos para el almacenamiento y transmisión
de señales de audio. En el fondo, se trata de un tipo particular de fichero
[RIFF](https://en.wikipedia.org/wiki/Resource_Interchange_File_Format) (*Resource
Interchange File Format*), utilizado no sólo para señales de audio sino también para señales de
otros tipos, como las imágenes estáticas o en movimiento, o secuencias MIDI (aunque, en el caso
del MIDI, con pequeñas diferencias que los hacen incompatibles).

La base de los ficheros RIFF es el uso de *cachos* (*chunks*, en inglés). Cada cacho,
o subcacho, está encabezado por una cadena de cuatro caracteres ASCII, que indica el tipo del cacho,
seguido por un entero sin signo de cuatro bytes, que indica el tamaño en bytes de lo que queda de
cacho sin contar la cadena inicial y el propio tamaño. A continuación, y en función del tipo de
cacho, se colocan los datos que lo forman.

Todo fichero RIFF incluye un primer cacho que lo identifica como tal y que empieza por la cadena
`'RIFF'`. A continuación, después del tamaño del cacho y en otra cadena de cuatro caracteres,
se indica el tipo concreto de información que contiene el fichero. En el caso concreto de los
ficheros de audio WAVE, esta cadena es igual a `'WAVE'`, y el cacho debe contener dos
*subcachos*: el primero, de nombre `'fmt '`, proporciona la información de cómo está
codificada la señal. Por ejemplo, si es PCM lineal, ADPCM, etc., o si es monofónica o estéreo. El
segundo subcacho, de nombre `'data'`, incluye las muestras de la señal.

Dispone de una descripción detallada del formato WAVE en la página
[WAVE PCM soundfile format](http://soundfile.sapp.org/doc/WaveFormat/) de Soundfile.

## Audio estéreo

La mayor parte de los animales, incluidos los del género *homo sapiens sapiens* sanos y completos,
están dotados de dos órganos que actúan como transductores acústico-sensoriales (es decir, tienen dos
*oídos*). Esta duplicidad orgánica permite al bicho, entre otras cosas, determinar la dirección de
origen del sonido. En el caso de la señal de música, además, la duplicidad proporciona una sensación
de *amplitud espacial*, de realismo y de confort acústico.

En un principio, los equipos de reproducción de audio no tenían en cuenta estos efectos y sólo permitían
almacenar y reproducir una única señal para los dos oídos. Es el llamado *sonido monofónico* o
*monoaural*. Una alternativa al sonido monofónico es el *estereofónico* o, simplemente, *estéreo*. En
él, se usan dos señales independientes, destinadas a ser reproducidas a ambos lados del oyente: los
llamados *canal izquierdo* (**L**) y *derecho* (**R**).

Aunque los primeros experimentos con sonido estereofónico datan de finales del siglo XIX, los primeros
equipos y grabaciones de este tipo no se popularizaron hasta los años 1950 y 1960. En aquel tiempo, la
gestión de los dos canales era muy rudimentaria. Por ejemplo, los instrumentos se repartían entre los
dos canales, con unos sonando exclusivamente a la izquierda y el resto a la derecha. Es el caso de las
primeras grabaciones en estéreo de los Beatles: las versiones en alemán de los singles *She loves you*
y *I want to hold your hand*. Así, en esta última (de la que dispone de un fichero en Atenea con sus
primeros treinta segundos, [Komm, gib mir deine Hand](wav/komm.wav)), la mayor parte de los instrumentos
suenan por el canal derecho, mientras que las voces y las características palmas lo hacen por el izquierdo.

Un problema habitual en los primeros años del sonido estereofónico, y aún vigente hoy en día, es que no
todos los equipos son capaces de reproducir los dos canales por separado. La solución comúnmente
adoptada consiste en no almacenar cada canal por separado, sino en la forma semisuma, $(L+R)/2$, y
semidiferencia, $(L-R)/2$, y de tal modo que los equipos monofónicos sólo accedan a la primera de ellas.
De este modo, estos equipos pueden reproducir una señal completa, formada por la suma de los dos
canales, y los estereofónicos pueden reconstruir los dos canales estéreo.

Por ejemplo, en la radio FM estéreo, la señal, de ancho de banda 15 kHz, se transmite del modo siguiente:

- En banda base, $0\le f\le 15$ kHz, se transmite la suma de los dos canales, $L+R$. Esta es la señal
  que son capaces de reproducir los equipos monofónicos.

- La señal diferencia, $L-R$, se transmite modulada en amplitud con una frecuencia de portadora
  $f_m = 38$ kHz.

  - Por tanto, ocupa la banda $23 \mathrm{kHz}\le f\le 53 \mathrm{kHz}$, que sólo es accedida por los
    equipos estéreo, y, en el caso de colarse en un reproductor monofónico, ocupa la banda no audible.

- También se emite una sinusoide de $19 \mathrm{kHz}$, denominada *señal piloto*, que se usa para
  demodular síncronamente la señal diferencia.

- Finalmente, la señal de audio estéreo puede acompañarse de otras señales de señalización y servicio en
  frecuencias entre $55.35 \mathrm{kHz}$ y $94 \mathrm{kHz}$.

En los discos fonográficos, la semisuma de las señales está grabada del mismo modo que se haría en una
grabación monofónica, es decir, en la profundidad del surco; mientras que la semidiferencia se graba en el
desplazamiento a izquierda y derecha de la aguja. El resultado es que un reproductor mono, que sólo atiende
a la profundidad del surco, reproduce casi correctamente la señal monofónica, mientras que un reproductor
estéreo es capaz de separar los dos canales. Es posible que algo de la información de la semisuma se cuele
en el reproductor mono, pero, como su amplitud es muy pequeña, se manifestará como un ruido muy débil,
apenas perceptible.

En general, todos estos sistemas se basan en garantizar que el reproductor mono recibe correctamente la
semisuma de canales y que, si algo de la semidiferencia se cuela en la reproducción, sea en forma de un
ruido inaudible.

## Tareas a realizar

Escriba el fichero `estereo.py` que incluirá las funciones que permitirán el manejo de los canales de una
señal estéreo y su codificación/decodificación para compatibilizar ésta con sistemas monofónicos.


### Manejo de los canales de una señal estéreo

En un fichero WAVE estéreo con señales de 16 bits, cada muestra de cada canal se codifica con un entero de
dos bytes. La señal se almacena en el *cacho* `'data'` alternando, para cada muestra de $x[n]$, el valor
del canal izquierdo y el derecho:

<img src="img/est%C3%A9reo.png" width="380px">

#### Función `estereo2mono(ficEste, ficMono, canal=2)`

La función lee el fichero `ficEste`, que debe contener una señal estéreo, y escribe el fichero `ficMono`,
con una señal monofónica. El tipo concreto de señal que se almacenará en `ficMono` depende del argumento
`canal`:

- `canal=0`: Se almacena el canal izquierdo $L$.
- `canal=1`: Se almacena el canal derecho $R$.
- `canal=2`: Se almacena la semisuma $(L+R)/2$. Ha de ser la opción por defecto.
- `canal=3`: Se almacena la semidiferencia $(L-R)/2$.

#### Función `mono2estereo(ficIzq, ficDer, ficEste)`

Lee los ficheros `ficIzq` y `ficDer`, que contienen las señales monofónicas correspondientes a los canales
izquierdo y derecho, respectivamente, y construye con ellas una señal estéreo que almacena en el fichero
`ficEste`.

### Codificación estéreo usando los bits menos significativos

En la línea de los sistemas usados para codificar la información estéreo en señales de radio FM o en los
surcos de los discos fonográficos, podemos usar enteros de 32 bits para almacenar los dos canales de 16 bits:

- En los 16 bits más significativos se almacena la semisuma de los dos canales.

- En los 16 bits menos significativos se almacena la semidiferencia.

Los sistemas monofónicos sólo son capaces de manejar la señal de 32 bits. Esta señal es prácticamente
idéntica a la señal semisuma, ya que la semisuma ocupa los 16 bits más significativos. La señal
semidiferencia aparece como un ruido añadido a la señal, pero, como su amplitud es $2^{16}$ veces más
pequeña, será prácticamente inaudible (la relación señal a ruido es del orden de 90 dB).

Los sistemas estéreo son capaces de aislar las dos partes de la señal y, con ellas, reconstruir los dos
canales izquierdo y derecho.

<img src="img/est%C3%A9reo_cod.png" width="510px">

#### Función `codEstereo(ficEste, ficCod)`

Lee el fichero `ficEste`, que contiene una señal estéreo codificada con PCM lineal de 16 bits, y
construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas
monofónicos como por sistemas estéreo preparados para ello.

#### Función `decEstereo(ficCod, ficEste)`

Lee el fichero `ficCod` con una señal monofónica de 32 bits en la que los 16 bits más significativos
contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la
semidiferencia, y escribe el fichero `ficEste` con los dos canales por separado en el formato de los
ficheros WAVE estéreo.

### Entrega

#### Fichero `estereo.py`

- El fichero debe incluir una cadena de documentación que incluirá el nombre del alumno y una descripción
  del contenido del fichero.

- Es muy recomendable escribir, además, sendas funciones que *empaqueten* y *desempaqueten* las cabeceras
  de los ficheros WAVE a partir de los datos contenidos en ellas.

- Aparte de `struct`, no se puede importar o usar ningún módulo externo.

- Se deben evitar los bucles. Se valorará el uso, cuando sea necesario, de *comprensiones*.

- Los ficheros se deben abrir y cerrar usando gestores de contexto.

- Las funciones deberán comprobar que los ficheros de entrada tienen el formato correcto y, en caso
  contrario, elevar la excepción correspondiente.

- Los ficheros resultantes deben ser reproducibles correctamente usando cualquier reproductor estándar;
  por ejemplo, el Windows Media Player o similar. Es probable, muy probable, que tenga que modificar los
  datos de las cabeceras de los ficheros para conseguirlo.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el uso de los estándares
  marcados por PEP-ocho.

#### Comprobación del funcionamiento

Es responsabilidad del alumno comprobar que las distintas funciones realizan su cometido de manera correcta.
Para ello, se recomienda usar la canción [Komm, gib mir deine Hand](wav/komm.wav), suminstrada al efecto.
De todos modos, recuerde que, aunque sea en alemán, se trata de los Beatles, así que procure no destrozar
innecesariamente la canción.

#### Código desarrollado
```python
"""
estereo.py

Alex Muñoz Paton

Manejo de señales de audio estéreo en formato WAVE PCM. Este módulo proporciona
funciones para extraer canales de ficheros estéreo, construir estéreo a partir
de ficheros mono, y codificar/decodificar señales estéreo en 32 bits compatibles
con reproductores monofónicos.

Solo se usa la biblioteca estándar `struct`.
"""

import struct as st


# ---------------------------------------------------------------------------
# Constantes del formato WAVE PCM
# ---------------------------------------------------------------------------

_RIFF_ID    = b'RIFF'
_WAVE_ID    = b'WAVE'
_FMT_ID     = b'fmt '   # 4 caracteres: 'fmt' + espacio
_DATA_ID    = b'data'
_PCM_FORMAT = 1          # PCM lineal sin compresión


# ---------------------------------------------------------------------------
# Funciones auxiliares de cabecera
# ---------------------------------------------------------------------------

def _leer_cabecera(f):
    """
    Lee y valida la cabecera de un fichero WAVE PCM abierto en modo binario.

    Devuelve un diccionario con los campos de la cabecera:
        riff_size, num_channels, sample_rate, byte_rate,
        block_align, bits_per_sample, data_size
    """
    # RIFF
    riff_id   = f.read(4)
    riff_size = st.unpack('<I', f.read(4))[0]
    wave_id   = f.read(4)

    if riff_id != _RIFF_ID:
        raise ValueError(f"El fichero no comienza con 'RIFF' (encontrado: {riff_id})")
    if wave_id != _WAVE_ID:
        raise ValueError(f"El fichero no es de tipo WAVE (encontrado: {wave_id})")

    # fmt
    fmt_id   = f.read(4)
    fmt_size = st.unpack('<I', f.read(4))[0]

    if fmt_id != _FMT_ID:
        raise ValueError(f"Se esperaba el subchunk 'fmt ' (encontrado: {fmt_id})")

    (audio_format, num_channels, sample_rate,
     byte_rate, block_align, bits_per_sample) = st.unpack('<HHIIHH', f.read(16))

    # Saltar bytes adicionales del  fmt si los hubiera
    if fmt_size > 16:
        f.read(fmt_size - 16)

    if audio_format != _PCM_FORMAT:
        raise ValueError(f"Solo se admite PCM lineal (audio_format={audio_format})")

    # Data
    data_id   = f.read(4)
    data_size = st.unpack('<I', f.read(4))[0]

    if data_id != _DATA_ID:
        raise ValueError(f"Se esperaba el subchunk 'data' (encontrado: {data_id})")

    return {
        'riff_size':       riff_size,
        'num_channels':    num_channels,
        'sample_rate':     sample_rate,
        'byte_rate':       byte_rate,
        'block_align':     block_align,
        'bits_per_sample': bits_per_sample,
        'data_size':       data_size,
    }


def _escribir_cabecera(f, num_channels, sample_rate, bits_per_sample, data_size):
    """
    Escribe la cabecera WAVE PCM estándar en el fichero abierto en modo binario.
    """
    block_align = num_channels * bits_per_sample // 8
    byte_rate   = sample_rate * block_align
    riff_size   = 4 + 8 + 16 + 8 + data_size  # 'WAVE' + fmt chunk + data chunk

    f.write(_RIFF_ID)
    f.write(st.pack('<I', riff_size))
    f.write(_WAVE_ID)

    f.write(_FMT_ID)
    f.write(st.pack('<I', 16))  # Tamaño fijo del subchunk fmt para PCM
    f.write(st.pack('<HHIIHH',
                    _PCM_FORMAT, num_channels, sample_rate,
                    byte_rate, block_align, bits_per_sample))

    f.write(_DATA_ID)
    f.write(st.pack('<I', data_size))


# ---------------------------------------------------------------------------
# Funciones principales
# ---------------------------------------------------------------------------

def estereo2mono(ficEste, ficMono, canal=2):
    """
    Lee el fichero WAVE estéreo ficEste (PCM 16 bits) y escribe ficMono
    con la señal monofónica seleccionada por canal:

        canal=0  ->  canal izquierdo L
        canal=1  ->  canal derecho R
        canal=2  ->  semisuma  (L+R)/2  [por defecto]
        canal=3  ->  semidiferencia  (L-R)/2
    """
    if canal not in (0, 1, 2, 3):
        raise ValueError(f"El argumento canal debe ser 0, 1, 2 o 3 (recibido: {canal})")

    with open(ficEste, 'rb') as fe:
        cab = _leer_cabecera(fe)

        if cab['num_channels'] != 2:
            raise ValueError("El fichero de entrada debe ser estéreo (2 canales)")
        if cab['bits_per_sample'] != 16:
            raise ValueError("Solo se admiten señales PCM de 16 bits")

        num_muestras = cab['data_size'] // cab['block_align']
        datos_raw    = fe.read(cab['data_size'])

    muestras = st.unpack(f'<{2 * num_muestras}h', datos_raw)

    canal_L = muestras[0::2]
    canal_R = muestras[1::2]

    if canal == 0:
        mono = canal_L
    elif canal == 1:
        mono = canal_R
    elif canal == 2:
        mono = tuple((l + r) // 2 for l, r in zip(canal_L, canal_R))
    else:  # canal == 3
        mono = tuple((l - r) // 2 for l, r in zip(canal_L, canal_R))

    data_size_mono = num_muestras * 2  # 1 canal x 2 bytes

    with open(ficMono, 'wb') as fm:
        _escribir_cabecera(fm,
                           num_channels=1,
                           sample_rate=cab['sample_rate'],
                           bits_per_sample=16,
                           data_size=data_size_mono)
        fm.write(st.pack(f'<{num_muestras}h', *mono))


def mono2estereo(ficIzq, ficDer, ficEste):
    """
    Lee los ficheros mono ficIzq (canal L) y ficDer (canal R) y construye
    el fichero WAVE estéreo ficEste alternando muestras L y R.

    Ambos ficheros deben tener la misma frecuencia de muestreo y 16 bits por muestra.
    """
    with open(ficIzq, 'rb') as fi:
        cab_izq = _leer_cabecera(fi)

        if cab_izq['num_channels'] != 1:
            raise ValueError("ficIzq debe ser un fichero monofónico (1 canal)")
        if cab_izq['bits_per_sample'] != 16:
            raise ValueError("Solo se admiten señales PCM de 16 bits")

        num_izq   = cab_izq['data_size'] // 2
        datos_izq = st.unpack(f'<{num_izq}h', fi.read(cab_izq['data_size']))

    with open(ficDer, 'rb') as fd:
        cab_der = _leer_cabecera(fd)

        if cab_der['num_channels'] != 1:
            raise ValueError("ficDer debe ser un fichero monofónico (1 canal)")
        if cab_der['bits_per_sample'] != 16:
            raise ValueError("Solo se admiten señales PCM de 16 bits")
        if cab_der['sample_rate'] != cab_izq['sample_rate']:
            raise ValueError("Los ficheros deben tener la misma frecuencia de muestreo")

        num_der   = cab_der['data_size'] // 2
        datos_der = st.unpack(f'<{num_der}h', fd.read(cab_der['data_size']))

    num_muestras = min(num_izq, num_der)

    estereo = [valor
               for par in zip(datos_izq[:num_muestras], datos_der[:num_muestras])
               for valor in par]

    data_size_este = num_muestras * 4  # 2 canales x 2 bytes

    with open(ficEste, 'wb') as fe:
        _escribir_cabecera(fe,
                           num_channels=2,
                           sample_rate=cab_izq['sample_rate'],
                           bits_per_sample=16,
                           data_size=data_size_este)
        fe.write(st.pack(f'<{2 * num_muestras}h', *estereo))


def codEstereo(ficEste, ficCod):
    """
    Lee el fichero WAVE estéreo ficEste (PCM 16 bits) y escribe ficCod
    con una señal monofónica de 32 bits donde:

        bits 31-16  ->  semisuma    (L+R)/2
        bits 15-0   ->  semidiferencia  (L-R)/2
    """
    with open(ficEste, 'rb') as fe:
        cab = _leer_cabecera(fe)

        if cab['num_channels'] != 2:
            raise ValueError("El fichero de entrada debe ser estéreo (2 canales)")
        if cab['bits_per_sample'] != 16:
            raise ValueError("Solo se admiten señales PCM de 16 bits")

        num_muestras = cab['data_size'] // cab['block_align']
        muestras     = st.unpack(f'<{2 * num_muestras}h', fe.read(cab['data_size']))

    canal_L = muestras[0::2]
    canal_R = muestras[1::2]

    cod = tuple((((l + r) // 2) << 16) | (((l - r) // 2) & 0xFFFF) for l, r in zip(canal_L, canal_R))

    data_size_cod = num_muestras * 4  # 1 canal x 4 bytes

    with open(ficCod, 'wb') as fc:
        _escribir_cabecera(fc,
                           num_channels=1,
                           sample_rate=cab['sample_rate'],
                           bits_per_sample=32,
                           data_size=data_size_cod)
        fc.write(st.pack(f'<{num_muestras}i', *cod))


def decEstereo(ficCod, ficEste):
    """
    Lee el fichero ficCod con una señal monofónica de 32 bits donde:

        bits 31-16  ->  semisuma    M = (L+R)/2
        bits 15-0   ->  semidiferencia  D = (L-R)/2  (con signo extendido)

    Reconstruye los canales:
        L = M + D
        R = M - D

    y escribe el fichero WAVE estéreo ficEste.
    """
    with open(ficCod, 'rb') as fc:
        cab = _leer_cabecera(fc)

        if cab['num_channels'] != 1:
            raise ValueError("El fichero codificado debe ser monofónico (1 canal)")
        if cab['bits_per_sample'] != 32:
            raise ValueError("El fichero codificado debe tener 32 bits por muestra")

        num_muestras = cab['data_size'] // 4
        muestras_cod = st.unpack(f'<{num_muestras}i', fc.read(cab['data_size']))

    def _signo16(v):
        """Extiende el signo de los 16 bits menos significativos."""
        v16 = v & 0xFFFF
        return v16 if v16 < 0x8000 else v16 - 0x10000

    semisuma = tuple(m >> 16 for m in muestras_cod)
    semidif  = tuple(_signo16(m) for m in muestras_cod)

    canal_L = tuple(s + d for s, d in zip(semisuma, semidif))
    canal_R = tuple(s - d for s, d in zip(semisuma, semidif))

    estereo = [valor
               for par in zip(canal_L, canal_R)
               for valor in par]

    data_size_este = num_muestras * 4  # 2 canales x 2 bytes

    with open(ficEste, 'wb') as fe:
        _escribir_cabecera(fe,
                           num_channels=2,
                           sample_rate=cab['sample_rate'],
                           bits_per_sample=16,
                           data_size=data_size_este)
        fe.write(st.pack(f'<{2 * num_muestras}h', *estereo))
```


##### Código de `estereo2mono()`
```python
def estereo2mono(ficEste, ficMono, canal=2):
    """
    Lee el fichero WAVE estéreo ficEste (PCM 16 bits) y escribe ficMono
    con la señal monofónica seleccionada por canal:

        canal=0  ->  canal izquierdo L
        canal=1  ->  canal derecho R
        canal=2  ->  semisuma  (L+R)/2  [por defecto]
        canal=3  ->  semidiferencia  (L-R)/2
    """
    if canal not in (0, 1, 2, 3):
        raise ValueError(f"El argumento canal debe ser 0, 1, 2 o 3 (recibido: {canal})")

    with open(ficEste, 'rb') as fe:
        cab = _leer_cabecera(fe)

        if cab['num_channels'] != 2:
            raise ValueError("El fichero de entrada debe ser estéreo (2 canales)")
        if cab['bits_per_sample'] != 16:
            raise ValueError("Solo se admiten señales PCM de 16 bits")

        num_muestras = cab['data_size'] // cab['block_align']
        datos_raw    = fe.read(cab['data_size'])

    muestras = st.unpack(f'<{2 * num_muestras}h', datos_raw)

    canal_L = muestras[0::2]
    canal_R = muestras[1::2]

    if canal == 0:
        mono = canal_L
    elif canal == 1:
        mono = canal_R
    elif canal == 2:
        mono = tuple((l + r) // 2 for l, r in zip(canal_L, canal_R))
    else:  # canal == 3
        mono = tuple((l - r) // 2 for l, r in zip(canal_L, canal_R))

    data_size_mono = num_muestras * 2  # 1 canal x 2 bytes

    with open(ficMono, 'wb') as fm:
        _escribir_cabecera(fm,
                           num_channels=1,
                           sample_rate=cab['sample_rate'],
                           bits_per_sample=16,
                           data_size=data_size_mono)
        fm.write(st.pack(f'<{num_muestras}h', *mono))
```

##### Código de `mono2estereo()`
```python
def mono2estereo(ficIzq, ficDer, ficEste):
    """
    Lee los ficheros mono ficIzq (canal L) y ficDer (canal R) y construye
    el fichero WAVE estéreo ficEste alternando muestras L y R.

    Ambos ficheros deben tener la misma frecuencia de muestreo y 16 bits por muestra.
    """
    with open(ficIzq, 'rb') as fi:
        cab_izq = _leer_cabecera(fi)

        if cab_izq['num_channels'] != 1:
            raise ValueError("ficIzq debe ser un fichero monofónico (1 canal)")
        if cab_izq['bits_per_sample'] != 16:
            raise ValueError("Solo se admiten señales PCM de 16 bits")

        num_izq   = cab_izq['data_size'] // 2
        datos_izq = st.unpack(f'<{num_izq}h', fi.read(cab_izq['data_size']))

    with open(ficDer, 'rb') as fd:
        cab_der = _leer_cabecera(fd)

        if cab_der['num_channels'] != 1:
            raise ValueError("ficDer debe ser un fichero monofónico (1 canal)")
        if cab_der['bits_per_sample'] != 16:
            raise ValueError("Solo se admiten señales PCM de 16 bits")
        if cab_der['sample_rate'] != cab_izq['sample_rate']:
            raise ValueError("Los ficheros deben tener la misma frecuencia de muestreo")

        num_der   = cab_der['data_size'] // 2
        datos_der = st.unpack(f'<{num_der}h', fd.read(cab_der['data_size']))

    num_muestras = min(num_izq, num_der)

    estereo = [valor
               for par in zip(datos_izq[:num_muestras], datos_der[:num_muestras])
               for valor in par]

    data_size_este = num_muestras * 4  # 2 canales x 2 bytes

    with open(ficEste, 'wb') as fe:
        _escribir_cabecera(fe,
                           num_channels=2,
                           sample_rate=cab_izq['sample_rate'],
                           bits_per_sample=16,
                           data_size=data_size_este)
        fe.write(st.pack(f'<{2 * num_muestras}h', *estereo))
```
##### Código de `codEstereo()`
```python
def codEstereo(ficEste, ficCod):
    """
    Lee el fichero WAVE estéreo ficEste (PCM 16 bits) y escribe ficCod
    con una señal monofónica de 32 bits donde:

        bits 31-16  ->  semisuma    (L+R)/2
        bits 15-0   ->  semidiferencia  (L-R)/2
    """
    with open(ficEste, 'rb') as fe:
        cab = _leer_cabecera(fe)

        if cab['num_channels'] != 2:
            raise ValueError("El fichero de entrada debe ser estéreo (2 canales)")
        if cab['bits_per_sample'] != 16:
            raise ValueError("Solo se admiten señales PCM de 16 bits")

        num_muestras = cab['data_size'] // cab['block_align']
        muestras     = st.unpack(f'<{2 * num_muestras}h', fe.read(cab['data_size']))

    canal_L = muestras[0::2]
    canal_R = muestras[1::2]

    cod = tuple((((l + r) // 2) << 16) | (((l - r) // 2) & 0xFFFF) for l, r in zip(canal_L, canal_R))

    data_size_cod = num_muestras * 4  # 1 canal x 4 bytes

    with open(ficCod, 'wb') as fc:
        _escribir_cabecera(fc,
                           num_channels=1,
                           sample_rate=cab['sample_rate'],
                           bits_per_sample=32,
                           data_size=data_size_cod)
        fc.write(st.pack(f'<{num_muestras}i', *cod))
```
##### Código de `decEstereo()`
```python
def decEstereo(ficCod, ficEste):
    """
    Lee el fichero ficCod con una señal monofónica de 32 bits donde:

        bits 31-16  ->  semisuma    M = (L+R)/2
        bits 15-0   ->  semidiferencia  D = (L-R)/2  (con signo extendido)

    Reconstruye los canales:
        L = M + D
        R = M - D

    y escribe el fichero WAVE estéreo ficEste.
    """
    with open(ficCod, 'rb') as fc:
        cab = _leer_cabecera(fc)

        if cab['num_channels'] != 1:
            raise ValueError("El fichero codificado debe ser monofónico (1 canal)")
        if cab['bits_per_sample'] != 32:
            raise ValueError("El fichero codificado debe tener 32 bits por muestra")

        num_muestras = cab['data_size'] // 4
        muestras_cod = st.unpack(f'<{num_muestras}i', fc.read(cab['data_size']))

    def _signo16(v):
        """Extiende el signo de los 16 bits menos significativos."""
        v16 = v & 0xFFFF
        return v16 if v16 < 0x8000 else v16 - 0x10000

    semisuma = tuple(m >> 16       for m in muestras_cod)
    semidif  = tuple(_signo16(m)   for m in muestras_cod)

    canal_L = tuple(s + d for s, d in zip(semisuma, semidif))
    canal_R = tuple(s - d for s, d in zip(semisuma, semidif))

    estereo = [valor
               for par in zip(canal_L, canal_R)
               for valor in par]

    data_size_este = num_muestras * 4  # 2 canales x 2 bytes

    with open(ficEste, 'wb') as fe:
        _escribir_cabecera(fe,
                           num_channels=2,
                           sample_rate=cab['sample_rate'],
                           bits_per_sample=16,
                           data_size=data_size_este)
        fe.write(st.pack(f'<{2 * num_muestras}h', *estereo))
``` 

#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en
el repositorio, incluyendo el realce sintáctico del código fuente insertado.
