const { Op } = require("sequelize");
const router = require('express').Router();
const { XMLBuilder } = require('fast-xml-parser');

router.post('/', async function(req, resp, next) {
    if (!req.xml || !req.xml.transaction_id) {
        resp.status(404).send({msg: "Incorrect request"});
        return;
    }

    let user = await req.db.user.findOne({ where: { id: req.authedUserId } });

    let transaction = await req.db.transaction.findOne({
        where: {
            id: req.xml.transaction_id,
            [Op.or]: [
                { sender_accountID: user.accountID },
                { recipient_accountID: user.accountID }
            ]
        }
    })

    let xmlBuilder = new XMLBuilder()
    resp.set('Content-Type', 'text/xml').send(xmlBuilder.build({
        xml: {
            msg: "ok",
            data: {
                id: transaction.id,
                sender_accountID: transaction.sender_accountID,
                recipient_accountID: transaction.recipient_accountID,
                status: transaction.status,
                diamondsCount: transaction.diamondsCount,
                description: transaction.description,
                createdAt: transaction.createdAt,
            }
        }
    }))
});

module.exports = router;