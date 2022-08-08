const { DataTypes } = require('sequelize')

module.exports = (sequelize) => {
    return sequelize.define(
        "user",
        {
            login: {
                type: DataTypes.STRING,
                allowNull: false,
                unique: true,
                validate: {
                    isAlphanumeric: true,
                },
            },
            password: {
                type: DataTypes.STRING,
                allowNull: false,
                validate: {
                    isAlphanumeric: true,
                },
            },
            accountID: {
                type: DataTypes.STRING,
                allowNull: false,
                unique: true,
                validate: {
                    isUUID: 4,
                },
            },
            diamondsCount: {
                type: DataTypes.BIGINT,
            },
        },
        {
            timestamps: false,
        }
    );
};

