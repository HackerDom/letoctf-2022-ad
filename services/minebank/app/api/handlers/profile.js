const router = require('express').Router();

router.get('/', async function(req, resp, next) {
    let user = await req.db.user.findOne({ where: { id: req.authedUserId } });
    if (!user) {
        resp.status(404).send({msg: "Can't find user. Please, sign up first", redirect: "/signup"});
        return;
    }
    resp.send({
        msg: "ok",
        data: {
            login: user.login,
            diamondsCount: user.diamondsCount,
            accountID: user.accountID,
        }
    });
});

module.exports = router;