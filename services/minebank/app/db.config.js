/*module.exports = {
    dialect: "sqlite",
    storage: "db.sqlite",
    pool: {
        max: 10,
        min: 0,
        idle: 10000,
        acquire: 30000
    }
};*/

module.exports = {
  HOST: "postgres",
  USER: "minebank",
  PASSWORD: "minebank",
  DB: "minebank",
  dialect: "postgres",
  pool: {
    max: 5,
    min: 0,
    acquire: 30000,
    idle: 10000
  }
}