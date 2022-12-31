FROM node:16.13.0-alpine3.14

WORKDIR /app/frontend

COPY package.json package-lock.json ./

RUN npm install -g pnpm

RUN pnpm install

COPY . .

RUN pnpm build

EXPOSE 4173

CMD ["pnpm", "preview"]