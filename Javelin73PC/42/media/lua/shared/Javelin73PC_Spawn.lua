-- Append a unique entry without replacing another vehicle or a zone definition.
require "VehicleZoneDefinition"

local zone_weights = { parkingstall = 0.35, medium = 0.5, good = 1.0 }
for zone_name, weight in pairs(zone_weights) do
    local zone = VehicleZoneDistribution[zone_name]
    if zone and zone.vehicles then
        zone.vehicles["Base.Javelin73PC"] = { index = 0, spawnChance = weight }
    end
end
