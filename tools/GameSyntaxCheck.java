import java.nio.file.Files;
import java.nio.file.Path;
import se.krka.kahlua.luaj.compiler.LuaCompiler;
import se.krka.kahlua.j2se.J2SEPlatform;
import zombie.scripting.ScriptParser;

/** Syntax-only checks using the installed game's compiler. Never executes mod Lua. */
public final class GameSyntaxCheck {
    public static void main(String[] args) throws Exception {
        int count = 0;
        for (String argument : args) {
            Path path = Path.of(argument);
            String source = Files.readString(path);
            if (argument.endsWith(".lua")) {
                LuaCompiler.loadstring(source, path.getFileName().toString(), J2SEPlatform.getInstance().newTable());
            } else {
                ScriptParser.parse(ScriptParser.stripComments(source));
            }
            System.out.println("PARSED " + path.getFileName());
            count++;
        }
        System.out.println("PASS: " + count + " files parsed by game classes; runtime behavior untested");
    }
}
