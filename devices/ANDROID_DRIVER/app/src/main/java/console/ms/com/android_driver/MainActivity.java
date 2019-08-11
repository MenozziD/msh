package console.ms.com.android_driver;


import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.util.Enumeration;
import java.util.Map;

import android.Manifest;
import android.app.Application;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.hardware.Sensor;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.GridLayout;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.os.Bundle;
import android.widget.Toast;


public class MainActivity extends AppCompatActivity  {


    private static final String TAG_Visible = "Visible";
    private static final String TAG_Server = "Server";

    public String getTAG_Visible()
    {
        return TAG_Visible;
    }
    public String getTAG_Server()
    {
        return TAG_Server;
    }

    private ManageXml manageXml;
    public ManageXml getManageXml(){return manageXml;}
    private PermissionManager permissionManager;
    public PermissionManager getPermissionManager(){return permissionManager;}

    /* SERVER */
    private Button bServer;
    private TextView tvServer;
    private TextView tvStatus;
    private TextView tvStartLog;
    public Button getbServer() {return bServer; }
    public TextView gettvStatus() {return tvStatus; }
    public TextView gettvServer() {return tvServer; }

    /* SENSOR */
    private LinearLayout vwSensorTitolo;
    private TextView[] tvSensori;
    public TextView[] gettvSensori() {return tvSensori; }
    private Button bSensorDim;
    private GridLayout vwSensor;
    public Button getbSensorDim() {return bSensorDim; }
    public GridLayout getVwSensor() {return vwSensor; }

    /* SET */
    private Button bSetDim;
    private GridLayout vwSet;
    private EditText etDeviceName;
    private EditText etTimeUpdate;
    public Button getbSetDim() {return bSetDim; }
    public GridLayout getVwSet() {return vwSet; }
    public EditText getetDeviceName() {return etDeviceName; }
    public EditText getetTimeUpdate() {return etTimeUpdate; }

    /* LOG */
    private Button bLogDim;
    private Button bDeleteLog;
    private GridLayout vwLog;
    private TextView infoLog;
    public Button getbLogDim() {return bLogDim; }
    public Button getbDeleteLog() {return bDeleteLog; }
    public GridLayout getVwLog() {return vwLog; }
    public TextView getinfoLog() {return infoLog; }


    @Override
    protected void onStart() {  super.onStart(); }


    @Override
    protected void onResume() { super.onResume(); }

    @Override
    protected void onPause() { super.onPause(); }


    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        Toast toast;
        setContentView(R.layout.activity_main);
        AscoltatoreMainActivity Ascoltatore = new AscoltatoreMainActivity(this);
        App this_app = App.getInstance();

        File f = new File(getFilesDir(), "config.xml");
        manageXml = new ManageXml(f);
        permissionManager= new PermissionManager(this);
        permissionManager.checkAllPermission();
        if (permissionManager.getWRITE_EXTERNAL_STORAGE())
        {
            FileManager.makeAppDirectory();
        }

        /* SERVER */
        tvServer = (TextView) findViewById(R.id.tvServer);
        tvServer.setText(WebServer.getIpAddress()+":"+WebServer.HttpServerPORT);
        tvServer.setOnClickListener(Ascoltatore);
        tvStatus = (TextView) findViewById(R.id.tvStatus);
        bServer=findViewById(R.id.bServer);
        bServer.setOnClickListener(Ascoltatore);
        bServer.setTag("");

        tvSensori= new TextView[3];
        tvSensori[0] = (TextView) findViewById(R.id.tvTYPE_MAGNETIC_FIELD_OUT);
        tvSensori[1] = (TextView) findViewById(R.id.tvTYPE_LIGHT_OUT);
        tvSensori[2] = (TextView) findViewById(R.id.tvTYPE_PROXIMITY_OUT);

        /* SENSOR */
        vwSensor=findViewById(R.id.vwSensor);
        bSensorDim=findViewById(R.id.bSensorDim);
        bSensorDim.setOnClickListener(Ascoltatore);
        bSensorDim.setTag(TAG_Visible);
        bSensorDim.callOnClick();
        vwSensorTitolo=findViewById(R.id.vwSensorTitolo);
        vwSensorTitolo.setVisibility(View.INVISIBLE);

        /* SET */
        vwSet=findViewById(R.id.vwSet);
        etDeviceName = (EditText) findViewById(R.id.etDeviceName);
        etDeviceName.setText(manageXml.get_h1());
        etTimeUpdate = (EditText) findViewById(R.id.etTimeUpdate);
        etTimeUpdate.setText(manageXml.get_timeupdate());
        bSetDim=findViewById(R.id.bSetDim);
        bSetDim.setOnClickListener(Ascoltatore);
        bSetDim.setTag(TAG_Visible);
        bSetDim.callOnClick();

        /* LOG */
        vwLog=findViewById(R.id.vwLog);
        infoLog=findViewById(R.id.tvStatusLogMex);

        bLogDim=findViewById(R.id.bLogDim);
        bLogDim.setOnClickListener(Ascoltatore);
        bDeleteLog=findViewById(R.id.bDeleteLog);
        bDeleteLog.setOnClickListener(Ascoltatore);
        bLogDim.setTag(TAG_Visible);
        bLogDim.callOnClick();

        if(this_app.isServerServiceRunning(ServizioWebServer.class))
        {
            getbServer().setTag(getTAG_Server());
            gettvStatus().setText("ON");
            gettvStatus().setTextColor(Color.GREEN);
            getbServer().setBackgroundResource(R.drawable.stop);
        }else{
            gettvStatus().setText("OFF");
            gettvStatus().setTextColor(Color.RED);
            getbServer().setTag("");
            getbServer().setBackgroundResource(R.drawable.play);
        }


    }



    @Override
    protected void onDestroy() {
        super.onDestroy();
    }

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



}

