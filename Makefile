init:
	pip install pipenv
	pipenv install
	mkdir workspace

run:
	( \
		pipenv run streamlit run file_uploader.py \
	)

two:
	touch two

three:
	touch three

clean:
	rm -f start-server two three