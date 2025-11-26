import time
from collections import Counter
import matplotlib.pyplot as plt

def leerArchivoFNA(ruta, lineas=20):
    secuencia = ""
    with open(ruta, "r") as f:
        contador = 0
        for linea in f:
            if not linea.startswith(">"):
                secuencia += linea.strip().upper()
                contador += 1
                if contador >= lineas:
                    break
    return secuencia

# Funcion auxiliar
def contarRepeticiones(secuencia, patron):
    conteo = 0
    for i in range(len(secuencia) - len(patron) + 1):
        if secuencia[i:i + len(patron)] == patron:
            conteo += 1
    return conteo

def esPalindromo(cadena):
    return cadena == cadena[::-1]

# Fuerza bruta
def palindromoFuerzaBruta(cadena):

    if len(cadena) == 0:
        return ""

    mejor_palindromo = cadena[0]
    max_longitud = 1

    # Probar todas las subcadenas posibles
    for i in range(len(cadena)):
        for j in range(i + max_longitud, len(cadena) + 1):
            subcadena = cadena[i:j]
            if esPalindromo(subcadena) and len(subcadena) > max_longitud:
                max_longitud = len(subcadena)
                mejor_palindromo = subcadena

    return mejor_palindromo

# divide y venceras
def palindromoDyV(cadena):
    if len(cadena) == 0:
        return ""
    if len(cadena) == 1:
        return cadena

    mitad = len(cadena) // 2
    izquierda = palindromoDyV(cadena[:mitad])
    derecha = palindromoDyV(cadena[mitad:])
    centro = palindromoCentral(cadena, mitad)

    return max([izquierda, derecha, centro], key=len)

def palindromoCentral(cadena, mitad):
    """Expande desde el centro para buscar palíndromos."""
    mejor = ""
    for centro in range(mitad - 1, mitad + 2):
        if centro < 0 or centro >= len(cadena):
            continue

        # Palíndromos de longitud impar
        i, j = centro, centro
        while i >= 0 and j < len(cadena) and cadena[i] == cadena[j]:
            if (j - i + 1) > len(mejor):
                mejor = cadena[i:j + 1]
            i -= 1
            j += 1

        # Palíndromos de longitud par
        i, j = centro, centro + 1
        while i >= 0 and j < len(cadena) and cadena[i] == cadena[j]:
            if (j - i + 1) > len(mejor):
                mejor = cadena[i:j + 1]
            i -= 1
            j += 1

    return mejor

# Programacion Dinamica
def palindromoPD(cadena):

    n = len(cadena)
    if n == 0:
        return ""

    # Tabla DP: tabla[i][j] indica si cadena[i:j+1] es palíndromo
    tabla = [[False] * n for _ in range(n)]
    inicio = 0
    maxLen = 1

    # Todos los caracteres individuales son palíndromos
    for i in range(n):
        tabla[i][i] = True

    # Verificar palíndromos de longitud 2
    for i in range(n - 1):
        if cadena[i] == cadena[i + 1]:
            tabla[i][i + 1] = True
            inicio = i
            maxLen = 2

    # Verificar palíndromos de longitud >= 3
    for k in range(3, n + 1):
        for i in range(n - k + 1):
            j = i + k - 1
            if cadena[i] == cadena[j] and tabla[i + 1][j - 1]:
                tabla[i][j] = True
                if k > maxLen:
                    inicio = i
                    maxLen = k

    return cadena[inicio:inicio + maxLen]

# Voraz - Expansion desde el centro
def palindromoVoraz(cadena):

    if len(cadena) == 0:
        return ""

    mejor_palindromo = cadena[0]

    # ESTRATEGIA VORAZ: Probar todos los centros posibles
    for i in range(len(cadena)):
        pal_impar = expandirDesdeCentro(cadena, i, i)  # Centro único (longitud impar)
        pal_par = expandirDesdeCentro(cadena, i, i + 1)  # Centro doble (longitud par)

        # Seleccionar el mejor localmente (decisión voraz)
        mejor_local = max([pal_impar, pal_par], key=len)

        # Actualizar el mejor global
        if len(mejor_local) > len(mejor_palindromo):
            mejor_palindromo = mejor_local

    return mejor_palindromo

def expandirDesdeCentro(cadena, izquierda, derecha):

    while (izquierda >= 0 and derecha < len(cadena) and
           cadena[izquierda] == cadena[derecha]):
        izquierda -= 1
        derecha += 1
    # Al salir del while, retrocedemos un paso para obtener el palíndromo válido
    return cadena[izquierda + 1:derecha]

