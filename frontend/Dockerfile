# frontend/Dockerfile
FROM node:20

WORKDIR /app

# -- deps --
COPY package*.json ./
RUN npm install          # installs axios, react, vite, …

# -- source --
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
