import asyncio
import sys
from copy import copy
from time import sleep
from uuid import UUID, uuid4

import httpx
import requests
import yaml
from aiofile import async_open
from common.utils import (
    disable_unnecessary_loggers,
    get_args,
    get_logging_config,
    levelDEBUG,
    levelINFO,
)


class ConfigManager:
    def __init__(self) -> None:
        self._config_file = "config/config.yaml"
        self.BOT_ACTIVE = True

        self.secrets_data = {}
        args = get_args()
        self.ENV = args.env

        if self.ENV != "dev":
            disable_unnecessary_loggers()

        self.logging_config = get_logging_config(
            levelDEBUG if self.ENV == "dev" else levelINFO
        )
        self.logger = self.logging_config.configure()()

        self.load_creds_sync()
        error = self.get_creds()
        if error:
            self.logger.error(error)
            sys.exit(1)
        self.logger.info("Creds from config were loaded")

        error = self.load_secrets_sync()
        if error:
            self.logger.error(error)
            if self.ENV == "dev":
                sys.exit(1)
            self.logger.error("waiting 120 secs for secrets storage")
            sleep(120)
            error = self.load_secrets_sync()
        if error:
            self.logger.error(error)
            sys.exit(1)

        no_secrets = self.apply_secrets(get_db=True)
        if no_secrets:
            self.logger.error(f"No secrets found: {no_secrets}")
            sys.exit(1)
        self.logger.info("Secrets were loaded")

        self.lock = asyncio.Lock()

    def load_creds_sync(self) -> None:
        with open(self._config_file, "r") as f:
            self.creds_data = yaml.safe_load(f.read())

    async def load_creds_async(self) -> None:
        async with async_open(self._config_file, "r") as f:
            self.creds_data = yaml.safe_load(await f.read())

    def get_creds(self) -> str:
        try:
            self.SECRETS_DOMAIN = self.creds_data["secrets_domain"] or ""
            self.SECRETS_HEADER = self.creds_data["secrets_header"] or ""
            self.SECRETS_TOKEN = self.creds_data["secrets_token"] or ""
        except Exception:
            return "Error getting secrets creds from config-file"
        return ""

    async def update_creds(self, updated_creds: dict) -> None:
        self.creds_data.update(updated_creds)

        self.SECRETS_DOMAIN = self.creds_data["secrets_domain"]
        self.SECRETS_HEADER = self.creds_data["secrets_header"]
        self.SECRETS_TOKEN = self.creds_data["secrets_token"]

        async with async_open(self._config_file, "w") as f:
            yaml.dump(self.creds_data, f)

    def load_secrets_sync(self) -> str:
        try:
            response = requests.get(
                f"{self.SECRETS_DOMAIN}/api/secrets",
                headers={self.SECRETS_HEADER: self.SECRETS_TOKEN},
            )
            if response.status_code != 200:
                return (
                    f"Error getting data from secrets response - {response.status_code}"
                )
        except Exception as e:
            return f"Error getting data from secrets - {e}"

        try:
            self.secrets_data = response.json()["content"]
            return ""
        except Exception:
            return "Error getting secrets from response"

    async def load_secrets_async(self) -> str:
        try:
            async with httpx.AsyncClient(
                base_url=self.SECRETS_DOMAIN,
                headers={self.SECRETS_HEADER: self.SECRETS_TOKEN},
            ) as ac:
                response = await ac.get("/api/secrets")
                if response.status_code != 200:
                    return f"Error getting data from secrets response - {response.status_code}"
        except Exception as e:
            return f"Error getting data from secrets - {e}"

        try:
            self.secrets_data = response.json()["content"]
            return ""
        except Exception:
            return "Error getting secrets from response"

    def apply_secrets(self, get_db: bool) -> list[str]:
        no_secrets = []

        # database: need to get only at startup
        if get_db:
            db_data = self.secrets_data.get(f"{self.ENV}/db")
            try:
                self.DB_CONNECTION_STRING: str = db_data["connection string"]
            except Exception:
                no_secrets.append(f"{self.ENV}/db")

        # initial admin credentials
        admin_data = self.secrets_data.get(f"{self.ENV}/admin")
        try:
            self.ADMIN_LOGIN: str = admin_data["login"]
            self.ADMIN_PASSWORD: str = admin_data["password"]
            self.ADMIN_UUID: UUID = uuid4()
            self.ADMIN_TOKEN: str = admin_data["token"]
        except Exception:
            no_secrets.append(f"{self.ENV}/admin")

        # domain
        domain_data = self.secrets_data.get(f"{self.ENV}/domain")
        try:
            self.DOMAIN: str = domain_data["domain"]
        except Exception:
            no_secrets.append(f"{self.ENV}/domain")

        # auth service info
        auth_data = self.secrets_data.get(f"{self.ENV}/auth")
        try:
            self.AUTH_TOKEN_NAME: str = auth_data["token_name"]
            self.AUTH_TOKEN_SECRET: str = auth_data["token_secret"]
            self.AUTH_TOKEN_EXPIRE: int = auth_data["expire"]
        except Exception:
            no_secrets.append(f"{self.ENV}/auth")

        return no_secrets

    async def get_admin_uuid(self) -> UUID:
        async with self.lock:
            return self.ADMIN_UUID

    async def change_admin_uuid(self) -> UUID:
        async with self.lock:
            self.ADMIN_UUID = uuid4()
            return self.ADMIN_UUID

    async def update_admin_password(self, new_password: str) -> str:
        old_password = copy(self.ADMIN_PASSWORD)

        self.ADMIN_PASSWORD = new_password
        self.secrets_data[f"{self.ENV}/admin"]["password"] = new_password

        update_secrets_result = ""
        try:
            async with httpx.AsyncClient(
                base_url=self.SECRETS_DOMAIN,
                headers={self.SECRETS_HEADER: self.SECRETS_TOKEN},
            ) as ac:
                data = {"data": self.secrets_data[f"{self.ENV}/admin"]}
                response = await ac.put(f"/api/secrets/{self.ENV}/admin", json=data)
                if response.status_code != 200:
                    update_secrets_result = (
                        f"Error updating data in secrets - {response.status_code}"
                    )
        except Exception as e:
            update_secrets_result = f"Error updating data in secrets - {e}"

        if update_secrets_result:
            self.ADMIN_PASSWORD = old_password
            self.secrets_data[f"{self.ENV}/admin"]["password"] = old_password
        return update_secrets_result


cfg = ConfigManager()
