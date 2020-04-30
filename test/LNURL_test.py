import requests, time, json, time, threading, logging
from lnurl import Lnurl, LnurlResponse, handle


def wallet_action():
    sleep = 3
    logger.info(f"Starts in {sleep} seconds")
    time.sleep(sleep)

    res = handle(lnurl_string)  # LnurlWithdrawResponse

    # Test wrong k1
    k1 = "TestWithNonExistendUUID"
    pr = "lnbc5u1p0fa0g0pp5z0xnnq63p7fx7vs3t4sx9sapk3lvpeppffy0pursn6fz5m99xr0qdqqcqzpgxqyz5vqsp59kyl2900ggel0e8gr2s3uv4ze5d96aqdm0q597npqn4mlkm0fwes9qy9qsq8s2d96sljuhnu9za7edskaxlmur2rxuzhg4ckyctq970nsplxev8ccdfs9jmw75t79vvxhqpsz3r83xf7qzc9fcss8jxwmkdgxt7kusp0j3dl5"
    data = {"k1": k1, "pr": pr}
    logger.info(f"Submits k1: {k1}, pr: {pr}")
    response_withdraw = requests.get(res.callback, params=data)
    logger.info(response_withdraw.json())
    logger.info("")
    time.sleep(sleep)

    # Test wrong UUID
    k1 = res.k1
    pr = "lnbc5u1p0fa0g0pp5z0xnnq63p7fx7vs3t4sx9sapk3lvpeppffy0pursn6fz5m99xr0qdqqcqzpgxqyz5vqsp59kyl2900ggel0e8gr2s3uv4ze5d96aqdm0q597npqn4mlkm0fwes9qy9qsq8s2d96sljuhnu9za7edskaxlmur2rxuzhg4ckyctq970nsplxev8ccdfs9jmw75t79vvxhqpsz3r83xf7qzc9fcss8jxwmkdgxt7kusp0j3dl5"
    data = {"k1": k1, "pr": pr}
    logger.info(f"Submits k1: {k1}, pr: {pr}")
    response_withdraw = requests.get(request_url + "/non-existent-uuid", params=data)
    logger.info(response_withdraw.json())
    logger.info("")

    invoices = [
        "lnbc4u1p02kyjapp5p2zpheg2x5xjz9k9ne7r599csvv42ldvuadx0y4590tzg3md9jnqdqc2p5x7etwd9uzqurp09kk2mn5xqrrss9qtzqqqqqq9qsqsp547cq27ahjm9x995qj0akwdp302mqusmnx5jh79gwa0nd53k0xf4qrzjqwryaup9lh50kkranzgcdnn2fgvx390wgj5jd07rwr3vxeje0glclle759a9cpjcqyqqqqlgqqqqqeqqjqjaklqv4vcy3c6dgex3kuhvcd5fmes0a90n3plp4f6uqzpynsmcnsl28ul7v5x08ul6pchh3v9hjj8ppfah9tg6g9yqv2q2k9qpka6uspenmrm7",
        "lnbc5u1p0fa0g0pp5z0xnnq63p7fx7vs3t4sx9sapk3lvpeppffy0pursn6fz5m99xr0qdqqcqzpgxqyz5vqsp59kyl2900ggel0e8gr2s3uv4ze5d96aqdm0q597npqn4mlkm0fwes9qy9qsq8s2d96sljuhnu9za7edskaxlmur2rxuzhg4ckyctq970nsplxev8ccdfs9jmw75t79vvxhqpsz3r83xf7qzc9fcss8jxwmkdgxt7kusp0j3dl",
        "lnbc5u1p0fa0g0pp5z0xnnq63p7fx7vs3t4sx9sapk3lvpeppffy0pursn6fz5m99xr0qdqqcqzpgxqyz5vqsp59kyl2900ggel0e8gr2s3uv4ze5d96aqdm0q597npqn4mlkm0fwes9qy9qsq8s2d96sljuhnu9za7edskaxlmur2rxuzhg4ckyctq970nsplxev8ccdfs9jmw75t79vvxhqpsz3r83xf7qzc9fcss8jxwmkdgxt7kusp0j3dl5",
    ]
    # Test wrong amount, faulty checksum and correct invoice
    for invoice in invoices:
        time.sleep(sleep)
        k1 = res.k1
        pr = invoice
        data = {"k1": k1, "pr": pr}
        logger.info(f"Submits k1: {k1}, pr: {pr}")

        response_withdraw = requests.get(res.callback, params=data)
        response_withdraw.json()
        logger.info(response_withdraw.json())
        logger.info("")


logging.basicConfig(level="INFO", format="%(threadName)-6s | %(message)s")
logger = logging.getLogger(__name__)

threading.current_thread().name = "main"
request_url = "http://lnurl.test:5000/v1/lnurl"
data = {"amount": 500}
response = requests.post(request_url, json=data)

lnurl_string = response.json()["lnurl"]
logger.info("Received LNURL:" + lnurl_string)
callback = response.json()["callback"]
logger.info
logger.info("Received 'await-invoice' URL:" + callback)

wallet_thread = threading.Thread(target=wallet_action, name="wallet")
wallet_thread.start()

logger.info(f"Starts longpolling at {callback} \n")
response = requests.get(callback)
logger.info('Here is the invoice your wallet just submitted over "LNURLProxyAPI:"')
logger.info(response.json()["invoice"])