# Comparacion y analisis
def compararMetodos(secuencia, longitudes=[8, 12, 16, 20]):
    """Compara todos los métodos para diferentes longitudes de subsecuencia."""
    resultados = []

    print("Comparación de algoritmmos para la busqueda de palindromos")

    for n in longitudes:
        if n > len(secuencia):
            continue

        subcadena = secuencia[:n]
        print(f"\n{' '}")
        print(f"Longitud n = {n}")
        print(f"{' '}")

        tiempos = {}
        palindromos = {}

        # 1. Fuerza Bruta (solo para n pequeños)
        if n <= 20:
            inicio = time.time()
            palFB = palindromoFuerzaBruta(subcadena)
            tiempoFB = time.time() - inicio
            tiempos['Fuerza Bruta'] = tiempoFB
            palindromos['Fuerza Bruta'] = palFB
            repFB = contarRepeticiones(secuencia, palFB)
            print(f"Fuerza Bruta: '{palFB}' ({len(palFB)} bases)")
            print(f"  Repeticiones: {repFB}, Tiempo: {tiempoFB:.5f}s")

        # 2. Divide y Vencerás
        inicio = time.time()
        palDyV = palindromoDyV(subcadena)
        tiempoDyV = time.time() - inicio
        tiempos['Divide y Vencerás'] = tiempoDyV
        palindromos['Divide y Vencerás'] = palDyV
        repDyV = contarRepeticiones(secuencia, palDyV)
        print(f"Divide y Vencerás: '{palDyV}' ({len(palDyV)} bases)")
        print(f"  Repeticiones: {repDyV}, Tiempo: {tiempoDyV:.5f}s")

        # 3. Programación Dinámica
        inicio = time.time()
        palPD = palindromoPD(subcadena)
        tiempoPD = time.time() - inicio
        tiempos['Programación Dinámica'] = tiempoPD
        palindromos['Programación Dinámica'] = palPD
        repPD = contarRepeticiones(secuencia, palPD)
        print(f"Programación Dinámica: '{palPD}' ({len(palPD)} bases)")
        print(f"  Repeticiones: {repPD}, Tiempo: {tiempoPD:.5f}s")

        # 4. Algoritmo Voraz
        inicio = time.time()
        palVoraz = palindromoVoraz(subcadena)
        tiempoVoraz = time.time() - inicio
        tiempos['Algoritmo Voraz'] = tiempoVoraz
        palindromos['Algoritmo Voraz'] = palVoraz
        repVoraz = contarRepeticiones(secuencia, palVoraz)
        print(f"Algoritmo Voraz: '{palVoraz}' ({len(palVoraz)} bases)")
        print(f"  Repeticiones: {repVoraz}, Tiempo: {tiempoVoraz:.5f}s")

        resultados.append((n, tiempos, palindromos))

    return resultados

def graficarResultados(resultados):
    """Genera gráficos comparativos de tiempos de ejecución."""
    if not resultados:
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Definir todos los métodos posibles desde el principio
    todos_metodos = ['Fuerza Bruta', 'Divide y Vencerás', 'Programación Dinámica', 'Algoritmo Voraz']
    colores = ['violet', 'skyblue', 'limegreen', 'pink']

    # Gráfico 1: Tiempos de ejecución
    for i, metodo in enumerate(todos_metodos):
        x = [r[0] for r in resultados if metodo in r[1]]
        y = [r[1][metodo] for r in resultados if metodo in r[1]]
        if x and y:
            ax1.plot(x, y, 'o-', label=metodo, color=colores[i], linewidth=2, markersize=8)

    ax1.set_xlabel('Tamaño de la cadena (n)')
    ax1.set_ylabel('Tiempo de ejecución (segundos)')
    ax1.set_title('Comparación de Tiempos de Ejecución\n(Menor es mejor)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Gráfico 2: Longitudes de palíndromos encontrados
    for i, metodo in enumerate(todos_metodos):
        x = [r[0] for r in resultados if metodo in r[2]]
        y = [len(r[2][metodo]) for r in resultados if metodo in r[2]]
        if x and y:
            ax2.plot(x, y, 's-', label=metodo, color=colores[i], linewidth=2, markersize=8)

    ax2.set_xlabel('Tamaño de la cadena (n)')
    ax2.set_ylabel('Longitud del palíndromo encontrado')
    ax2.set_title('Efectividad en Encontrar Palíndromos\n(Mayor es mejor)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

def main():
    ruta = "Datos/GCA_000864885.1_ViralProj15500_genomic.fna"

    secuencia = leerArchivoFNA(ruta)
    print(f"Se leyeron las primeras 20 lineas del archivo ({len(secuencia)} bases)")
    print(f"Primeros 50 caracteres: {secuencia[:50]}...")

    # Comparación de algoritmos
    resultados = compararMetodos(secuencia, longitudes=[8, 12, 16, 20])

    # Gráficos comparativos
    graficarResultados(resultados)

if __name__ == "__main__":
    main()