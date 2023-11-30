const { MongoClient } = require('mongodb');

                //Replace 
const uri = "atlast connection";
const client = new MongoClient(uri, {useNewUrlParser: true, useUnifiedTopology:true});

async function connect() {
    try {
        await client.connect();
        console.log("Connected to MongoDB Atlas");
        return client;
    } catch (e){
        console.error(e);
    }
}

module.exports = { connect };