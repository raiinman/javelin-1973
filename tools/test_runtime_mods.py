"""Run extracted debug-scenario mod initialization and save guards in native Lua VM."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from prepare_runtime_test import AUDIT, gameplay_source

GAME = Path(os.environ.get('J73_TEST_GAME', 'C:/Games/ProjectZomboid'))
TOOLS = Path(__file__).resolve().parent


@unittest.skipUnless((GAME/'projectzomboid.jar').is_file() and shutil.which('javac'),
                     'requires installed shipped Lua VM and JDK')
class RuntimeModInitializationTests(unittest.TestCase):
    def test_debug_route_copies_mods_before_world_creation_and_preserves_resume(self):
        helper = AUDIT[AUDIT.index('local function initialize_visual_mods()'):AUDIT.index('local function run_audit()')]
        begin = AUDIT.index('    setSandbox = function()')
        sandbox = AUDIT[begin:AUDIT.index('    onStart = function()', begin)].replace('__SAVE_TEST__', 'true')
        vanilla = (GAME/'media/lua/client/DebugUIs/DebugScenarios.lua').read_text(encoding='utf-8')
        begin = vanilla.index('function DebugScenarios:launchScenario(scenario)')
        launch = vanilla[begin:vanilla.index('function doDebugScenarios()', begin)]
        begin = AUDIT.index('        local function start_visual_test()')
        auto = AUDIT[begin:AUDIT.index('        Events.OnRenderTick.Add(start_visual_test)', begin)].replace('__SAVE_TEST__', 'true')
        copied = gameplay_source(True)
        begin = copied.index('    check(getDebug(), "Persistence test requires debug scenario")')
        guard = copied[begin:copied.index('    getCore():setNoSave(false)', begin)]
        setup = r'''
local TAG = ''
local function check(value,message) assert(value,message) end
local defaultMods = {mods={'PZToolkitBridge','Javelin73PC','UnrelatedEnabled'},maps={'CustomMap','Muldraugh, KY'}}
local currentMods = {mods={},maps={}}
local copies, created, resumed, resetRequired = 0, false, false, false
local function same(a,b)
 assert(#a==#b)
 for i=1,#a do assert(a[i]==b[i]) end
end
local function isActive(self,id)
 for _,name in ipairs(self.mods) do if name==id then return true end end
 return false
end
defaultMods.isModActive=isActive;currentMods.isModActive=isActive
function currentMods:copyFrom(source)
 copies=copies+1;self.mods={};self.maps={}
 for _,name in ipairs(source.mods) do self.mods[#self.mods+1]=name end
 for _,name in ipairs(source.maps) do self.maps[#self.maps+1]=name end
end
ActiveMods={getById=function(id)
 if id=='default' then return defaultMods end
 assert(id=='currentGame');return currentMods
end,requiresResetLua=function(mods) assert(mods==currentMods);return resetRequired end}
function getDebug() return true end
local world={setMap=function() end,setGameMode=function() end}
function getWorld() return world end
function getCore() return {setNoSave=function() end} end
function SystemDisablerCall() end
SystemDisabler={setDoZombieCreation=SystemDisablerCall}
SandboxVars={}
function ZombRand(n) return 1 end
function createWorld(name)
 assert(currentMods:isModActive('Javelin73PC'),'world created before currentGame mod initialization')
 same(currentMods.mods,defaultMods.mods);same(currentMods.maps,defaultMods.maps)
 created=true
end
GameWindow={doRenderEvent=function() end}
Events={OnNewGame={Add=function() end},LoadGridsquare={Add=function() end},OnRenderTick={Remove=function() end}}
LoadingQueueState={new=function() return {} end}
function forceChangeState(state) assert(created) end
DebugScenarios={ongamestart=function() end,onloadgs=function() end,instance={setVisible=function() end}}
MainScreen={instance={}}
'''
        assertions = r'''
local scenario={
''' + sandbox + r'''
}
debugScenarios={J73VisualTest=scenario}
DebugScenarios:launchScenario(scenario)
assert(created and copies==1,'fresh route did not initialize exactly once')
same(defaultMods.mods,{'PZToolkitBridge','Javelin73PC','UnrelatedEnabled'})
same(defaultMods.maps,{'CustomMap','Muldraugh, KY'})
created=false;defaultMods.mods={'PZToolkitBridge'}
local before=copies
local ok,err=pcall(function() DebugScenarios:launchScenario(scenario) end)
assert(not ok and not created and copies==before,'missing target was allowed to create/alter a world')
defaultMods.mods={'PZToolkitBridge','Javelin73PC','NewDefaultOnly'}
currentMods.mods={'PZToolkitBridge','Javelin73PC','SavedWorldOnly'}
J73GameplayAudit={tryResume=function() resumed=true;return true end}
''' + auto + r'''
start_visual_test()
assert(resumed and copies==before,'resume copied default over saved-world selection')
same(currentMods.mods,{'PZToolkitBridge','Javelin73PC','SavedWorldOnly'})
local function save_guard_probe()
''' + guard + r'''
 return true
end
assert(save_guard_probe(),'valid active/loaded set refused')
currentMods.mods={'PZToolkitBridge'}
ok,err=pcall(save_guard_probe)
assert(not ok and string.find(err,'Refusing save without Javelin73PC'),'missing target passed pre-save guard')
currentMods.mods={'PZToolkitBridge','Javelin73PC'};resetRequired=true
ok,err=pcall(save_guard_probe)
assert(not ok and string.find(err,'mismatched loaded mod set'),'loaded set mismatch passed pre-save guard')
'''
        green = setup + helper + launch + assertions
        # Regression control removes only the fix's actual scenario callback call.
        red = green.replace('        initialize_visual_mods()\n', '', 1)
        self.assertNotEqual(red, green)
        with tempfile.TemporaryDirectory(prefix='j73-mods-vm-') as folder:
            output = Path(folder)
            jar = GAME/'projectzomboid.jar'
            compile_result = subprocess.run(['javac','--release','25','-classpath',str(jar),'-d',str(output),
                str(TOOLS/'RuntimePoseClockCheck.java')],capture_output=True,text=True)
            self.assertEqual(compile_result.returncode,0,compile_result.stdout+compile_result.stderr)
            for colour, source in [('red',red),('green',green)]:
                script=output/(colour+'.lua');script.write_text(source,encoding='utf-8')
                run=subprocess.run([str(GAME/'jre64/bin/java.exe'),'-classpath',str(output)+os.pathsep+str(jar),
                    'RuntimePoseClockCheck',str(script)],cwd=GAME,capture_output=True,text=True)
                if colour=='red':
                    self.assertNotEqual(run.returncode,0,'regression control unexpectedly passed')
                    self.assertIn('world created before currentGame mod initialization',run.stdout+run.stderr)
                    print('RED proved: removing only setSandbox initialization fails before world creation')
                else:
                    self.assertEqual(run.returncode,0,run.stdout+run.stderr)
                    print('GREEN proved: actual initialization, full mods/maps copy, resume preservation and pre-save guards pass')


if __name__ == '__main__':
    unittest.main()
