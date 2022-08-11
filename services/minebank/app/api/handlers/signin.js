const router = require('express').Router();

router.post('/', async function(req, resp, next) {
    if (req.isAuthorized) {
        resp.status(400).send({msg: "Please, log out first", redirect: "/logout"});
        return;
    }

    let login = req.body.login;
    let password = req.body.password;
    if (!login || !password) {
        resp.status(400).send({msg: "Please, enter login and password"})
        return
    }

    let user = await req.db.user.findOne({ where: { login: login, password: password } });
    if (!user) {
        resp.status(404).send({msg: "Can't find user. Please, sign up first", redirect: "/signup"});
        return;
    }

    resp.cookie("auth", await req.authenticator.append(user.id)).send({msg: "ok"});
});

module.exports = router;