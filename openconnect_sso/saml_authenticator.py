import structlog

from openconnect_sso.browser import Browser

log = structlog.get_logger()


def authenticate_in_browser(proxy, auth_info, display_mode, chrome_driver_path, override_script=None, cfg=None):
    with Browser(cfg, proxy, display_mode, chrome_driver_path) as browser:
        return browser.authenticate_at(
            auth_info.login_url, auth_info.token_cookie_name, override_script
        )
