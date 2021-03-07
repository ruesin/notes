#!/bin/sh

export TZ='Asia/Shanghai'

# npm install -g hexo-cli

SHELL_DIR=$(cd "$(dirname "$0")";pwd)
cd $SHELL_DIR

ROOT_DIR=$SHELL_DIR/..

DEPLOY_TEMP_DIR=$SHELL_DIR/deploy_temp

git clone git@github.com:ruesin/hexo.git $DEPLOY_TEMP_DIR

cd $DEPLOY_TEMP_DIR && npm install

rm -rf ./source/_posts/ ./source/images/

mkdir -p ./source/_posts/ && mkdir -p ./source/images/

cp -r $ROOT_DIR/docs/* ./source/_posts/ && cp -r $ROOT_DIR/images/* ./source/images/

cp $ROOT_DIR/CNAME ./source/

cp $ROOT_DIR/favicon.ico ./source/

hexo clean && hexo generate

cd public
git init
git config user.name "ruesin"
git config user.email "ruesin@gmail.com"
git remote add origin git@github.com:ruesin/notes.git
git add .
git commit -m "Travis CI Auto Builder at `date +"%Y-%m-%d %H:%M"`"
git push --force --quiet "git@github.com:ruesin/notes.git" master:gh-pages

rm -rf $DEPLOY_TEMP_DIR