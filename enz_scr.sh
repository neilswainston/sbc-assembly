pip install synbiochem-py

export PYTHONPATH=$PYTHONPATH:.

python assembly/app/enz_scr/enz_scr_pipeline.py \
	data/enz_scr/enz_scr.csv \
	ENZ