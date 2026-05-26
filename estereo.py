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
 