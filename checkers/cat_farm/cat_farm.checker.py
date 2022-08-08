from gornilo import Checker, PutRequest, GetRequest, CheckRequest, Verdict
from random import randint
from api import Api
from uuid import uuid4
from gornilo.utils import generate_flag

checker = Checker()


def gen_cords():
    return randint((2 ** 30) * -1, 2 ** 30), randint((2 ** 30) * -1, 2 ** 30)


@checker.define_check
def check(req: CheckRequest) -> Verdict:
    x, y = gen_cords()
    x1, y1 = x-1, y+1

    api = Api(req.hostname)

    cat_id_1 = str(uuid4())
    cat_id_2 = str(uuid4())
    api.add_cat(cat_id_1, generate_flag(), x, y)
    api.add_cat(cat_id_2, generate_flag(), x1, y1)

    res = api.meow_meow(x - 2, y - 2)
    if cat_id_1 not in res or cat_id_2 not in res:
        return Verdict.MUMBLE("Can't do meow-meow")

    return Verdict.OK()


@checker.define_put(vuln_num=1, vuln_rate=1)
def put(put_req: PutRequest) -> Verdict:
    x, y = gen_cords()
    api = Api(put_req.hostname)
    cat_id_1 = str(uuid4())
    api.add_cat(cat_id_1, put_req.flag, x, y)
    return Verdict.OK(cat_id_1)


@checker.define_get(vuln_num=1)
def get(get_req: GetRequest) -> Verdict:
    api = Api(get_req.hostname)
    name = api.get_cat_name(get_req.flag_id)
    if name.strip() == get_req.flag.strip():
        return Verdict.OK()
    return Verdict.CORRUPT("Ur lost ur kitties!")


checker.run()