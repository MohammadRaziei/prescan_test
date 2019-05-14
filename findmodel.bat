@echo off
python json_path.py models.json | FINDSTR %1
PAUSE