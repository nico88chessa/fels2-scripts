Setup ambiente venv

creazione ambiente virtuale python:

./python3 -m venv ~/workspace/fels2-scripts/venv/

Successivamente, aggiungere all'ambiente virtuale i seguenti pacchetti

<ol>
<li>./pip install bitarray</li>
<li>./pip install Pillow</li>
<li>./pip install pyside2</li>
</ol>

Per la parte ui, bisogna aggiungere i seguenti pacchetti:

Pacchetti da installare nell'ambiente virtuale:
<ol>
<li>pip install pyside2 (versione utilizzata: 5.14.1)</li>
</ol>

Comandi utili:
generazione .py da file .qrc
<tt>.\pyside2-rcc.exe C:\Users\nicola\workspace\csv-synchronizer\resources.qrc -o C:\Users\nicola\workspace\csv-synchronizer\resources.py</tt>

generazione eseguibile
1. andare nella cartella venv\Scripts
2. eseguire il comando:
<tt>.\pyinstaller.exe ..\\..\\main.py -w --distpath ..\\..\\dist</tt>

Nota per Pycharm:
in modalita' debug, i QTimer non funzionano correttamente in multithread con QThread.
Per farli funzionare, all'interno di PyCharm bisogna disabilitare la voce PyQt:
File - Settings - Python Debugger - PyQt Compatible NON FLAGGATO
Peccato che cosi' facendo il debug funziona solamente nel main thread (quindi e' impossibile 
debuggare in PyCharm in multithreading con Pyside 2 (PyCharm 2019.3))