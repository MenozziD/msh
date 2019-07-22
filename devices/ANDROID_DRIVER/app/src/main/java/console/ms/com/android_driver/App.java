package console.ms.com.android_driver;

import android.app.Application;
import android.content.Intent;

public class App extends Application {

    private static App sInstance;
    private Intent server_intent;

    @Override
    public void onCreate() {
        super.onCreate();
        sInstance = this;
        server_intent= new Intent(this, ServizioWebServer.class);
    }

    public static App getInstance() { return App.sInstance; }

    public void startServerService() { startService(server_intent); }

    public void stopServerService() { stopService(server_intent); }

}
