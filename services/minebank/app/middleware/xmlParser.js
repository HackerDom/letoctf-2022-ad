'use strict';
const {XMLParser, XMLBuilder} = require('fast-xml-parser');

function concatXML(target, source) {
    for (const attr in source)
        typeof target[attr] === "object" && typeof source[attr] === "object" ?
            concatXML(target[attr], source[attr]) : target[attr] = source[attr]
}

module.exports = function (req, resp, next) {
    try {
        const parser = new XMLParser({ ignoreDeclaration: true })
        const builder = new XMLBuilder()

        const jsonXml = parser.parse(req.body)
        if (!jsonXml.xml) {
            resp.status(400).send(builder.build({xml: {msg: "xml field not found"}}))
            return
        }
        concatXML(req, jsonXml)
    } catch (e) {
        console.log(e)
        resp.status(400).send({msg: "incorrect xml"})
        return
    }
    next()
}
