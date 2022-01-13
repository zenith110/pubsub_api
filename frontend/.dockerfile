# build environment
FROM node:13.12.0-alpine
WORKDIR /home/frontend
COPY package.json ./
COPY package-lock.json ./
RUN npx browserslist@latest --update-db
RUN npm i --silent
EXPOSE 3000
COPY . ./
CMD ["npm", "run", "start"]