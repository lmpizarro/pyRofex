from rava import dolar_mep_hoy


flujos = """
Bono,Fecha,Interés,Amortización,Total
pmm29,19/09/2024,2.21,7.69,9.90
pmm29,19/03/2025,1.99,7.69,9.68
pmm29,19/09/2025,1.77,7.69,9.46
pmm29,19/03/2026,1.55,7.69,9.24
pmm29,21/09/2026,1.34,7.69,9.03
pmm29,19/03/2027,1.09,7.69,8.78
pmm29,20/09/2027,0.89,7.69,8.58
pmm29,20/03/2028,0.66,7.69,8.35
pmm29,19/09/2028,0.44,7.69,8.13
pmm29,19/03/2029,0.22,7.72,7.94
sa24d,3/6/2024,3.87,7.50,11.37
sa24d,2/12/2024,3.49,7.50,10.99
sa24d,2/6/2025,3.19,12.50,15.69
sa24d,1/12/2025,2.64,12.50,15.14
sa24d,1/6/2026,2.13,12.50,14.63
sa24d,1/12/2026,1.59,12.50,14.09
sa24d,1/6/2027,1.06,12.50,13.56
sa24d,1/12/2027,0.53,12.50,13.03
bna26,19/07/2024,7.09,0.00,7.09
bna26,19/10/2024,2.38,0.00,2.38
bna26,19/01/2025,2.38,0.00,2.38
bna26,19/04/2025,2.33,0.00,2.33
bna26,19/07/2025,2.36,25.00,27.36
bna26,19/10/2025,1.79,25.00,26.79
bna26,19/01/2026,1.19,25.00,26.19
bna26,19/04/2026,0.58,25.00,25.58
ndt25,29/04/2024,3.41,7.69,11.10
ndt25,28/10/2024,3.10,7.69,10.79
ndt25,28/04/2025,2.91,7.69,10.60
ndt25,27/10/2025,2.63,7.69,10.32
ndt25,27/04/2026,2.38,7.69,10.07
ndt25,27/10/2026,2.12,7.69,9.81
ndt25,27/04/2027,1.85,7.69,9.54
ndt25,27/10/2027,1.59,7.69,9.28
ndt25,27/04/2028,1.32,7.69,9.01
ndt25,27/10/2028,1.06,7.69,8.75
ndt25,27/04/2029,0.79,7.69,8.48
ndt25,29/10/2029,0.54,7.69,8.23
ndt25,29/04/2030,0.27,7.72,7.99
ba37d,1/9/2024,3.13,1.83,4.96
ba37d,1/3/2025,3.19,2.25,5.44
ba37d,1/9/2025,3.12,2.25,5.37
ba37d,1/3/2026,3.04,2.90,5.94
ba37d,1/9/2026,2.95,2.90,5.85
ba37d,1/3/2027,2.85,3.28,6.13
ba37d,1/9/2027,2.74,3.28,6.02
ba37d,1/3/2028,2.63,3.47,6.10
ba37d,1/9/2028,2.52,3.47,5.99
ba37d,1/3/2029,2.40,3.79,6.19
ba37d,1/9/2029,2.28,3.79,6.07
ba37d,1/3/2030,2.15,3.08,5.23
ba37d,1/9/2030,2.05,3.08,5.13
ba37d,1/3/2031,1.95,3.59,5.54
ba37d,1/9/2031,1.83,3.59,5.42
ba37d,1/3/2032,1.71,3.77,5.48
ba37d,1/9/2032,1.59,3.77,5.36
ba37d,1/3/2033,1.46,3.94,5.40
ba37d,1/9/2033,1.33,3.94,5.27
ba37d,1/3/2034,1.20,4.20,5.40
ba37d,1/9/2034,1.06,4.20,5.26
ba37d,1/3/2035,0.92,4.40,5.32
ba37d,1/9/2035,0.78,4.40,5.18
ba37d,1/3/2036,0.63,4.67,5.30
ba37d,1/9/2036,0.47,4.67,5.14
ba37d,1/3/2037,0.32,4.83,5.15
ba37d,1/9/2037,0.16,4.83,4.99
co26,29/04/2024,0.61,3.13,3.74
co26,29/07/2024,0.56,3.13,3.68
co26,28/10/2024,0.50,3.13,3.62
co26,27/01/2025,0.44,3.13,3.57
co26,28/04/2025,0.39,3.13,3.52
co26,28/07/2025,0.33,3.13,3.46
co26,27/10/2025,0.28,3.13,3.40
co26,27/01/2026,0.22,3.13,3.35
co26,27/04/2026,0.17,3.13,3.29
co26,27/07/2026,0.11,3.13,3.24
co26,27/10/2026,0.06,3.13,3.18
al41,10/7/2024,1.76,0.00,1.76
al41,9/1/2025,1.74,0.00,1.74
al41,10/7/2025,1.76,0.00,1.76
al41,9/1/2026,1.74,0.00,1.74
al41,10/7/2026,1.76,0.00,1.76
al41,11/1/2027,1.76,0.00,1.76
al41,12/7/2027,1.76,0.00,1.76
al41,10/1/2028,1.73,3.57,5.30
al41,10/7/2028,1.69,3.57,5.26
al41,9/1/2029,1.62,3.57,5.19
al41,10/7/2029,1.57,3.57,5.14
al41,9/1/2030,2.08,3.57,5.65
al41,10/7/2030,2.01,3.57,5.58
al41,9/1/2031,1.90,3.57,5.47
al41,10/7/2031,1.84,3.57,5.41
al41,9/1/2032,1.73,3.57,5.30
al41,12/7/2032,1.68,3.57,5.25
al41,10/1/2033,1.55,3.57,5.12
al41,11/7/2033,1.49,3.57,5.06
al41,9/1/2034,1.38,3.57,4.95
al41,10/7/2034,1.31,3.57,4.88
al41,9/1/2035,1.21,3.57,4.78
al41,10/7/2035,1.14,3.57,4.71
al41,9/1/2036,1.04,3.57,4.61
al41,10/7/2036,0.96,3.57,4.53
al41,9/1/2037,0.87,3.57,4.44
al41,10/7/2037,0.79,3.57,4.36
al41,11/1/2038,0.70,3.57,4.27
al41,12/7/2038,0.61,3.57,4.18
al41,10/1/2039,0.52,3.57,4.09
al41,11/7/2039,0.44,3.57,4.01
al41,9/1/2040,0.35,3.57,3.92
al41,10/7/2040,0.26,3.57,3.83
al41,9/1/2041,0.17,3.57,3.74
al41,10/7/2041,0.09,3.61,3.70
al30,10/7/2024,0.38,4.00,4.38
al30,9/1/2025,0.36,8.00,8.36
al30,10/7/2025,0.33,8.00,8.33
al30,9/1/2026,0.30,8.00,8.30
al30,10/7/2026,0.27,8.00,8.27
al30,11/1/2027,0.24,8.00,8.24
al30,12/7/2027,0.21,8.00,8.21
al30,10/1/2028,0.42,8.00,8.42
al30,10/7/2028,0.35,8.00,8.35
al30,9/1/2029,0.28,8.00,8.28
al30,10/7/2029,0.21,8.00,8.21
al30,9/1/2030,0.14,8.00,8.14
al30,10/7/2030,0.07,8.00,8.07
BPOD7,31/10/2024,4.21,0.00,4.21
BPOD7,30/04/2025,2.50,0.00,2.50
BPOD7,31/10/2025,2.50,0.00,2.50
BPOD7,30/04/2026,2.50,0.00,2.50
BPOD7,31/10/2026,2.50,0.00,2.50
BPOD7,30/04/2027,2.50,50.00,52.50
BPOD7,31/10/2027,1.25,50.00,51.25
bpy26,31/08/2024,1.45,0.00,1.45
bpy26,30/11/2024,0.75,0.00,0.75
bpy26,28/02/2025,0.73,0.00,0.73
bpy26,31/05/2025,0.76,0.00,0.76
bpy26,31/08/2025,0.75,0.00,0.75
bpy26,30/11/2025,0.75,33.00,33.75
bpy26,28/02/2026,0.49,33.00,33.49
bpy26,31/05/2026,0.26,34.00,34.26
bpj25,31/07/2024,0.00,8.33,8.33
bpj25,31/08/2024,0.00,8.33,8.33
bpj25,30/09/2024,0.00,8.33,8.33
bpj25,31/10/2024,0.00,8.33,8.33
bpj25,30/11/2024,0.00,8.33,8.33
bpj25,31/12/2024,0.00,8.33,8.33
bpj25,31/01/2025,0.00,8.33,8.33
bpj25,28/02/2025,0.00,8.33,8.33
bpj25,31/03/2025,0.00,8.33,8.33
bpj25,30/04/2025,0.00,8.33,8.33
bpj25,31/05/2025,0.00,8.33,8.33
bpj25,30/06/2025,0.00,8.37,8.37
bb37d,1/9/2024,2.75,0.00,2.75
bb37d,1/3/2025,2.94,0.00,2.94
bb37d,1/9/2025,2.94,0.00,2.94
bb37d,1/3/2026,2.94,0.00,2.94
bb37d,1/9/2026,2.94,0.00,2.94
bb37d,1/3/2027,2.94,0.00,2.94
bb37d,1/9/2027,2.94,0.00,2.94
bb37d,1/3/2028,2.94,0.00,2.94
bb37d,1/9/2028,2.94,0.75,3.69
bb37d,1/3/2029,2.92,0.75,3.67
bb37d,1/9/2029,2.89,0.75,3.64
bb37d,1/3/2030,2.87,6.15,9.02
bb37d,1/9/2030,2.69,6.15,8.84
bb37d,1/3/2031,2.51,6.35,8.86
bb37d,1/9/2031,2.32,6.35,8.67
bb37d,1/3/2032,2.14,6.35,8.49
bb37d,1/9/2032,1.95,6.35,8.30
bb37d,1/3/2033,1.76,6.35,8.11
bb37d,1/9/2033,1.58,6.35,7.93
bb37d,1/3/2034,1.39,5.90,7.29
bb37d,1/9/2034,1.22,5.90,7.12
bb37d,1/3/2035,1.04,5.90,6.94
bb37d,1/9/2035,0.87,5.90,6.77
bb37d,1/3/2036,0.70,5.90,6.60
bb37d,1/9/2036,0.52,5.90,6.42
bb37d,1/3/2037,0.35,5.98,6.33
bb37d,1/9/2037,0.18,5.97,6.15
gd46,10/7/2024,1.82,0.00,1.82
gd46,9/1/2025,2.05,2.27,4.32
gd46,10/7/2025,2.03,2.27,4.30
gd46,9/1/2026,1.96,2.27,4.23
gd46,10/7/2026,1.93,2.27,4.20
gd46,11/1/2027,1.89,2.27,4.16
gd46,12/7/2027,1.84,2.27,4.11
gd46,10/1/2028,1.87,2.27,4.14
gd46,10/7/2028,1.84,2.27,4.11
gd46,9/1/2029,2.03,2.27,4.30
gd46,10/7/2029,2.00,2.27,4.27
gd46,9/1/2030,1.92,2.27,4.19
gd46,10/7/2030,1.89,2.27,4.16
gd46,9/1/2031,1.81,2.27,4.08
gd46,10/7/2031,1.77,2.27,4.04
gd46,9/1/2032,1.70,2.27,3.97
gd46,12/7/2032,1.68,2.27,3.95
gd46,10/1/2033,1.57,2.27,3.84
gd46,11/7/2033,1.54,2.27,3.81
gd46,9/1/2034,1.46,2.27,3.73
gd46,10/7/2034,1.43,2.27,3.70
gd46,9/1/2035,1.36,2.27,3.63
gd46,10/7/2035,1.32,2.27,3.59
gd46,9/1/2036,1.24,2.27,3.51
gd46,10/7/2036,1.20,2.27,3.47
gd46,9/1/2037,1.13,2.27,3.40
gd46,10/7/2037,1.09,2.27,3.36
gd46,11/1/2038,1.03,2.27,3.30
gd46,12/7/2038,0.97,2.27,3.24
gd46,10/1/2039,0.90,2.27,3.17
gd46,11/7/2039,0.86,2.27,3.13
gd46,9/1/2040,0.79,2.27,3.06
gd46,10/7/2040,0.74,2.27,3.01
gd46,9/1/2041,0.68,2.27,2.95
gd46,10/7/2041,0.63,2.27,2.90
gd46,9/1/2042,0.57,2.27,2.84
gd46,10/7/2042,0.52,2.27,2.79
gd46,9/1/2043,0.45,2.27,2.72
gd46,10/7/2043,0.40,2.27,2.67
gd46,11/1/2044,0.35,2.27,2.62
gd46,11/7/2044,0.29,2.27,2.56
gd46,9/1/2045,0.23,2.27,2.50
gd46,10/7/2045,0.17,2.27,2.44
gd46,9/1/2046,0.12,2.27,2.39
gd46,10/7/2046,0.06,2.39,2.45
bc37d,1/9/2024,2.50,0.00,2.50
bc37d,1/3/2025,2.63,0.00,2.63
bc37d,1/9/2025,2.63,0.00,2.63
bc37d,1/3/2026,2.63,0.00,2.63
bc37d,1/9/2026,2.63,0.00,2.63
bc37d,1/3/2027,2.63,0.00,2.63
bc37d,1/9/2027,2.63,0.00,2.63
bc37d,1/3/2028,2.63,0.00,2.63
bc37d,1/9/2028,2.63,0.75,3.38
bc37d,1/3/2029,2.61,0.75,3.36
bc37d,1/9/2029,2.59,0.75,3.34
bc37d,1/3/2030,2.57,6.15,8.72
bc37d,1/9/2030,2.40,6.15,8.55
bc37d,1/3/2031,2.24,6.35,8.59
bc37d,1/9/2031,2.08,6.35,8.43
bc37d,1/3/2032,1.91,6.35,8.26
bc37d,1/9/2032,1.74,6.35,8.09
bc37d,1/3/2033,1.58,6.35,7.93
bc37d,1/9/2033,1.41,6.35,7.76
bc37d,1/3/2034,1.24,5.90,7.14
bc37d,1/9/2034,1.09,5.90,6.99
bc37d,1/3/2035,0.93,5.90,6.83
bc37d,1/9/2035,0.78,5.90,6.68
bc37d,1/3/2036,0.62,5.90,6.52
bc37d,1/9/2036,0.47,5.90,6.37
bc37d,1/3/2037,0.31,5.98,6.29
bc37d,1/9/2037,0.16,5.97,6.13
ymcho,13/05/2024,1.40,7.69,9.09
ymcho,12/8/2024,1.20,7.69,8.89
ymcho,12/11/2024,1.04,7.69,8.73
ymcho,12/2/2025,0.87,7.69,8.56
ymcho,12/5/2025,0.69,7.69,8.38
ymcho,12/8/2025,0.52,7.69,8.21
ymcho,12/11/2025,0.35,7.69,8.04
ymcho,12/2/2026,0.17,7.72,7.89
tlc1o,18/07/2024,4.00,0.00,4.00
tlc1o,21/01/2025,4.07,0.00,4.07
tlc1o,18/07/2025,3.93,0.00,3.93
tlc1o,20/01/2026,4.04,0.00,4.04
tlc1o,20/07/2026,4.00,100.00,104.00
ruc7o,21/06/2024,4.19,0.00,4.19
ruc7o,12/1/2025,4.21,100.00,104.21
mgcho,4/5/2024,2.49,0.00,2.49
mgcho,4/11/2024,2.52,0.00,2.52
mgcho,4/5/2025,2.47,100.00,102.47
yca6o,29/07/2024,4.25,0,4.25
yca6o,28/01/2025,4.23,0,4.23
yca6o,28/07/2025,4.25,100,104.25
mtcgo,2/4/2024,2.80,0.00,2.80
mtcgo,30/06/2024,2.68,0.00,2.68
mtcgo,30/09/2024,2.74,0.00,2.74
mtcgo,30/12/2024,2.74,0.00,2.74
mtcgo,31/03/2025,2.74,0.00,2.74
mtcgo,30/06/2025,2.74,0.00,2.74
mtcgo,30/09/2025,2.74,0.00,2.74
mtcgo,30/12/2025,2.74,0.00,2.74
mtcgo,30/03/2026,2.74,0.00,2.74
mtcgo,30/06/2026,2.74,100.00,102.74
ymcjo,2/4/2024,3.50,0.00,3.50
ymcjo,30/09/2024,3.46,0.00,3.46
ymcjo,31/03/2025,3.50,0.00,3.50
ymcjo,30/09/2025,3.50,0.00,3.50
ymcjo,30/03/2026,3.50,0.00,3.50
ymcjo,30/09/2026,3.50,0.00,3.50
ymcjo,30/03/2027,3.50,0.00,3.50
ymcjo,30/09/2027,3.50,0.00,3.50
ymcjo,30/03/2028,3.50,0.00,3.50
ymcjo,2/10/2028,3.54,0.00,3.54
ymcjo,3/4/2029,3.52,0.00,3.52
ymcjo,1/10/2029,3.46,0.00,3.46
ymcjo,1/4/2030,3.50,0.00,3.50
ymcjo,30/09/2030,3.48,25.00,28.48
ymcjo,31/03/2031,2.63,0.00,2.63
ymcjo,30/09/2031,2.63,18.75,21.38
ymcjo,30/03/2032,1.97,0.00,1.97
ymcjo,30/09/2032,1.97,14.06,16.03
ymcjo,30/03/2033,1.48,0.00,1.48
ymcjo,30/09/2033,1.48,42.19,43.67
ymcjo,1/9/2034,1.09,5.90,6.99
ymcjo,1/3/2035,0.93,5.90,6.83
ymcjo,1/9/2035,0.78,5.90,6.68
ymcjo,1/3/2036,0.62,5.90,6.52
ymcjo,1/9/2036,0.47,5.90,6.37
ymcjo,1/3/2037,0.31,5.98,6.29
ymcjo,1/9/2037,0.16,5.97,6.13
ymcio,1/7/2024,4.50,0.00,4.50
ymcio,30/12/2024,4.48,0.00,4.48
ymcio,30/06/2025,4.50,0.00,4.50
ymcio,30/12/2025,4.50,0.00,4.50
ymcio,30/06/2026,4.50,14.28,18.78
ymcio,30/12/2026,3.86,14.28,18.14
ymcio,30/06/2027,3.21,14.28,17.49
ymcio,30/12/2027,2.57,14.28,16.85
ymcio,30/06/2028,1.93,14.28,16.21
ymcio,1/1/2029,1.29,14.28,15.57
ymcio,2/7/2029,0.65,14.32,14.97
ymcqo,13/06/2024,2.51,0.00,2.51
ymcqo,13/12/2024,2.51,0.00,2.51
ymcqo,13/06/2025,2.49,0.00,2.49
ymcqo,13/12/2025,2.51,0.00,2.51
ymcqo,13/02/2026,0.85,100.00,100.85
"""

