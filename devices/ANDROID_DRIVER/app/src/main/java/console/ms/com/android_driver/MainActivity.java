package console.ms.com.android_driver;


import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import android.Manifest;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.hardware.Camera;
import android.media.CamcorderProfile;
import android.media.MediaRecorder;
import android.os.Environment;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.Surface;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.GridLayout;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.os.Bundle;
import android.widget.Toast;

import static android.provider.MediaStore.Files.FileColumns.MEDIA_TYPE_IMAGE;
import static android.provider.MediaStore.Files.FileColumns.MEDIA_TYPE_VIDEO;


public class MainActivity extends AppCompatActivity implements SurfaceHolder.Callback {



    private String tag ="TAG";

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

    private PermissionManager permissionManager;
    public PermissionManager getPermissionManager(){return permissionManager;}
    private ManageXml manageXml;
    public ManageXml getManageXml(){return manageXml;}
    public static final int PERMISSION_ALL = 1;

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
    private TextView tvStatusLogMex;
    public Button getbLogDim() {return bLogDim; }
    public Button getbDeleteLog() {return bDeleteLog; }
    public GridLayout getVwLog() {return vwLog; }
    public TextView gettvStatusLogMex() {return tvStatusLogMex; }
    public boolean IsOn =false;


    public static SurfaceView mSurfaceView;
    public static SurfaceHolder mSurfaceHolder;
    public static Camera mCamera;
    public static boolean mPreviewRunning;
    private Button mButton;
    public Button getButton (){return mButton;}

    @Override
    protected void onStart() {  super.onStart(); }


    @Override
    protected void onResume() {
        super.onResume();
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        Toast toast;
        setContentView(R.layout.activity_main);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        AscoltatoreMainActivity Ascoltatore = new AscoltatoreMainActivity(this);
        App this_app = App.getInstance();


        /* Permission
            Questo per impostare all'avvio le permission e richiderle se mancano.
            Per chiederle serve un activity quindi lo faccio qui
         */
        permissionManager=new PermissionManager();
        permissionManager.checkPermissions(this);
        
        /*
            CAMERA
         */
        // Create our Preview view and set it as the content of our activity.
        mCamera=Camera.open();

        mSurfaceView = (SurfaceView) findViewById(R.id.surfaceView1);
        mSurfaceHolder = mSurfaceView.getHolder();
        mSurfaceHolder.addCallback(this);
        mSurfaceHolder.setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);

        mButton = (Button) findViewById(R.id.button_capture);
        mButton.setOnClickListener(Ascoltatore);





        /* SERVER */
        tvServer = (TextView) findViewById(R.id.tvServer);
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
        //etDeviceName.setText(manageXml.get_h1());
        etTimeUpdate = (EditText) findViewById(R.id.etTimeUpdate);
        //etTimeUpdate.setText(manageXml.get_timeupdate());
        bSetDim=findViewById(R.id.bSetDim);
        bSetDim.setOnClickListener(Ascoltatore);
        bSetDim.setTag(TAG_Visible);
        bSetDim.callOnClick();

        /* LOG */
        vwLog=findViewById(R.id.vwLog);
        tvStatusLogMex=findViewById(R.id.tvStatusLogMex);

        bLogDim=findViewById(R.id.bLogDim);
        bLogDim.setOnClickListener(Ascoltatore);
        bDeleteLog=findViewById(R.id.bDeleteLog);
        bDeleteLog.setOnClickListener(Ascoltatore);
        bLogDim.setTag(TAG_Visible);
        bLogDim.callOnClick();

        if(this_app.isServerServiceRunning(ServizioADTW.class))
        {
            getbServer().setTag(getTAG_Server());
            gettvStatus().setText("ON");
            gettvStatus().setTextColor(Color.GREEN);
            getbServer().setBackgroundResource(R.drawable.stop);
            gettvServer().setText(WebServer.getIpAddress()+":"+WebServer.HttpServerPORT);
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

    public static MainActivity getActivity()  {
       MainActivity result=null;
       try {
           Class activityThreadClass = Class.forName("android.app.ActivityThread");
           Object activityThread = activityThreadClass.getMethod("currentActivityThread").invoke(null);
           Field activitiesField = activityThreadClass.getDeclaredField("mActivities");
           activitiesField.setAccessible(true);

           Map<Object, Object> activities = (Map<Object, Object>) activitiesField.get(activityThread);
           if (activities == null)
               result= null;

           for (Object activityRecord : activities.values()) {
               Class activityRecordClass = activityRecord.getClass();
               Field pausedField = activityRecordClass.getDeclaredField("paused");
               pausedField.setAccessible(true);
               if (!pausedField.getBoolean(activityRecord)) {
                   Field activityField = activityRecordClass.getDeclaredField("activity");
                   activityField.setAccessible(true);
                   MainActivity activity = (MainActivity) activityField.get(activityRecord);
                   result= activity;
               }
           }
       } catch (NoSuchMethodException e) {
           e.printStackTrace();
       } catch (InvocationTargetException e) {
           e.printStackTrace();
       } catch (NoSuchFieldException e) {
           e.printStackTrace();
       } catch (IllegalAccessException e) {
           e.printStackTrace();
       } catch (ClassNotFoundException e) {
           e.printStackTrace();
       }
       finally {
           return result;
       }
    }



    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           String permissions[], int[] grantResults) {
        Log.d(tag, "Permission callback called-------");
        switch (requestCode) {
            case PERMISSION_ALL: {

                Map<String, Integer> perms = new HashMap<>();
                // Initialize the map with both permissions
                perms.put(Manifest.permission.SEND_SMS, PackageManager.PERMISSION_GRANTED);
                perms.put(Manifest.permission.ACCESS_FINE_LOCATION, PackageManager.PERMISSION_GRANTED);
                // Fill with actual results from user
                if (grantResults.length > 0) {
                    for (int i = 0; i < permissions.length; i++)
                        perms.put(permissions[i], grantResults[i]);
                    // Check for both permissions
                    if (permissionManager.getpermissionsOK()) {
                        Log.d(tag, "All services permission granted");
                        // process the normal flow
                        //else any one or both the permissions are not granted
                    } else {
                        Log.d(tag, "Some permissions are not granted ask again ");
                        //permission is denied (this is the first time, when "never ask again" is not checked) so ask again explaining the usage of permission
                        // shouldShowRequestPermissionRationale will return true
                        //show the dialog or snackbar saying its necessary and try again otherwise proceed with setup.
                        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
                    }
                }
            }
        }
    }


    @Override
    public void surfaceCreated(SurfaceHolder holder) {

    }

    @Override
    public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {

    }

    @Override
    public void surfaceDestroyed(SurfaceHolder holder) {

    }
}


