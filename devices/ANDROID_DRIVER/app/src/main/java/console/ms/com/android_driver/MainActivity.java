package console.ms.com.android_driver;


import java.io.File;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.util.Map;

import android.Manifest;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.GridLayout;
import android.widget.LinearLayout;
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

    private PermissionManager permissionManager;
    public PermissionManager getPermissionManager(){return permissionManager;}
    private ManageXml manageXml;
    public ManageXml getManageXml(){return manageXml;}

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

        /* Permission
            Questo per impostare all'avvio le permission e richiderle se mancano.
            Per chiederle serve un activity quindi lo faccio qui
            Scrivo su Xml Tag delle permission
         */
        File f = new File(getFilesDir(), "config.xml");
        permissionManager=new PermissionManager(f);
        permissionManager.setWRITE_EXTERNAL_STORAGE(PermissionManager.checkPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE,this));
        permissionManager.setREAD_EXTERNAL_STORAGE(PermissionManager.checkPermission(Manifest.permission.READ_EXTERNAL_STORAGE,this));
        permissionManager.WritePermissionManagerInXml();

        /* Creazione Directory App su memoria esterna*/
        if (PermissionManager.checkPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE,this))
            FileManager.makeAppDirectory();
        FileManager.Log(getResources().getString(R.string.mex_PermissionManager),getResources().getString(R.string.mex_Log_Type_Info));

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
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        int PERMISSION_REQUEST_CODE=1;
        boolean result=false;
        // If this is our permission request result.
        if(requestCode==PERMISSION_REQUEST_CODE)
        {
            if(grantResults.length > 0)
            {
                if(grantResults[0]==PackageManager.PERMISSION_GRANTED)
                    result=true;
                if (permissions[0].equals(Manifest.permission.WRITE_EXTERNAL_STORAGE))
                    permissionManager.setWRITE_EXTERNAL_STORAGE(result);
                if (permissions[0].equals(Manifest.permission.READ_EXTERNAL_STORAGE))
                    permissionManager.setREAD_EXTERNAL_STORAGE(result);
                permissionManager.WritePermissionManagerInXml();
                FileManager.Log(permissions[0],Integer.toString(grantResults[0]));
            }
        }
    }

}

