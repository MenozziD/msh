package console.ms.com.android_driver;

import android.Manifest;
import android.content.pm.PackageManager;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;

import org.xmlpull.v1.XmlPullParser;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.security.Permission;

import console.ms.com.android_driver.MainActivity;
import console.ms.com.android_driver.ManageXml;
import console.ms.com.android_driver.R;

import static android.content.Context.MODE_PRIVATE;

public class PermissionManager {

    private ManageXml manageXml;
    private MainActivity activity;
    private boolean WRITE_EXTERNAL_STORAGE=false;
    public boolean getWRITE_EXTERNAL_STORAGE (){return WRITE_EXTERNAL_STORAGE;}
    public void setWRITE_EXTERNAL_STORAGE (Boolean value){this.WRITE_EXTERNAL_STORAGE=value;}
    private boolean READ_EXTERNAL_STORAGE=false;
    public boolean getREAD_EXTERNAL_STORAGE (){return READ_EXTERNAL_STORAGE;}
    public void setREAD_EXTERNAL_STORAGE (Boolean value){this.READ_EXTERNAL_STORAGE=value;}


    public PermissionManager (File configFile){
        manageXml=new ManageXml(configFile);
    }

    static void requestPermission(MainActivity activity , String permission, int requestCode)
    {
        ActivityCompat.requestPermissions(activity, new String[] { permission }, requestCode);
    }

    public void WritePermissionManagerInXml(){
        manageXml.set_app_permission_write(WRITE_EXTERNAL_STORAGE);
        manageXml.set_app_permission_read(READ_EXTERNAL_STORAGE);
        manageXml.writeXml();
    }

    public void ReadPermissionManagerInXml(){
        manageXml.readXml();
        WRITE_EXTERNAL_STORAGE=manageXml.get_app_permission_write();
        READ_EXTERNAL_STORAGE=manageXml.get_app_permission_read();
    }

    // Function to check and request permission
    static boolean checkPermission(String permission, MainActivity activity)
    {
        boolean result=false;
        // Checking if permission is not granted
        if (ContextCompat.checkSelfPermission(activity, permission) == PackageManager.PERMISSION_GRANTED)
            result=true;
        else
            if (activity != null) requestPermission(activity,permission,1);
        return result;
    }


}

