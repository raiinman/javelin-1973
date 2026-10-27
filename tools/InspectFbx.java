import jassimp.AiAnimation;
import jassimp.AiMesh;
import jassimp.AiPostProcessSteps;
import jassimp.AiScene;
import jassimp.Jassimp;
import jassimp.JassimpLibraryLoader;
import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.EnumSet;
import org.lwjgl.util.vector.Matrix4f;

/** Read-only import probe using the installed game's Assimp and mesh resolver. */
public class InspectFbx {
    public static void main(String[] args) throws Exception {
        if (args.length < 2) {
            throw new IllegalArgumentException("Usage: InspectFbx <game-directory> <fbx> [mesh-node ...]");
        }
        Path game = Path.of(args[0]).toAbsolutePath();
        Jassimp.setLibraryLoader(new JassimpLibraryLoader() {
            public void loadLibrary() {
                System.load(game.resolve("jassimp64.dll").toString());
            }
        });
        // Match FileTask_LoadMesh.loadFBX defaults. MAKE_LEFT_HANDED flips Z;
        // a raw Assimp import gives misleading vehicle nose/axle anchors.
        var flags = EnumSet.of(AiPostProcessSteps.FIND_INSTANCES,
                AiPostProcessSteps.MAKE_LEFT_HANDED, AiPostProcessSteps.LIMIT_BONE_WEIGHTS,
                AiPostProcessSteps.TRIANGULATE, AiPostProcessSteps.OPTIMIZE_MESHES,
                AiPostProcessSteps.REMOVE_REDUNDANT_MATERIALS,
                AiPostProcessSteps.JOIN_IDENTICAL_VERTICES);
        AiScene scene = Jassimp.importFile(Path.of(args[1]).toAbsolutePath().toString(), flags);
        System.out.println("POSTPROCESS " + flags);
        System.out.println("IMPORTED meshes=" + scene.getNumMeshes()
                + " animations=" + scene.getNumAnimations());
        Class<?> processorClass = Class.forName(
                "zombie.core.skinnedmodel.model.jassimp.ProcessedAiScene");
        Constructor<?> constructor = processorClass.getDeclaredConstructor();
        constructor.setAccessible(true);
        Object processor = constructor.newInstance();
        Method findMesh = processorClass.getDeclaredMethod("findMesh", AiScene.class, String.class);
        findMesh.setAccessible(true);
        Method meshTransform = processorClass.getDeclaredMethod(
                "initMeshTransform", AiScene.class, AiMesh.class);
        meshTransform.setAccessible(true);
        for (int index = 2; index < args.length; index++) {
            String name = args[index];
            AiMesh mesh = (AiMesh) findMesh.invoke(processor, scene, name);
            if (mesh == null) {
                System.out.println("UNRESOLVED " + name);
                continue;
            }
            Matrix4f transform = (Matrix4f) meshTransform.invoke(processor, scene, mesh);
            float[] low = {Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY};
            float[] high = {Float.NEGATIVE_INFINITY, Float.NEGATIVE_INFINITY, Float.NEGATIVE_INFINITY};
            float[] renderLow = low.clone();
            float[] renderHigh = high.clone();
            for (int vertex = 0; vertex < mesh.getNumVertices(); vertex++) {
                float x = mesh.getPositionX(vertex);
                float y = mesh.getPositionY(vertex);
                float z = mesh.getPositionZ(vertex);
                float[] point = transform == null ? new float[] {x, y, z} : new float[] {
                        transform.m00*x + transform.m10*y + transform.m20*z + transform.m30,
                        transform.m01*x + transform.m11*y + transform.m21*z + transform.m31,
                        transform.m02*x + transform.m12*y + transform.m22*z + transform.m32};
                // Vehicle rendering transposes ModelMesh.transform before multiplication.
                // These bounds omit model-script scale and vehicle/world placement.
                float[] renderPoint = transform == null ? new float[] {x, y, z} : new float[] {
                        transform.m00*x + transform.m01*y + transform.m02*z + transform.m03,
                        transform.m10*x + transform.m11*y + transform.m12*z + transform.m13,
                        transform.m20*x + transform.m21*y + transform.m22*z + transform.m23};
                if (vertex == 0) {
                    System.out.println("RENDER_VERTEX0 " + name + " " + Arrays.toString(renderPoint));
                }
                for (int axis = 0; axis < 3; axis++) {
                    low[axis] = Math.min(low[axis], point[axis]);
                    high[axis] = Math.max(high[axis], point[axis]);
                    renderLow[axis] = Math.min(renderLow[axis], renderPoint[axis]);
                    renderHigh[axis] = Math.max(renderHigh[axis], renderPoint[axis]);
                }
            }
            System.out.println("RESOLVED " + name + " mesh=" + mesh.getName()
                    + " vertices=" + mesh.getNumVertices());
            System.out.println("NATIVE_TRANSFORM " + transform);
            System.out.println("TRANSFORMED_BOUNDS " + Arrays.toString(low) + " " + Arrays.toString(high));
            System.out.println("RENDER_BOUNDS " + name + " " + Arrays.toString(renderLow) + " " + Arrays.toString(renderHigh));
        }
        for (AiAnimation animation : scene.getAnimations()) {
            String name = animation.getName();
            String clip = name.substring(name.lastIndexOf('|') + 1);
            System.out.println("ANIMATION name=" + name + " clip=" + clip
                    + " duration=" + animation.getDuration()
                    + " ticksPerSecond=" + animation.getTicksPerSecond()
                    + " channels=" + animation.getNumChannels());
        }
    }
}
