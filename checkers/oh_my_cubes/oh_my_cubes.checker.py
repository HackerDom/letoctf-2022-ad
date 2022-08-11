#!/usr/bin/env python3.9
import json
import os
import re
import subprocess
from random import randrange

from gornilo import Checker, CheckRequest, PutRequest, GetRequest, Verdict
from uuid import uuid4

checker = Checker()


def randomize() -> str:
    return str(uuid4())


class Object(object):
    pass


@checker.define_check
def check(check_request: CheckRequest) -> Verdict:
    path = os.path.dirname(os.path.realpath(__file__))
    r = subprocess.Popen([f"{path}/client", f"--addr={check_request.hostname}", "--command=check"], stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    lines = r.stdout.readlines()
    Log(lines)
    return ParseVerdict(lines)


@checker.define_put(vuln_num=1, vuln_rate=1)
def put(put_request: PutRequest) -> Verdict:
    path = os.path.dirname(os.path.realpath(__file__))
    r = subprocess.Popen([f"{path}/client", f"--addr={put_request.hostname}", "--command=put1", f"--data={put_request.flag}"], stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    lines = r.stdout.readlines()
    Log(lines)
    return ParseVerdict(lines)


@checker.define_get(vuln_num=1)
def get(get_request: GetRequest) -> Verdict:
    print(get_request.flag_id)
    path = os.path.dirname(os.path.realpath(__file__))
    r = subprocess.Popen([f"{path}/client", f"--addr={get_request.hostname}", "--command=get1", f"--data={get_request.flag_id[:]}"], stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    lines = r.stdout.readlines()
    Log(lines)
    return ParseVerdict(lines)


@checker.define_put(vuln_num=2, vuln_rate=1)
def put2(put_request: PutRequest) -> Verdict:
    path = os.path.dirname(os.path.realpath(__file__))
    r = subprocess.Popen([f"{path}/client", f"--addr={put_request.hostname}", "--command=put2", f"--data={put_request.flag}"], stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    lines = r.stdout.readlines()
    Log(lines)
    return ParseVerdict(lines)


@checker.define_get(vuln_num=2)
def get2(get_request: GetRequest) -> Verdict:
    print(get_request.flag_id)
    path = os.path.dirname(os.path.realpath(__file__))
    r = subprocess.Popen(
        [f"{path}/client", f"--addr={get_request.hostname}", "--command=get2", f"--data={get_request.flag_id[:]}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    lines = r.stdout.readlines()
    Log(lines)
    return ParseVerdict(lines)


def ParseVerdict(lines) -> Verdict:
    code = None
    reason = None
    for line in lines[-2:]:
        code_search = re.search("VERDICT_CODE:(?P<code>[0-9]+)", line.decode("utf-8"))
        reason_search = re.search("VERDICT_REASON:(?P<reason>.*)$", line.decode("utf-8"))
        if code_search:
            code = int(code_search.group(1))

        if reason_search:
            reason = reason_search.group(1)

    if code == None or reason == None:
        return Verdict.CHECKER_ERROR("Can't parse verdict")

    return Verdict(code, reason)


def Log(lines):
    for line in lines:
        print(line.decode("utf-8"))




if __name__ == '__main__':
    checker.run()