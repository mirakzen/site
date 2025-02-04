from api.answers import HTTPanswer
from api.routes.games import RouterController as ControllerGames
from api.routes.projects import RouterController as ControllerProjects
from api.routes.socials import RouterController as ControllerSocials
from litestar import Router, get
from litestar.status_codes import HTTP_200_OK
from versions import APP_VERSION_DICT


@get("/versions", sync_to_thread=False, exclude_from_auth=True)
def get_version() -> dict[str, str]:
    return HTTPanswer(HTTP_200_OK, APP_VERSION_DICT)


router = Router(path="/api", route_handlers=[get_version])
router.register(Router("/games", route_handlers=[ControllerGames]))
router.register(Router("/projects", route_handlers=[ControllerProjects]))
router.register(Router("/socials", route_handlers=[ControllerSocials]))
