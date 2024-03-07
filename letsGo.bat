@echo off

:: Activar el entorno virtual
call env\Scripts\activate

python getAnimeSeasons.py
python getFirstEpisode.py
python getAllLInks.py
