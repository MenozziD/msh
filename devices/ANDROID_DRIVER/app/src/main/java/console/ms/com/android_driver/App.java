package console.ms.com.android_driver;

import android.app.ActivityManager;
import android.app.Application;
import android.content.Context;
import android.content.Intent;

public class App extends Application {

    private static App sInstance;
    private Intent server_intent;
    private Intent camera_intent;


    @Override
    public void onCreate() {
        super.onCreate();
        sInstance = this;
        server_intent= new Intent(this, ServizioADTW.class);
        camera_intent= new Intent(this, ServizioCamera.class);

    }

    public static App getInstance() { return App.sInstance; }

    public void startServerService() {
        try {
            if (!isServerServiceRunning(ServizioADTW.class)) {
                startService(server_intent);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void stopServerService() {
        try {
            if (isServerServiceRunning(ServizioADTW.class)) {
                stopService(server_intent);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

    }


    public void startCameraService() {
        try {
            if (!isServerServiceRunning(ServizioADTW.class)) {
                startService(camera_intent);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void stopCameraService() {
        try {
            if (isServerServiceRunning(ServizioCamera.class)) {
                stopService(camera_intent);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    public boolean isServerServiceRunning(Class<?> serviceClass) {
        ActivityManager manager = (ActivityManager) getSystemService(Context.ACTIVITY_SERVICE);
        for (ActivityManager.RunningServiceInfo service : manager.getRunningServices(Integer.MAX_VALUE)) {
            if (serviceClass.getName().equals(service.service.getClassName())) {
                return true;
            }
        }
        return false;
    }


}
