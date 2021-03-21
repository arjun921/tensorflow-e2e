init:
	pip install pipenv
	pipenv install
	mkdir workspace

upload:
	( \
		pipenv run streamlit run file_uploader.py \
	)

train:
	( \
		# export workspace=$(workspace) \
		echo "pipenv run streamlit run train.py $(workspace)" \
		# pipenv run streamlit run train.py \
	)


clean:
	rm -f start-server two three