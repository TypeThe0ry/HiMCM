[out:json][timeout:90];(
way["highway"~"^(motorway|trunk|primary|secondary)(_link)?$"](43.218111,-80.412828,44.492242,-78.539759);
way["waterway"~"^(river|canal)$"](43.218111,-80.412828,44.492242,-78.539759);
way["natural"="coastline"](43.218111,-80.412828,44.492242,-78.539759);
way["highway"~"^(tertiary|residential)(_link)?$"](43.655471,-79.620768,43.835134,-79.372072);
);out geom;