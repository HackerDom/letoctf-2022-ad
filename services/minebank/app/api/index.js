const auth = require("../middleware/auth");
const xmlParser = require("../middleware/xmlParser");
const router = require("express").Router();

router.use("/", auth.optional, require("./handlers/index"));
router.use("/signup", auth.optional, require("./handlers/signup"));
router.use("/signin", auth.optional, require("./handlers/signin"));
router.use("/logout", auth.required, require("./handlers/logout"));
router.use("/profile", auth.required, require("./handlers/profile"));
router.use("/transaction-info", auth.required, xmlParser, require("./handlers/transaction_info"));
router.use("/transaction", auth.required, require("./handlers/transaction"));

module.exports = router;
