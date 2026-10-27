"""Exercise actual reload Lua against a real Java HashSet in the shipped VM."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

GAME = Path(os.environ.get('J73_TEST_GAME', 'C:/Games/ProjectZomboid'))
TOOLS = Path(__file__).resolve().parent
JAVA = r'''
import java.nio.file.*;
import java.util.*;
import se.krka.kahlua.j2se.J2SEPlatform;
import se.krka.kahlua.converter.*;
import zombie.Lua.KahluaNumberConverter;
import zombie.Lua.LuaManager.Exposer;
import se.krka.kahlua.luaj.compiler.LuaCompiler;
import se.krka.kahlua.vm.KahluaThread;
public class VehicleSetCheck {
 public static void main(String[] args) throws Exception {
  var platform=J2SEPlatform.getInstance();var env=platform.newEnvironment();
  var manager=new KahluaConverterManager();KahluaNumberConverter.install(manager);
  var exposer=new Exposer(manager,platform,env);
  for (var type : new Class<?>[]{HashSet.class,Iterator.class,ArrayList.class}) exposer.setExposed(type);
  for (var type : new Class<?>[]{HashSet.class,Iterator.class,ArrayList.class}) exposer.exposeLikeJava(type,env);
  env.rawset("vehicleSet",new HashSet<Object>());
  env.rawset("cargoList",new ArrayList<Object>());
  var closure=LuaCompiler.loadstring(Files.readString(Path.of(args[0])),"vehicle-set-regression",env);
  var thread=new KahluaThread(platform,env);thread.debugOwnerThread=Thread.currentThread();
  thread.call(closure,null,null,null);
  System.out.println("PASS: actual HashSet/Iterator and ArrayList exposed to shipped Lua VM");
 }
}
'''


@unittest.skipUnless((GAME/'projectzomboid.jar').is_file() and shutil.which('javac'),
                     'requires installed shipped Lua VM and JDK')
class RuntimeVehicleSetTests(unittest.TestCase):
    def test_save_marker_rejects_clamping_before_save(self):
        gameplay=(TOOLS/'runtime_gameplay.lua').read_text(encoding='utf-8')
        begin=gameplay.index('local function save_snapshot(car)')
        actual=gameplay[begin:gameplay.index('function J73GameplayAudit.visualFinal(',begin)]
        source=r'''
local TAG,TOKEN,RECORD='[J73_AUDIT] ','test-token','test-record'
local function check(value,message) assert(value,message) end
local saved,written,fuel,requested,engine,window,loot=false,false,0,nil,nil,false,false
local messages={}
function print(message) messages[#messages+1]=message end
function getDebug() return true end
function getCore() return {setNoSave=function(self,value) assert(value==false) end} end
function getWorld() return {getGameMode=function() return 'Sandbox' end,getWorld=function() return '12345' end} end
function save(value) assert(value==true);saved=true end
function getFileWriter() return {write=function() written=true end,close=function() end} end
local gas={setContainerContentAmount=function(self,value) requested=value;fuel=math.max(0,math.min(value,35)) end,
 getContainerContentAmount=function() return fuel end,getContainerCapacity=function() return 35 end}
local windowState={setOpen=function(self,value) window=value end,setOpenDelta=function(self,value) assert(value==1) end}
local parts={GasTank=gas,Engine={setCondition=function(self,value) engine=value end},
 WindowFrontLeft={getWindow=function() return windowState end},
 TruckBed={getItemContainer=function() return {AddItem=function(self,id)
  assert(id=='Base.Screwdriver');loot=true;return {getModData=function() return {} end} end} end}}
local car={shutOff=function() end,setHeadlightsOn=function(self,value) assert(value==false) end,
 getPartById=function(self,id) return parts[id] end,getModData=function() return {} end}
local function clamped_control()
''' + actual.replace('12.25','37.25') + r'''
save_snapshot(car)
end
local ok,err=pcall(clamped_control)
assert(not ok and string.find(tostring(err),'marker was clamped'),tostring(err))
assert(requested==37.25 and fuel==35,'control did not reproduce native capacity clamp')
assert(not saved and not written and not engine and not loot,'clamped control reached save or later mutations')
''' + actual + r'''
save_snapshot(car)
assert(requested==12.25 and fuel==12.25 and saved and written,'safe marker failed to save exact amount')
assert(engine==83 and window and loot,'remaining snapshot state was not prepared')
assert(string.find(messages[1],'SAVE_FUEL requested=12.25; readback=12.25; capacity=35'),table.concat(messages,';'))
'''
        with tempfile.TemporaryDirectory(prefix='j73-save-fuel-') as folder:
            output=Path(folder);java_source=output/'VehicleSetCheck.java';script=output/'test.lua'
            java_source.write_text(JAVA,encoding='utf-8');script.write_text(source,encoding='utf-8')
            jar=GAME/'projectzomboid.jar'
            compiled=subprocess.run(['javac','--release','25','-classpath',str(jar),'-d',str(output),str(java_source)],
                                    capture_output=True,text=True)
            self.assertEqual(compiled.returncode,0,compiled.stdout+compiled.stderr)
            run=subprocess.run([str(GAME/'jre64/bin/java.exe'),'-classpath',str(output)+os.pathsep+str(jar),
                                'VehicleSetCheck',str(script)],cwd=GAME,capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stdout+run.stderr)

    def test_reload_finds_tagged_car_in_real_native_set(self):
        gameplay=(TOOLS/'runtime_gameplay.lua').read_text(encoding='utf-8')
        begin=gameplay.index('function J73GameplayAudit.verifyReload(visual_final)')
        actual=gameplay[begin:gameplay.index('function J73GameplayAudit.start(',begin)]
        source=r'''
local TAG,TOKEN='[J73_AUDIT] ','J73-disposable-persistence-v1'
local function check(value,message) assert(value,message) end
local now,callback,removed=0,nil,false
local messages={}
function print(message) messages[#messages+1]=message end
function getTimestampMs() return now end
function getCell() return {getVehicles=function() return vehicleSet end} end
Events={OnTick={Add=function(fn) callback=fn end,Remove=function(fn) assert(fn==callback);removed=true end}}
J73GameplayAudit={}
''' + actual + r'''
assert(vehicleSet.get==nil,'fixture unexpectedly supplies indexed Set.get')
J73GameplayAudit.verifyReload(false)
callback()
assert(not removed,'empty set should wait for the tagged car')
local unrelated={getModData=function() return {} end}
vehicleSet:add(unrelated)
now=100;callback()
assert(not removed,'real HashSet enumeration failed: '..table.concat(messages,';'))
local item={getModData=function() return {J73PersistenceToken=TOKEN} end}
cargoList:add(item)
local window={isOpen=function() return true end,getOpenDelta=function() return 1 end}
local fuel={getContainerContentAmount=function() return 12.25 end}
local engine={getCondition=function() return 83 end}
local windowPart={getWindow=function() return window end}
local trunk={getItemContainer=function() return {getItems=function() return cargoList end} end}
local parts={GasTank=fuel,Engine=engine,WindowFrontLeft=windowPart,TruckBed=trunk}
local modDataCalls=0
local car={getModData=function() modDataCalls=modDataCalls+1;return {J73PersistenceToken=TOKEN} end,
 getScript=function() return {getFullName=function() return 'Base.Javelin73PC' end} end,
 getPartById=function(self,id) return parts[id] end}
vehicleSet:add(car)
now=200;callback()
assert(removed and modDataCalls>0,'tagged saved car was not enumerated')
assert(#messages==1 and string.find(messages[1],'PASS real save/reload'),table.concat(messages,';'))
'''
        with tempfile.TemporaryDirectory(prefix='j73-real-set-') as folder:
            output=Path(folder);java_source=output/'VehicleSetCheck.java';script=output/'test.lua'
            java_source.write_text(JAVA,encoding='utf-8');script.write_text(source,encoding='utf-8')
            jar=GAME/'projectzomboid.jar'
            compiled=subprocess.run(['javac','--release','25','-classpath',str(jar),'-d',str(output),str(java_source)],
                                    capture_output=True,text=True)
            self.assertEqual(compiled.returncode,0,compiled.stdout+compiled.stderr)
            run=subprocess.run([str(GAME/'jre64/bin/java.exe'),'-classpath',str(output)+os.pathsep+str(jar),
                                'VehicleSetCheck',str(script)],cwd=GAME,capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stdout+run.stderr)
            print(run.stdout.strip())


if __name__ == '__main__':
    unittest.main()
