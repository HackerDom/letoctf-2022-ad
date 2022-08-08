from gornilo import Checker, PutRequest, GetRequest, CheckRequest, Verdict
from gornilo.http_clients import requests_with_retries

checker = Checker()


@checker.define_check
def check(req: CheckRequest) -> Verdict:
    return Verdict.OK()


@checker.define_put(vuln_num=1, vuln_rate=1)
def put(putReq: PutRequest) -> Verdict:
    return Verdict.OK()


@checker.define_get(vuln_num=1)
def get(getReq: GetRequest) -> Verdict:
    return Verdict.OK()


checker.run()