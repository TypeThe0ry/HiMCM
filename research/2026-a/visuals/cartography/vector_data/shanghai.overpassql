[out:json][timeout:90];(
way["highway"~"^(motorway|trunk|primary|secondary)(_link)?$"](30.806449,120.940719,31.584218,121.904527);
way["waterway"~"^(river|canal)$"](30.806449,120.940719,31.584218,121.904527);
way["natural"="coastline"](30.806449,120.940719,31.584218,121.904527);
way["highway"~"^(tertiary|residential)(_link)?$"](31.102976,121.322207,31.282639,121.532233);
);out geom;