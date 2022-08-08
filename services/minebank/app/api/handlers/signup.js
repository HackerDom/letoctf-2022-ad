const { v4: uuidv4 } = require('uuid');
const router = require('express').Router();

router.post('/', async function(req, resp, next) {
    if (req.isAuthorized) {
        resp.status(400).send({msg: "Please, log out first", redirect: "/logout"});
        return;
    }

    try {
        const newUser = await req.db.user.create({
            login: req.body.login,
            password: req.body.password,
            accountID: uuidv4(),
            diamondsCount: 100,
        });
        resp.cookie('auth', await req.authenticator.append(newUser.id)).send({msg: "ok"});
    } catch (e) {
        console.log(e.message);
        resp.status(400).send({msg: "Incorrect user info. Please, check fields"});
    }

});

module.exports = router;