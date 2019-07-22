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


public class ServizioWebServer  extends Service {

    private static final int NOTIF_ID = 1;
    private static final String NOTIF_CHANNEL_ID = "Channel_Id";
    private MainActivity activity;

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

        webServer.close();
        webServer=null;
        activity.gettvStatus().setText("OFF");
        activity.gettvStatus().setTextColor(Color.RED);
        activity.getbServer().setBackgroundResource(R.drawable.play);
        for (int i=0; i<sensorsOnBoard.maxNumberofSensor;i++)
        {
            sensorManager.unregisterListener(sensorsOnBoard.getListenerSensore(i));
        }

        // Tell the user we stopped.
        //Toast.makeText(this, R.string.remote_service_stopped, Toast.LENGTH_SHORT).show();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId){

        // do your jobs here
        try {
            activity=this.getActivity();
            sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
            sensorsOnBoard= new SensorsOnBoard(sensorManager,activity.gettvSensori());
            //startService(new Intent(this, ServizioWebServer.class));
            sensorsOnBoard.scanSensors();
            for (int i=0; i<sensorsOnBoard.maxNumberofSensor;i++)
            {
                sensorManager.registerListener(sensorsOnBoard.getListenerSensore(i), sensorsOnBoard.getSensore(i), SensorManager.SENSOR_DELAY_FASTEST);
                //sensorManager.registerListener(lightEventListener, lightSensor, SensorManager.SENSOR_DELAY_FASTEST);
            }
            webServer=new WebServer(this);
            activity.gettvServer().setText("Server :"+webServer.getIpAddress()+":" + Integer.toString(webServer.HttpServerPORT ));
            webServer.getHttpServerThread().start();
            activity.gettvStatus().setText("ON");
            activity.gettvStatus().setTextColor(Color.GREEN);
            activity.getbServer().setBackgroundResource(R.drawable.stop);

        } catch (NoSuchFieldException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } catch (InvocationTargetException e) {
            e.printStackTrace();
        }
        //webServer.close();
        // do your jobs here
        startForeground();

        return super.onStartCommand(intent, flags, startId);
    }

    public MainActivity getServiceActivity(){return activity;}
    public SensorsOnBoard getSensorsOnBoard(){return sensorsOnBoard;}

    public static MainActivity getActivity() throws NoSuchFieldException, IllegalAccessException, NoSuchMethodException, ClassNotFoundException, InvocationTargetException {
        Class activityThreadClass = Class.forName("android.app.ActivityThread");
        Object activityThread = activityThreadClass.getMethod("currentActivityThread").invoke(null);
        Field activitiesField = activityThreadClass.getDeclaredField("mActivities");
        activitiesField.setAccessible(true);

        Map<Object, Object> activities = (Map<Object, Object>) activitiesField.get(activityThread);
        if (activities == null)
            return null;

        for (Object activityRecord : activities.values()) {
            Class activityRecordClass = activityRecord.getClass();
            Field pausedField = activityRecordClass.getDeclaredField("paused");
            pausedField.setAccessible(true);
            if (!pausedField.getBoolean(activityRecord)) {
                Field activityField = activityRecordClass.getDeclaredField("activity");
                activityField.setAccessible(true);
                MainActivity activity = (MainActivity) activityField.get(activityRecord);
                return activity;
            }
        }

        return null;
    }


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
