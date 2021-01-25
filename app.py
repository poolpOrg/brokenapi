#! /usr/bin/env python3
#
# Copyright (c) 2021 Gilles Chehade <gilles@poolp.org>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import hashlib
import random
import string
import time

import bottle


@bottle.get("/chaos")
def _():
    try:
        output = bottle.request.GET.get('output', '0')
        output = int(output)
        output_variation = bottle.request.GET.get('output_variation', '0')
        output_variation = float(output_variation)

        mem_cost = bottle.request.GET.get('mem_cost', '0')
        mem_cost = int(mem_cost)
        mem_cost_variation = bottle.request.GET.get('mem_cost_variation', '0')
        mem_cost_variation = float(mem_cost_variation)

        cpu_cost = bottle.request.GET.get('cpu_cost', '0')
        cpu_cost = int(cpu_cost)
        cpu_cost_variation = bottle.request.GET.get('cpu_cost_variation', '0')
        cpu_cost_variation = int(cpu_cost_variation)

        time_cost = bottle.request.GET.get('time_cost', '0.0')
        time_cost = float(time_cost)
        time_cost_variation = bottle.request.GET.get('time_cost_variation', '0')
        time_cost_variation = float(time_cost_variation)

        failure_code = bottle.request.GET.get('failure_code', '500')
        failure_code = int(failure_code)
        failure_rate = bottle.request.GET.get('failure_rate', '0')
        failure_rate = int(failure_rate)
    except:
        raise bottle.HTTPError(400)

    if cpu_cost:
        _ = hashlib.pbkdf2_hmac("sha256", b"4b4db33f154d34db33f", b"4d34db33f154b4db33f",
            cpu_cost + random.randint(0, cpu_cost_variation), 32)

    if time_cost:
        time.sleep(time_cost + random.uniform(0.0, time_cost_variation))

    if mem_cost:
        retbuf = [random.choice(string.ascii_letters) \
                    for _ in range(0, mem_cost + random.randint(0, mem_cost_variation))]

    if failure_rate:
        rnd = random.random() * 100
        if rnd < float(failure_rate):
            raise bottle.HTTPError(failure_code)

    if output:
        output_real = output + random.randint(0, output_variation)

        if not mem_cost:
            return [random.choice(string.ascii_letters) for _ in range(0, output_real)]
        if len(retbuf) == output_real:
            return retbuf
        if len(retbuf) > output_real:
            return retbuf[0:output_real]
        return retbuf + [random.choice(string.ascii_letters) \
            for _ in range(0, output_real-len(retbuf))]

    return ""

if __name__ == "__main__":
    bottle.run(server='cherrypy')
