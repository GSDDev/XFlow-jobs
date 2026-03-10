#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
EJEMPLO DE ESTRUCTURA PARA JOB DE XFLOW
================================================================================

Nombre del Archivo: ProjectCode_ProjectName.py
Propósito: Este archivo sirve como template/ejemplo de cómo debe estructurarse
           un job para la plataforma XFlow.

-------------------------------------------------------------------------------
ESTRUCTURA OBLIGATORIA PARA JOBS DE XFLOW:
-------------------------------------------------------------------------------

1. ENCABEZADO DEL ARCHIVO:
   - Shebang (#!/usr/bin/env python3)
   - Codificación (utf-8)
   - Docstring con descripción detallada

2. IMPORTS:
   - Importar todas las librerías necesarias al inicio
   - Usar logging obligatoriamente para tracking

3. CONFIGURACIÓN DE LOGGING:
   - Configurar logging básico
   - Definir logger específico para el job

4. FUNCIÓN PRINCIPAL main():
   - Función que contiene la lógica principal del job
   - Recibe parámetros en formato diccionario
   - Retorna diccionario con resultados (status, message, data)

5. VALIDACIÓN DE ENTRADAS:
   - Validar todos los parámetros recibidos
   - Manejar casos edge y errores

6. BLOQUE if __name__ == "__main__":
   - Parsear argumentos de línea de comandos
   - Ejecutar función main()
   - Imprimir resultado en formato JSON

-------------------------------------------------------------------------------
FORMATO DE ENTRADA (esperado desde XFlow):
-------------------------------------------------------------------------------
Los parámetros se reciben a través de --params en formato JSON:
{
    "input_file": "ruta/al/archivo.csv",
    "delimiter": ",",
    "encoding": "utf-8",
    "options": {
        "remove_duplicates": true,
        "fill_na": 0
    }
}

-------------------------------------------------------------------------------
FORMATO DE SALIDA (requerido para XFlow):
-------------------------------------------------------------------------------
Siempre retornar un diccionario JSON con:
{
    "status": "success" | "error" | "warning",
    "message": "Descripción clara del resultado",
    "data": {
        "output_file": "ruta/al/resultado.csv",
        "records_processed": 1000,
        "execution_time": 2.5,
        "custom_data": {}
    }
}

-------------------------------------------------------------------------------
REQUISITOS MÍNIMOS:
-------------------------------------------------------------------------------
✔ Manejo de excepciones (try-catch)
✔ Logging en puntos clave
✔ Documentación de funciones (docstrings)
✔ Validación de parámetros
✔ Retorno estructurado
✔ Compatibilidad con argumentos CLI

-------------------------------------------------------------------------------
EJEMPLO DE USO DESDE TERMINAL:
-------------------------------------------------------------------------------
python ProjectCode_ProjectName.py --params '{"input_file": "datos.csv"}'

-------------------------------------------------------------------------------
AUTOR: [Tu Nombre]
VERSIÓN: 1.0.0
FECHA: 2024
TAGS: template, ejemplo, estructura, xflow
================================================================================
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from typing import Dict, Any, Optional

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.FileHandler('job_execution.log')  # Opcional: guardar en archivo
    ]
)

logger = logging.getLogger('XFlow_Job')  # Logger específico para XFlow

def validate_params(params: Dict[str, Any]) -> bool:
    """
    Valida que los parámetros requeridos estén presentes y sean válidos.
    
    Args:
        params: Diccionario con parámetros a validar
        
    Returns:
        bool: True si los parámetros son válidos, False en caso contrario
    """
    required_params = ['input_file']  # Lista de parámetros requeridos
    
    for param in required_params:
        if param not in params:
            logger.error(f"Parámetro requerido no encontrado: {param}")
            return False
    
    # Validaciones específicas según el tipo de parámetro
    if 'delimiter' in params and len(params['delimiter']) != 1:
        logger.warning(f"Delimitador inválido '{params['delimiter']}', usando ',' por defecto")
        params['delimiter'] = ','  # Asignar valor por defecto
    
    return True

