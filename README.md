# cintel-04-local
run as administrator

py -m venv .venv

.venv\Scripts\Activate

py -m pip install --upgrade pip setuptools

py -m pip install --upgrade -r requirements.txt

shiny run --reload --launch-browser penguins/app.py

#Had to pip install websockets==10.4 for local running
It is incompatible with newer version of websockets - stemming from shiny

#Seaborn is not ocmpatible currently with Python 3.13 will need force downgrade to 3.12 to see Seaborn histogram unfortunately

shiny static-assets remove
shinylive export penguins docs

py -m http.server --directory docs --bind localhost 8008