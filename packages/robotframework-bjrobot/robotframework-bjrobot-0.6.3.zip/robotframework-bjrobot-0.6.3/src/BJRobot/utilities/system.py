import os
import errno
import platform
from selenium.webdriver.common.keys import Keys
import ConfigParser
from robot.api import logger


class System:

    def __init__(self):
        pass

    @classmethod
    def search_file_contains(cls, path, keyword):
        for filename in os.listdir(path):
            fp = os.path.join(path, filename)
            if os.path.isdir(fp) and keyword in filename:
                return fp
            elif os.path.isdir(fp):
                cls.search_file_contains(fp, keyword)

    @staticmethod
    def read_config_param(section, option):
        cf = ConfigParser.ConfigParser()
        cf.read('..' + os.sep + 'settings' + os.sep + 'platform.cfg')
        print cf.get(section=section, option=option)

    @staticmethod
    def create_directory(path):
        target_dir = os.path.dirname(path)
        if not os.path.exists(target_dir):
            try:
                os.makedirs(target_dir)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(target_dir):
                    pass
                else:
                    raise

    @staticmethod
    def get_os_name():
        return platform.system().lower()

    @staticmethod
    def is64bit():
        return platform.architecture()[0].lower() == "64bit"

    @staticmethod
    def map_ascii_key_code_to_key(key_code):
        mapping = {
            0: Keys.NULL,
            8: Keys.BACK_SPACE,
            9: Keys.TAB,
            10: Keys.RETURN,
            13: Keys.ENTER,
            24: Keys.CANCEL,
            27: Keys.ESCAPE,
            32: Keys.SPACE,
            42: Keys.MULTIPLY,
            43: Keys.ADD,
            44: Keys.SEPARATOR,
            45: Keys.SUBTRACT,
            56: Keys.DECIMAL,
            57: Keys.DIVIDE,
            59: Keys.SEMICOLON,
            61: Keys.EQUALS,
            127: Keys.DELETE
        }
        key = mapping.get(key_code)
        if key is None:
            key = chr(key_code)
        return key

    @staticmethod
    def map_named_key_code_to_special_key(key_name):
        try:
            return getattr(Keys, key_name)
        except AttributeError:
            message = "Unknown key named '%s'." % key_name
            raise ValueError(message)

    @staticmethod
    def set_proxy(url):
        if url is not None and len(url) > 0 and url.lower() != "none":
            return {
                "httpProxy": url,
                "ftpProxy": url,
                "sslProxy": url,
                "socksProxy": url,
                "noProxy": 'localhost',
                "proxyType": "MANUAL",
                "autodetect": False
            }
        else:
            return {
                "httpProxy": '',
                "ftpProxy": '',
                "sslProxy": '',
                "socksProxy": '',
                "noProxy": 'localhost',
                "proxyType": "DIRECT",
                "autodetect": False
            }

    @staticmethod
    def escape_xpath_value(value):
        value = unicode(value)
        if '"' in value and '\'' in value:
            parts_wo_apos = value.split('\'')
            return "concat('%s')" % "', \"'\", '".join(parts_wo_apos)
        if '\'' in value:
            return "\"%s\"" % value
        return "'%s'" % value

    @staticmethod
    def parse_locator(locator):
        prefix = None
        criteria = locator
        if not locator.startswith('//'):
            locator_parts = locator.partition('=')
            if len(locator_parts[1]) > 0:
                prefix = locator_parts[0].strip()
                criteria = locator_parts[2].strip()
        return prefix.lower(), criteria

    @staticmethod
    def normalize_result(elements):
        if not isinstance(elements, list):
            logger.debug("WebDriver find returned %s" % elements)
            return []
        return elements

# if __name__ == '__main__':
#     print System.parse_locator("xpath =//div[@class=text]").__str__()
