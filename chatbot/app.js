const express = require('express');
const bodyParser = require('body-parser');
const dialogflow = require('@google-cloud/dialogflow');
require('dotenv').config();
const cors = require('cors');

// Load credentials from .env file
const CREDENTIALS = JSON.parse(process.env.CREDENTIALS);

// Google Dialogflow Project ID
const PROJECT_ID = CREDENTIALS.project_id;

// Create a new session client
const sessionClient = new dialogflow.SessionsClient({
    credentials: {
        private_key: CREDENTIALS.private_key,
        client_email: CREDENTIALS.client_email,
    },
});

// Initialize Express app
const app = express();

// Middleware
app.use(cors()); // Enable CORS
app.use(bodyParser.json()); // Parse JSON requests

// Endpoint to handle Dialogflow queries
app.post('/dialogflow', async (req, res) => {
    const { queryText, sessionId, languageCode } = req.body;

    const sessionPath = sessionClient.projectAgentSessionPath(PROJECT_ID, sessionId);

    const request = {
        session: sessionPath,
        queryInput: {
            text: {
                text: queryText,
                languageCode: languageCode || 'en',
            },
        },
    };

    try {
        const responses = await sessionClient.detectIntent(request);
        const result = responses[0].queryResult;
        console.log('Detected intent:', result.intent.displayName); // Log intent
        console.log('Fulfillment text:', result.fulfillmentText); // Log response
        res.json({
            intent: result.intent.displayName,
            response: result.fulfillmentText,
        });
    } catch (error) {
        console.error('Error detecting intent:', error);
        res.status(500).send('Error detecting intent');
    }
});

// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
