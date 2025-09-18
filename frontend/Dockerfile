# Gebruik Node.js 20 als basis
FROM node:20

# Stel de werkdirectory in
WORKDIR /app

# Kopieer package.json en package-lock.json
COPY package*.json ./

# Installeer dependencies
RUN npm install

# Kopieer de rest van de app
COPY . .

# Expose poort 3000 (standaard Vue dev server)
EXPOSE 3000

# Start de ontwikkelserver
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
