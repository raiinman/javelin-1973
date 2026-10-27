import java.nio.file.Files;
import java.nio.file.Path;
import se.krka.kahlua.luaj.compiler.LuaCompiler;
import se.krka.kahlua.j2se.J2SEPlatform;
import se.krka.kahlua.vm.KahluaThread;

/** Execute supplied isolated Lua regressions with fake runtime objects, no game. */
public final class RuntimePoseClockCheck {
    public static void main(String[] args) throws Exception {
        var platform = J2SEPlatform.getInstance();
        var environment = platform.newEnvironment();
        var closure = LuaCompiler.loadstring(Files.readString(Path.of(args[0])), "pose-clock-test", environment);
        var thread = new KahluaThread(platform, environment);
        thread.debugOwnerThread = Thread.currentThread();
        thread.call(closure, null, null, null);
        System.out.println("PASS: isolated shipped-Lua-VM regression");
    }
}
