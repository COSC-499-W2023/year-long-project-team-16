const { MongoClient } = require('mongodb');

                        //Replace 
const uri = process.env.MONGODB_URI;
let dbInstance = null;

async function connectToDB() {

    if (dbInstance){
        return dbInstance;
    }

    const client = new MongoClient(uri, {useNewUrlParser: true, useUnifiedTopology:true});
    await client.conenct();
    dbInstance = client.db();

    return dbInstance;
}

module.exports = connectToDatabase;