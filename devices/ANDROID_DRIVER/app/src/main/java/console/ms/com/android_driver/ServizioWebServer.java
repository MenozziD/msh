package console.ms.com.android_driver;

import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.graphics.Color;
import android.hardware.SensorManager;
import android.os.IBinder;
import android.support.annotation.ColorInt;
import android.support.annotation.Nullable;
import android.support.v4.app.NotificationCompat;

import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.util.Map;


public class ServizioWebServer extends Service {

    private static final int NOTIF_ID = 1;
    private static final String NOTIF_CHANNEL_ID = "Channel_Id";


    private SensorManager sensorManager;
    private SensorsOnBoard sensorsOnBoard;
    private WebServer webServer;

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }


    @Override
    public void onDestroy() {

        if (webServer != null ) webServer.close();
        webServer=null;
        /*
        for (int i=0; i<sensorsOnBoard.maxNumberofSensor;i++)
        {
            sensorManager.unregisterListener(sensorsOnBoard.getListenerSensore(i));
        }

        // Tell the user we stopped.
        //Toast.makeText(this, R.string.remote_service_stopped, Toast.LENGTH_SHORT).show();
        */
    }


    
    @Override
    public int onStartCommand(Intent intent, int flags, int startId){

        int result=0;

        // do your jobs here
        try {

            sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
            sensorsOnBoard= new SensorsOnBoard(sensorManager,MainActivity.getActivity().gettvSensori());
            sensorsOnBoard.scanSensors();
            webServer=new WebServer(this);

            for (int i=0; i<sensorsOnBoard.maxNumberofSensor;i++)
            {
                sensorManager.registerListener(sensorsOnBoard.getListenerSensore(i), sensorsOnBoard.getSensore(i), SensorManager.SENSOR_DELAY_FASTEST);
                //sensorManager.registerListener(lightEventListener, lightSensor, SensorManager.SENSOR_DELAY_FASTEST);
            }
            if (!WebServer.getIpAddress().equals(""))
            {
                webServer.getHttpServerThread().start();
                startForeground();
                result=super.onStartCommand(intent, flags, startId);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        finally {
            return result;
        }

    }

    public SensorsOnBoard getSensorsOnBoard(){return sensorsOnBoard;}



    private void startForeground() {
        Intent notificationIntent = new Intent(this, MainActivity.class);

        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0,
                notificationIntent, 0);

        startForeground(NOTIF_ID, new NotificationCompat.Builder(this,
                NOTIF_CHANNEL_ID) // don't forget create a notification channel first
                .setOngoing(true)
                .setSmallIcon(R.drawable.sensor)
                .setContentTitle(getString(R.string.app_name))
                .setContentText("Service is running background")
                .setContentIntent(pendingIntent)
                .build());
    }
}
