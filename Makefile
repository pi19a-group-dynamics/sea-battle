run:
	python main.py

install:
	pyinstaller main.py --onefile --noconsole --icon=sources\images\icon.ico