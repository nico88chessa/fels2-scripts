Setup ambiente venv

creazione ambiente virtuale python:

./python3 -m venv ~/workspace/fels2-scripts/venv/

Successivamente, aggiungere all'ambiente virtuale i seguenti pacchetti

<ol>
  <li>./pip install bitarray==1.2.1</li>
  <li>./pip install Pillow==7.0.0</li>
  <li>./pip install PySide2==5.14.1</li>
</ol>

In data 18/03/2020, si sta usando python 3.8.1 (pare che i precedenti abbiano problemi con PySide 5.14.x)
e i pacchetti usati sono (da comando pip list):

<ul>
  <li>bitarray - versione 1.2.1</li>
  <li>Pillow - versione 7.0.0</li>
  <li>pip - versione 20.0.2</li>
  <li>PySide2 - versione 5.14.1</li>
  <li>setuptools - versione 41.2.0</li>
  <li>shiboken2 - versione 5.14.1 (installato automaticamente con PySide2)</li>
</ul>

Per installare una specifica versione, bisogna dare il comando:
<tt>
  pip install pacchett==versione
  es.: pip install PySide2==5.14.1
</tt>

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

Per eseguire il sw da console, eseguire il seguente comando (facendo attenzione ai percorsi); l'idea e' che
bisogna impostare correttamente la variabile PYTHONPATH
<tt>
  PYTHONPATH=`pwd`/fels2scripts/ ./venv/bin/python .gui/fels2-gui.py
</tt>
