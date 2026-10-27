"""Execute the actual audit scheduler in the shipped Lua VM with a fake clock."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from prepare_runtime_test import AUDIT

GAME = Path(os.environ.get('J73_TEST_GAME', 'C:/Games/ProjectZomboid'))
TOOLS = Path(__file__).resolve().parent


class RuntimePoseClockTests(unittest.TestCase):
    @unittest.skipUnless((GAME/'projectzomboid.jar').is_file() and shutil.which('javac'),
                         'requires the installed game compiler and JDK')
    def test_editor_pause_preserves_all_inspection_intervals(self):
        begin = AUDIT.index('local function cycle_panels(car)')
        end = AUDIT.index('debugScenarios.J73VisualTest', begin)
        suite_begin = AUDIT.index('local function begin_gameplay()')
        suite_end = AUDIT.index('Events.OnTick.Add(begin_gameplay)', suite_begin)
        suite = AUDIT[suite_begin:suite_end].replace('__SUITE_DELAY__', '65000')
        source = r'''
local now, tick, removed = 0, nil, false
local marks = {}
local TAG, visual_test_active, panel_cycle_active = '', true, false
local function check(value, message) assert(value, message) end
function getDebug() return true end
function getTimestampMs() return now end
function print(message) marks[#marks+1] = message end
Events = { OnTick = {
    Add = function(callback) tick = callback end,
    Remove = function(callback) assert(callback == tick); removed = true end
} }
local parts = {}
local function part(id)
    if not parts[id] then
        local value = { open=false, delta=0 }
        function value:getDoor() return self end
        function value:getWindow() return self end
        function value:setOpen(open) self.open = open end
        function value:setOpenDelta(delta) self.delta = delta end
        parts[id] = value
    end
    return parts[id]
end
local car = {}
function car:getPartById(id) return part(id) end
function car:playPartAnim(value, animation) end
''' + AUDIT[begin:end] + r'''
cycle_panels(car)
assert(panel_cycle_active, 'panel cycle must guard the gameplay suite')
for i=1,50 do now=now+100; tick() end
now=now+180000; tick()
assert(#marks == 1 and not removed, 'editor pause skipped an inspection pose')
for i=1,149 do now=now+100; tick() end
assert(#marks == 2 and parts.DoorFrontLeft.open and parts.TrunkDoor.open,
       'open panels did not receive their inspection interval')
for i=1,200 do now=now+100; tick() end
assert(#marks == 3 and parts.DoorFrontLeft.open and parts.WindowFrontLeft.open,
       'lowered windows with open doors did not receive their interval')
for i=1,200 do now=now+100; tick() end
assert(#marks == 4 and not parts.DoorFrontLeft.open and not parts.WindowFrontLeft.open,
       'final pose did not restore closed parts')
assert(removed, 'completed pose callback remains registered')
assert(not panel_cycle_active, 'completed pose cycle still blocks gameplay')
local started, gameplay_started = 0, false
J73GameplayAudit = { start=function() gameplay_started=true end }
Events.OnTick.Remove = function(callback) end
''' + suite + r'''
now = 1000000
panel_cycle_active = true
begin_gameplay()
assert(not gameplay_started, 'gameplay started during the delayed panel cycle')
panel_cycle_active = false
begin_gameplay()
assert(gameplay_started, 'gameplay did not start after the panel cycle')
'''
        with tempfile.TemporaryDirectory(prefix='j73-pose-clock-') as folder:
            output = Path(folder).resolve()
            script = output/'test.lua'
            script.write_text(source, encoding='utf-8')
            jar = GAME/'projectzomboid.jar'
            compile_result = subprocess.run(['javac', '--release', '25', '-classpath', str(jar),
                '-d', str(output), str(TOOLS/'RuntimePoseClockCheck.java')], capture_output=True, text=True)
            self.assertEqual(compile_result.returncode, 0, compile_result.stdout+compile_result.stderr)
            java = GAME/'jre64/bin/java.exe'
            run = subprocess.run([str(java), '-classpath', str(output)+os.pathsep+str(jar),
                'RuntimePoseClockCheck', str(script)], cwd=GAME, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout+run.stderr)


if __name__ == '__main__':
    unittest.main()
