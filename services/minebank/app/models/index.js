const dbConfig = require("../db.config");
const Sequelize = require("sequelize");
const sequelize = new Sequelize(dbConfig.DB, dbConfig.USER, dbConfig.PASSWORD, {host: dbConfig.HOST, dialect: dbConfig.dialect});

const db = {};
db.Sequelize = Sequelize;
db.sequelize = sequelize;
db.user = require("./user.model.js")(sequelize);
db.transaction = require("./transaction.model")(sequelize, db.user);
db.transaction_status = Object.freeze({
    "processing": 0,
    "successful": 1,
    "incorrectAccountID": 2,
    "notEnoughDiamonds": 3,
});

module.exports = db;
