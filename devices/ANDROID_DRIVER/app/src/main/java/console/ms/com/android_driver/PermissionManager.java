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

import console.ms.com.android_driver.MainActivity;
import console.ms.com.android_driver.ManageXml;
import console.ms.com.android_driver.R;

import static android.content.Context.MODE_PRIVATE;

public class PermissionManager {

    private ManageXml manageXml;
    private MainActivity activity;
    private boolean WRITE_EXTERNAL_STORAGE=false;
    public boolean getWRITE_EXTERNAL_STORAGE (){return WRITE_EXTERNAL_STORAGE;}
    private boolean READ_EXTERNAL_STORAGE=false;
    public boolean getREAD_EXTERNAL_STORAGE (){return READ_EXTERNAL_STORAGE;}



    public PermissionManager (MainActivity pMainActivity){
        activity=pMainActivity;
        manageXml=activity.getManageXml();
    }

    public void requestPermission(String permission, int requestCode)
    {
        ActivityCompat.requestPermissions(activity, new String[] { permission }, requestCode);
    }

    public void checkAllPermission() {

        try {
            // Leggo facendo richiesta se non autorizzato e salvo variabili XML
            manageXml.set_app_permission_write(checkPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE, true));
            manageXml.set_app_permission_read(checkPermission(Manifest.permission.READ_EXTERNAL_STORAGE, true));
            manageXml.writeXml();
            // Assegno proprieta classe e Log
            WRITE_EXTERNAL_STORAGE=manageXml.get_app_permission_write();
            READ_EXTERNAL_STORAGE=manageXml.get_app_permission_read();
            FileManager.Log("WRITE_EXTERNAL_STORAGE "+Boolean.toString(WRITE_EXTERNAL_STORAGE),FileManager.Log_Info);
            FileManager.Log("READ_EXTERNAL_STORAGE "+Boolean.toString(READ_EXTERNAL_STORAGE),FileManager.Log_Info);
        } catch (Exception e) {
            e.printStackTrace();
            FileManager.Log(e.toString(),FileManager.Log_Error);
        }

    }


    // Function to check and request permission
    public boolean checkPermission(String permission, boolean doRequest)
    {
        boolean result=false;
        // Checking if permission is not granted
        if (ContextCompat.checkSelfPermission(activity, permission) == PackageManager.PERMISSION_GRANTED)
            result=true;
        else
            if (doRequest) requestPermission(permission,1);
        return result;
    }


}

