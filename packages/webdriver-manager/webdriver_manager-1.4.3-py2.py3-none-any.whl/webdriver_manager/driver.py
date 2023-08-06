import logging

import requests

from webdriver_manager import config
from webdriver_manager import utils
from webdriver_manager.config import Configuration
from webdriver_manager.utils import validate_response, OSType


class Driver(object):
    def __init__(self, version, os_type):
        self.config = Configuration(file_name=config.filename,
                                    config_folder=config.folder,
                                    section=self.__class__.__name__)
        self.config.set("version", version)
        self._url = self.config.url
        self.name = self.config.name
        self._version = self.config.version
        self.os_type = os_type

    def get_url(self):
        url = "{url}/{ver}/{name}_{os}.zip"
        return url.format(url=self._url,
                          ver=self.get_version(),
                          name=self.name,
                          os=self.os_type)

    def get_version(self):
        if self._version == "latest":
            return self.get_latest_release_version()
        return self._version

    def get_latest_release_version(self):
        raise NotImplementedError("Please implement this method")


class ChromeDriver(Driver):
    def __init__(self, version, os_type):
        super(ChromeDriver, self).__init__(version, os_type)

    def get_latest_release_version(self):
        file = requests.get(self.config.driver_latest_release_url)
        return file.text.rstrip()


class GeckoDriver(Driver):
    def __init__(self, version, os_type):
        super(GeckoDriver, self).__init__(version, os_type)

    def get_latest_release_version(self):
        resp = requests.get(self.latest_release_url)
        validate_response(self, resp)
        return resp.json()["tag_name"]

    def get_url(self):
        # https://github.com/mozilla/geckodriver/releases/download/v0.11.1/geckodriver-v0.11.1-linux64.tar.gz
        logging.warning(
            "Getting latest mozila release info for {0}".format(self.get_version()))
        resp = requests.get(self.tagged_release_url)
        validate_response(self, resp)
        assets = resp.json()["assets"]
        ver = self.get_version()
        name = "{0}-{1}-{2}".format(self.name, ver, self.os_type)
        output_dict = [asset for asset in assets if
                       asset['name'].startswith(name)]
        return output_dict[0]['browser_download_url']

    @property
    def latest_release_url(self):
        token = self.config.gh_token
        url = self.config.driver_latest_release_url
        if token:
            return "{base_url}?access_token={access_token}".format(base_url=url,
                                                                   access_token=token)
        return url

    @property
    def tagged_release_url(self):
        token = self.config.gh_token
        url = self.config.mozila_release_tag.format(self.get_version())
        if token:
            return url + "?access_token={0}".format(token)
        return url


class PhantomJsDriver(Driver):
    def __init__(self, version, os_type):
        super(PhantomJsDriver, self).__init__(version, os_type)

    def get_latest_release_version(self):
        token = self.config.gh_token
        url = self.config.driver_tags_url
        if token:
            url = "{}?access_token={}".format(url, token)

        resp = requests.get(url=url)
        validate_response(self, resp)
        return resp.json()[0]['name']

    def get_url(self):
        name = "{name}-{version}-{os}".format(name=self.name,
                                              version=self.get_version(),
                                              os=self.__file_name())
        return "{url}/{name}".format(url=self.config.url,
                                     name=name)

    def __file_name(self):
        if self.os_type == OSType.MAC:
            return "macosx.zip"
        elif self.os_type == OSType.WIN:
            return "windows.zip"
        elif self.os_type == OSType.LINUX and utils.os_architecture() == 64:
            return "linux-x86_64.tar.bz2"
        elif self.os_type == OSType.LINUX and utils.os_architecture() == 32:
            return "linux-i686.tar.bz2"
        else:
            raise ValueError("No such driver for os type {}".format(utils.os_type()))


class EdgeDriver(Driver):
    def get_latest_release_version(self):
        return self.get_version()

    def __init__(self, version, os_type):
        super(EdgeDriver, self).__init__(version, os_type)

    def get_version(self):
        return self._version

    def get_url(self):
        return "{}/{}.exe".format(self._url, self.name)