def main(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Función principal del job para XFlow.
    
    Esta función contiene toda la lógica de negocio del job.
    
    Args:
        params: Diccionario con los parámetros de entrada proporcionados por XFlow
        
    Returns:
        Dict[str, Any]: Diccionario con:
            - status: "success", "error" o "warning"
            - message: Descripción del resultado
            - data: Datos adicionales del procesamiento
    """
    start_time = datetime.now()
    logger.info("=" * 50)
    logger.info(f"Iniciando job: ProjectCode_ProjectName")
    logger.info(f"Parámetros recibidos: {json.dumps(params, indent=2)}")
    
    try:
        # PASO 1: Validar parámetros de entrada
        if not validate_params(params):
            return {
                "status": "error",
                "message": "Validación de parámetros fallida",
                "data": {"received_params": params}
            }
        
        # PASO 2: Extraer parámetros con valores por defecto
        input_file = params.get('input_file')
        delimiter = params.get('delimiter', ',')
        encoding = params.get('encoding', 'utf-8')
        options = params.get('options', {})
        
        logger.info(f"Procesando archivo: {input_file}")
        logger.info(f"Configuración: delimiter='{delimiter}', encoding={encoding}")
        
        # PASO 3: Lógica principal del job
        # ----------------------------------------------------------------------
        # Aquí va tu código específico de procesamiento
        # Ejemplo:
        # data = read_csv(input_file, delimiter, encoding)
        # data = clean_data(data, options)
        # output_file = save_results(data)
        # ----------------------------------------------------------------------
        
        # Simulación de procesamiento (ejemplo)
        logger.info("Ejecutando lógica principal del job...")
        
        # Resultado simulado
        result_data = {
            "input_file": input_file,
            "output_file": f"processed_{input_file}",
            "records_processed": 1500,
            "execution_details": {
                "delimiter_used": delimiter,
                "encoding_used": encoding,
                "options_applied": options
            }
        }
        
        logger.info("Job completado exitosamente")
        status = "success"
        message = "Job ejecutado correctamente"
        
    except FileNotFoundError as e:
        logger.error(f"Archivo no encontrado: {str(e)}")
        status = "error"
        message = f"Error de archivo: {str(e)}"
        result_data = {}
        
    except PermissionError as e:
        logger.error(f"Error de permisos: {str(e)}")
        status = "error"
        message = f"Permiso denegado: {str(e)}"
        result_data = {}
        
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        status = "error"
        message = f"Error en la ejecución: {str(e)}"
        result_data = {}
    
    finally:
        # Calcular tiempo de ejecución
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        # Registrar tiempo de ejecución en el resultado
        if isinstance(result_data, dict):
            result_data['execution_time_seconds'] = execution_time
        
        logger.info(f"Tiempo de ejecución: {execution_time:.2f} segundos")
        logger.info("=" * 50)
    
    # Retornar resultado en formato estándar XFlow
    return {
        "status": status,
        "message": message,
        "data": result_data
    }

if __name__ == "__main__":
    """
    Punto de entrada para ejecución desde línea de comandos.
    XFlow ejecutará el job llamando a este bloque.
    """
    parser = argparse.ArgumentParser(description='Job para XFlow - ProjectCode_ProjectName')
    parser.add_argument('--params', type=str, 
                       help='Parámetros en formato JSON string',
                       default='{}')
    
    args = parser.parse_args()
    
    try:
        # Parsear los parámetros JSON
        params = json.loads(args.params)
        logger.info("Parámetros parseados correctamente")
        
    except json.JSONDecodeError as e:
        logger.error(f"Error parseando JSON de parámetros: {str(e)}")
        params = {}  # Usar diccionario vacío en caso de error
        
    # Ejecutar el job
    result = main(params)
    
    # Imprimir resultado como JSON (XFlow leerá esto)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Salir con código apropiado
    sys.exit(0 if result['status'] == 'success' else 1)
