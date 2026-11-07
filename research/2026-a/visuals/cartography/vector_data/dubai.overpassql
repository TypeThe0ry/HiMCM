[out:json][timeout:90];(
way["highway"~"^(motorway|trunk|primary|secondary)(_link)?$"](24.909235,54.962962,25.471379,55.621463);
way["waterway"~"^(river|canal)$"](24.909235,54.962962,25.471379,55.621463);
way["natural"="coastline"](24.909235,54.962962,25.471379,55.621463);
way["highway"~"^(tertiary|residential)(_link)?$"](25.132895,55.233091,25.312558,55.431689);
);out geom;