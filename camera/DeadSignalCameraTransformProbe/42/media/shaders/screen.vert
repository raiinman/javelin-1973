#version 330

// Original image-transform probe. This does not rotate world geometry.
layout (location = 0) in vec2 aPos;
layout (location = 1) in vec2 aUV;
layout (location = 2) in vec4 aColor;

uniform mat4 ModelViewProjection;
uniform vec2 TextureSize;
uniform vec4 SearchMode;
uniform vec4 ParamInfo;
uniform vec4 VarInfo;

out vec4 vColor;
out vec2 vUV;

void main()
{
    vec4 clip = ModelViewProjection * vec4(aPos, 0.0, 1.0);

    // Only the opt-in Lua transport writes this sentinel. Native search wins.
    bool transformActive = VarInfo.x == 0.0
        && SearchMode.x > 31.5 && SearchMode.x < 32.5
        && abs(SearchMode.y) <= 0.3501
        && abs(ParamInfo.w) <= 3.141693
        && abs(VarInfo.y) <= 1.396364
        && TextureSize.x > 0.0 && TextureSize.y > 0.0
        && abs(clip.w) > 0.000001;

    if (transformActive)
    {
        float aspect = TextureSize.x / TextureSize.y;
        vec2 point = clip.xy / clip.w;
        point.x *= aspect;

        float cosine = cos(ParamInfo.w);
        float sine = sin(ParamInfo.w);
        point = vec2(cosine * point.x - sine * point.y,
                     sine * point.x + cosine * point.y);
        point.x /= aspect;
        point.y *= cos(VarInfo.y);

        // Pan values are fractions of viewport dimensions, with positive Y down.
        point += vec2(2.0 * (SearchMode.x - 32.0), -2.0 * SearchMode.y);
        clip.xy = point * clip.w;
    }

    gl_Position = clip;
    vColor = aColor;
    vUV = aUV;
}
