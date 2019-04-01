#define IS_PYGAME 0
#define JAVA_NAMESPACE "org.kivy.android"
#define BOOTSTRAP "sdl2"
#define JNI_NAMESPACE "org/kivy/android"
#define IS_SDL2 1
#define PY2 0
JNIEnv *SDL_AndroidGetJNIEnv(void);
#define SDL_ANDROID_GetJNIEnv SDL_AndroidGetJNIEnv
