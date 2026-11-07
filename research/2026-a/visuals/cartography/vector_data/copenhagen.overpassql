[out:json][timeout:90];(
way["highway"~"^(motorway|trunk|primary|secondary)(_link)?$"](55.608081,12.425203,55.738857,12.671027);
way["waterway"~"^(river|canal)$"](55.608081,12.425203,55.738857,12.671027);
way["natural"="coastline"](55.608081,12.425203,55.738857,12.671027);
way["highway"~"^(tertiary|residential)(_link)?$"](55.630718,12.469885,55.720550,12.629195);
);out geom;