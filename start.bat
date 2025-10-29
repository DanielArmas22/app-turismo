@echo off
echo ========================================
echo   Guia Turistica Virtual
echo   Iniciando aplicacion...
echo ========================================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\" (
    echo Creando entorno virtual...
    python -m venv venv
    echo.
)

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate
echo.

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt --quiet
echo.

REM Iniciar aplicacion
echo Iniciando Streamlit...
echo La aplicacion se abrira en tu navegador
echo Presiona Ctrl+C para detener
echo.
streamlit run app.py

pause
