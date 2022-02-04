package:
	python -m pip-compile requirements.in
	python -m pip install -r requirements.txt --target packages/ --upgrade

invoke:
	sam local invoke FileGenerator1 --profile nara -e test\event.json

clean:
	rm -r -fo packages