#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
JOB XFLOW: GSD01_AbrirTXT
================================================================================

Nombre: GSD01_AbrirTXT - Apertura y escritura de archivo TXT
Descripción: Este job abre un archivo de texto, escribe "HOLA MUNDO", 
             mantiene el archivo abierto por 15 segundos y luego lo cierra.

Autor: [Tu Nombre]
Versión: 1.0.0
Fecha: 2024
Tags: archivos, txt, ejemplo, basico, demostracion

-------------------------------------------------------------------------------
PARÁMETROS DE ENTRADA:
-------------------------------------------------------------------------------
{
    "file_path": "ruta/del/archivo.txt",  // Opcional (default: "./output.txt")
    "message": "HOLA MUNDO",               // Opcional (default: "HOLA MUNDO")
    "wait_seconds": 15                      // Opcional (default: 15)
}

-------------------------------------------------------------------------------
SALIDA:
-------------------------------------------------------------------------------
{
    "status": "success|error",
    "message": "Descripción del resultado",
    "data": {
        "file_path": "ruta/completa/del/archivo.txt",
        "message_written": "HOLA MUNDO",
        "wait_time": 15,
        "file_exists": true,
        "file_size_bytes": 10
    }
}
================================================================================
"""

import argparse
import json
import logging
import sys
import os
import time
from datetime import datetime
from typing import Dict, Any

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - GSD01_AbrirTXT - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('XFlow_Job_GSD01')

def validate_params(params: Dict[str, Any]) -> bool:
    """
    Valida los parámetros de entrada del job.
    
    Args:
        params: Diccionario con los parámetros
        
    Returns:
        bool: True si son válidos, False si no
    """
    # Verificar tipos de datos si se proporcionan
    if 'wait_seconds' in params:
        try:
            wait_time = int(params['wait_seconds'])
            if wait_time < 0:
                logger.error("wait_seconds no puede ser negativo")
                return False
            params['wait_seconds'] = wait_time  # Asegurar que sea entero
        except (ValueError, TypeError):
            logger.error("wait_seconds debe ser un número válido")
            return False
    
    if 'message' in params and not isinstance(params['message'], str):
        logger.error("message debe ser un string")
        return False
    
    if 'file_path' in params and not isinstance(params['file_path'], str):
        logger.error("file_path debe ser un string")
        return False
    
    return True

def main(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Función principal: Abre un TXT, escribe "HOLA MUNDO", espera 15 segundos y cierra.
    
    Args:
        params: Diccionario con parámetros de configuración
        
    Returns:
        Dict con el resultado de la operación
    """
    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info("INICIANDO JOB: GSD01_AbrirTXT")
    logger.info("=" * 60)
    logger.info(f"Parámetros recibidos: {json.dumps(params, indent=2, ensure_ascii=False)}")
    
    # Valores por defecto
    file_path = params.get('file_path', './output.txt')
    message = params.get('message', 'HOLA MUNDO')
    wait_seconds = params.get('wait_seconds', 15)
    
    # Validar parámetros
    if not validate_params(params):
        return {
            "status": "error",
            "message": "Validación de parámetros fallida",
            "data": {
                "received_params": params,
                "defaults_used": {
                    "file_path": file_path,
                    "message": message,
                    "wait_seconds": wait_seconds
                }
            }
        }
    
    file_handle = None
    try:
        # PASO 1: Crear directorio si no existe
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            logger.info(f"Creando directorio: {directory}")
            os.makedirs(directory, exist_ok=True)
        
        # PASO 2: Abrir archivo en modo escritura
        logger.info(f"📄 Abriendo archivo: {file_path}")
        file_handle = open(file_path, 'w', encoding='utf-8')
        
        # PASO 3: Escribir mensaje
        logger.info(f"✍️ Escribiendo mensaje: '{message}'")
        file_handle.write(message)
        file_handle.flush()  # Asegurar que se escriba inmediatamente
        logger.info("✅ Mensaje escrito correctamente")
        
        # PASO 4: Mantener abierto por X segundos
        logger.info(f"⏳ Manteniendo archivo abierto durante {wait_seconds} segundos...")
        
        # Mostrar cuenta regresiva
        for i in range(wait_seconds, 0, -1):
            logger.info(f"   Cerrando en {i} segundos...")
            time.sleep(1)
        
        # PASO 5: Cerrar archivo
        logger.info("🔒 Cerrando archivo...")
        file_handle.close()
        file_handle = None
        logger.info("✅ Archivo cerrado correctamente")
        
        # Verificar que el archivo se creó correctamente
        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        
        logger.info("=" * 60)
        logger.info("✅ JOB COMPLETADO CON ÉXITO")
        logger.info("=" * 60)
        
        return {
            "status": "success",
            "message": f"Archivo procesado correctamente: se escribió '{message}' en {file_path}",
            "data": {
                "file_path": os.path.abspath(file_path),
                "message_written": message,
                "wait_time": wait_seconds,
                "file_exists": os.path.exists(file_path),
                "file_size_bytes": file_size,
                "execution_time_seconds": (datetime.now() - start_time).total_seconds(),
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except PermissionError as e:
        logger.error(f"❌ Error de permisos al escribir archivo: {str(e)}")
        return {
            "status": "error",
            "message": f"No se tienen permisos para escribir en {file_path}",
            "data": {
                "error_type": "PermissionError",
                "error_details": str(e),
                "file_path": file_path
            }
        }
        
    except IOError as e:
        logger.error(f"❌ Error de E/S al manipular archivo: {str(e)}")
        return {
            "status": "error",
            "message": f"Error de entrada/salida con el archivo",
            "data": {
                "error_type": "IOError",
                "error_details": str(e),
                "file_path": file_path
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Error inesperado: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": f"Error inesperado durante la ejecución: {str(e)}",
            "data": {
                "error_type": type(e).__name__,
                "error_details": str(e)
            }
        }
        
    finally:
        # Garantizar que el archivo se cierre incluso si hay error
        if file_handle and not file_handle.closed:
            logger.info("🔒 Cerrando archivo en bloque finally...")
            file_handle.close()
            logger.info("✅ Archivo cerrado en bloque finally")

if __name__ == "__main__":
    """
    Punto de entrada para ejecución desde XFlow
    """
    parser = argparse.ArgumentParser(description='GSD01_AbrirTXT - Job para escribir en TXT')
    parser.add_argument('--params', type=str, help='Parámetros en formato JSON', default='{}')
    
    args = parser.parse_args()
    
    try:
        # Parsear parámetros
        params = json.loads(args.params)
        logger.info("✅ Parámetros JSON parseados correctamente")
        
    except json.JSONDecodeError as e:
        logger.error(f"❌ Error parseando JSON: {str(e)}")
        logger.info("Usando parámetros por defecto...")
        params = {}
    
    # Ejecutar job
    result = main(params)
    
    # Imprimir resultado (XFlow capturará esto)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Código de salida
    sys.exit(0 if result['status'] == 'success' else 1)
