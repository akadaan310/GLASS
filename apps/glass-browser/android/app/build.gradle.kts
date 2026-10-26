plugins { id("com.android.application") }
android {
    namespace = "org.glass.nativebrowser"
    compileSdk = 36
    defaultConfig { applicationId = "org.glass.nativebrowser"; minSdk = 29; targetSdk = 36; versionCode = 1; versionName = "0.1.0" }
    externalNativeBuild { cmake { path = file("src/main/cpp/CMakeLists.txt"); version = "3.22.1" } }
    ndkVersion = "27.2.12479018"
    buildTypes { getByName("release") { isMinifyEnabled = false } }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_17; targetCompatibility = JavaVersion.VERSION_17 }
    defaultConfig { ndk { abiFilters += listOf("arm64-v8a") } }
}
