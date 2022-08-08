const router = require('express').Router();
const path = require('path');

router.get('/', async function(req, resp ,next) {
    resp.sendFile(path.resolve(__dirname, "../../views", "index.html"))
});

module.exports = router;