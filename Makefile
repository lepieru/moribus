run:
	python -OO src/main.py

clean:
	rm -f src/*~ src/*.pyc src/*.pyo
	rm -rf src/__pycache__
