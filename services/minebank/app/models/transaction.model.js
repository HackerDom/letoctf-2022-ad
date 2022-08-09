const { DataTypes } = require('sequelize')

module.exports = (sequelize, userModel) => {
    return sequelize.define(
        "transaction",
        {
            sender_accountID: {
                type: DataTypes.STRING,
                allowNull: false,
                references: {
                    model: userModel,
                    key: "accountID",
                },
                validate: {
                    isUUID: 4,
                },
            },
            recipient_accountID: {
                type: DataTypes.STRING,
                allowNull: false,
                references: {
                    model: userModel,
                    key: "accountID",
                },
                validate: {
                    isUUID: 4,
                },
            },
            status: {
                type: DataTypes.SMALLINT,
                defaultValue: 0,
            },
            diamondsCount: {
                type: DataTypes.BIGINT,
                allowNull: false,
            },
            description: {
                type: DataTypes.STRING,
                allowNull: false,
            }
        },
        {
            timestamps: true,
            updatedAt: false,
        }
    );
};

