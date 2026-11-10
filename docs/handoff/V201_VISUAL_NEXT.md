Current status: the first figure is in the sole main, page16. See [current implementation and verification](CURRENT_SPATIAL_UPDATE.md). The following acquisition inventory is retained as the pre-implementation plan; current source records are in `research/2026-a/visuals/current_spatial/`.

# Satellite and quantitative3D: first figure delivered

The user requested satellite and three-dimensional figures with stronger art direction. This remains an active deliverable after the V200/V201 numerical migration. The visual inventory below prevents an attractive map from changing the measured research object.

## Available evidence

- `research/2026-a/data/task4_access/8133_hexes.zip`: Singapore, 5,400 author-published hexes; `9808_hexes.zip`: Zurich, 845 hexes. The source manifest and README bind the author dataset. The `c_f` field measures modelled mean walking time to 20 generic Learning POIs for retained resident grids. It is not observed student travel or access to the current pool inventory. Individual city source dates are not supplied.
- Existing satellite imagery and cached OSM road/water layers cover Copenhagen, Toronto, Dubai and Shanghai. Zurich and Singapore satellite panels need new documented acquisition. See `research/2026-a/visuals/cartography/satellite/README.md` and its manifest; do not reuse another city's image under a new label.
- Current Zurich and Singapore swimming inventory sources are named facility lists with operating restrictions. They do not yet supply a verified aligned geographic layer or student catchments. General commute values in the original CSV do not describe trips to these facilities.
- No measured DEM, building heights or physical three-dimensional city mesh was identified in the repository.

## Design and acquisition

Prepare a 6.5-inch figure with a restrained satellite locator and a clearly labelled quantitative layer. Record product, acquisition/composite date, source resolution, coverage, projection, attribution and rendering operations. If building/terrain geometry is used, acquire real heights/elevation first. An alternative is an explicitly labelled three-dimensional data surface with height encoding the measured travel-time field; it must not look like measured terrain or building heights. Keep a two-dimensional comparison panel so the encoded values remain readable.

The first defensible mapped claim is resident access to generic Learning POIs under the archived author model. A student-access claim requires matching facility coordinates, eligibility/opening hours, student population and route calculations. Do not silently rename the existing resident proxy.

Use clear typographic hierarchy, purposeful contrast and open space informed by [LandingLove](https://www.landing.love/) and the [Awwwards editorial reference](https://assets.awwwards.com/awards/gallery/2023/07/HOT-RIGHT-NOW-BOOK-2023.pdf). These references guide presentation; they do not provide geographic evidence. All inserted figure text remains at least9pt. Final caption, map scale and source scope must survive actual manuscript-size rendering.
