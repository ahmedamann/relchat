# Use Node.js 20 base image
FROM node:20

WORKDIR /app

ENV NODE_ENV=development

COPY ./package*.json ./

RUN npm install --legacy-peer-deps

COPY . .

RUN npm run build

RUN npm install -g serve

EXPOSE 5173

CMD ["serve", "-s", "dist", "-l", "5173"]