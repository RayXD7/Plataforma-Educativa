import os
def generar_hash(tam=25):
    """
    Genera un hash aleatorio de tamaño especificado.
    Esta función utiliza el módulo 'os' para generar un hash aleatorio en formato binario.
    Si el tamaño especificado es menor o igual a 25, se ajusta automáticamente a 25 bytes.
    La función devuelve una lista que contiene:
    1. El hash en formato binario.
    2. El hash convertido a una cadena hexadecimal.
    Parámetros:
    tam (int): El tamaño deseado del hash en bytes. Por defecto es 25.
    Retorna:
    list: Una lista donde el primer elemento es el hash en formato binario
          y el segundo elemento es el hash en formato hexadecimal.
    """
    # Si el tamaño es menor o igual a 25, se establece a 25
    if tam <= 25:
        tam = 25
    
    # Genera un hash aleatorio de 'tam' bytes
    data = os.urandom(tam)
    
    return {'dato binario':data} , {'dato hexadecimal':data.hex()}

if __name__ == "__main__":
    # Imprime el hash generado en formato binario y en formato hexadecimal
    print(generar_hash())