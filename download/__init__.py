from ong_utils import create_pool_manager, OngConfig
_cfg = OngConfig("campamento_masterchef")
config = _cfg.config
logger = _cfg.logger

http = create_pool_manager()