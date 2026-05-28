"""
Constantes físicas e valores padrão para simulação de fibra óptica
"""

import math

# Constantes Físicas
SPEED_OF_LIGHT = 299792458  # m/s no vácuo
PLANCK_CONSTANT = 6.62607015e-34  # J⋅s
ELECTRON_CHARGE = 1.602176634e-19  # C

# Potência inicial usada na simulação, em miliwatts
INITIAL_POWER_MW = 1.0

# Atenuação didática para cabo metálico.
# Este valor é usado apenas para comparação educativa com a fibra óptica.
# Em cabos metálicos reais, a perda depende da frequência, do tipo de cabo,
# da qualidade da instalação e das interferências eletromagnéticas.
METAL_ATTENUATION_DB_PER_KM = 2.0

# Parâmetros da Fibra Óptica
FIBER_PARAMS = {
    'ATTENUATION_COEF': 0.2,  # dB/km (típico para 1550nm)
    'DISPERSION_COEF': 17.0,  # ps/(nm⋅km)
    'NUMERICAL_APERTURE': 0.13,
    'CORE_DIAMETER_SM': 9.0,  # μm (single-mode)
    'CORE_DIAMETER_MM': 50.0,  # μm (multi-mode)
    'CLADDING_DIAMETER': 125.0,  # μm
}

# Comprimentos de Onda Comuns (nm)
WAVELENGTHS = {
    'O_BAND': 1310,
    'C_BAND': 1550,
    'L_BAND': 1625,
    'MM_850': 850,
    'MM_1300': 1300
}

# Índices de Refração
REFRACTIVE_INDEX = {
    'CORE': 1.4682,
    'CLADDING': 1.4629,
    'AIR': 1.0003
}

# Fórmulas Úteis
def calculate_group_velocity(wavelength, refractive_index):
    """Calcula velocidade de grupo na fibra"""
    return SPEED_OF_LIGHT / refractive_index


def calculate_propagation_delay(distance_km, refractive_index):
    """Calcula atraso de propagação (ms)"""
    distance_m = distance_km * 1000
    velocity = calculate_group_velocity(1550, refractive_index)
    return (distance_m / velocity) * 1000  # em ms


def db_to_linear(db_value):
    """Converte dB para escala linear"""
    return 10 ** (db_value / 10)


def linear_to_db(linear_value):
    """Converte escala linear para dB"""
    return 10 * math.log10(linear_value)