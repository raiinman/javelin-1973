import java.nio.file.Files;
import java.nio.file.Path;
import se.krka.kahlua.j2se.J2SEPlatform;
import se.krka.kahlua.luaj.compiler.LuaCompiler;
import se.krka.kahlua.vm.KahluaThread;

/** Runs the actual adapter against a controlled native API boundary. */
public final class CameraRuntimeCheck {
    public static void main(String[] args) throws Exception {
        var platform=J2SEPlatform.getInstance();
        var environment=platform.newEnvironment();
        var thread=new KahluaThread(platform,environment);
        thread.debugOwnerThread=Thread.currentThread();
        for (int i=0;i<2;i++) {
            var value=thread.call(LuaCompiler.loadstring(Files.readString(Path.of(args[i])),args[i],environment),new Object[0]);
            environment.rawset(i==0?"state_module":"bridge_module",value);
        }
        var suite=thread.call(LuaCompiler.loadstring(Files.readString(Path.of(args[2])),"adapter-fixture",environment),new Object[0]);
        thread.call(LuaCompiler.loadstring(Files.readString(Path.of(args[3])),"adapter",environment),new Object[0]);
        var result=thread.pcall(suite,new Object[0]);
        if (!Boolean.TRUE.equals(result[0])) throw new AssertionError(java.util.Arrays.toString(result));
        System.out.println("PASS: actual zoom adapter targets, suspension and native API fixture");
    }
}
