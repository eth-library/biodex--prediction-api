#!/bin/sh

echo "loading family"
python3 manage.py loaddata fixturefiles/family.json
echo "loading subfamily"
python3 manage.py loaddata fixturefiles/subfamily.json
echo "loading genus"
python3 manage.py loaddata fixturefiles/genus.json
echo "loading species"
python3 manage.py loaddata fixturefiles/species.json
echo "loading image"
python3 manage.py loaddata fixturefiles/image.json
echo "loading image classfications"
python3 manage.py loaddata fixturefiles/imageClassification.json
echo "loading prediction models"
python3 manage.py loaddata fixturefiles/predModel.json
echo "loading harvard images"
python3 manage.py loaddata fixturefiles/Image_harvard.json
echo "loading harvard image classifications"
python3 manage.py loaddata fixturefiles/ImageClassification_harvard.json
