@echo off
:: Crear el entorno virtual
virtualenv env

:: Activar el entorno virtual
call env\Scripts\activate

:: Instalar los requisitos desde requirements.txt
pip install scrapy==2.11.1
pip install -r requirements.txt
