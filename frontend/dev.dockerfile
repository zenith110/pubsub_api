# build environment
FROM node:13.12.0-alpine
WORKDIR /home/frontend
COPY package.json ./
COPY package-lock.json ./
RUN npm i --silent
RUN npx browserslist@latest --update-db
EXPOSE 3000
COPY . ./
CMD ["npm", "run", "start"]