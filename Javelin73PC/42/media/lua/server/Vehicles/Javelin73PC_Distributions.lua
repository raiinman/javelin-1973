-- Use the game's ordinary sports-car loot pools. This table owns only this mod ID.
require "Vehicles/VehicleDistributions"

table.insert(VehicleDistributions, 1, {
    Javelin73PC = { Normal = VehicleDistributions.NormalSports },
})
