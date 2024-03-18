from typing import Any, List, Optional, Union




from pydantic import (

    AnyHttpUrl,

    ConfigDict,

    PostgresDsn,

    ValidationInfo,

    field_validator,

)

from pydantic_settings import BaseSettings






class Settings(BaseSettings):

    """Application settings"""




    PROJECT_NAME: str = "FastApi template"

    API_ROOT_PATH: str = "/api/v1"

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []




    CUSTOMER_API_HOSTNAME: str

    POSTGRES_SERVER: str

    POSTGRES_USER: str

    POSTGRES_PASSWORD: str

    POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None




    model_config = ConfigDict(env_file=".env", case_sensitive=True)




    @field_validator("BACKEND_CORS_ORIGINS", mode="before")

    @classmethod

    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:

        """Validate cors origins"""

        if isinstance(v, str) and not v.startswith("["):

            return [i.strip() for i in v.split(",")]

        if isinstance(v, (list, str)):

            return v

        raise ValueError(v)




    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")

    @classmethod

    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:

        """Validate db connection"""

        if isinstance(v, str):

            return v

        return PostgresDsn.build(

            scheme="postgresql",

            username=info.data.get("POSTGRES_USER"),

            password=info.data.get("POSTGRES_PASSWORD"),

            host=info.data.get("POSTGRES_SERVER"),

            path=f"{info.data.get('POSTGRES_DB') or ''}",

        )






settings = Settings()
