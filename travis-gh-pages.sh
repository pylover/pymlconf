#!/usr/bin/env bash
set -e # Exit with nonzero exit code if anything fails

# Save some useful information
REPO=`git config remote.origin.url`
SHA=`git rev-parse --verify HEAD`

# Get the deploy key by using Travis's stored variables to decrypt deploy_key.enc
ENCRYPTED_KEY_VAR="encrypted_${ENCRYPTION_LABEL}_key"
ENCRYPTED_IV_VAR="encrypted_${ENCRYPTION_LABEL}_iv"
ENCRYPTED_KEY=${!ENCRYPTED_KEY_VAR}
ENCRYPTED_IV=${!ENCRYPTED_IV_VAR}
OUT_KEY="pymlconf-travis-gh-pages"

openssl aes-256-cbc -K $ENCRYPTED_KEY -iv $ENCRYPTED_IV -in pymlconf-travis-gh-pages.enc -out $OUT_KEY -d
chmod 600 $OUT_KEY
eval `ssh-agent -s`
ssh-add $OUT_KEY


# Clone/checkout the gh-pages branch from Github alongside the master branch working copy directory :
cd ..
git clone -b gh-pages git@github.com:pylover/pymlconf.git pymlconf.io
cd pymlconf.io
git pull origin gh-pages
cd ..

# Build in-project documents: sphinx/html
cd pymlconf/sphinx
make html

# Build pymlconf.io documents: ../../pymlconf.io
make deploy

# Commit & push
cd ../../pymlconf.io/
git config user.name "Travis CI"
git config user.email "$COMMIT_AUTHOR_EMAIL"
touch .nojekyll 
git add .nojekyll
git add .

git commit -am "Deploy to GitHub Pages: ${SHA}"
git push origin gh-pages
