'use strict';
const crypto = require('crypto');


class Authenticator {
    #sessions = {};
    #n = Math.floor(Math.random() * 100000);

    constructor() {
        this.optional  = this.optional.bind(this);
        this.required  = this.required.bind(this);
    }

    async append(id) {
        this.#n += 1;
        const cookie = crypto.createHash('md5').update(this.#n.toString()).digest("hex");
        if (cookie in this.#sessions)
            return this.#sessions[cookie];
        this.#sessions[cookie] = id;
        return cookie;
    }

    async clear(cookie) {
        const id = this.#sessions[cookie];
        delete this.#sessions[cookie];
        return id;
    }

    optional(req, resp, next) {
        req.isAuthorized = 'auth' in req.cookies && req.cookies['auth'] in this.#sessions;
        req.authenticator = this;
        req.authedUserId = req.isAuthorized ? this.#sessions[req.cookies.auth] : undefined;
        next();
    }

    required(req, resp, next) {
        if ('auth' in req.cookies && req.cookies['auth'] in this.#sessions) {
            req.authenticator = this;
            req.authedUserId = this.#sessions[req.cookies.auth];
            next();
        } else
            resp.sendStatus(401);
    }
}

module.exports = new Authenticator();
