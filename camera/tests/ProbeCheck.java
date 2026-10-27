import java.nio.file.Files;
import java.nio.file.Path;
import se.krka.kahlua.j2se.J2SEPlatform;
import se.krka.kahlua.luaj.compiler.LuaCompiler;
import se.krka.kahlua.vm.KahluaTable;
import se.krka.kahlua.vm.KahluaThread;

/** Executes only original sampling tests; compiles UI Lua without running game UI. */
public final class ProbeCheck {
    public static void main(String[] args) throws Exception {
        var platform = J2SEPlatform.getInstance();
        KahluaTable environment = platform.newEnvironment();
        var thread = new KahluaThread(platform, environment);
        thread.debugOwnerThread = Thread.currentThread();
        Object module = thread.call(LuaCompiler.loadstring(Files.readString(Path.of(args[0])), "sample", environment), new Object[0]);
        environment.rawset("sample", module);
        Object[] result = thread.pcall(LuaCompiler.loadstring(Files.readString(Path.of(args[1])), "tests", environment), new Object[0]);
        if (!Boolean.TRUE.equals(result[0])) throw new AssertionError(java.util.Arrays.toString(result));
        for (int i=2; i<args.length; i++) {
            LuaCompiler.loadstring(Files.readString(Path.of(args[i])), "client-source", environment);
        }
        System.out.println("PASS: sample behavior and UI syntax; native execution is a separate check");
    }
}
