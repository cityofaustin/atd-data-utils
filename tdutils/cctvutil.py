"""
Utilities to interact for CCTV traffic cameras.
"""
import shutil
import requests


def get_cctv_img(path, camera):
    print("get_img {}".format(path))

    if "IP" in camera:
        url = "http://{}/jpeg".format(camera["IP"])

    else:
        return

    try:
        res = requests.get(url, timeout=0.1, stream=True)

        if res.status_code == 200:
            with open(path, "wb") as outfile:
                res.raw.decode_content = True
                shutil.copyfileobj(res.raw, outfile)

            del res

    except requests.exceptions.Timeout:
        return

    except requests.exceptions.RequestException:
        return
