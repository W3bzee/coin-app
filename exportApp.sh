#!/bin/bash
printf "\nStarting Coin-App Export\n"

#read -p "Version: " version

while true; do
    read -p "Version: "  DIR

    if [ -d "$DIR" ]; then
        echo "directory $DIR already exist"
        sleep 1
    else
        mkdir -p $DIR
        printf "\n"
        echo "$DIR created..."
        break
    fi
done

# Export the application
python -m PyInstaller --onefile --windowed --icon=assets\\coin.ico mainApp.py

# Populate dist folder w/: assets, Database, stylesheets, and .env
cp -r assets dist
cp -r Database dist
cp -r stylesheets dist
cp -r .env dist
printf "\nRelocated Database, stylesheets & other assets\n"

# Relocate mainApp.spec
mv mainApp.spec $DIR
printf "\nRelocated mainApp.spec\n"

# Relocate dist & build folders
mv dist $DIR
mv build $DIR

printf "\n$DIR created succesfully!"
