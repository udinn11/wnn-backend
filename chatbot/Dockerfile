FROM node:18

# Set working directory
WORKDIR /chatbot

# Copy dependencies and install
COPY package*.json ./
RUN npm install

#Copy env
COPY .env .env

# Copy chatbot source code
COPY . .

# Expose port
EXPOSE 5000

# Run chatbot
CMD ["node", "app.js"]
