VERSION=$(cat VERSION)
docker build -t ahbotpriceupdater:$VERSION -t ahbotpriceupdater:latest .