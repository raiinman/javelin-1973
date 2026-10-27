-- Activate this vehicle's permanent original cabin and cargo lining.
J73Vehicles = J73Vehicles or {}

function J73Vehicles.InitInterior(vehicle, part)
    if vehicle:getScriptName() == "Base.Javelin73PC" then
        part:setModelVisible("Default", true)
    end
end
