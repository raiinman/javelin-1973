import java.nio.file.Files;
import java.nio.file.Path;
import se.krka.kahlua.j2se.J2SEPlatform;
import se.krka.kahlua.luaj.compiler.LuaCompiler;
import se.krka.kahlua.vm.KahluaThread;

public final class FastLoadCheck {
    public static void main(String[] args) throws Exception {
        var platform = J2SEPlatform.getInstance();
        var environment = platform.newEnvironment();
        var thread = new KahluaThread(platform, environment);
        thread.debugOwnerThread = Thread.currentThread();
        for (String arg : args) {
            if (arg.startsWith("compile-only:")) {
                var path = arg.substring("compile-only:".length());
                LuaCompiler.loadstring(Files.readString(Path.of(path)), path, environment);
                continue;
            }
            var result = thread.pcall(LuaCompiler.loadstring(Files.readString(Path.of(arg)), arg, environment), new Object[0]);
            if (!Boolean.TRUE.equals(result[0])) throw new AssertionError(java.util.Arrays.toString(result));
        }
        System.out.println("PASS: actual Fast Load adapter lifecycle fixture; native timing is separate");
    }
}
