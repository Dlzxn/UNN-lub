#!/bin/bash

# Копируем файлы в нужные директории
echo "Удаляем старые файлы ~/UNN/"
sudo rm -rf ~/UNN
sudo rm -rf ~/.local/share/applications/UNN.desktop

echo "Создаем рабочую директорию..."
mkdir ~/UNN
mkdir ~/UNN/icon

echo "Копируем файлы в /UNN/program..."
sudo cp -r UNN/* ~/UNN/ || { echo "Ошибка копирования файлов"; exit 1; }


echo "Переносим папки..."
sudo cp -r ~/UNN/usr/local/bin/_internal/analytic ~/UNN/usr/local/bin/
sudo cp -r ~/UNN/usr/local/bin/_internal/bd ~/UNN/usr/local/bin/
sudo cp -r ~/UNN/usr/local/bin/_internal/cashe ~/UNN/usr/local/bin/
sudo cp -r ~/UNN/usr/local/bin/_internal/Interface ~/UNN/usr/local/bin/
sudo cp -r ~/UNN/usr/local/bin/_internal/parser ~/UNN/usr/local/bin/
sudo cp -r ~/UNN/usr/local/share/icons/hicolor/256x256/apps/unn.png /usr/share/icons/


#echo "Копируем файлы в /UNN/program..."
#sudo cp -r myapp/usr/local/share/* ~/UNN/program/ || { echo "Ошибка копирования файлов"; exit 1; }
#
echo "Копируем файлы в /.local/..."
sudo cp -r UNN/usr/local/bin/UNN.desktop ~/.local/share/applications || { echo "Ошибка копирования файлов"; exit 1; }

echo "Выдаем права доступа..."
sudo chmod -R 777 ~/UNN/*

#echo "Переносим UNN..."
#sudo cp -r ~/UNN/program/UNN ~/UNN/program/_internal/

# Обновляем базу данных ярлыков
echo "Обновляем базу данных ярлыков..."
update-desktop-database ~/.local/share/applications || { echo "Ошибка обновления базы данных ярлыков"; exit 1; }

echo "Установка завершена!"
echo "Хорошего пользования! by DlzxnDev"
