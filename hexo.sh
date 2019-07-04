#!/bin/sh

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
cd $SHELL_FOLDER

if [ ! -d "./.hexo" ]; then
  git clone git@github.com:ruesin/hexo.git .hexo
  cd .hexo
  npm install
  cd $SHELL_FOLDER
fi

# clean
cd .hexo
hexo clean

rm -rf ./source/_posts ./source/images
if [ ! -d "./source/_posts/" ]; then
  mkdir -p ./source/_posts/
fi
if [ ! -d "./source/images/" ]; then
  mkdir -p ./source/images/
fi
cp -r ../docs/ ./source/_posts/
cp -r ../images/ ./source/images/

hexo server
# hexo g