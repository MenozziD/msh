package console.ms.com.android_driver;

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
import android.support.annotation.ColorInt;
import android.support.annotation.Nullable;
import android.support.v4.app.NotificationCompat;

import java.io.File;
import java.io.FileNotFoundException;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.util.Map;


public class ServizioWebServer extends Service {

    private static final int NOTIF_ID = 1;
    private static final String NOTIF_CHANNEL_ID = "Channel_Id";


    private SensorManager sensorManager;
    private SensorsOnBoard sensorsOnBoard;
    public SensorsOnBoard getSensorsOnBoard(){return sensorsOnBoard;}
    private WebServer webServer;
    private ManageXml manageXml;
    public ManageXml getManageXml(){return manageXml;}

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }


    @Override
    public void onDestroy() {

        if (webServer != null ) webServer.close();
        webServer=null;
        FileManager.Log("Web Server OFF!","Info");

        for (int i=0; i<sensorsOnBoard.maxNumberofSensor;i++)
        {
            sensorManager.unregisterListener(sensorsOnBoard.getListenerSensore(i));
        }
        FileManager.Log("Ascoltatori Sensori UNREGISTER!","Info");
        // Tell the user we stopped.
        //Toast.makeText(this, R.string.remote_service_stopped, Toast.LENGTH_SHORT).show();

    }



    @Override
    public int onStartCommand(Intent intent, int flags, int startId){

        int result=0;

        // do your jobs here
        try {

            File f = new File(this.getFilesDir(), "config.xml");
            manageXml = new ManageXml(f);

            FileManager.Log("File config.xml letto!","Info");

            sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
            sensorsOnBoard= new SensorsOnBoard(sensorManager);
            sensorsOnBoard.scanSensors();

            webServer=new WebServer(this);

            for (int i=0; i<sensorsOnBoard.maxNumberofSensor;i++) {
                if (sensorsOnBoard.getsensori()[i] != null)
                    sensorManager.registerListener(sensorsOnBoard.getListenerSensore(i), sensorsOnBoard.getSensore(i), SensorManager.SENSOR_DELAY_FASTEST);
            }
            FileManager.Log(sensorsOnBoard.toString(),"Info");
            FileManager.Log("Ascoltatori Sensori REGISTER!","Info");


            webServer.getHttpServerThread().start();
            FileManager.Log("Web Server ON!","Info");

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
                startMyOwnForeground();
            else
                startForeground(1, new Notification());

            result=super.onStartCommand(intent, flags, startId);
            FileManager.Log("Servizio avviato in Background!","Info");

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
