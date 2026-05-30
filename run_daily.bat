@echo off
cd /d "C:\Users\Joyclyn\ClaudeCode\human-behaviour\website"
set PY="C:\Users\Joyclyn\AppData\Local\Programs\Python\Python311-arm64\python.exe"
%PY% generate_entry.py
%PY% publish.py
