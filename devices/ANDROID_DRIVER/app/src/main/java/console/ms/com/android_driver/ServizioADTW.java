package console.ms.com.android_driver;

import android.Manifest;
import android.annotation.TargetApi;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.hardware.SensorManager;
import android.os.Build;
import android.os.IBinder;
import android.provider.MediaStore;
import android.support.annotation.ColorInt;
import android.support.annotation.Nullable;
import android.support.v4.app.NotificationCompat;

import java.io.File;
import java.io.FileNotFoundException;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.util.Map;


public class ServizioADTW extends Service {

    private static final int NOTIF_ID = 1;
    private static final String NOTIF_CHANNEL_ID = "Channel_Id";


    private SensorsOnBoard sensorsOnBoard;
    public SensorsOnBoard getSensorsOnBoard(){return sensorsOnBoard;}
    private WebServer webServer;
    private ManageXml manageXml;
    public ManageXml getManageXml(){return manageXml;}
    private File configFile;
    public File getConfigFile(){return configFile;}
    private PermissionManager permissionManager;
    public PermissionManager getPermissionManager(){return permissionManager;}


    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }


    @Override
    public void onDestroy() {

        try
        {
            if (webServer != null ) webServer.close();
            webServer=null;
            FileManager.Log(getResources().getString(R.string.mex_WebServer_OFF),getResources().getString(R.string.mex_Log_Type_Info));
            if (sensorsOnBoard != null ) sensorsOnBoard.Close();
            sensorsOnBoard=null;
            FileManager.Log(getResources().getString(R.string.mex_SensorOnBoard_OFF),getResources().getString(R.string.mex_Log_Type_Info));
            super.onDestroy();
        }catch (Exception e) {
            e.printStackTrace();
            FileManager.Log(e.toString(),getResources().getString(R.string.mex_Log_Type_Error));
        }
        finally {
            FileManager.Log(getResources().getString(R.string.mex_Service_OFF),getResources().getString(R.string.mex_Log_Type_Info));
            super.onDestroy();
        }
        // Tell the user we stopped.
        //Toast.makeText(this, R.string.remote_service_stopped, Toast.LENGTH_SHORT).show();
    }



    @Override
    public int onStartCommand(Intent intent, int flags, int startId){

        int result=0;

        try {
            configFile = new File(this.getFilesDir(), "config.xml");
            manageXml=new ManageXml(configFile);
            permissionManager= new PermissionManager(configFile);
            permissionManager.ReadPermissionManagerInXml();
            if(permissionManager.getWRITE_EXTERNAL_STORAGE())
                FileManager.makeAppDirectory();
            FileManager.Log(getResources().getString(R.string.mex_PermissionManager),getResources().getString(R.string.mex_Log_Type_Info));
            sensorsOnBoard= new SensorsOnBoard((SensorManager) getSystemService(SENSOR_SERVICE));
            FileManager.Log(sensorsOnBoard.toString(),getResources().getString(R.string.mex_Log_Type_Info));

            webServer=new WebServer(this);
            webServer.getHttpServerThread().start();
            FileManager.Log(getResources().getString(R.string.mex_WebServer_ON),getResources().getString(R.string.mex_Log_Type_Info));


            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
                startMyOwnForeground();
            else
                startForeground(1, new Notification());

            FileManager.Log(getResources().getString(R.string.mex_Service_ON),getResources().getString(R.string.mex_Log_Type_Info));
            result=super.onStartCommand(intent, flags, startId);

        } catch (Exception e) {
            e.printStackTrace();
            FileManager.Log(e.toString(),FileManager.Log_Error);
        }
        finally {
            return result;
        }

    }

    @TargetApi(26)
    private void startMyOwnForeground(){
        String NOTIFICATION_CHANNEL_ID = "com.example.simpleapp";
        String channelName = "My Background Service";
        NotificationChannel chan = new NotificationChannel(NOTIFICATION_CHANNEL_ID, channelName, NotificationManager.IMPORTANCE_NONE);
        chan.setLightColor(Color.BLUE);
        chan.setLockscreenVisibility(Notification.VISIBILITY_PRIVATE);
        NotificationManager manager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
        assert manager != null;
        manager.createNotificationChannel(chan);

        NotificationCompat.Builder notificationBuilder = new NotificationCompat.Builder(this, NOTIFICATION_CHANNEL_ID);
        Notification notification = notificationBuilder.setOngoing(true)
                .setSmallIcon(R.drawable.sensor)
                .setContentTitle("App is running in background")
                .setPriority(NotificationManager.IMPORTANCE_MIN)
                .setCategory(Notification.CATEGORY_SERVICE)
                .build();
        startForeground(2, notification);
    }

}
