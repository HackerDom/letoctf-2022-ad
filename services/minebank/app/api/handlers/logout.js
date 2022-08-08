const router = require('express').Router();

router.get('/', async function(req, resp, next) {
    await req.authenticator.clear(req.authedUserId)
    resp.clearCookie("auth");
    resp.redirect("/")
});

module.exports = router;