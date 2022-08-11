const { validate: isValidUUID, uuidv4} = require('uuid');
const router = require('express').Router();

router.post('/', async function(req, resp, next) {
    let diamondsCount = parseInt(req.body.diamondsCount);
    let recipient_accountID = req.body.recipient_accountID;
    let description = req.body.description;
    if (!diamondsCount || !isValidUUID(recipient_accountID) || !description) {
        resp.status(400).send({msg: "Incorrect transaction info"});
        return;
    }

    let user = await req.db.user.findOne({ where: { id: req.authedUserId } });
    const userDiamonds = parseInt(user.diamondsCount)
    let newTransaction;
    try {
        newTransaction = await req.db.transaction.create({
            sender_accountID: user.accountID,
            recipient_accountID: recipient_accountID,
            diamondsCount: diamondsCount,
            description: description,
        });
    } catch (e) {
        resp.status(400).send({msg: "Incorrect transaction info"});
        return;
    }

    resp.send({msg: "Transaction created", redirect: "/transaction", data: {"transaction_id": newTransaction.id}});

    if (userDiamonds < diamondsCount) {
        await newTransaction.update({ status: req.db.transaction_status.notEnoughDiamonds });
        return
    }

    await user.update({ diamondsCount: userDiamonds - diamondsCount });

    let recipientUser = await req.db.user.findOne({ where: { accountID: recipient_accountID } });
    if (!recipientUser) {
        await newTransaction.update({ status: req.db.transaction_status.incorrectAccountID });
        await user.update({ diamondsCount: userDiamonds + diamondsCount });
        return;
    }
    await recipientUser.update({ diamondsCount: parseInt(recipientUser.diamondsCount) + diamondsCount });
    await newTransaction.update({ status: req.db.transaction_status.successful });
});

router.get('/', async function(req, resp, next) {
    let user = await req.db.user.findOne({ where: { id: req.query.usr || req.authedUserId } });

    if (!user) {
        resp.status(400).send({msg: "User not found"});
        return;
    }

    let t_transactions = await req.db.transaction.findAll({
        where: { sender_accountID: user.accountID },
    });

    let r_transactions = await req.db.transaction.findAll({
        where: { recipient_accountID: user.accountID, status: req.db.transaction_status.successful },
    });

    resp.send({
        msg: "ok",
        data: {
            transmitted: t_transactions.map(
                (t_transaction) => {
                    return {
                        id: t_transaction.id,
                        accountID: t_transaction.recipient_accountID,
                        status: t_transaction.status,
                        diamondsCount: t_transaction.diamondsCount,
                        description: t_transaction.description,
                    };
                }
            ),
            received: r_transactions.map(
                (r_transaction) => {
                    return {
                        id: r_transaction.id,
                        accountID: r_transaction.sender_accountID,
                        status: r_transaction.status,
                        diamondsCount: r_transaction.diamondsCount,
                        description: r_transaction.description,
                    };
                }
            ),
        }
    });
});

module.exports = router;