usdMep = 991.25 # dolar_mep_hoy()

import requests
from bs4 import BeautifulSoup
import json

def closePrice(bono='ba37d'):
    ''' devuelve la ultima cotizacion de un bono en pesos expresado en dolar'''
    url = f'https://www.rava.com/perfil/{bono}'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    table = soup.find("main").find("perfil-p")
    last = 0
    try:
        return float(json.loads(table.attrs[':res'])['cuad_tecnico'][0]['ultimonum'])
    except:
        print(bono)
        return last

prices = {'pmm29': 66700.0, 'ba37d': 44370.0, 'sa24d': 80500.0, 'bna26': 106440.0, 'ndt25':91000,
          'co26': 35400.0, 'al41': 43595.0, 'al30': 55790.0, 'BPOD7': 74550, 'bpy26': 80700.0,
          'bpj25': 95380.0, 'bb37d': 41000.0, 'gd46': 50780.0, 'bc37d': 39000.0, 'tlc1o': 104000,
          'ruc7o': 103000, 'mgcho': 100000, 'mtcgo': 107500, 'ymcjo': 92190, 'ymcio': 106180,
          'yca6o': 104700, 'ymcho': 66420.0, 'ymcqo': 97480}
bonos = [
         {'ticker': 'pmm29', 'value': 68500.0/usdMep,  'tipo': 'bono', 'estado': 'MZA', 'per': 2},
         {'ticker': 'ba37d', 'value': 43900.0/usdMep,  'tipo': 'bono', 'estado': 'PBA', 'per': 2},
         {'ticker': 'sa24d', 'value': 81000.0/usdMep,  'tipo': 'bono', 'estado': 'SAL', 'per': 2},
         {'ticker': 'bna26', 'value': 106700.0/usdMep, 'tipo': 'bono', 'estado': 'NQN', 'per': 4},
         {'ticker': 'ndt25', 'value': 92000.0/usdMep,  'tipo': 'bono', 'estado': 'NQN', 'per': 2},
         {'ticker': 'co26',  'value': 36700.0/usdMep,  'tipo': 'bono', 'estado': 'CBA', 'per': 4},
         {'ticker': 'al41',  'value': 45500.0/usdMep,  'tipo': 'bono', 'estado': 'ARG', 'per': 2},
         {'ticker': 'al30',  'value': 55070.0/usdMep,  'tipo': 'bono', 'estado': 'ARG', 'per': 2},
         {'ticker': 'BPOD7', 'value': 76100.0/usdMep,  'tipo': 'bono', 'estado': 'ARG', 'per': 2},
         {'ticker': 'bpy26', 'value': 81170.0/usdMep,  'tipo': 'bono', 'estado': 'ARG', 'per': 4},
         {'ticker': 'bpj25', 'value': 97850.0/usdMep,  'tipo': 'bono', 'estado': 'ARG', 'per': 12},
         {'ticker': 'bb37d', 'value': 39600.0/usdMep,  'tipo': 'bono', 'estado': 'PBA', 'per': 2},
         {'ticker': 'gd46',  'value': 49890.0/usdMep,  'tipo': 'bono', 'estado': 'ARG', 'per': 2 },
         {'ticker': 'bc37d', 'value': 38000.0/usdMep,  'tipo': 'bono', 'estado': 'PBA', 'per': 2 },
         {'ticker': 'tlc1o', 'value': 107600.0/usdMep, 'tipo': 'on',   'estado': 'TECO',  'per': 2},
         {'ticker': 'ruc7o', 'value': 106000.0/usdMep, 'tipo': 'on',   'estado': 'MSU',   'per': 1},
         {'ticker': 'mgcho', 'value': 105000.0/usdMep, 'tipo': 'on',   'estado': 'PAMPA', 'per': 2},
         {'ticker': 'mtcgo', 'value': 113800.0/usdMep, 'tipo': 'on',   'estado': 'MTELL', 'per': 4},
         {'ticker': 'ymcjo', 'value': 99350.0/usdMep,  'tipo': 'on',   'estado': 'YPF',   'per': 2},
         {'ticker': 'ymcio', 'value': 108900.0/usdMep, 'tipo': 'on',   'estado': 'YPF',   'per': 2},
         {'ticker': 'yca6o', 'value': 108500.0/usdMep, 'tipo': 'on',   'estado': 'YPF',   'per': 2},
         {'ticker': 'ymcho', 'value': 68600.0/usdMep,  'tipo': 'on',   'estado': 'YPF',   'per': 4 },
         {'ticker': 'ymcqo', 'value': 100790.0/usdMep, 'tipo': 'on',   'estado': 'YPF',   'per': 2},
]

bonos__ = [
         {'ticker': 'ae38', 'value': 49.24,  'tipo': 'bono', 'estado': 'ARG', 'per': 2},
         {'ticker': 'al35', 'value': 45.6,  'tipo': 'bono', 'estado': 'ARG', 'per': 2},
         {'ticker': 'al41', 'value': 43.75,  'tipo': 'bono', 'estado': 'ARG', 'per': 2},
         {'ticker': 'gd46', 'value': 49.45,  'tipo': 'bono', 'estado': 'ARG', 'per': 2},
         {'ticker': 'al29', 'value': 56.6,  'tipo': 'bono', 'estado': 'ARG', 'per': 2},
         {'ticker': 'ba37d', 'value': 43740/991.25,  'tipo': 'bono', 'estado': 'PBA', 'per': 2},
]

# print({b['ticker']:closePrice(b['ticker']) for b in bonos})

for b in bonos:
    b['value'] = prices[b['ticker']] / usdMep
