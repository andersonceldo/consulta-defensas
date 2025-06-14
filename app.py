# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1A6nYUyOabSo3lhooiVweSj0sbW2zrhqa
"""

import pandas as pd
from datetime import datetime
import streamlit as st
import os

# Configuración de página
st.set_page_config(page_title="Consulta de Defensas UTPL", page_icon="🎓")

# Cargar los datos desde CSV o Excel
@st.cache_data
def load_data():
    try:
        # Buscar archivo de datos
        if os.path.exists('Separador_en_Python.csv'):
            df = pd.read_csv('Separador_en_Python.csv', dtype={'CEDULA': str})
        elif os.path.exists('Separador en Python.xlsx'):
            df = pd.read_excel('Separador en Python.xlsx', header=None)
            
            # Buscar fila que contiene "CEDULA"
            for idx, row in df.iterrows():
                if 'CEDULA' in str(row.values):
                    headers = row
                    data_rows = df.iloc[idx+1:]
                    break
            
            # Asignar encabezados y limpiar
            data_rows.columns = headers
            df = data_rows.reset_index(drop=True)

            # Limpiar columna CEDULA y convertir FECHA
            df['CEDULA'] = df['CEDULA'].astype(str).str.strip()
            if 'FECHA SIMPLE' in df.columns:
                df['FECHA SIMPLE'] = pd.to_datetime(df['FECHA SIMPLE'], errors='coerce')
        else:
            return None, "Archivo no encontrado. Verifique que 'Separador en Python.xlsx' esté en la carpeta raíz."

        return df, None

    except Exception as e:
        return None, f"Error al cargar los datos: {str(e)}"

# Función de consulta optimizada
def consultar_defensa(cedula):
    df, error = load_data()
    if error or df is None:
        return None, error or "Datos no disponibles."

    try:
        estudiante = df[df['CEDULA'].str.strip() == cedula.strip()]
        if estudiante.empty:
            return None, "No se encontró ningún estudiante con esa cédula."

        datos = estudiante.iloc[0]
        hoy = datetime.now().date()

        fecha_defensa = datos['FECHA SIMPLE'].date() if pd.notna(datos['FECHA SIMPLE']) else None
        fecha_str = datos['FECHA SIMPLE'].strftime('%d/%m/%Y') if fecha_defensa else 'No programado'

        info = {
            'nombre': datos.get('APELLIDOS Y NOMBRES', 'No disponible'),
            'opcion': datos.get('OPCION DE TITULACIÓN EX. COM./TIC/TT', 'No especificada'),
            'fecha': fecha_str,
            'hora': datos.get('HORA', 'No especificada'),
            'enlace': datos.get('ENLACES', '#'),
            'hoy': fecha_defensa == hoy if fecha_defensa else False
        }

        return info, None

    except Exception as e:
        return None, f"Error al procesar la consulta: {str(e)}"

# Interfaz de usuario mejorada
def main():
    st.title("🎓 Consulta de Defensas de Titulación - UTPL")
    st.markdown("Ingrese su número de cédula para conocer sus detalles de defensa.")

    cedula = st.text_input("Cédula:", placeholder="Ejemplo: 1234567890")

    if st.button("Consultar", type="primary"):
        if not cedula or not cedula.isdigit():
            st.warning("Por favor ingrese una cédula válida (solo números).")
        else:
            with st.spinner("Buscando información..."):
                info, error = consultar_defensa(cedula)

                if error:
                    st.error(error)
                else:
                    st.success(f"Información encontrada para: **{info['nombre']}**")
                    st.write(f"**Opción de titulación:** {info['opcion']}")
                    
                    if info['hoy']:
                        st.balloons()
                        st.warning("⚠️ ¡Tienes defensa HOY!")
                        st.write(f"**Fecha:** {info['fecha']}")
                        st.write(f"**Hora:** {info['hora']}")
                        if info['enlace'].startswith(('http://', 'https://')): 
                            st.markdown(f"[🔗 Unirse a la reunión]({info['enlace']})")
                    else:
                        st.info("📅 Hoy no tienes defensa programada.")
                        st.write(f"**Próximo evento:** {info['fecha']} - {info['hora']}")

    st.markdown("---")
    st.caption("© 2025 | Sistema de Consulta de Defensas | UTPL")

if __name__ == "__main__":
    main()
