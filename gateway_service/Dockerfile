# Usa la imagen oficial de Node.js como base
FROM node:14

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo package.json y package-lock.json a la imagen
COPY package*.json ./

# Instala las dependencias del proyecto
RUN npm install

# Copia el resto de la aplicación al directorio de trabajo
COPY . .

# Expone el puerto en el que la aplicación se ejecutará
EXPOSE 5002

# Comando para ejecutar la aplicación
CMD ["node", "server.js"]
