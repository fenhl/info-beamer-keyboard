#!/bin/sh

# make sure everything is executed relative to this script's location
cd "${0:a:h}"

rm node/data.json
echo '{}' > node/data.json
info-beamer node &

info_beamer_keyboard/__main__.py
