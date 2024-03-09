@echo off
setlocal

rem Comprobar si la carpeta env existe
if exist "env" (
    rem Activar el entorno virtual
    call env\Scripts\activate
) else (
    rem Crear un nuevo entorno virtual
    virtualenv env
    call env\Scripts\activate
    rem Instalar los requisitos
    pip install -r requirements.txt
)

rem Ejecutar el script de interfaz en Python
python interface.py

echo Put the anime for example "Boku no hero" / "Berserk" 
echo you will get a json with all chapters in the path

endlocal